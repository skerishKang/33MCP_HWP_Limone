"""Contract tests for the narrowly scoped local-34/local-35 integration.

All HWP COM behavior is mocked. PDF tests use a synthetic file and real
PyMuPDF only when installed; CI may skip them.
"""
from contextlib import contextmanager
import importlib.util
import pathlib
import tempfile
import unittest
from unittest import mock

from hwp_unified.workflow import HwpWorkflowError, run_replace_job
from hwp_unified.conversion import ConversionError, pdf_to_html, hwp_to_html


class FakeParams:
    def __init__(self):
        self.HSet = object()
        self.FindString = ""
        self.ReplaceString = ""
        self.IgnoreMessage = 0


class FakeAction:
    def __init__(self, hwp, fail=False):
        self.hwp = hwp
        self.fail = fail
        self.calls = []
    def GetDefault(self, command, values):
        self.calls.append(("default", command))
        return True
    def Execute(self, command, values):
        self.calls.append(("execute", command))
        if not self.fail:
            params = self.hwp.HParameterSet.HFindReplace
            self.hwp.text = self.hwp.text.replace(params.FindString, params.ReplaceString)
        return not self.fail


class FakeHwp:
    def __init__(self, save_result=True, replace_result=True):
        self.opened = []
        self.saved = []
        self.save_result = save_result
        self.text = "old text in a synthetic document"
        self.HParameterSet = mock.Mock(HFindReplace=FakeParams())
        self.HAction = FakeAction(self, fail=not replace_result)
    def GetTextFile(self, fmt, options):
        return self.text
    def Open(self, path, fmt, opt):
        self.opened.append(path)
        return True
    def SaveAs(self, path, fmt, opt):
        self.saved.append((path, fmt, opt))
        if self.save_result:
            pathlib.Path(path).write_bytes(b"synthetic HWP, not a valid real file")
        return self.save_result


@contextmanager
def fake_session(hwp):
    yield hwp


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.src = self.root / "source.hwp"
        self.src.write_bytes(b"source must never change")
        self.dst = self.root / "result.hwp"

    def test_success_creates_nonempty_result_without_touching_original(self):
        hwp = FakeHwp()
        result = run_replace_job(str(self.src), str(self.dst),
                                 {"old": "new"}, lambda: fake_session(hwp))
        self.assertEqual(result, str(self.dst))
        self.assertTrue(self.dst.is_file())
        self.assertEqual(self.src.read_bytes(), b"source must never change")
        self.assertEqual(hwp.HAction.calls[-1], ("execute", "AllReplace"))
        self.assertEqual(hwp.saved[0][1:], ("HWP", ""))

    def test_existing_output_never_overwritten(self):
        self.dst.write_bytes(b"already there")
        with self.assertRaises(HwpWorkflowError):
            run_replace_job(str(self.src), str(self.dst), {"old": "new"},
                            lambda: fake_session(FakeHwp()))
        self.assertEqual(self.dst.read_bytes(), b"already there")

    def test_save_error_leaves_no_output_or_temp(self):
        with self.assertRaisesRegex(HwpWorkflowError, "SaveAs failed"):
            run_replace_job(str(self.src), str(self.dst), {"old": "new"},
                            lambda: fake_session(FakeHwp(save_result=False)))
        self.assertFalse(self.dst.exists())
        self.assertFalse(list(self.root.glob("hwp_mcp_*")))

    def test_failed_replace_leaves_source_and_output_unchanged(self):
        with self.assertRaisesRegex(HwpWorkflowError, "replacement"):
            run_replace_job(str(self.src), str(self.dst), {"old": "new"},
                            lambda: fake_session(FakeHwp(replace_result=False)))
        self.assertEqual(self.src.read_bytes(), b"source must never change")
        self.assertFalse(self.dst.exists())

    def test_invalid_paths_and_actions_do_not_start_hwp(self):
        factory = mock.Mock(side_effect=AssertionError("COM should not start"))
        for replacements in ({}, {"": "bad"}, {1: "bad"}):
            with self.assertRaises(HwpWorkflowError):
                run_replace_job(str(self.src), str(self.dst), replacements, factory)
        with self.assertRaises(HwpWorkflowError):
            run_replace_job(str(self.src), str(self.src), {"a": "b"}, factory)
        factory.assert_not_called()


@unittest.skipUnless(importlib.util.find_spec("fitz"), "Optional PyMuPDF not installed")
class NativePdfTests(unittest.TestCase):
    def setUp(self):
        import fitz
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.pdf = self.root / "test.pdf"
        pdf = fitz.open()
        page = pdf.new_page()
        page.insert_text((60, 60), "Hello & test <markup>")
        pdf.save(str(self.pdf))
        pdf.close()

    def test_editable_html_escapes_pdf_text(self):
        output = pathlib.Path(pdf_to_html(str(self.pdf), str(self.root), "editable"))
        html = output.read_text(encoding="utf-8")
        self.assertIn("Hello &amp; test &lt;markup&gt;", html)
        self.assertNotIn("<markup>", html)

    def test_faithful_mode_preserves_approximate_block_position(self):
        output = pathlib.Path(pdf_to_html(str(self.pdf), str(self.root), "faithful"))
        html = output.read_text(encoding="utf-8")
        self.assertIn("position:absolute", html)
        self.assertIn("Hello", html)

    def test_output_never_overwritten(self):
        target = self.root / "test.editable.html"
        target.write_text("keep", encoding="utf-8")
        with self.assertRaisesRegex(ConversionError, "exists"):
            pdf_to_html(str(self.pdf), str(self.root), "editable")
        self.assertEqual(target.read_text(encoding="utf-8"), "keep")

    def test_scanned_pdf_fails_clearly_without_ocr_claim(self):
        import fitz
        empty = self.root / "scan.pdf"
        pdf = fitz.open()
        pdf.new_page()
        pdf.save(str(empty))
        pdf.close()
        with self.assertRaisesRegex(ConversionError, "OCR is not implemented"):
            pdf_to_html(str(empty), str(self.root))

    def test_hwp_to_pdf_to_html_with_stubbed_com_only(self):
        class FakeConversionHwp:
            def Open(self, path, fmt, opt):
                return True
            def SaveAs(self, path, fmt, opt):
                pathlib.Path(path).write_bytes(self.pdf.read_bytes())
                return True
        source = self.root / "sample.hwp"
        source.write_bytes(b"fake input HWP")
        fake = FakeConversionHwp()
        fake.pdf = self.pdf
        with mock.patch("hwp_unified.conversion.isolated_hwp_session",
                        side_effect=lambda: fake_session(fake)):
            result = hwp_to_html(str(source), str(self.root))
        self.assertEqual(pathlib.Path(result).name, "sample.editable.html")
        self.assertIn("Hello", pathlib.Path(result).read_text(encoding="utf-8"))
        self.assertFalse(list(self.root.glob("hwp_convert_*")))


if __name__ == "__main__":
    unittest.main()
