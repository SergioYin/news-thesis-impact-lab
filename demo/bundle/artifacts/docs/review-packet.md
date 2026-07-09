# Review Packet Guide

The packet is designed for local research triage. It links static catalyst notes to thesis claims and portfolio exposure so a reviewer can decide which notes deserve human follow-up.

## Packet Fields

- `impacted_tickers`: ticker-level score, direction, confidence, exposure, affected claims, prompts, and warnings.
- `attention_score`: deterministic triage score from event count, confidence, thesis coverage, exposure, and warnings.
- `direction`: textual read of local impact hints, not a trading signal.
- `next_review_prompts`: action-free research questions for human review.
- `warnings`: stale source and missing thesis notices.
- `boundaries`: explicit non-advice and non-broker constraints included in every generated packet.

## Trend History Fields

`trend-history --packets examples/history/*.json --out demo/trend` reads prior/current packet JSON files, sorts them by `generated_at` and file name, and writes `trend_history.json`, `trend_history.md`, and no-JavaScript `trend_history.html`.

- `snapshots`: deterministic ordered packet periods.
- `ticker_histories`: per-ticker timeline with score direction, new/cleared/changed status, latest direction, and exposure trend.
- `persistent_warnings`: stale or repeated warning identities observed across multiple periods.
- `next_review_queue`: latest-period research prompts prioritized by persistent warnings and attention score.

## Scenario Stress Fields

`scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario` reads an existing impact packet and illustrative scenario fixtures. It writes `scenario_stress.json`, `scenario_stress.md`, and no-JavaScript `scenario_stress.html`.

- `scenario_results`: named macro, sector, and company shock coverage with risk levels and matched tickers.
- `ticker_stresses`: per-ticker stress score, stress flags, exposure overlap, matched shocks, thesis contradiction prompts, and confidence downgrade suggestion.
- `exposure_overlap`: direct ticker scenario hits, matched thesis/theme/position tags, and risk levels.
- `confidence_downgrade_suggestion`: deterministic research-confidence triage suggestion, not a portfolio or trading instruction.
- `next_review_queue`: highest-priority human review prompts from scenario overlap.

## Review Ledger Fields

`review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger` reads the current packet, trend history, scenario stress review, and an optional prior ledger. It writes `review_ledger.json`, `review_ledger.md`, and no-JavaScript `review_ledger.html`.

- `items`: stable review issues keyed by `ticker|issue_type|source`.
- `status`: `new` for first-seen active issues, `open` for carried-forward active issues, `watch` for prior watch items that remain active, and `resolved` when previous issues no longer appear in current evidence.
- `severity`: deterministic triage severity from packet warnings, persistent warnings, attention scores, and stress risk.
- `first_seen` and `latest_seen`: retained across runs so repeated use preserves history.
- `evidence_links`: local artifact paths and source labels that justify the issue.
- `next_action`: research maintenance task only; it is not a trade, allocation, broker, or account action.
- `expiry_days` and `stale`: age-based review hygiene flags for unresolved items.
- `summary`: compact counts by ticker, status, and severity.

## Promotion Review Artifacts

`visual-receipt --out demo/visual` scans `demo/index.html`, `demo/gallery.html`, `demo/trend/trend_history.html`, `demo/scenario/scenario_stress.html`, and `demo/ledger/review_ledger.html` without screenshots or browser automation. It writes `visual_receipt.json` and `visual_receipt.md` with title, role, route, path, byte count, SHA-256, no-script status, boundary status, capture command, and review notes.

`cold-start-walkthrough --out demo/walkthrough` writes `walkthrough.json` and `walkthrough.md` for a 2-5 minute first-user path. It includes exact commands, expected artifacts, interpretation guidance, and failure modes that preserve the no-live-data, no-broker, no-orders, no-advice boundaries.

`evidence-hub --out demo/evidence` reads generated artifacts under `demo/` plus `release/manifest.json` and writes `evidence_hub.json`, `evidence_hub.md`, and no-JavaScript `evidence_hub.html`.

- `matrix`: reviewer-facing artifact rows with path, type, user question answered, maturity rubric category, release and promotion gate relevance, regeneration command, SHA-256, no-JavaScript status for HTML, boundary coverage, and limitations.
- `rubric_scores`: product, runnable, user-value, evidence, engineering, showcase, and risk scores with artifact counts and rationale.
- `release_gate_evidence` and `promotion_gate_evidence`: explicit artifact path lists for gate review.
- `known_limitations`: static-review limits that preserve the no-live-data, no-broker, no-orders, no-advice boundaries.

`bundle-export --out demo/bundle` writes a plain-file agent reuse bundle. It creates `bundle_manifest.json`, `bundle_manifest.md`, no-JavaScript `bundle_manifest.html`, `bundle_copy_list.json`, and copied public artifacts under `demo/bundle/artifacts/`.

- `artifacts`: source path, bundle path, SHA-256, byte count, role, regenerate command, package boundary, and safety boundary tags for each public demo, example, release, documentation, and agent skill artifact needed to reproduce the current evidence path.
- `bundle_copy_list.json`: deterministic copy list for reuse agents that need to move or inspect the plain files without a zip archive.
- `bundle-inspect --manifest demo/bundle/bundle_manifest.json --format json|md`: validates copied files exist and hashes match, summarizes missing or changed artifacts, and exits nonzero on mismatch.
- Safety tags preserve the no-live-data, non-advice, no-broker, no-orders, and human-review boundaries; the bundle contains no private references or live data integrations.

## Review Flow

1. Read boundaries first.
2. Check warnings before interpreting scores.
3. Use `review_queue` to identify notes needing thesis maintenance.
4. Update local event or thesis JSON when research notes change.
5. Rebuild the packet and compare against the previous packet.
6. Build trend history from `examples/history/*.json` when reviewing multi-period drift.
7. Run scenario stress with `examples/scenarios.json` to surface illustrative stress overlaps and thesis contradiction prompts.
8. Run `review-ledger` with `examples/review_ledger_previous.json` when checking repeated-use status transitions.
9. Generate `visual-receipt --out demo/visual` and confirm no-script and boundary summaries are true.
10. Generate `cold-start-walkthrough --out demo/walkthrough` and confirm the first-user path still matches the public artifacts.
11. Generate `release-manifest --out release`, then `evidence-hub --out demo/evidence`, and confirm the hub includes hashes, gate relevance, no-script status, boundary coverage, and limitations.
12. Generate `bundle-export --out demo/bundle`, then run `bundle-inspect --manifest demo/bundle/bundle_manifest.json --format json` to confirm copied public artifacts are intact for agent reuse.
13. Run `validate-release` before publishing to confirm demo artifacts remain deterministic and retain the research boundaries.

## Release Readiness

`maturity-report --out demo/maturity` writes Markdown and JSON scoring for product, runnable, user-value, evidence, engineering, showcase, and risk dimensions. The report includes release and promotion gate booleans derived from those scores and the release validation result, which now requires the evidence hub and bundle inspection gates.
