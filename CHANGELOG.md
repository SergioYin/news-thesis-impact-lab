# Changelog

## 1.0.0 - 2026-07-10

- Added `asset-health` CLI command for deterministic public showcase hardening artifacts under `demo/health/`.
- Added asset health JSON, Markdown, and no-JavaScript HTML with package metadata, advertised command coverage, generated artifact freshness, wheel/sdist presence, repo skill status, local-neutral docs, private-reference scan summary, finance boundary coverage, and final release/promote checklist.
- Integrated asset health with release validation, release manifest, evidence hub, bundle export, demo gallery, maturity report, README, review docs, agent skill, changelog, and tests.
- Added private-reference scan summary behavior that ignores `scripts/privacy_scan.py` regex definitions while still scanning public source and docs.
- Bumped package metadata to 1.0.0 for public showcase readiness.

## 0.9.0 - 2026-07-10

- Added `decision-journal` CLI command for research meeting draft export from impact packet, compare report, trend history, scenario stress, review ledger, and evidence hub artifacts.
- Added decision journal JSON, Markdown, and no-JavaScript HTML artifacts with thesis questions, evidence excerpts, risk flags, unresolved assumptions, editable review-decision placeholders, owner/date blanks, follow-up checklist, explicit boundaries, and a no-recommendation statement.
- Integrated decision journal artifacts with demo gallery, visual receipt, cold-start walkthrough, evidence hub, bundle export, release validation, release manifest, maturity evidence, README, review docs, agent skill, and tests.
- Added validation for deterministic journal output, no-script HTML, and no action-language terms in the journal artifacts.
- Bumped package metadata to 0.9.0.

## 0.8.0 - 2026-07-10

- Added `bundle-export` CLI command for plain-file agent reuse bundles with `bundle_manifest.json`, `bundle_manifest.md`, `bundle_manifest.html`, `bundle_copy_list.json`, and copied public artifacts under `artifacts/`.
- Added `bundle-inspect` CLI command to validate referenced bundle files exist and match SHA-256 hashes, with JSON or Markdown output and nonzero exit on missing or changed artifacts.
- Integrated bundle artifacts with release validation, release manifest commands, maturity evidence, demo gallery, evidence hub, cold-start walkthrough, README, review docs, agent skill, and tests.
- Preserved research-only boundaries with explicit package boundary tags and safety tags for no live data, non-advice, no broker access, no orders, and human review.
- Bumped package metadata to 0.8.0.

## 0.7.0 - 2026-07-10

- Added `evidence-hub` CLI command for reviewer-facing release audit bundles over generated demo artifacts and `release/manifest.json`.
- Added evidence hub JSON, Markdown, and no-JavaScript HTML artifacts with artifact classification, user question answered, maturity rubric category, release and promotion gate relevance, regeneration command, SHA-256, no-JavaScript status, boundary coverage, and limitations.
- Integrated the evidence hub with release validation, release manifest commands, maturity evidence, demo gallery, cold-start walkthrough, README, review docs, agent skill, and tests.
- Bumped package metadata to 0.7.0.

## 0.6.0 - 2026-07-10

- Added `review-ledger` CLI command for repeated-use state across packet, trend history, scenario stress, and optional previous ledger artifacts.
- Added ledger JSON, Markdown, and no-JavaScript HTML artifacts with stable item keys, new/open/watch/resolved status transitions, severity, first/latest seen dates, evidence links, research-only next actions, expiry days, stale flags, and compact summaries.
- Added `examples/review_ledger_previous.json` to demonstrate carry-forward, watch, stale, and resolved behavior.
- Integrated review ledger with demo gallery, visual receipt, walkthrough, release manifest, release validation, maturity evidence, README, review docs, agent skill, and tests.

## 0.5.0 - 2026-07-10

- Added `scenario-stress` CLI command for deterministic illustrative stress review from an impact packet and `examples/scenarios.json`.
- Added scenario JSON, Markdown, and no-JavaScript HTML artifacts with macro, sector, and company shocks, ticker/tag exposure overlap, risk levels, stress flags, thesis contradiction prompts, confidence downgrade suggestions, and next review queue.
- Integrated scenario stress with demo gallery, release manifest, release validation, maturity evidence, README, review docs, agent skill, and tests.

## 0.4.0 - 2026-07-10

- Added `visual-receipt` CLI command for deterministic static HTML capture receipts with hashes, no-script checks, boundary checks, and review notes.
- Added `cold-start-walkthrough` CLI command for a 2-5 minute first-user path with commands, expected artifacts, interpretation guidance, and failure modes.
- Integrated promotion-readiness artifacts with gallery, release manifest, release validation, maturity evidence, README, review docs, agent skill, and tests.

## 0.3.0 - 2026-07-10

- Added `trend-history` CLI command for multi-period packet history.
- Added trend JSON, Markdown, and no-JavaScript HTML artifacts with score direction, status transitions, persistent warnings, exposure trend, and next review queue.
- Added realistic `examples/history/*.json` packet fixtures and release validation for trend artifact determinism.
- Updated gallery, manifest, maturity evidence, README, review docs, agent skill, and tests for the v0.3.0 workflow.

## 0.2.0 - 2026-07-10

- Added `.gitignore` and release validation for deterministic demo artifacts, boundaries, and referenced example files.
- Added `validate-release` and `maturity-report` CLI commands with JSON/Markdown readiness evidence.
- Added tests for release validation and maturity reporting.

## 0.1.0 - 2026-07-10

- Initial public asset with stdlib-only CLI.
- Added `build-packet`, `compare`, and `selfcheck` commands.
- Added example inputs, deterministic demo outputs, tests, review docs, and privacy scan script.
