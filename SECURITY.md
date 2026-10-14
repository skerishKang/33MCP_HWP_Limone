# Security Policy

## Supported versions
No version has been newly designated as security-supported in the unified roadmap. The repository is undergoing code and licensing review. See [Release Process](docs/RELEASE_PROCESS.md).

## Reporting a vulnerability
Do **not** put credentials, customer HWP documents, session tokens, or exploit details that would reveal a private system into a public issue. If GitHub's private vulnerability reporting is enabled for this repository, use that mechanism. Otherwise contact the repository owner privately through an established trusted channel; do not publish the sensitive material until the maintainer has arranged a safe reporting method.

For reproducible non-sensitive security bugs (e.g., synthetic file path traversal or mocked permission checks), a standard GitHub issue is appropriate.

Please include affected version/commit, how the issue can be reproduced using synthetic data, impact and any safe workaround. Do not attempt to access systems or content that you are not authorized to test.

## Security principles
- Respect local filesystem allowlists; reject path escapes.
- Protect real HWP/PDF content, temporary files, conversion results and backups.
- Never log auth tokens or actual customer document text by default.
- Avoid automatically launching or terminating unrelated HWP instances.
- Changes to security boundaries need focused negative tests, and actual Windows checks when COM is involved.
- Third-party licenses and credential/history scanning are required before new public code imports.

See [Security and License checklist](docs/SECURITY_AND_LICENSE.md) and [issue #10](https://github.com/skerishKang/33MCP_HWP_Limone/issues/10).
