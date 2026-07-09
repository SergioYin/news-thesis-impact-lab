# news-thesis-impact-lab

`news-thesis-impact-lab` is a zero-dependency Python CLI for static, local, research-only finance notes. It maps local catalyst events to ticker thesis sensitivities, portfolio exposure, source freshness warnings, and action-free review queues.

It is for analysts, builders, and agent workflows that need deterministic review packets from local JSON inputs without live market data, broker access, or private services.

## 3-Command Quickstart

```bash
PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo
PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare
PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json
```

## Demo Artifacts

- [Demo gallery](demo/gallery.html): no-JavaScript landing page for the public artifact set.
- [Impact packet](demo/impact_packet.md): affected tickers, scores, warnings, and review prompts.
- [Compare report](demo/compare/compare.md): current versus previous packet deltas.
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

news-thesis-impact-lab selfcheck
news-thesis-impact-lab validate-release
news-thesis-impact-lab maturity-report --out demo/maturity
news-thesis-impact-lab demo-gallery --out demo/gallery.html
news-thesis-impact-lab release-manifest --out release
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
- `demo/maturity/maturity_report.json` and `demo/maturity/maturity_report.md`: release and promotion readiness scoring.
- `demo/gallery.html`: static no-JavaScript gallery that links the public demo and release artifacts.
- `release/manifest.json` and `release/manifest.md`: deterministic release manifest with hashes and build placeholders.

## Input Shape

The examples under `examples/` are intentionally small and local. Events include tickers, themes, source dates, source labels, summaries, and impact hints. Theses include claims, sensitivities, risks, and opportunities. Portfolio entries include static weights.

## Development

```bash
python -m pytest -q
PYTHONPATH=src python -m news_thesis_impact_lab selfcheck
PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json
PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release
PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html
PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity
python scripts/privacy_scan.py
git diff --check
```

Packaging is configured through `pyproject.toml`. If the optional `build` module is installed:

```bash
python -m build
```
