# Advanced HWP MCP roadmap — evidence-first reset (2026-10-15 KST)

> **OWNER SCOPE OVERRIDE — 2026-10-15:** Work ONLY on `skerishKang/33MCP_HWP_Limone`. No external OSS work, upstream PRs, forks, outside repo reviews, comments, follow-ups or monitoring. Existing outside actions are historical and must not trigger new work. Prioritise our issue #1/#5 startup/save repair and #11 Windows COM failure. Issue #16 is internal product readiness; competitor benchmarking and outside contribution are no longer required. See `AGENTS.md`.
 

> **Current priority: determine whether continued HWP development creates distinctive OSS value.** The earlier plan to integrate local workdiary 33+34+35 is a hypothesis, **not an approved unconditional build order**.
>
> [Evidence and decision rules](OSS_FIT_REVIEW.md) · [Epic #3](https://github.com/skerishKang/33MCP_HWP_Limone/issues/3) · [OSS viability #16](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16)

## NOW — preserve users, determine value

- [ ] [#5](https://github.com/skerishKang/33MCP_HWP_Limone/issues/5) Fix external [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1): no unrequested HWP launch, real save/reopen; don't close without actual evidence.
- [ ] [#11](https://github.com/skerishKang/33MCP_HWP_Limone/issues/11) Investigate the Windows COM failure and confirm any fix using synthetic documents in a suitable test environment. The observed `combase.dll` crash is not fixed by adding a subprocess.
- [ ] [#16](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16) Compare with established alternatives, seek genuine user needs, test ONE concrete differentiator and decide INVEST / MAINTAIN / PIVOT.
- [ ] [#4](https://github.com/skerishKang/33MCP_HWP_Limone/issues/4) Identify needed local source/provenance only for relevant fixes.
- [ ] [#10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10) Rights/secrets/license audit before any new publication or public code import.

**Existing asset:** [Draft PR #2](https://github.com/skerishKang/33MCP_HWP_Limone/pull/2), HEAD `da39919`: lazy-init/save improvements + opt-in experimental text workflow and PDF conversion. Locally 24/24 tests and exact-head GitHub CI passed; **real Windows HWP acceptance did not pass**. Preserve; no Ready/merge/release. Experimental tools default OFF.

## HOLD — new architecture/features, not abandoned

The following remain visible for future reuse, but an agent must **not pick one merely because it is numbered or appears next in a roadmap**:

- [#6](https://github.com/skerishKang/33MCP_HWP_Limone/issues/6) COM/common architecture expansion
- [#7](https://github.com/skerishKang/33MCP_HWP_Limone/issues/7) 34 workflow, table editing, rollback
- [#8](https://github.com/skerishKang/33MCP_HWP_Limone/issues/8) 35 conversion pipeline and accuracy work
- [#9](https://github.com/skerishKang/33MCP_HWP_Limone/issues/9) Unified packaging
- [#12](https://github.com/skerishKang/33MCP_HWP_Limone/issues/12) Installer/GUI enhancements
- [#13](https://github.com/skerishKang/33MCP_HWP_Limone/issues/13) Templates
- [#14](https://github.com/skerishKang/33MCP_HWP_Limone/issues/14) Batch processing
- [#15](https://github.com/skerishKang/33MCP_HWP_Limone/issues/15) Before/after diff

Resume only a specifically justified subset if [#16](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16) records a source-backed INVEST decision or the owner explicitly prioritizes a discrete user issue.

## Release and submission

- No official release while known install/save problems or Windows acceptance failures remain.
- Do not claim a simulated accuracy figure or a mocked COM test proves native HWP fidelity.
- An OSS application must accurately demonstrate maintainer work, quality and actual adoption; acceptance is not promised.
- Licensing/rights/public scope remain the owner's decision. No automatic new repo, bundled private app, LICENSE change, or source disclosure.

## Operating rule for agents

1. Read [AGENTS](../AGENTS.md), this roadmap and [OSS_FIT_REVIEW](OSS_FIT_REVIEW.md).
2. Check exact GitHub state, real failures, issue owner and currently active PRs.
3. Prefer one proven bug fix or one discriminating experiment; avoid feature-count races.
4. Report what was tested (mock/static/real), the actual reason for failure and next possible fix.
5. Keep HOLD issues open for traceability; do not auto-merge Draft PR #2.

This replaces the prior mandatory Phase 0→1→2 build train without erasing its design history.
