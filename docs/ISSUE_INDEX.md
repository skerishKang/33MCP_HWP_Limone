# GitHub issues — HWP unification

**Epic:** [#3](https://github.com/skerishKang/33MCP_HWP_Limone/issues/3). Existing public repository remains the only official repo.

| Priority | Issue | Work | Dependency |
|---|---|---|---|
| P0 | [#4](https://github.com/skerishKang/33MCP_HWP_Limone/issues/4) | 33/34/35 source inventory + provenance | None |
| P0 | [#5](https://github.com/skerishKang/33MCP_HWP_Limone/issues/5) | Bug #1 startup and SaveAs proof | Draft PR #2 |
| P0 | [#6](https://github.com/skerishKang/33MCP_HWP_Limone/issues/6) | Common COM/file/result boundaries | #4 |
| P1 | [#7](https://github.com/skerishKang/33MCP_HWP_Limone/issues/7) | Local 34 workflow engine | #4, #6 |
| P1 | [#8](https://github.com/skerishKang/33MCP_HWP_Limone/issues/8) | Local 35 conversion with real accuracy | #4, #6 |
| P1 | [#9](https://github.com/skerishKang/33MCP_HWP_Limone/issues/9) | Packaging and compatibility | #5, #6 |
| P0 | [#10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10) | Security, source rights and licensing | #4 |
| P0 | [#11](https://github.com/skerishKang/33MCP_HWP_Limone/issues/11) | Live Windows E2E + distinct mocks | #5, #7, #8 as available |
| P1 | [#12](https://github.com/skerishKang/33MCP_HWP_Limone/issues/12) | Simple Windows setup and GUI | #5, #9 |
| P2 | [#13](https://github.com/skerishKang/33MCP_HWP_Limone/issues/13) | Document templates | #7 |
| P2 | [#14](https://github.com/skerishKang/33MCP_HWP_Limone/issues/14) | Batch edit and recovery | #7 |
| P2 | [#15](https://github.com/skerishKang/33MCP_HWP_Limone/issues/15) | Before/after diff reports | #7, #8 optional |
| P1 | [#16](https://github.com/skerishKang/33MCP_HWP_Limone/issues/16) | Open-source maintenance/release/OSS application | #10, #11 |

Existing issue [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1) is external user feedback; keep open until accepted evidence. Draft PR [#2](https://github.com/skerishKang/33MCP_HWP_Limone/pull/2) is not merged or real-HWP verified.

## Labels and status convention
Issue titles mark P0/P1/P2 to avoid dependence on repository label configuration.
Accepted result statuses: `NOT_RUN`, `MOCK_ONLY`, `NOT_IMPLEMENTED`, `FAILED`, `BLOCKED`, `REAL_WINDOWS_PASS`.

Prioritize reproduction/working behavior. Do not repeatedly request owner authorization for ordinary technical choices.
