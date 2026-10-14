# Architecture decisions and open owner choices

## ADR-001 — Preserve existing GitHub repository
**Decision:** integrate local 33/34/35 into `skerishKang/33MCP_HWP_Limone`. Do **not** create another repo.
**Reason:** existing users, stars, issue #1, source history and MCP entrypoint should continue to work.

## ADR-002 — One MCP interface, separate modules
**Decision:** keep a single stdio MCP server while factoring HWP editing, automation and conversion into separate internal modules.
**Reason:** users should install one product; components need distinct Windows vs cross-platform dependencies and verification.
**Status:** design only, implementation issue #6 / #9.

## ADR-003 — Import selectively, never blindly copy the full three folders
**Decision:** existing local source folders remain untouched, and a clean staged copy includes only rights-cleared, relevant modules.
**Reason:** local 34 has operational stubs, local 35 hardcoded simulated scores, and local 33 includes multiple versions and local environment data.
**Status:** audit #4.

## ADR-004 — Real HWP test beats documentation claims
**Decision:** a passing mock/CI run cannot represent a user-visible HWP result. Actual Windows+HWP create→save→reopen proof is required to mark core integration successful.
**Status:** #11.

## ADR-005 — No new licensing decision through documentation
**Decision:** local 33 includes an MIT file; public GitHub main does not. Owner confirms rights and LICENSE choice in #10 before publishing consolidated files.
**Status:** owner decision outstanding; do not infer entitlement to copy all code.

## ADR-006 — Documentation PR separated from functional fixes
**Decision:** keep the governance/docs PR independent from unverified code fixes in Draft PR #2. Conflicts involving `README.md` and `CONTRIBUTING.md` must be reconciled before merging either PR. No automatic merge.
**Reason:** a successful documentation update must not quietly deploy unproven Windows COM changes.

## Questions reserved for owner
- Does the owner authorize consolidating rights-cleared local 33/34/35 code for public OSS publication?
- Which license(s), if any, apply after verifying contributors and third-party components?
- Are there commercial/proprietary components that must remain separate?

Other code details may be decided by implementers with issue evidence.
