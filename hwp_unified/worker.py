"""Crash-isolated Windows HWP operations.

A buggy COM server can crash Python in combase.dll (0xC0000005). Run
experimental HWP work in a dedicated child process, not the MCP host.
The child accepts a single bounded JSON request on stdin and writes one JSON
result to stdout. This is not a service, socket or generic code executor.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


class WorkerError(RuntimeError):
    pass


def invoke_hwp_worker(operation: str, **kwargs: Any) -> str:
    if operation not in ("replace", "hwp_to_html"):
        raise WorkerError("Unsupported HWP worker operation")
    if sys.platform != "win32":
        raise WorkerError("HWP COM operations require Windows and Hancom Hangul")
    payload = {"operation": operation, "params": kwargs}
    encoded = json.dumps(payload, ensure_ascii=False)
    if len(encoded) > 131072:
        raise WorkerError("HWP job request exceeds size limit")
    try:
        run = subprocess.run(
            [sys.executable, "-m", "hwp_unified.worker"],
            input=encoded,
            text=True,
            capture_output=True,
            timeout=90,
            cwd=str(Path(__file__).resolve().parent.parent),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise WorkerError("HWP COM worker timed out; job did not complete") from exc
    except OSError as exc:
        raise WorkerError("Unable to launch HWP COM worker") from exc

    result = None
    try:
        result = json.loads(run.stdout.strip())
    except (ValueError, TypeError):
        pass
    if run.returncode != 0:
        if isinstance(result, dict) and isinstance(result.get("error"), str):
            raise WorkerError("HWP worker failed: " + result["error"][:600])
        raise WorkerError(
            f"HWP COM worker exited abnormally (code {run.returncode}); "
            "MCP host preserved, output unverified"
        )
    if not isinstance(result, dict) or result.get("ok") is not True:
        raise WorkerError("HWP worker returned an invalid completion result")
    output = result.get("output")
    if not isinstance(output, str) or not output:
        raise WorkerError("HWP worker did not provide an output path")
    if not Path(output).is_file() or Path(output).stat().st_size == 0:
        raise WorkerError("HWP worker output file is missing or empty")
    return output


def _execute(payload):
    if not isinstance(payload, dict) or set(payload) != {"operation", "params"}:
        raise WorkerError("Invalid HWP worker request")
    operation, params = payload["operation"], payload["params"]
    if not isinstance(params, dict):
        raise WorkerError("Invalid HWP worker params")
    if operation == "replace" and set(params) == {"source", "destination", "replacements"}:
        from .workflow import run_replace_job
        return run_replace_job(**params)
    if operation == "hwp_to_html" and set(params) == {"source", "output_dir", "mode"}:
        from .conversion import hwp_to_html
        return hwp_to_html(**params)
    raise WorkerError("Unsupported HWP operation or parameters")


def main():
    try:
        raw = sys.stdin.read(131073)
        if not raw or len(raw) > 131072:
            raise WorkerError("Missing or oversized input")
        output = _execute(json.loads(raw))
        print(json.dumps({"ok": True, "output": output}, ensure_ascii=False))
        return 0
    except Exception as exc:
        # Do not emit a traceback containing document text or customer data.
        print(json.dumps({"ok": False, "error": str(exc)[:600]}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
