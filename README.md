# news-thesis-impact-lab

`news-thesis-impact-lab` is a zero-dependency Python CLI for static, local, research-only finance notes. It maps local catalyst events to ticker thesis sensitivities, portfolio exposure, source freshness warnings, and action-free review queues.

It is for analysts, builders, and agent workflows that need deterministic review packets from local JSON inputs without live market data, broker access, or private services.

## 8-Command Quickstart

```bash
PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo
PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare
PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend
PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario
PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger
PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release
PYTHONPATH=src python -m news_thesis_impact_lab evidence-hub --out demo/evidence
PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json
```

## Demo Artifacts

- [Demo gallery](demo/gallery.html): no-JavaScript landing page for the public artifact set.
- [Impact packet](demo/impact_packet.md): affected tickers, scores, warnings, and review prompts.
- [Compare report](demo/compare/compare.md): current versus previous packet deltas.
- [Trend history](demo/trend/trend_history.md): multi-period score direction, new/cleared/changed statuses, persistent warnings, exposure trend, and next review queue.
- [Scenario stress review](demo/scenario/scenario_stress.md): illustrative macro, sector, and company shocks mapped to ticker/tag exposure, stress flags, thesis contradiction prompts, confidence downgrade suggestions, and next review queue.
- [Review ledger](demo/ledger/review_ledger.md): repeated-use issue ledger keyed by ticker, issue type, and source with carry-forward, resolved status, severity, stale flags, evidence links, and next research maintenance action.
- [Visual receipt](demo/visual/visual_receipt.md): static HTML capture receipt with hashes, no-script checks, and boundary checks.
- [Cold-start walkthrough](demo/walkthrough/walkthrough.md): 2-5 minute first-user path with exact commands, expected artifacts, interpretation guide, and failure modes.
- [Evidence hub](demo/evidence/evidence_hub.md): reviewer-facing matrix with artifact purpose, rubric area, release and promotion gate relevance, regeneration command, SHA-256, no-JavaScript status, boundary coverage, and limitations.
- [Maturity report](demo/maturity/maturity_report.md): release and promotion readiness gates.
- [Release manifest](release/manifest.md): package version, hashes, regeneration commands, verification commands, boundaries, and distribution placeholders.

## Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Installable CLI

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .

news-thesis-impact-lab build-packet \
  --events examples/events.json \
  --theses examples/theses.json \
  --portfolio examples/portfolio.json \
  --out demo

news-thesis-impact-lab compare \
  --current demo/impact_packet.json \
  --previous examples/previous_packet.json \
  --out demo/compare

news-thesis-impact-lab trend-history \
  --packets examples/history/*.json \
  --out demo/trend

news-thesis-impact-lab scenario-stress \
  --packet demo/impact_packet.json \
  --scenarios examples/scenarios.json \
  --out demo/scenario

news-thesis-impact-lab review-ledger \
  --packet demo/impact_packet.json \
  --trend demo/trend/trend_history.json \
  --scenario demo/scenario/scenario_stress.json \
  --previous examples/review_ledger_previous.json \
  --out demo/ledger

news-thesis-impact-lab selfcheck
news-thesis-impact-lab validate-release
news-thesis-impact-lab maturity-report --out demo/maturity
news-thesis-impact-lab demo-gallery --out demo/gallery.html
news-thesis-impact-lab visual-receipt --out demo/visual
news-thesis-impact-lab cold-start-walkthrough --out demo/walkthrough
news-thesis-impact-lab release-manifest --out release
news-thesis-impact-lab evidence-hub --out demo/evidence
```

Equivalent module form:

```bash
PYTHONPATH=src python -m news_thesis_impact_lab selfcheck
```

## Artifact Details

- `demo/impact_packet.json`: structured impacted tickers, scores, warnings, review prompts, and boundaries.
- `demo/impact_packet.md`: deterministic review packet.
- `demo/index.html`: static no-JavaScript demo.
- `demo/compare/compare.json` and `demo/compare/compare.md`: current versus previous packet deltas.
- `demo/trend/trend_history.json`, `demo/trend/trend_history.md`, and `demo/trend/trend_history.html`: deterministic multi-period packet history.
- `demo/scenario/scenario_stress.json`, `demo/scenario/scenario_stress.md`, and `demo/scenario/scenario_stress.html`: deterministic illustrative stress scenario review.
- `demo/ledger/review_ledger.json`, `demo/ledger/review_ledger.md`, and `demo/ledger/review_ledger.html`: deterministic repeated-use review ledger with status transitions.
- `demo/visual/visual_receipt.json` and `demo/visual/visual_receipt.md`: deterministic static capture receipt for promotion review.
- `demo/walkthrough/walkthrough.json` and `demo/walkthrough/walkthrough.md`: first-user walkthrough with commands, artifacts, interpretation, and failure modes.
- `demo/maturity/maturity_report.json` and `demo/maturity/maturity_report.md`: release and promotion readiness scoring.
- `demo/evidence/evidence_hub.json`, `demo/evidence/evidence_hub.md`, and `demo/evidence/evidence_hub.html`: deterministic reviewer evidence matrix over generated demo artifacts and `release/manifest.json`.
- `demo/gallery.html`: static no-JavaScript gallery that links the public demo and release artifacts.
- `release/manifest.json` and `release/manifest.md`: deterministic release manifest with hashes and build placeholders.

## Input Shape

The examples under `examples/` are intentionally small and local. Events include tickers, themes, source dates, source labels, summaries, and impact hints. Theses include claims, sensitivities, risks, and opportunities. Portfolio entries include static weights. `examples/scenarios.json` contains illustrative macro, sector, and company shocks with ticker/tag exposures and risk levels. The packet fixtures under `examples/history/*.json` are prior/current review packets for exercising trend history without live data. `examples/review_ledger_previous.json` demonstrates ledger carry-forward, watch, and resolved behavior for repeat use.

## Development

```bash
python -m pytest -q
PYTHONPATH=src python -m news_thesis_impact_lab selfcheck
PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json
PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend
PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario
PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger
PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release
PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html
PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual
PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough
PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity
PYTHONPATH=src python -m news_thesis_impact_lab evidence-hub --out demo/evidence
python scripts/privacy_scan.py
git diff --check
```

Packaging is configured through `pyproject.toml`. If the optional `build` module is installed:

```bash
python -m build
```
