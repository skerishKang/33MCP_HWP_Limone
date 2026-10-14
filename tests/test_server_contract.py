"""Platform-independent regression tests for the HWP MCP startup/save contract.

Fake modules are used deliberately: these tests do NOT prove real Windows/HWP integration.
"""
import importlib.util
import os
import pathlib
import sys
import tempfile
import types
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]


class FakeFastMCP:
    def __init__(self, name):
        self.name = name
        self.registered_tools = []

    def tool(self):
        def register(function):
            self.registered_tools.append(function.__name__)
            return function
        return register

    def run(self):
        return None


def load_server():
    mcp = types.ModuleType("mcp")
    mcp.__path__ = []
    server = types.ModuleType("mcp.server")
    server.__path__ = []
    fastmcp = types.ModuleType("mcp.server.fastmcp")
    fastmcp.FastMCP = FakeFastMCP

    win32com = types.ModuleType("win32com")
    win32com.__path__ = []
    client = types.ModuleType("win32com.client")
    client.gencache = types.SimpleNamespace(EnsureDispatch=mock.Mock())
    client.Dispatch = mock.Mock()
    win32com.client = client

    pythoncom = types.ModuleType("pythoncom")
    pythoncom.CoInitialize = mock.Mock()
    pythoncom.CoUninitialize = mock.Mock()

    fake_modules = {
        "mcp": mcp,
        "mcp.server": server,
        "mcp.server.fastmcp": fastmcp,
        "win32com": win32com,
        "win32com.client": client,
        "pythoncom": pythoncom,
        "win32api": types.ModuleType("win32api"),
        "win32con": types.ModuleType("win32con"),
    }
    with mock.patch.dict(sys.modules, fake_modules):
        spec = importlib.util.spec_from_file_location(
            "hwp_server_under_test", ROOT / "advanced_hwp_server.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    return module, client


class ServerContractTests(unittest.TestCase):
    def setUp(self):
        self.server, self.client = load_server()
        self.controller = self.server.hwp_controller
        self.controller.hwp = mock.Mock()
        self.controller.current_document = "new_document"
        self.init_guard = mock.patch.object(
            self.controller, "check_initialization", return_value=True
        )
        self.init_guard.start()
        self.addCleanup(self.init_guard.stop)

    def test_experimental_mcp_tools_are_off_by_default(self):
        with mock.patch.dict(os.environ, {"HWP_MCP_ENABLE_EXPERIMENTAL": "0"}):
            server, _ = load_server()
        self.assertNotIn("replace_document_text", server.mcp.registered_tools)
        self.assertNotIn("convert_pdf_to_html", server.mcp.registered_tools)
        self.assertNotIn("convert_hwp_to_html", server.mcp.registered_tools)
        self.assertIn("save_document", server.mcp.registered_tools)

    def test_experimental_mcp_tools_require_explicit_opt_in(self):
        with mock.patch.dict(os.environ, {"HWP_MCP_ENABLE_EXPERIMENTAL": "1"}):
            server, _ = load_server()
        self.assertIn("replace_document_text", server.mcp.registered_tools)
        self.assertIn("convert_pdf_to_html", server.mcp.registered_tools)
        self.assertIn("convert_hwp_to_html", server.mcp.registered_tools)

    def test_com_initialization_failure_balances_thread_apartment(self):
        controller = self.server.AdvancedHwpController()
        self.client.gencache.EnsureDispatch.side_effect = RuntimeError("no COM")
        self.client.Dispatch.side_effect = RuntimeError("fallback unavailable")
        with mock.patch.object(self.server.pythoncom, "CoInitialize") as coinit, mock.patch.object(
            self.server.pythoncom, "CoUninitialize"
        ) as couninit:
            self.assertFalse(controller.initialize())
            coinit.assert_called_once()
            couninit.assert_called_once()
            self.assertIsNone(controller.hwp)
            self.assertFalse(controller.is_initialized)
            self.assertIsNone(controller._com_owner_thread_id)

    def test_failed_visibility_setup_releases_com_apartment(self):
        controller = self.server.AdvancedHwpController()
        hwp = mock.Mock()
        hwp.XHwpWindows.Count = 1
        hwp.XHwpWindows.Item.side_effect = RuntimeError("window COM failed")
        self.client.gencache.EnsureDispatch.return_value = hwp
        with mock.patch.object(self.server.pythoncom, "CoInitialize") as coinit, mock.patch.object(
            self.server.pythoncom, "CoUninitialize"
        ) as couninit:
            self.assertFalse(controller.initialize())
            coinit.assert_called_once()
            couninit.assert_called_once()
            self.assertFalse(controller.is_initialized)
            self.assertIsNone(controller.hwp)

    def test_coinitialize_failure_must_not_call_couninitialize(self):
        controller = self.server.AdvancedHwpController()
        with mock.patch.object(
            self.server.pythoncom, "CoInitialize", side_effect=RuntimeError("apartment unavailable")
        ), mock.patch.object(self.server.pythoncom, "CoUninitialize") as couninit:
            self.assertFalse(controller.initialize())
            couninit.assert_not_called()
            self.client.gencache.EnsureDispatch.assert_not_called()

    def test_com_initialization_is_idempotent_and_close_balances_once(self):
        controller = self.server.AdvancedHwpController()
        hwp = mock.Mock()
        hwp.XHwpWindows.Count = 0
        self.client.gencache.EnsureDispatch.return_value = hwp
        with mock.patch.object(self.server.pythoncom, "CoInitialize") as coinit, mock.patch.object(
            self.server.pythoncom, "CoUninitialize"
        ) as couninit:
            self.assertTrue(controller.initialize())
            self.assertTrue(controller.initialize())
            coinit.assert_called_once()
            self.assertIs(controller.hwp, hwp)
            self.assertTrue(controller.close())
            self.assertFalse(controller.close())
            couninit.assert_called_once()
            self.assertFalse(controller.is_initialized)

    def test_wrong_thread_cannot_reuse_or_uninitialize_com(self):
        controller = self.server.AdvancedHwpController()
        hwp = mock.Mock()
        hwp.XHwpWindows.Count = 0
        self.client.gencache.EnsureDispatch.return_value = hwp
        with mock.patch.object(self.server.pythoncom, "CoInitialize") as coinit, mock.patch.object(
            self.server.pythoncom, "CoUninitialize"
        ) as couninit:
            self.assertTrue(controller.initialize())
            with mock.patch.object(
                self.server.threading, "get_ident",
                return_value=controller._com_owner_thread_id + 100,
            ):
                with self.assertRaisesRegex(RuntimeError, "COM thread"):
                    controller.check_initialization()
                with self.assertRaisesRegex(RuntimeError, "COM thread"):
                    controller.close()
            self.assertEqual(coinit.call_count, 1)
            couninit.assert_not_called()
            self.assertTrue(controller.close())
            couninit.assert_called_once()

    def test_server_shutdown_releases_same_thread_com_once(self):
        hwp = mock.Mock()
        hwp.XHwpWindows.Count = 0
        self.client.gencache.EnsureDispatch.return_value = hwp
        with mock.patch.object(self.server.pythoncom, "CoInitialize") as coinit, mock.patch.object(
            self.server.pythoncom, "CoUninitialize"
        ) as couninit, mock.patch.object(self.server.mcp, "run") as run:
            self.assertTrue(self.controller.initialize())
            self.server.main()
            run.assert_called_once()
            coinit.assert_called_once()
            couninit.assert_called_once()
            self.assertFalse(self.controller.is_initialized)

    def test_import_does_not_open_log_file_in_unwritable_client_directory(self):
        # MCP clients may launch the script with an arbitrary working directory.
        # Import must not attempt to create a default log file.
        with mock.patch("logging.FileHandler",
                        side_effect=AssertionError("unexpected disk log")):
            server, _ = load_server()
        self.assertIsNotNone(server.mcp)

    def test_create_failure_must_not_claim_success(self):
        self.controller.hwp.HAction.Run.return_value = False
        message = self.server.create_document()
        self.assertIn("실패", message)
        self.assertEqual(self.controller.current_document, "new_document")

    def test_nonexistent_file_does_not_initialize_hwp(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = str(pathlib.Path(directory) / "absent.hwp")
            with mock.patch.object(
                self.controller, "check_initialization",
                side_effect=AssertionError("do not launch Hangul for missing file"),
            ):
                message = self.server.open_document(missing)
        self.assertIn("파일을 찾을 수 없습니다", message)

    def test_file_open_false_must_not_claim_success(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "synthetic.hwp"
            source.write_bytes(b"synthetic for mocked contract")
            self.controller.hwp.CreateAction.return_value.Execute.return_value = False
            message = self.server.open_document(str(source))
        self.assertIn("실패", message)
        self.assertEqual(self.controller.current_document, "new_document")

    def test_file_open_success_updates_current_document(self):
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / "synthetic.hwp"
            source.write_bytes(b"synthetic for mocked contract")
            self.controller.hwp.CreateAction.return_value.Execute.return_value = True
            message = self.server.open_document(str(source))
            self.assertIn("열었습니다", message)
            self.assertEqual(self.controller.current_document, str(source))

    def test_launching_mcp_does_not_launch_hwp(self):
        with mock.patch.object(self.controller, "initialize", side_effect=AssertionError(
            "HWP was initialized at MCP startup"
        )), mock.patch.object(self.server.mcp, "run") as run:
            self.server.main()
            run.assert_called_once()

    def test_new_document_requires_explicit_save_path(self):
        message = self.server.save_document()
        self.assertIn("file_path", message)
        self.controller.hwp.SaveAs.assert_not_called()
        self.controller.hwp.HAction.Run.assert_not_called()

    def test_missing_folder_fails_before_hwp_call(self):
        with tempfile.TemporaryDirectory() as directory:
            target = str(pathlib.Path(directory) / "not-created" / "out.hwp")
            message = self.server.save_document(target)
        self.assertIn("실패", message)
        self.controller.hwp.SaveAs.assert_not_called()

    def test_saveas_false_never_claims_success(self):
        with tempfile.TemporaryDirectory() as directory:
            target = str(pathlib.Path(directory) / "out.hwp")
            self.controller.hwp.SaveAs.return_value = False
            message = self.server.save_document(target)
        self.assertIn("실패", message)
        self.assertEqual(self.controller.current_document, "new_document")

    def test_saveas_true_without_file_never_claims_success(self):
        with tempfile.TemporaryDirectory() as directory:
            target = str(pathlib.Path(directory) / "missing.hwp")
            self.controller.hwp.SaveAs.return_value = True
            message = self.server.save_document(target)
        self.assertIn("실패", message)
        self.assertEqual(self.controller.current_document, "new_document")

    def test_saveas_success_updates_document_after_disk_check(self):
        with tempfile.TemporaryDirectory() as directory:
            target = str(pathlib.Path(directory) / "saved.hwp")

            def simulate_save(path, fmt, options):
                self.assertEqual((fmt, options), ("HWP", ""))
                pathlib.Path(path).write_bytes(b"mock hwp bytes")
                return True

            self.controller.hwp.SaveAs.side_effect = simulate_save
            message = self.server.save_document(target)
            self.assertIn("저장했습니다", message)
            self.assertEqual(self.controller.current_document, target)

    def test_failed_in_place_save_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            target = pathlib.Path(directory) / "existing.hwp"
            target.write_bytes(b"existing")
            self.controller.current_document = str(target)
            self.controller.hwp.HAction.Run.return_value = False
            message = self.server.save_document()
        self.assertIn("실패", message)


if __name__ == "__main__":
    unittest.main()
