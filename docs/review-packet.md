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

## Review Flow

1. Read boundaries first.
2. Check warnings before interpreting scores.
3. Use `review_queue` to identify notes needing thesis maintenance.
4. Update local event or thesis JSON when research notes change.
5. Rebuild the packet and compare against the previous packet.
6. Build trend history from `examples/history/*.json` when reviewing multi-period drift.
7. Run `validate-release` before publishing to confirm demo artifacts remain deterministic and retain the research boundaries.

## Release Readiness

`maturity-report --out demo/maturity` writes Markdown and JSON scoring for product, runnable, user-value, evidence, engineering, showcase, and risk dimensions. The report includes release and promotion gate booleans derived from those scores and the release validation result.
