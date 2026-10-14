"""Source-preserving HWP batch replacement inspired by local 34's action model.

This is a deliberately narrow, job-scoped implementation. It does not import
the unverified local 34 driver (whose table and journal methods are stubs).
Output is a new file: no overwrite, no false success, and no unbounded actions.
"""
from contextlib import contextmanager
import os
from pathlib import Path
import tempfile
from typing import Callable, ContextManager, Mapping


class HwpWorkflowError(RuntimeError):
    """User-facing failure for an HWP workflow."""


def validate_job(source: str, destination: str, replacements: Mapping[str, str]):
    source_path = Path(source).expanduser().resolve(strict=True)
    destination_path = Path(destination).expanduser().resolve()
    if not source_path.is_file() or source_path.suffix.lower() != ".hwp":
        raise HwpWorkflowError("Input must be an existing .hwp file")
    if destination_path.suffix.lower() != ".hwp":
        raise HwpWorkflowError("Output path must end in .hwp")
    if source_path == destination_path:
        raise HwpWorkflowError("Output must differ from the source (no overwrite)")
    if not destination_path.parent.is_dir():
        raise HwpWorkflowError("Output directory does not exist")
    if destination_path.exists():
        raise HwpWorkflowError("Output exists; refusing to overwrite")
    if not isinstance(replacements, dict) or not 1 <= len(replacements) <= 32:
        raise HwpWorkflowError("Provide 1 to 32 text replacements as a dictionary")
    for old, new in replacements.items():
        if not isinstance(old, str) or not isinstance(new, str):
            raise HwpWorkflowError("All replacement keys and values must be strings")
        if not old or len(old) > 1024 or len(new) > 4096:
            raise HwpWorkflowError("Replacement text is empty or too long")
        if old in new:
            raise HwpWorkflowError("A replacement cannot contain its own search term")
    for old in replacements:
        if any(old in value for key, value in replacements.items() if key != old):
            raise HwpWorkflowError("Overlapping replacement terms are not supported")
    return source_path, destination_path


@contextmanager
def isolated_hwp_session():
    """Own a fresh COM instance, never reuse or close a user's existing session."""
    try:
        import pythoncom
        import win32com.client
    except ImportError as exc:
        raise HwpWorkflowError("Windows, pywin32 and Hancom Hangul are required") from exc
    pythoncom.CoInitialize()
    hwp = None
    try:
        # DispatchEx is used intentionally: this job must own what it closes.
        hwp = win32com.client.DispatchEx("HWPFrame.HwpObject")
        yield hwp
    finally:
        if hwp is not None:
            try:
                hwp.Quit()
            except Exception:
                pass
        pythoncom.CoUninitialize()


def run_replace_job(
    source: str,
    destination: str,
    replacements: dict[str, str],
    session_factory: Callable[[], ContextManager] = isolated_hwp_session,
) -> str:
    """Replace document text and publish a new nonempty .hwp without overwriting.

    The action list intentionally excludes unsupported table-cell operations.
    Actual fidelity must be verified by reopening on Windows with Hangul.
    """
    src, out = validate_job(source, destination, replacements)
    # Same-directory temp enables atomic hard-link publish without overwriting.
    descriptor, pending = tempfile.mkstemp(
        prefix=".hwp-mcp-", suffix=".hwp", dir=str(out.parent)
    )
    os.close(descriptor)
    os.unlink(pending)
    try:
        with session_factory() as hwp:
            if not hwp.Open(str(src), "HWP", ""):
                raise HwpWorkflowError("Hangul could not open the source HWP")
            original_text = hwp.GetTextFile("TEXT", "")
            if not isinstance(original_text, str):
                raise HwpWorkflowError("Cannot verify original HWP text; no change made")
            for old in replacements:
                if old not in original_text:
                    raise HwpWorkflowError("A requested search term was absent from the document")
            for old, new in replacements.items():
                params = hwp.HParameterSet.HFindReplace
                hwp.HAction.GetDefault("AllReplace", params.HSet)
                params.FindString = old
                params.ReplaceString = new
                params.IgnoreMessage = 1
                result = hwp.HAction.Execute("AllReplace", params.HSet)
                if not result:
                    raise HwpWorkflowError("Hangul could not confirm replacement for a requested term")
            final_text = hwp.GetTextFile("TEXT", "")
            if not isinstance(final_text, str):
                raise HwpWorkflowError("Cannot verify modified HWP text")
            for old, new in replacements.items():
                if old in final_text or new not in final_text:
                    raise HwpWorkflowError("Text replacement read-back verification failed")
            if not hwp.SaveAs(pending, "HWP", ""):
                raise HwpWorkflowError("Hangul SaveAs failed")
        if not os.path.isfile(pending) or os.path.getsize(pending) == 0:
            raise HwpWorkflowError("Hangul did not produce a nonempty HWP output")
        # Exclusive link: unlike os.replace, never silently overwrite target.
        try:
            os.link(pending, out)
        except FileExistsError as exc:
            raise HwpWorkflowError("Output was created concurrently; no overwrite") from exc
        except OSError as exc:
            raise HwpWorkflowError("Atomic output publication failed; destination unchanged") from exc
        return str(out)
    finally:
        if os.path.exists(pending):
            os.unlink(pending)
