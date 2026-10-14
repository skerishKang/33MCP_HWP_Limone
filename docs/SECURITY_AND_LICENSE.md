# Security, rights and publishing checklist

**This is a decision document, not legal advice or an OSS license grant.** No license/public upload is authorized merely because a source folder is local.

## Copyright / provenance
- GitHub `main` has **no LICENSE** at 2026-10-15. Its README's statement “MIT” is not equivalent to verifying all current files' provenance or shipping the full license terms.
- Local `workdiary/33-MCP_HWP/LICENSE` contains MIT Copyright (c) 2024 skerishKang. Verify ownership and file history before adopting for this repository.
- Local 34 and 35 had no top-level LICENSE in the initial survey. Absence is not permission to copy into an open-source repo.
- Independent third-party clones inside `workdiary/42.mcp_server`, `112-Gemini-Browser` and similar folders remain attributable to their authors, not this repository.
- Require an owner decision to apply an explicit LICENSE and finalize redistributable source list. Do not accidentally add commercial/customer artifacts.

## Public file categories
| Class | Public default | Reason |
|---|---|---|
| Original source code with provenance cleared | Conditional | owner rights, dependency notices and code audit |
| Examples using fictional names, generated synthetic docs | Conditional | no real customer data |
| Public README, instructions, tests using mocks | Usually safe after review | may still contain internal paths or credentials |
| `.env`, API keys, service accounts, sessions, cookies | NEVER | live credentials |
| Real HWP/PDF/DOCX/XLSX customer or personal docs | NEVER without explicit documented authorization | private/regulated content |
| `.git` from copied folder, runtime DB, logs, backups, caches, screenshots | NEVER by default | history/private data |
| Downloaded third-party repository copy | Do not rebrand as original | copyright attribution and license obligations |

## Pre-upload checks
1. Build a manifest of intended source files; copy an explicit allowlist to an **empty** staging tree, not the full source root.
2. Inspect raw text **and git history** for keys, usernames, file-system paths, private customer data, and copyright headers; report findings without displaying secrets.
3. Review dependencies and third-party files/assets, including templates/font resources, for notices.
4. Verify all samples are synthetic and binary artifacts intentionally redistributable.
5. Ensure install instructions use placeholder/portable paths and `.env.example` dummy values only.
6. Check HWP COM process permissions, path traversal, arbitrary command execution, export output routes, upload surfaces.
7. Ask project owner to decide only unresolved rights/license/public-scope questions. Do not create a new repository as a workaround.
8. Open Draft PR. Do not merge/publicly release until blocking findings are resolved.

## Runtime access controls
- Default only expressly specified input/output roots; reject traversal and unexpected symlink escapes.
- Avoid destructive overwrite unless user explicitly opts in. Isolate temporary files and backups per job.
- MCP tool outputs contain concise status, not document contents, auth tokens or full machine details unless necessary and consented.
- Actual Windows HWP COM calls require explicit test in the supported runtime; mocked permission checks are not production guarantees.

Tracking #10 (license/audit), #4 (provenance), #11 (acceptance), #16 (release).
