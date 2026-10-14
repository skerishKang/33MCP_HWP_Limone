"""Explicit opt-in real Windows/Hangul acceptance (synthetic document only).

Usage: python scripts/windows_hwp_smoke.py --run
No customer files are accessed, and all temporary test documents are deleted.
Does not auto-run with CI. DispatchEx creates job-owned HWP instances.
"""
import argparse
import pathlib
import sys
import tempfile
from contextlib import contextmanager

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))


@contextmanager
def hwp_session():
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    hwp = None
    try:
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")
        yield hwp
    finally:
        if hwp is not None:
            try:
                hwp.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="Launch real Hangul and use temp test files")
    args = parser.parse_args()
    if not args.run:
        print("NOT_RUN: pass --run to opt in to real Windows/Hangul smoke.")
        return 2
    from hwp_unified.workflow import run_replace_job
    from hwp_unified.conversion import hwp_to_html

    with tempfile.TemporaryDirectory(prefix="hwp_mcp_synthetic_") as temp:
        work = pathlib.Path(temp)
        source = work / "input.hwp"
        updated = work / "output.hwp"
        original = "HWP_MCP_SMOKE_ORIGINAL"
        changed = "HWP_MCP_SMOKE_UPDATED"

        with hwp_session() as hwp:
            if not hwp.HAction.Run("FileNew"):
                raise RuntimeError("HWP FileNew failed")
            action = hwp.HAction
            insert = hwp.HParameterSet.HInsertText
            action.GetDefault("InsertText", insert.HSet)
            insert.Text = original
            if not action.Execute("InsertText", insert.HSet):
                raise RuntimeError("HWP InsertText failed")
            if not hwp.SaveAs(str(source), "HWP", ""):
                raise RuntimeError("HWP SaveAs source failed")
        if not source.is_file() or source.stat().st_size == 0:
            raise RuntimeError("Source HWP was not created")

        result = run_replace_job(str(source), str(updated), {original: changed})
        if result != str(updated):
            raise RuntimeError("Unexpected workflow path")

        with hwp_session() as hwp:
            if not hwp.Open(str(updated), "HWP", ""):
                raise RuntimeError("Cannot reopen output HWP")
            text = hwp.GetTextFile("TEXT", "")
            if changed not in text or original in text:
                raise RuntimeError("Reopened HWP text does not match expected replacement")

        html = pathlib.Path(hwp_to_html(str(updated), str(work)))
        if not html.is_file() or not html.read_text(encoding="utf-8").strip():
            raise RuntimeError("Conversion failed to generate HTML")
        print("REAL_WINDOWS_PASS: create, SaveAs, replace, reopen, HWP->PDF->HTML")
        print("Synthetic HWP sizes:", source.stat().st_size, updated.stat().st_size)
        print("HTML bytes:", html.stat().st_size)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        import traceback
        traceback.print_exc()
        print("REAL_WINDOWS_FAILED:", type(exc).__name__, str(exc), file=sys.stderr)
        sys.exit(1)
