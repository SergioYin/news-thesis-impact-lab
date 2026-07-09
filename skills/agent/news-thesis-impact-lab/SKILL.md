# news-thesis-impact-lab

Use this skill when a user needs to create, refresh, or inspect static local finance research packets with `news-thesis-impact-lab`.

## Workflow

1. Keep all inputs local JSON files. Do not fetch live market, broker, or news data.
2. Build a packet:

   ```bash
   news-thesis-impact-lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo
   ```

3. Compare a packet:

   ```bash
   news-thesis-impact-lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare
   ```

4. Build trend history from prior/current packets:

   ```bash
   news-thesis-impact-lab trend-history --packets examples/history/*.json --out demo/trend
   ```

5. Run checks:

   ```bash
   python -m pytest -q
   PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend
   PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual
   PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough
   PYTHONPATH=src python -m news_thesis_impact_lab selfcheck
   PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json
   PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release
   PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html
   PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity
   python scripts/privacy_scan.py
   git diff --check
   ```

6. Public packaging artifacts:

   ```bash
   news-thesis-impact-lab release-manifest --out release
   news-thesis-impact-lab demo-gallery --out demo/gallery.html
   ```

## Acceptance Criteria

- `release/manifest.json` and `release/manifest.md` are deterministic and include package version, key artifact hashes, regenerate commands, verify commands, finance safety boundaries, and wheel/sdist placeholders when `dist/` files are absent.
- `demo/gallery.html` is static no-JavaScript HTML and links the impact packet, compare report, trend history, maturity report, release manifest, quickstart commands, and finance boundaries.
- `demo/trend/trend_history.json`, `demo/trend/trend_history.md`, and `demo/trend/trend_history.html` are deterministic outputs from `examples/history/*.json`.
- `demo/visual/visual_receipt.json` and `demo/visual/visual_receipt.md` are deterministic static HTML capture receipts with no-script and boundary checks.
- `demo/walkthrough/walkthrough.json` and `demo/walkthrough/walkthrough.md` describe the 2-5 minute first-user path, exact commands, expected artifacts, interpretation guide, and failure modes.
- `validate-release --format json` passes after public artifacts are generated.
- Tests, selfcheck, privacy scan, and `git diff --check` pass.
- No runtime dependencies, workflow files, private references, live data fetches, broker actions, or investment advice are introduced.

## Boundaries

Outputs are research notes only. Do not turn review prompts into buy, sell, hold, allocation, execution, or broker instructions.
