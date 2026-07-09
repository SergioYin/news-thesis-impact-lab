# Changelog

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
