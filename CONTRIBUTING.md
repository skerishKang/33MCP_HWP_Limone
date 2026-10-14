# Contributing — Advanced HWP MCP

We welcome bug reports, reproducible synthetic examples, documentation fixes and targeted patches that make Korean Hangul automation reliable.

## Before contributing
- Read [README](README.md), [roadmap](docs/ROADMAP.md), [architecture](docs/ARCHITECTURE.md) and [test plan](docs/TEST_PLAN.md).
- Search [existing issues](https://github.com/skerishKang/33MCP_HWP_Limone/issues), particularly [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1).
- Avoid introducing unrelated code from third-party tools; link upstream and license information if integration is proposed.
- New contributions that depend on a repository-wide OSS license should wait until [#10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10) resolves the explicit licensing policy.

## Reporting a bug
State the exact commit/tag, Windows edition, Python version, Hangul/HWP version, MCP client and tool called. Provide expected behavior, actual behavior and **minimal reproduction with a fictional HWP file**. A screenshot with usernames, customer data or token information should not be posted.

## Proposed change workflow
1. Reference one issue; create a small focused branch.
2. Add a failing test or explain precise reproduction, then fix the cause.
3. Separate static checks, mocked COM tests, and actual Windows/HWP acceptance.
4. For save/convert changes, validate a **real output artifact** and reopen it using a supported application. CI mocks are not enough.
5. Keep the old `advanced_hwp_server.py` entry point and public tools compatible unless the issue explicitly approves migration.
6. State untested cases in the PR. Large refactors should only follow evidence of a concrete problem.
7. Do not use personal/customer documents in tests, and do not commit `.env`, tokens, saved sessions, binary outputs, local path-specific config or copied upstream repos.

## Source modules
The project aims to incorporate verified, rights-cleared code from local 33 (MCP), 34 (workflow), 35 (converter). They are not all implemented in GitHub main. Never present local stubs or simulated numbers as an accepted public feature.

## License
The historic GitHub README said MIT but the public repository currently lacks a LICENSE file. Local 33 has a separate MIT file. The repository owner must complete the [license and provenance review](docs/SECURITY_AND_LICENSE.md) before formal redistribution terms are declared.

Questions: use GitHub Issues without posting secrets. Security-sensitive reports: follow [SECURITY.md](SECURITY.md).
