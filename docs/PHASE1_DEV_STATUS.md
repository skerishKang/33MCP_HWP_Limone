# Phase 1 integration — verified status (2026-10-15 KST)

**Repository:** existing `skerishKang/33MCP_HWP_Limone`, branch `feat/oss-revival-20261015` / Draft PR #2.
**Local sources:** read-only `workdiary/33-MCP_HWP`, `34-hwp-automation`, `35-hwp-pdf-html`.
**Staging workspace:** a separate clone outside `workdiary`; no original source folder modified.

## Implemented in this branch

1. **Source-preserving HWP text batch** (`hwp_unified/workflow.py`): job-owned `DispatchEx` session, validated inputs, bounded replacement dictionary, original file never overwritten, exclusive output publication, pre/post text read-back; no arbitrary commands or table stubs.
2. **PDF native text → HTML** (`hwp_unified/conversion.py`): uses optional PyMuPDF, escapes content, editable / approximate-position modes, refuses output overwrite, reports missing native PDF text instead of claiming OCR.
3. **HWP → PDF → native text HTML** (`hwp_unified/conversion.py`): isolated HWP COM export to verified PDF, optional PyMuPDF extraction, transient PDF deletion, no input-file modification. **Not yet live-validated**.
4. Three MCP tool wrappers (`replace_document_text`, `convert_pdf_to_html`, `convert_hwp_to_html`) registered **only** when `HWP_MCP_ENABLE_EXPERIMENTAL=1`; they do not change default tool discovery.
5. Optional dependencies through `requirements-convert.txt`; explicit `scripts/windows_hwp_smoke.py --run` synthetic E2E runner (never in CI).

## Tests and real-world results

- **17/17 local unittest** cases passed (7 earlier mocked server contracts + 10 new targeted workflow/PDF tests). PyMuPDF 1.26.4 was installed on the development PC, so actual synthetic PDF render/HTML escaping passed.
- GitHub CI uses Python 3.10–3.12 and mock tests; optional PyMuPDF tests skip if not installed. CI does not prove HWP COM or actual HWP output.
- Windows dev PC: pywin32 306 installed and `HWPFrame.HwpObject` COM registration exists.
- **REAL_WINDOWS_PASS = NO**. Initial synthetic run reached HWP workflow but failed with `WinError 267` involving its pending output path. Subsequent synthetic COM runs were unstable, including a process exit code `-1073741819` (Windows access violation, `0xC0000005`). No successful create→replace→reopen→convert evidence obtained.
- Do **not** turn experimental HWP tools on by default or claim that the failed Windows smoke is resolved. Further diagnosis should use a dedicated HWP test environment, event logs, bitness/HWP COM compatibility and isolated minimal script; avoid repeatedly launching HWP on a working user desktop.

## Explicitly not done

- Local 34 table editing / field journaling remains **NOT_IMPLEMENTED** in original code. Only safe text replacement has been newly implemented.
- Local 34 transactional rollback/long-running job persistence not yet integrated. Current text batch preserves source and never overwrites target but does not guarantee a replayable rollback journal.
- Local 35's old “12/15 accuracy” scores are simulated; **not used**. Actual HWP/PDF layout and text fidelity remains **NOT_RUN**.
- OCR, HWPX parsing, template injection, multi-file cancellation, edit-diff report remain tracked feature requests rather than working features.
- License/third-party source audit (#10) remains OPEN; no local proprietary/third-party subtree copied into public GitHub and no LICENSE written.

## Next work, smallest first

1. Reproduce and understand the Windows COM crash and `WinError 267` on a dedicated test instance before exposing HWP workflow tools to users.
2. Validate the new HWP output by reopening in Hangul; verify source preservation and expected replacements.
3. Real HWP→PDF→HTML conversion with a synthetic test document, compare extracted text.
4. Address local 34 table-cell stubs and rollback/journal limitations with separate tests and changes.
5. Decide public OSS license after rights audit and launch a tagged release only with truthful environment matrix.

Related: Epic #3, source #4, baseline bug #5, design #6, workflow #7, converter #8, package #9, security #10, real acceptance #11.
