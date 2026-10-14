# OSS viability review — evidence before feature expansion

> **OWNER DIRECTIVE — 2026-10-15:** The earlier competitor-review/upstream-contribution tasks in this document are **superseded and not actionable**. Do not inspect, modify, comment on, monitor, or contribute to external repositories. The sole permitted development target is our own `skerishKang/33MCP_HWP_Limone`, including issue #1 reports inside this repository and our own local source. Re-evaluate investment from reproducible **internal** installation, SaveAs/reopen, COM stability, and maintainer readiness evidence. All historical competitor references below remain context only; do not treat them as assignments.


**Decision date:** 2026-10-15 KST
**Scope:** this existing public HWP MCP repository. Broader confidential/undisclosed project comparisons must remain outside this public repository.

## Current operating decision

**Status: MAINTAIN_AND_EVALUATE. No major 33/34/35 merger or new feature programme is authorized by this document.**
The overarching goal is meaningful open-source value and a credible maintainer contribution record, not the sheer number of tools or achieving an OpenAI program benefit at any cost.

Keep the current public code, issue #1, documentation, prior developer contributions and experimental Draft PR #2. Do not merge the Draft or advertise real HWP success until the real-world defects are resolved. New experimental functions remain OFF by default.

This is a prioritization reset, **not** a decision to delete code, close users' issues, relicense the repository, or abandon HWP.

## What the evidence currently supports

| Signal | Verified observation | Limitation |
|---|---|---|
| External user | Public issue [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1): Gemini CLI installation and reports of auto-start/save trouble | One report; does not demonstrate broad sustained adoption |
| HWP implementation | Existing COM-backed MCP; extra local 33 implementation, local 34 workflow, local 35 converter exist | Many advertised tools/behaviors lack real Windows acceptance |
| Development work | [Draft PR #2](https://github.com/skerishKang/33MCP_HWP_Limone/pull/2), HEAD `da39919588b78e96fc42fabc90cdb94a0d37c469`, contains experimental workflow/converter code + opt-in gate | Mock tests and CI green; **Windows acceptance NOT PASS** |
| Native conversion | Synthetic PDF native-text → HTML test passed locally | OCR, tables, HWP fidelity and real HWP→PDF→HTML NOT PROVEN |
| Windows HWP stability | Real attempts recorded WinError 267 and `combase.dll` `0xC0000005` process crash; child process isolation implemented | Isolation is a mitigation, **not** a demonstrated COM bug fix |
| Local 34 + 35 | Automation/format-conversion ideas and some code exist | Local 34 table API stubs and local 35 simulated score cannot count as working differentiation |
| Licensing | Local 33 has a MIT license file, public main has no repo-wide LICENSE | Audit rights and secure explicit owner decision before licensing/copying |

No current evidence proves the project is superior to established alternatives, eligible for a particular program, or ready to ship.

## Competitive gap review (Issue #16)

Compare a small set of actively maintained HWP/HWPX tooling (including non-MCP alternatives) against **the same real-world workflows**:
1. Install time and prerequisites: clean Windows + Hangul versus cross-platform operation without Hangul.
2. HWP/HWPX format coverage, roundtrip fidelity, real table/paragraph/style operations.
3. Actual document save and reopen behavior with synthetic complicated Korean templates.
4. Reproducibility, error recovery and usability from Claude/Gemini/Codex where supported.
5. Maintenance frequency, community-reported issues and open license/provenance clarity.

**Do not equate feature-list size with quality.** Capture named upstream project links, pinned revisions, license and reproducible results, not unverified marketing claims. Do not copy third-party code as our own.

## Short, decisive evidence tasks

**A — User repair (issue #5, external #1):** demonstrate that starting MCP does not start Hangul and a simple synthetic HWP create→save→reopen works in one documented Windows environment. If blocked, preserve the exact failure and the next smallest diagnostic, not an artificial PASS.

**B — Competitive differentiator (issue #16):** choose **one** narrow document workflow where comparable tools seem weak. Test our implementation and at least one credible alternative on the same synthetic document. Publish factual strengths and weaknesses. Do not invent benchmarks.

**C — Authentic adoption (issue #16):** solicit voluntary feedback, respond to issue #1, and observe real external installs, pull requests and bug reports. Stars alone are not users and need no artificial inflation.

**D — Maintainability/legal readiness (#4/#10):** audit source provenance, secret-bearing history and the public license decision before any new code imports/release.

## Decision at the end of evidence collection

Record one outcome in issue #16, supported by links/logs and an actual maintainer decision:

- **INVEST:** demonstrable user demand AND measurable advantage in a narrow HWP workflow. Resume only the smallest issue that serves it (#6–#9, #12–#15 as applicable).
- **MAINTAIN:** useful for existing users but no demonstrated advantage. Fix bugs and maintain, do not expand aggressively.
- **PIVOT:** little user demand/weak edge relative to mature alternatives. Keep the public repository honest and usable; prioritize another codebase or upstream open-source contribution separately.

There is **no default timeframe or unsupported numerical star threshold**. Evaluate when the factual comparisons are complete, and use maintainer attention efficiently.

## Automation / agent stop rule

Until an INVEST decision is explicitly recorded in #16:
- **ACTIVE:** #1, #5, #11 (actual defect), #16 (market evidence); #4/#10 limited to necessary source/license/public-readiness audit.
- **HOLD:** #6–#9, #12–#15 (new feature architecture, conversion expansion, GUI, document templates, batch, diff).
- **PRESERVE:** Draft PR #2 without Ready/merge, especially its experimental default-OFF tools; no new repo, release or license.
- Current HWP code is **not** a dependency or implementation mandate for PADIEM Connector; any reusable technology can be evaluated separately.

**Program context:** OpenAI Codex for OSS has a competitive application process. This document does not assert admission criteria or benefits beyond the actual current program's published terms. Application preparation must be based on real open-source maintainer contributions, not promises of future usage.

Official information: https://developers.openai.com/community/codex-for-oss
