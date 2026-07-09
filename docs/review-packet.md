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

## Promotion Review Artifacts

`visual-receipt --out demo/visual` scans `demo/index.html`, `demo/gallery.html`, and `demo/trend/trend_history.html` without screenshots or browser automation. It writes `visual_receipt.json` and `visual_receipt.md` with title, role, route, path, byte count, SHA-256, no-script status, boundary status, capture command, and review notes.

`cold-start-walkthrough --out demo/walkthrough` writes `walkthrough.json` and `walkthrough.md` for a 2-5 minute first-user path. It includes exact commands, expected artifacts, interpretation guidance, and failure modes that preserve the no-live-data, no-broker, no-orders, no-advice boundaries.

## Review Flow

1. Read boundaries first.
2. Check warnings before interpreting scores.
3. Use `review_queue` to identify notes needing thesis maintenance.
4. Update local event or thesis JSON when research notes change.
5. Rebuild the packet and compare against the previous packet.
6. Build trend history from `examples/history/*.json` when reviewing multi-period drift.
7. Generate `visual-receipt --out demo/visual` and confirm no-script and boundary summaries are true.
8. Generate `cold-start-walkthrough --out demo/walkthrough` and confirm the first-user path still matches the public artifacts.
9. Run `validate-release` before publishing to confirm demo artifacts remain deterministic and retain the research boundaries.

## Release Readiness

`maturity-report --out demo/maturity` writes Markdown and JSON scoring for product, runnable, user-value, evidence, engineering, showcase, and risk dimensions. The report includes release and promotion gate booleans derived from those scores and the release validation result.
