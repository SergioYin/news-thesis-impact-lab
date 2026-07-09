# Visual Receipt

Generated: 2026-07-10
Capture type: static_html_receipt

Deterministic static capture receipt for promotion review; no screenshots, browser automation, network, or JavaScript execution required.

## Summary

- asset_count: 6
- all_no_script: true
- all_boundaries_present: true

## Captures

| Title | Role | Route | Path | Bytes | SHA-256 | No script | Boundaries | Capture command |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| News Thesis Impact Packet | impact packet scan view | `demo/index.html` | `demo/index.html` | 2940 | `593b6e4647d7b56f3f78cb4f6d4b73d80ce647bc729d61370029f2ee6906a10b` | true | true | `static read demo/index.html` |
| news-thesis-impact-lab Demo Gallery | artifact gallery entry point | `demo/gallery.html` | `demo/gallery.html` | 6380 | `568975fc278dc08b0600637f4cc7b185de52ed3bf294e36154765f410fadc785` | true | true | `static read demo/gallery.html` |
| Trend History | trend history scan view | `demo/trend/trend_history.html` | `demo/trend/trend_history.html` | 3354 | `6ee5d93b24967925391ec6d981bd5af49bc32efb2648cc89a92e7ae3ebb3186e` | true | true | `static read demo/trend/trend_history.html` |
| Scenario Stress Review | scenario stress scan view | `demo/scenario/scenario_stress.html` | `demo/scenario/scenario_stress.html` | 5936 | `69ce3af70beb4015c7ba2aedfd055e37be504657b0c18ce3d7ba9b400cffed2c` | true | true | `static read demo/scenario/scenario_stress.html` |
| Review Ledger | review ledger scan view | `demo/ledger/review_ledger.html` | `demo/ledger/review_ledger.html` | 8961 | `e33421e9c605deb57c62603957d753884655dab1c0435c99a981d2ba48c8e2d9` | true | true | `static read demo/ledger/review_ledger.html` |
| Decision Journal Draft | decision journal meeting draft | `demo/journal/decision_journal.html` | `demo/journal/decision_journal.html` | 16298 | `8f9205c709a817392c84bae9fcb7aaf24bdc6b0fde24278989b0a9a22ef1ba35` | true | true | `static read demo/journal/decision_journal.html` |

## Review Notes

- `demo/index.html`: Confirm impacted tickers, warnings, review prompts, and finance boundaries are visible without JavaScript.
- `demo/gallery.html`: Confirm first-screen artifact links, quickstart, and finance boundaries are visible without JavaScript.
- `demo/trend/trend_history.html`: Confirm multi-period status, persistent warning, review queue, and finance boundaries are visible without JavaScript.
- `demo/scenario/scenario_stress.html`: Confirm scenario coverage, ticker stress flags, contradiction prompts, confidence suggestions, and finance boundaries are visible without JavaScript.
- `demo/ledger/review_ledger.html`: Confirm repeated-use statuses, severity, stale flags, resolved carry-forward items, evidence links, and finance boundaries are visible without JavaScript.
- `demo/journal/decision_journal.html`: Confirm thesis questions, evidence excerpts, risk flags, assumptions, placeholder decisions, owner/date blanks, and no-recommendation boundaries are visible without JavaScript.

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.
