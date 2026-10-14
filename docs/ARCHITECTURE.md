# Unified Advanced HWP MCP — Proposed architecture

> **HOLD / historical design proposal (2026-10-15).** The 33/34/35 modular expansion described below is not an active implementation mandate. Maintain the existing single MCP entry point and investigate external issue #1 and native COM failures first. Resume only after the evidence-based [OSS suitability decision](OSS_FIT_REVIEW.md) in issue #16, or an explicit maintainer priority decision.


**Status: PROPOSED (not an implementation claim).** Keep the same GitHub repository and the existing MCP server entry point.

```text
Claude Desktop / Gemini CLI / other validated MCP clients
                      |
                   MCP stdio
                      |
          advanced_hwp_server.py
         (backwards-compatible tools)
                      |
                hwp_common
       COM/STA session + path guard
       error/result + file lifecycle
               /      |       \
              /       |        \
        hwp_mcp    hwp_automation    hwp_converter
        (local 33) (local 34)        (local 35)
        create,    job/sequence,     HWP->PDF->HTML
        edit,save  idempotency,      PDF->HTML
                   rollback
              \       |       /
               validated output files
```

## Module boundaries

### Existing public interface
- Keep `advanced_hwp_server.py` as the legacy entry point.
- Preserve tool names, arguments and response behavior as far as possible. Document every unavoidable breaking change and migration.
- The MCP stdio server must not write diagnostics to stdout other than protocol frames. Use stderr/file logs as appropriate.
- Do not launch HWP solely because a client connects.

### Common layer (planned)
- Own the Windows COM STA lifecycle in a single explicitly defined context; no competing module should terminate another module's HWP session.
- Resolve allowed input/output paths, symlink/realpath boundaries and write permissions.
- Define one normalized result envelope internally: `status`, `error_code`, `output_paths`, `retryable`, `details` (only when useful), without silently changing existing MCP return strings.
- Enforce safe defaults: do not overwrite the source file; copy to a separate destination; ephemeral work files removed only after verified success or explicit rollback.
- A failed operation must never return a success message simply because a COM API call did not raise an exception.

### Module 33: HWP document tools
- Document create/open, text, formatting, tables, image/section, save/reopen.
- Compare local v1/v3/core modules before choosing canonical implementation; do not assume the file named “v3” is better or production ready.
- Smoke path: client tool call → HWP COM → durable output → reopen and inspect actual contents.

### Module 34: Workflow engine
- `open -> replace -> fill_table -> save -> close` as minimum sequential workflow.
- Audit idempotency key scope, rollback physical backup and journal, stale lock and crash recovery.
- **Known stubs:** `fill_table`, `get_cell_value`, `get_text_at` in local driver must be implemented before relying on success/rollback semantics.

### Module 35: Conversion
- Keep separate paths for `HWP → PDF → HTML` and `PDF → HTML`; OCR of scanned PDFs is an optional capability.
- Use optional install extras for heavy converters/OCR so basic MCP stays lightweight.
- Specify whether output is layout-faithful or editable; evaluate using actual golden documents.
- Simulated evaluation in local `run_eval.py` may remain a demonstration, **not** acceptance evidence.

## Build and deployment
- Keep one public GitHub repository; independent modules, not three separately deployed products.
- Work on a separate scratch/worktree; retain the three local source folders and their histories unchanged.
- Merge selective, small PRs in dependency order. Compatibility and real Windows E2E before declaring release-ready.
- Avoid artificial gate proliferation. Short tests that isolate high-risk user journeys are preferred.

Tracking: #3 (epic), #6 (boundary), #7 (workflow), #8 (converter), #9 (packaging), #11 (verification).
