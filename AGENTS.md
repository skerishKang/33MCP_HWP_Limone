# AGENTS.md — Advanced HWP MCP working instructions

> Read at the start of each agent session in this repository. Also read `README.md`, `docs/ROADMAP.md`, `docs/PROJECT_INVENTORY.md`, and the active GitHub issue. These instructions guide contributors; they are not a guarantee that every AI tool automatically loads the file. Check the actual agent's startup convention.

## CURRENT PRIORITY OVERRIDE — 2026-10-15

The earlier instruction to "deliver one user-facing MCP server with full 33/34/35 integration" is **superseded as an unconditional implementation goal**.

**Current goal:** maintain existing users and determine whether this repository has a demonstrable, differentiated open-source use case. Read `docs/OSS_FIT_REVIEW.md` and current issue #16 before creating any new feature.

**Allowed without new scope:** investigate/fix external #1 and narrow COM failure (#5/#11); assess genuine demand, alternatives and differentiation (#16); scoped source/security/license audit (#4/#10); improve factual documentation and focused tests.

**On HOLD unless owner specifically reprioritizes or issue #16 records evidence-backed INVEST:** #6–#9 and #12–#15. Do not start large local 33+34+35 copying, table/GUI/batch/format feature work merely because the old roadmap describes it.

**Preserve:** existing `main`, users, local source folders, Draft PR #2 (experimental tools OFF by default), no release/merge/license change from this replan. A successful mocked CI does not cure observed `combase.dll` `0xC0000005` native crash.

**If evidence shows no worthwhile advantage, report MAINTAIN or PIVOT rather than manufacturing more features to increase OSS application odds.** Keep comparisons with other unpublished local projects in a nonpublic document; do not upload names or private code into this public repo.

## Mission and authority
- **One existing repository:** `skerishKang/33MCP_HWP_Limone`. Do **not** create a replacement repository.
- Reuse the best verified portions of local workdiary folders `33-MCP_HWP`, `34-hwp-automation`, `35-hwp-pdf-html`.
- Preserve one backwards-compatible MCP entry point and existing users; any modular 33/34/35 integration is **conditional** on the evidence-first decision in #16.
- Owner decides new business strategy, licensing, public/private scope and substantial disclosure. Routine technical work, documentation and Draft PRs are authorized in assigned scope.
- Do not delete original local projects, force-push, overwrite protected history, create production releases or silently change repository visibility.
- **Current special case:** Draft PR #2 already handles lazy startup, save truthfulness, installation guide and mock CI. Compare/coordinate rather than duplicate or merge it unverified.

## First five minutes
1. Check branch, HEAD, worktree diff, open PRs, issue #1, epic #3 and assigned issue.
2. Inspect existing code **before** planning replacements. Local 33 has multiple server versions and is not automatically newer/better than GitHub.
3. Record precise verified state (commit SHA, affected files) and identify shared paths other agents might own.
4. Pick the smallest change to resolve the active issue. Do not begin a broad rewrite or fabricate a new governance gate.
5. Separate what is known, observed, inferred, mock-tested, and Windows real-tested.

## Architectural boundaries
- Keep `advanced_hwp_server.py` and existing MCP tools/arguments compatible until a documented intentional migration.
- Propose internal layers: `hwp_common` (COM STA, file guards, results), `hwp_mcp` (33), `hwp_automation` (34), `hwp_converter` (35). **Proposed, not yet implemented.**
- COM session lifetime is owned by one component; no incidental HWP launch just from MCP startup.
- No routine stdout logging on MCP stdio. No success response for missing/empty/unopenable output.
- Default to preserve source documents and write results separately. Real filesystem checks must back save/convert claims.
- Converter/OCR heavyweight dependencies should not be necessary for basic MCP setup.
- Do not claim HWPX, macOS/Linux HWP COM, or unsupported clients are verified.

## Evidence requirements
- `MOCK_ONLY`: mock CI/test passed; no HWP COM proof.
- `REAL_WINDOWS_PASS`: OS, HWP, client versions and real artifact create/save/reopen proof.
- `NOT_RUN`: test not performed.
- `NOT_IMPLEMENTED`: incomplete/stub API, even when it returns `True`.
- `FAILED` / `BLOCKED`: include cause, impact and proposed solution.
- Local 34 `fill_table` and undo journal getters contain stubs; local 35's 12/15 accuracy is from a hardcoded simulated evaluation. Never report either as a live pass.
- Prefer focused short checks over unnecessary exhaustive suites. Tests must support, not delay, working software.
- Keep external issue #1 open until its actual complaint has been reproduced and resolved.

## Safe changes and data handling
- No public PR uploads of `.env`, tokens, cookie/session files, customer docs, logs, private business docs, copied third-party trees, test recordings, large binaries, or credential-bearing history.
- Work in a separate branch/worktree. Only copy inspected code/modules with rights cleared; retain attribution.
- Local 33 has an MIT LICENSE, but the current GitHub `main` does not. **Do not add a public license or assert repo-wide MIT solely on the basis of local files or README.** See #10.
- Treat generated examples as synthetic. Redact paths and usernames in issue reports and evidence.
- Do not share source files with secrets in public discussions. If a live secret is found, contain/report it without repeating the secret.

## Issue / PR routine
1. Link work to [epic #3](https://github.com/skerishKang/33MCP_HWP_Limone/issues/3) and one focused issue.
2. Commit only relevant files; label what was actually verified.
3. Use Draft PR for incomplete code or uncertain public/licensing changes. Keep a short reproduction/evidence block.
4. Check CI on exact HEAD. CI success alone is **not** release approval.
5. State what remains, then nominate the next concrete action. Close only with grounded acceptance evidence.
6. No automatic merge unless the assigned task authorizes it and the applicable compatibility/security/real-world conditions are met.

## Communication standard
- If a task fails, do not stop at 'cannot do it'. Explain **why**, what was verified, what is missing, and the most direct way to resolve it. Ask the owner only for a decision genuinely reserved for them.
- Never quietly transform public source material into proprietary claims or claim fake benchmark numbers.
- Preserve Korean public documentation; add concise English quickstart as the international OSS audience grows.

## Documentation map
- `docs/OSS_FIT_REVIEW.md`: current priority override and INVEST/MAINTAIN/PIVOT decision
- `docs/PROJECT_INVENTORY.md`: source provenance and gaps
- `docs/ARCHITECTURE.md`: proposed module boundaries
- `docs/ROADMAP.md`: issue sequence and acceptance milestones
- `docs/OPERATIONS.md`: installation/incident operations
- `docs/TEST_PLAN.md`: mock vs real acceptance
- `docs/SECURITY_AND_LICENSE.md`: publishing/permission gates
- `docs/RELEASE_PROCESS.md`: versions, release, rollback
- `CONTRIBUTING.md`: outside contributor guidance
- `SECURITY.md`: vulnerability reporting and sensitive-data handling

Last updated: 2026-10-15 KST.
