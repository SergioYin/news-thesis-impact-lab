# Cold User Walkthrough

This walkthrough is for a public first user who wants to understand and verify `news-thesis-impact-lab` in the first 10 minutes. It uses local fixture files only.

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Clone

```bash
git clone <repository-url> news-thesis-impact-lab
cd news-thesis-impact-lab
```

Expected result:

```text
README.md
pyproject.toml
src/news_thesis_impact_lab/
examples/
demo/
release/
```

If you already have the repository, start from the repository root and run:

```bash
pwd
```

Expected result: the path ends with `news-thesis-impact-lab`.

## Install From Source

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
news-thesis-impact-lab selfcheck
```

Expected output:

```text
runtime: ok
stdlib_only_runtime: ok
no_network_required: ok
research_boundaries_present: ok
selfcheck passed
```

## Wheel Install Check

Build a wheel only when you want to test packaged installation instead of editable source installation.

```bash
python -m pip install build
python -m build
python -m pip install --force-reinstall dist/news_thesis_impact_lab-1.0.1-py3-none-any.whl
news-thesis-impact-lab selfcheck
```

Expected output:

```text
Successfully built news_thesis_impact_lab-1.0.1-py3-none-any.whl
selfcheck passed
```

If `python -m build` is unavailable, skip the wheel check and continue with the editable install. The runtime package has no dependencies beyond the Python standard library.

## Quickstart Run

The README quickstart can be run either through `PYTHONPATH=src python -m news_thesis_impact_lab ...` or through the installed `news-thesis-impact-lab` console script. This short path builds the first packet and the release review artifacts most useful for cold-user comprehension.

```bash
news-thesis-impact-lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo
news-thesis-impact-lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare
news-thesis-impact-lab trend-history --packets examples/history/*.json --out demo/trend
news-thesis-impact-lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario
news-thesis-impact-lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger
news-thesis-impact-lab decision-journal --packet demo/impact_packet.json --compare demo/compare/compare.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --ledger demo/ledger/review_ledger.json --evidence demo/evidence/evidence_hub.json --out demo/journal
news-thesis-impact-lab demo-gallery --out demo/gallery.html
news-thesis-impact-lab evidence-hub --out demo/evidence
news-thesis-impact-lab bundle-export --out demo/bundle
news-thesis-impact-lab asset-health --out demo/health
news-thesis-impact-lab validate-release --format json
```

Expected output includes these lines:

```text
wrote demo/impact_packet.json
wrote demo/impact_packet.md
wrote demo/index.html
wrote demo/compare/compare.json
wrote demo/trend/trend_history.json
wrote demo/scenario/scenario_stress.json
wrote demo/ledger/review_ledger.json
wrote demo/journal/decision_journal.json
wrote demo/gallery.html
wrote demo/evidence/evidence_hub.json
wrote demo/bundle/bundle_manifest.json
wrote demo/health/asset_health.json
```

Expected `validate-release --format json` result:

```json
{
  "ok": true
}
```

The JSON output also includes detailed check records. The important cold-user signal is `"ok": true`.

## What To Open First

- `demo/gallery.html`: first public navigation surface.
- `demo/impact_packet.md`: the core local catalyst-to-thesis packet.
- `demo/evidence/evidence_hub.md`: artifact purpose, SHA-256, regeneration commands, no-JavaScript status, and limitations.
- `demo/health/asset_health.md`: release and promotion readiness, advertised command coverage, docs scan, bundle status, and boundary coverage.
- `demo/bundle/bundle_manifest.md`: plain-file bundle contents for agent reuse.
- `release/manifest.md`: release key artifacts, hashes, verification commands, and distribution placeholders.

## Troubleshooting

- `ModuleNotFoundError: news_thesis_impact_lab`: activate `.venv`, run `python -m pip install -e .`, or use `PYTHONPATH=src python -m news_thesis_impact_lab ...`.
- `news-thesis-impact-lab: command not found`: the console script is not installed in the active environment; rerun the editable install command.
- `validate-release` reports missing artifacts: rerun the quickstart commands in order, especially `evidence-hub`, `bundle-export`, and `asset-health`.
- `bundle-inspect` reports changed artifacts: rerun `news-thesis-impact-lab bundle-export --out demo/bundle` after regenerating demo artifacts.
- `asset-health` reports wheel or sdist missing: build distributions with `python -m build` when promotion packaging evidence is required. Release readiness can still be reviewed from source.
- Any expectation of live prices, fresh news, broker accounts, trade execution, portfolio allocation, or buy/sell/hold language is outside the project boundary.

## Verification Commands

```bash
python -m pytest -q
news-thesis-impact-lab validate-release --format json
news-thesis-impact-lab asset-health --out demo/health
news-thesis-impact-lab bundle-export --out demo/bundle
python scripts/privacy_scan.py
git diff --check
```

These commands verify the same cold-user boundaries: no advice, no live data, no broker integration, deterministic local artifacts, and public documentation coverage.
