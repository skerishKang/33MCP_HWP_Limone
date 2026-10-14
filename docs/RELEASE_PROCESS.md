# Versioning and public release process

**Current:** no new release is approved by this document. Existing GitHub branch `main` has old source, and Draft PR #2 is unmerged.

## Release types
- `alpha`: feature works in synthetic examples but has incomplete Windows matrix; state limitations.
- `beta`: repeatable installation + real Windows HWP acceptance on at least one declared OS/HWP/client combination; other combinations unverified.
- `stable`: all advertised workflows pass repeatable Windows acceptance and known severe issues are addressed.
- Use SemVer `MAJOR.MINOR.PATCH` for new public versions after initial policy decision; do not borrow historical local 33 `1.0.0` as evidence that the public repo has shipped it.

## Preparation checklist
- [ ] Merge only necessary code after resolving base conflict with Draft PR #2
- [ ] License and ownership audit #10 resolved and owner publicly approves LICENSE choice
- [ ] Source 33/34/35 provenance and rights manifest #4 done
- [ ] README and install instructions match **actual** code and version
- [ ] Existing MCP tool names and schemas smoke-tested
- [ ] Test matrix records exact SHA and Windows/HWP/client versions, including real save-reopen check
- [ ] 34 workflow does not claim success for stubbed editing
- [ ] 35 simulated numbers removed/replaced for public performance claims
- [ ] Synthetic fixture provenance established
- [ ] Secret/history scan and NOTICE/dependency license information reviewed
- [ ] Known failures and compatibility limits listed

## Procedure
1. Identify releasable HEAD with commit SHA and PRs. Do not merge uncertain code solely for convenience.
2. Run short CI regression. Run actual Windows/HWP E2E for changed integration surfaces.
3. Record supported versions, limitations, test results and change list in CHANGELOG.
4. Use owner-approved version/tag and a GitHub Release only after the above checks.
5. Publish a working installation example, synthetic sample and rollback instructions.
6. Re-check external issue #1 and other reporter issues; invite feedback without marking unverified features done.

## Rollback
- If a release breaks the baseline user journey, revert code using a new patch commit/PR or redeploy prior verified tag. Do not destroy tags/history to conceal failures.
- User documents, outputs and backups remain user-owned. Never auto-delete or 'undo' by overwriting the source without verification.
- Record root cause, affected versions, workarounds and minimum safe upgrade.

## OSS and community
- Maintainers must respond to practical issues and PRs; do not fabricate stars, downloads, benchmarks or usage.
- Codex for OSS application is an **application**, not eligibility approval; link real public work and use API credits only as program permits.
- Source code clarity, real HWP usefulness and externally reproducible examples matter more than inflated feature counts.

Issues: #3, #10, #11, #16. This release document is intentionally shorter than a multistage enterprise approval framework.
