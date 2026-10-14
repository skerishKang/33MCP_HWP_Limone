# Source inventory and evidence status

> **STATUS UPDATE — 2026-10-15:** Source mapping is preserved as reference evidence, **not an instruction to import 33/34/35 wholesale**. The priority is external user #1 repair and OSS competitive validation (#16). All proposed import decisions are on HOLD pending an evidence-backed INVEST decision or the owner's explicit scoped priority. See [OSS_FIT_REVIEW](OSS_FIT_REVIEW.md).


**Date:** 2026-10-15 KST  
**Target:** existing public GitHub repository `skerishKang/33MCP_HWP_Limone`. No new repository.  
**Source folders:** `workdiary/33-MCP_HWP`, `workdiary/34-hwp-automation`, `workdiary/35-hwp-pdf-html`. These are **local inputs**, not automatically part of this public repository.

## Baseline and discrepancies

| Source | Observed assets | What is NOT proved |
|---|---|---|
| GitHub `main` | `advanced_hwp_server.py`, `test_hwp_server.py`, Windows installation guide, Claude config, README | No recent HWP integration evidence; README performance assertions and broad feature claims are not benchmarks |
| Draft PR #2 | Lazy HWP initialization, more truthful save flow, dependency/doc updates, mocked CI checks | Draft; CI mocks do **not** prove live Windows COM or HWP output |
| Local 33 | `advanced_hwp_server.py`, `advanced_hwp_server_v3.py`, `hwp_core.py`, `hwp_document.py`, `hwp_table.py`, GUI config, `tests/`, `LICENSE`, CHANGELOG | Which v1/v3 modules execute end-to-end, compatibility, actual performance |
| Local 34 | `src/engine.py`, `src/hwp_driver.py`, rollback/locking/idempotency, mock/real tests, operational docs | `fill_table()` returns True without writing, `get_cell_value()` and `get_text_at()` return empty values; documented real-world successes need fresh reproducible proof |
| Local 35 | `src/pipelines`, `src/shared`, CLI, evaluation documents, tests | `scripts/run_eval.py` is **simulated** with embedded scores; 12/15 is NOT actual measured conversion accuracy; `main.py` references PipelineA/B without observed import/definition |
 
## Copyright and publicity status

- Local 33 contains `LICENSE` with “MIT License, Copyright (c) 2024 skerishKang”; GitHub `main` has **no** `LICENSE` file. A local license file is **not** approval to copy all local content or alter GitHub repo licensing.
- Check each copied module for upstream/third-party origins, assets, dependencies and notices. `42.mcp_server` contains third-party projects and must not be treated as the author's own code.
- Keep `.env`, credentials, logs, user documents, `.git` directories, build artifacts and personal filesystem paths **out** of import commits.
- Inspect existing Git history as well as working files before any public upload.
- Decisions about licensing, ownership or publishability belong to the project owner.

## Source-to-target decision worksheet

| Source | Proposed target | Decision | Required evidence |
|---|---|---|---|
| 33 MCP entry point | `advanced_hwp_server.py` | Keep wrapper for compatibility | Existing tool names and stdio behavior |
| 33 core document APIs | `src/hwp_mcp` / `src/hwp_common` | Compare then selectively import | Tests + Windows HWP |
| 34 workflow/action engine | `src/hwp_automation` | Selectively import; no stubs counted as done | Real write/rollback/idempotency proof |
| 35 conversion pipelines | `src/hwp_converter` | Isolate optional feature | Actual output/golden-set evaluation |
| 33 GUI installer | `scripts` / optional UI | Evaluate | Clean Windows installation |
| Local sample documents | Not in public repo by default | Do not copy | Explicit synthetic test data only |

**Tracking:** [Epic #3](https://github.com/skerishKang/33MCP_HWP_Limone/issues/3), [source audit #4](https://github.com/skerishKang/33MCP_HWP_Limone/issues/4), [licensing #10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10).
