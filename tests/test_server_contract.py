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
