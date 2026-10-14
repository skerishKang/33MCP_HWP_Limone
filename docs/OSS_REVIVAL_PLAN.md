# OSS revival and Codex for OSS readiness plan

Status: **implementation in progress, not yet eligible/approved**  
Baseline: `main` at `e9ced8bebe3c8c9358ca0bcf0f21eb1bbd044625`, 2025-07-11.  
Prepared: 2026-10-15 (KST). Maintainer approval is required for new license/release decisions.

## Why this repository

The repository provides a Windows HWP (Hangul) automation MCP server.
Public issue [#1](https://github.com/skerishKang/33MCP_HWP_Limone/issues/1) reports
a working Gemini CLI installation, unwanted HWP process startup on client launch,
and failure to locate saved documents. This is a real external-use and feedback signal,
not proof of broad adoption.

## Current evidence and gaps

- Public repository; observed 6 GitHub stars and 1 fork at the baseline review.
- README asserts MIT, but no LICENSE file. **No OSS license may be inferred from README alone.**
- No tagged release, GitHub Actions workflow, dedicated contributor guide, or portable client configuration at baseline.
- The original startup path eagerly initialized `HWPFrame.HwpObject`.
- The original save path used `FileSaveAs` with an unchecked Execute result.
- The old requirements included `pythoncom`, which ships with pywin32 on Windows rather than as its own installable requirement.
- Source includes methods using HWP COM action APIs that need version-specific Windows acceptance.
- The startup and save behavior require validation on a Windows machine with HWP installed.
- GitHub stars/forks, issue comments, and CI are **not** substitutes for real user acceptance.

## Phase A — restore actual utility (first priority)

- [x] Avoid launching HWP merely by starting the stdio MCP server.
- [x] Use HwpObject.SaveAs for explicit-path HWP saves; check API result and output file.
- [x] Require an explicit file path when saving a new/unsaved document.
- [x] Remove invalid `pythoncom` requirement.
- [x] Correct repository URL and generate local config without shipping a private machine path.
- [x] Add lightweight mocked checks and CI.
- [ ] Run end-to-end Windows test: connect → new document → insert text → save .hwp → reopen → confirm contents.
- [ ] Obtain explicit feedback from the original reporter or another user before closing #1.
- [ ] Review error messages and unexpected HWP dialogs and apply minimum targeted fixes.

## Phase B — trustworthy OSS maintenance

- [x] Record an honest roadmap and contribution guide.
- [ ] Audit copyright ownership, borrowed source/assets, third-party licenses, and HWP automation/API terms.
- [ ] Decide the repository license (MIT was only documented, not implemented). **Owner decision required.**
- [ ] Add a matching LICENSE file after approval.
- [ ] Confirm dependency versions and Windows/HWP compatibility matrix.
- [ ] Release a version tag only after acceptance; publish changelog and reproducible evidence.
- [ ] Respond to real community issues and accept reproducible PRs when appropriate.
- [ ] Add a targeted security policy once the supported versions and contact route are confirmed.

## Phase C — adoption and application

- [ ] Invite voluntary Windows users to try the documented example, and collect anonymized results.
- [ ] Measure real GitHub traffic, version downloads, issue responsiveness, external PRs, and known integrations.
- [ ] Offer bilingual quick start if there is English-language demand.
- [ ] Write a `<=500`-character, source-backed ecosystem importance statement.
- [ ] Write a `<=500`-character proposal for OpenAI API credit usage tied to open-source maintenance (issue triage / PR reviews / releases).
- [ ] Have the actual primary/core maintainer submit the application; never invent usage numbers.

Official information: https://developers.openai.com/community/codex-for-oss
Application: https://openai.com/form/codex-for-oss/

## Boundaries

- The public repository already exposes code and development artifacts; do not add user files, credentials, private business material, or customer content.
- Do not change license, repository visibility, or publish a release implicitly.
- Mocked CI green is **not** Windows COM proof.
- Leave #1 open until HWP end-to-end and reporter acceptance are verified.
- Do not add long review gates or unrelated re-architecture: fix the user's demonstrated failure first.
