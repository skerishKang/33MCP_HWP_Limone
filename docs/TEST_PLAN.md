# Verification & acceptance matrix

**Rule:** Tests must distinguish simulated, mocked, static, and actual Windows/HWP runs.

## Vocabulary
- `STATIC`: syntax, dependency or code inspection.
- `MOCK_ONLY`: mocked/fake COM tests without real Hangul.
- `REAL_WINDOWS_PASS`: Windows + installed Hancom Hangul + MCP client produces a real saved HWP and reopen-check.
- `NOT_RUN`: no evidence collected.
- `NOT_IMPLEMENTED`: stubbed code, no real effect.
- `FAILED`: repro against actual code.
- `BLOCKED`: evidence not obtainable; explain cause/next feasible step.

## Minimal matrix
| ID | Path | Expected proof | Status (as of 2026-10-15) |
|---|---|---|---|
| T01 | Python syntax/import | compile/import and dependencies | PR #2 CI passed; not merged |
| T02 | MCP server starts without launching HWP | process observation with client | MOCK_ONLY in PR #2; REAL NOT_RUN |
| T03 | Create→type→SaveAs explicit path | HWP success+output file | MOCK_ONLY in PR #2; REAL NOT_RUN |
| T04 | Saved HWP reopens and contains expected text | reopen/compare actual text | NOT_RUN |
| T05 | Existing file is preserved if save fails | original hash unchanged | NOT_RUN |
| T06 | Table cell actual write + readback | actual HWP cell value | NOT_IMPLEMENTED in local 34 stub |
| T07 | Workflow crash/fail rollback | before-after original hash + journal | NOT_RUN |
| T08 | Duplicate job idempotency | second execution avoids duplicate effects | MOCK code exists in local 34; REAL NOT_RUN |
| T09 | HWP→PDF→HTML | synthetic HWP, real PDF/HTML outputs | NOT_RUN |
| T10 | PDF→HTML scanned/native quality | gold sample + measured text/table/layout | NOT_RUN; local simulated scores do not count |
| T11 | Claude Desktop stdio configuration | client tools registered + task completed | NOT_RUN in current environment |
| T12 | Gemini CLI issue #1 reproduction/resolution | external reporter-compatible Windows setup | NOT_RUN |
| T13 | Public release secrets/license provenance | inspected file+history, owner decision | NOT_RUN |

## Small live acceptance suite
1. Record Windows/HWP/COM/Python/MCP-client versions and exact commit.
2. With a synthetic document, connect client and observe idle state (no Hangul launch).
3. Invoke create document tool (Hangul launches on demand), insert Korean text, save to a temporary allowed folder.
4. Confirm file exists, is nonempty, and reopen it using Hangul; check text.
5. Repeat on an existing input without mutating original. Simulate missing directory/permission/file locked failures.
6. When 34 integrated: verify actual table cell write and backup/rollback after induced mid-job failure.
7. When 35 integrated: run 15 or more documented **real** golden docs, calculate actual text/table/layout metrics, publish failures too.

## CI versus actual integration
- PR #2 adds mocked Python 3.10/3.11/3.12 regressions; it does **not** load Windows COM.
- CI should stay fast, deterministic and isolated; untrusted PR code should not run with customer data or secrets.
- Real Windows acceptance can be manually recorded for early versions. CI pass is not a release substitute.
- Real binaries/docs used for QA must be synthetic/authorized and should not be uploaded without checking rights.

## Report template
```text
HEAD: <sha>
Platform: Windows / Python / HWP version / MCP client
Case: T##
Result: STATIC | MOCK_ONLY | REAL_WINDOWS_PASS | NOT_RUN | NOT_IMPLEMENTED | FAILED | BLOCKED
Input: synthetic test fixture identifier
Output: verified file name, size, reopen-check result
Cause of failure: <precise reason>
Resolution / owner action: <next shortest concrete task>
```

The purpose is truthful troubleshooting rather than creating more review stages. Tracking #11, #5, #7, #8.
