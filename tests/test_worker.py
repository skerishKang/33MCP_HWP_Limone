"""Isolated subprocess boundary tests; never invokes real HWP COM."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from hwp_unified.worker import WorkerError, invoke_hwp_worker, _execute


class WorkerTests(unittest.TestCase):
    def test_unsupported_operation_does_not_start_process(self):
        with mock.patch("hwp_unified.worker.subprocess.run") as launch:
            with self.assertRaisesRegex(WorkerError, "Unsupported"):
                invoke_hwp_worker("shell", command="dir")
            launch.assert_not_called()

    def test_crash_exit_keeps_host_alive_and_reports_failure(self):
        completed = subprocess.CompletedProcess([], -1073741819, "", "")
        with mock.patch("hwp_unified.worker.sys.platform", "win32"), mock.patch(
            "hwp_unified.worker.subprocess.run", return_value=completed
        ):
            with self.assertRaisesRegex(WorkerError, "exited abnormally"):
                invoke_hwp_worker(
                    "replace", source="a.hwp", destination="b.hwp",
                    replacements={"old": "new"}
                )

    def test_timeout_is_reported_without_claiming_result(self):
        with mock.patch("hwp_unified.worker.sys.platform", "win32"), mock.patch(
            "hwp_unified.worker.subprocess.run",
            side_effect=subprocess.TimeoutExpired(["python"], 90)
        ):
            with self.assertRaisesRegex(WorkerError, "timed out"):
                invoke_hwp_worker(
                    "replace", source="a.hwp", destination="b.hwp",
                    replacements={"old": "new"}
                )

    def test_exclusive_result_must_exist_and_nonempty(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "synthetic.hwp"
            path.write_bytes(b"synthetic mock bytes")
            completed = subprocess.CompletedProcess(
                [], 0, json.dumps({"ok": True, "output": str(path)}), ""
            )
            with mock.patch("hwp_unified.worker.sys.platform", "win32"), mock.patch(
                "hwp_unified.worker.subprocess.run", return_value=completed
            ) as spawn:
                result = invoke_hwp_worker(
                    "replace", source="old.hwp", destination=str(path),
                    replacements={"old": "new"}
                )
                self.assertEqual(result, str(path))
                self.assertEqual(spawn.call_args.kwargs["timeout"], 90)

    def test_invalid_request_shape_never_calls_com(self):
        with self.assertRaisesRegex(WorkerError, "Unsupported"):
            _execute({"operation": "shell", "params": {"cmd": "test"}})
        with self.assertRaisesRegex(WorkerError, "Invalid"):
            _execute({"operation": "replace", "params": "not-object"})


if __name__ == "__main__":
    unittest.main()
