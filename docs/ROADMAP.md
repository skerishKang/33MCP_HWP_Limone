# Unified HWP MCP roadmap — 2026-10-15

**Single repository:** `skerishKang/33MCP_HWP_Limone`  
**Principle:** one user-facing HWP MCP tool, multiple independently testable components. The three local folders are **source references**; not yet merged.

## Phase 0 — evidence, user bug and public readiness (P0)
- [ ] [#4](https://github.com/skerishKang/33MCP_HWP_Limone/issues/4) inventory, source/third-party license audit, compare current GitHub vs local 33 / PR #2.
- [ ] [#5](https://github.com/skerishKang/33MCP_HWP_Limone/issues/5) resolve external user [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1); avoid duplicating [Draft PR #2](https://github.com/skerishKang/33MCP_HWP_Limone/pull/2).
- [ ] [#6](https://github.com/skerishKang/33MCP_HWP_Limone/issues/6) agree common COM, file safety and module boundaries.
- [ ] [#10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10) public source/secret/license audit (owner sign-off before LICENSE change).
- [ ] [#11](https://github.com/skerishKang/33MCP_HWP_Limone/issues/11) HWP Windows smoke and distinct mock suite.

**Exit:** no claim of real Windows save success without create→save→reopen proof; no automatic application start; source copies inventoried.

## Phase 1 — integrate verified functionality (P1)
- [ ] [#7](https://github.com/skerishKang/33MCP_HWP_Limone/issues/7) workflow engine, robust table editing and rollback.
- [ ] [#8](https://github.com/skerishKang/33MCP_HWP_Limone/issues/8) real HWP/PDF/HTML conversion & real accuracy measurement.
- [ ] [#9](https://github.com/skerishKang/33MCP_HWP_Limone/issues/9) backwards-compatible package with optional conversion extras.
- [ ] [#12](https://github.com/skerishKang/33MCP_HWP_Limone/issues/12) portable Windows setup/GUI.
- [ ] [#16](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16) version, community and Codex for OSS preparation.

**Exit:** reproducible fresh-machine install, baseline MCP interface preserved, failures truthful, public release only after actual Windows acceptance.

## Phase 2 — user-facing differentiation (P2)
- [ ] [#13](https://github.com/skerishKang/33MCP_HWP_Limone/issues/13) HWP official report/contract templates.
- [ ] [#14](https://github.com/skerishKang/33MCP_HWP_Limone/issues/14) batch jobs, progress, cancellation and recovery.
- [ ] [#15](https://github.com/skerishKang/33MCP_HWP_Limone/issues/15) before/after document diff report.

## Uncommitted ideas (not feature-complete)
- HWPX native parsing and mixed HWP/HWPX workflow
- Interactive preview and user-approved destructive edits
- OCR for scanned PDF and confidence reporting
- English quickstart / examples, public demo with synthetic documents
- General purpose plugin API for new document backends

**Decision rule:** add dedicated issues only after a distinct use case and expected behavior are clear; avoid scope creep before Phase 0.

## Ownership, priority and reporting
- The repository owner decides license and nonpublic material release; ordinary documentation/tests/PR preparation do not require repeated owner sign-offs.
- Define `DONE` only with explicit result+evidence; `MOCK_ONLY`, `NOT_RUN`, `FAILED`, `BLOCKED` are valid statuses.
- Do not merge, tag, push a release or close an external bug merely because CI is green.
