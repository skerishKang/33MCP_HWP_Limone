# Issue board — current priorities (2026-10-15 KST)

**Main decision:** [#16 OSS viability / competitive differentiation](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16). **Product epic:** [#3](https://github.com/skerishKang/33MCP_HWP_Limone/issues/3).

The old table ordered 33+34+35 feature building as an assumed plan. This new board distinguishes **active evidence/repair** from **conditional work on HOLD**.

| State | Issue | Scope | Next allowed action |
|---|---|---|---|
| ACTIVE | [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1) | Actual external Gemini CLI startup/save report | Reproduce and fix, preserve external feedback |
| ACTIVE | [#5](https://github.com/skerishKang/33MCP_HWP_Limone/issues/5) | Client compatibility/save | Real Windows save/reopen proof; coordinate Draft #2 |
| ACTIVE | [#11](https://github.com/skerishKang/33MCP_HWP_Limone/issues/11) | COM crash and real acceptance | Narrow isolated root-cause investigation |
| ACTIVE | [#16](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16) | OSS market/maintainer fit | Compare alternatives and record INVEST/MAINTAIN/PIVOT |
| CONDITIONAL | [#4](https://github.com/skerishKang/33MCP_HWP_Limone/issues/4) | Local 33/34/35 code and provenance | Read-only scoped source audit; do not copy whole folders |
| CONDITIONAL | [#10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10) | Rights/security/license | Required before license/public import/release |
| HOLD | [#6](https://github.com/skerishKang/33MCP_HWP_Limone/issues/6) | Shared COM architecture | Only if a justified user flow needs it |
| HOLD | [#7](https://github.com/skerishKang/33MCP_HWP_Limone/issues/7) | 34 workflow | No broad table/rollback expansion now |
| HOLD | [#8](https://github.com/skerishKang/33MCP_HWP_Limone/issues/8) | 35 converter | No unsupported fidelity/OCR promises |
| HOLD | [#9](https://github.com/skerishKang/33MCP_HWP_Limone/issues/9) | Packaging unification | No 3-project integration without differentiator |
| HOLD | [#12](https://github.com/skerishKang/33MCP_HWP_Limone/issues/12) | Installer/GUI | No new UX features while core real use fails |
| HOLD | [#13](https://github.com/skerishKang/33MCP_HWP_Limone/issues/13) | Templates | Need actual user case |
| HOLD | [#14](https://github.com/skerishKang/33MCP_HWP_Limone/issues/14) | Batch | Need proven reliable single-document flow |
| HOLD | [#15](https://github.com/skerishKang/33MCP_HWP_Limone/issues/15) | Diff | Need user demand and verified document comparison |

**Preserved experimental PR:** [#2](https://github.com/skerishKang/33MCP_HWP_Limone/pull/2) remains DRAFT/default OFF; local synthetic PDF success and 24 mocked/local tests are not real Windows HWP acceptance.

## Intake and closeout

- No new issues unless a distinct external defect or a validated differentiation experiment actually warrants one. Prefer #16 for comparisons.
- Maintainer work is not automatically abandoned by HOLD. Reopen implementation from issue context only after #16's explicit INVEST decision or a clearly prioritized owner request.
- Do not close #1 for mock CI, do not rewrite history, and do not mark a blocked native COM path green.
- [Evidence and decision rubric](OSS_FIT_REVIEW.md); [Roadmap](ROADMAP.md); [source inventory](PROJECT_INVENTORY.md).
