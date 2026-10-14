# Contributing to Advanced HWP MCP Server

Thank you for helping make Korean HWP automation more reliable.

## Before reporting a bug

Check existing issues, especially [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1).
Reproduce using the latest default branch and the [installation guide](INSTALLATION_GUIDE.md).
Please include:

- Windows edition, Python version, Hangul/HWP version, and MCP client/version
- Exact requested tool, arguments with **all sensitive paths/text anonymized**, expected and actual outcomes
- Whether the HWP file was physically created and could be reopened
- Redacted errors or logs, with API keys, names, tokens, customer documents, and local usernames removed

Do not attach real personal/customer HWP documents or screenshots containing sensitive content.
Use a synthetic document such as `Hello HWP MCP`.

## Changes and pull requests

1. Open an issue before large or incompatible behavior changes.
2. Keep changes small and tied to a reproducible problem.
3. Run `python -m unittest discover -s tests -v` for mocked checks.
4. For COM/API behavior changes, include a Windows/HWP manual test description.
5. Explain what was *not* tested. Do not claim Linux CI verifies HWP integration.
6. Do not add hard-coded local paths, secrets, or private source materials.

## License status

The historical README mentioned MIT, but a formal license file and code-rights audit
have not been completed. Please do not assume contributions may be redistributed as MIT
until a maintainer resolves this issue and documents a license clearly.
Significant external contributions should wait for an explicit contributor/license policy.

For unresolved questions, use GitHub Issues.
