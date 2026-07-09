# Cold-Start Walkthrough

Generated: 2026-07-10
Audience: First user reviewing the public demo from a clean checkout.
Duration: 2-5 minutes

Generate the local packet, compare, trend, scenario stress, repeated-use review ledger, visual receipt, walkthrough, evidence hub, and release validation evidence without network, broker, order, or advice behavior.

## Commands

```bash
PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab evidence-hub --out demo/evidence
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json
```

## Expected Artifacts

- `demo/impact_packet.json`
- `demo/impact_packet.md`
- `demo/index.html`
- `demo/compare/compare.json`
- `demo/compare/compare.md`
- `demo/trend/trend_history.json`
- `demo/trend/trend_history.md`
- `demo/trend/trend_history.html`
- `demo/scenario/scenario_stress.json`
- `demo/scenario/scenario_stress.md`
- `demo/scenario/scenario_stress.html`
- `demo/ledger/review_ledger.json`
- `demo/ledger/review_ledger.md`
- `demo/ledger/review_ledger.html`
- `demo/visual/visual_receipt.json`
- `demo/visual/visual_receipt.md`
- `demo/walkthrough/walkthrough.json`
- `demo/walkthrough/walkthrough.md`
- `demo/evidence/evidence_hub.json`
- `demo/evidence/evidence_hub.md`
- `demo/evidence/evidence_hub.html`

## Interpretation Guide

- Start with demo/gallery.html for the linked artifact set and finance boundaries.
- Read demo/impact_packet.md as a research triage packet; attention scores rank review urgency, not trades.
- Use demo/compare/compare.md to spot changes versus the previous static packet.
- Use demo/trend/trend_history.md to review score direction, warning persistence, exposure trend, and next review queue.
- Use demo/scenario/scenario_stress.md to review illustrative macro, sector, and company shock overlap against thesis language.
- Use demo/ledger/review_ledger.md to carry repeated review issues forward, mark absent issues resolved, and identify stale research maintenance items.
- Use demo/visual/visual_receipt.md to confirm static HTML pages pass no-script checks and retain boundaries.
- Use demo/evidence/evidence_hub.md to audit artifact purpose, release and promotion gate relevance, hashes, no-script status, boundary coverage, and limitations.
- Treat validate-release JSON as the promotion gate summary; every check should be true before publishing.

## Failure Modes And Boundaries

- Missing example JSON files cause packet, compare, trend, and validation commands to fail.
- Edited generated files cause deterministic release validation to report changed artifacts.
- Removing finance boundaries from public artifacts causes boundary validation to fail.
- Adding script tags to static demo HTML causes the visual receipt no-script summary to fail.
- Using live market data, broker integrations, orders, or advice language is outside project scope.

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.
