# Release Manifest

Package: news-thesis-impact-lab 0.3.0
Generated: 2026-07-10

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Key Artifacts

| Path | Exists | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| `README.md` | true | `fae8e9203fb8be52e29f9f4e69ceb760bdb7a3abb7ff854d60c8e7986ebe2d37` | 4810 |
| `pyproject.toml` | true | `9a336e42c3a4e37af22799995eb0fe7f8a9fa31cbf6affb8dc99bf69c47ded14` | 876 |
| `docs/review-packet.md` | true | `d64210a2b701f288a7be8472434f713a057821d71f52b6960a3e40eaf7c15f60` | 2220 |
| `demo/impact_packet.json` | true | `8f598eee1faf86f0cc0f846f420ecad744d313cec958398907c44ad242fa6073` | 5780 |
| `demo/impact_packet.md` | true | `59513e6d36d7081df9484642e02740b5a8014e4a5e733636ea98505ec09ced65` | 3597 |
| `demo/index.html` | true | `593b6e4647d7b56f3f78cb4f6d4b73d80ce647bc729d61370029f2ee6906a10b` | 2940 |
| `demo/gallery.html` | true | `853a1e2a6e1dea218be90f7a7ea8e8b4f33e86f4ee6f39d84e129c2c1b1a4b0e` | 3213 |
| `demo/compare/compare.json` | true | `aff81a073e9c644ddc280649398f1c13bfb159d81061db9c098d2be2f306ddf5` | 1439 |
| `demo/compare/compare.md` | true | `adc9ac2a4b2744593687353b0f5c3371aa83379fb0215746a1d2898f6f934787` | 712 |
| `demo/trend/trend_history.json` | true | `ff7b37f9ba163c0d7e863ac785f43e68373cff5b891e4b142c0a6e70714baa58` | 9470 |
| `demo/trend/trend_history.md` | true | `c95ffd8fe3435bea357eef8185fc782397d65e8e350c79650bba7e5d7ef92abd` | 1521 |
| `demo/trend/trend_history.html` | true | `6ee5d93b24967925391ec6d981bd5af49bc32efb2648cc89a92e7ae3ebb3186e` | 3354 |
| `examples/events.json` | true | `dc506f6452e1d37dc29ffef21ccd894c3e2b15b5e26e6e24bb2b0c5a7c3c0358` | 1410 |
| `examples/theses.json` | true | `29c80ca03dd125602cb0b19234385132fb5d2ad84c1a6442247d529c93d776c9` | 1824 |
| `examples/portfolio.json` | true | `c722c6bbe7cb29bf8f502a7d55cf7c3abac76451f3a18a9bb9ea708c268a260d` | 330 |
| `examples/previous_packet.json` | true | `a7f6cb631961c966fb3cea925e0b99a6cf192212eb6649070fddb86eae2ce274` | 929 |
| `examples/history/2026-06-26_packet.json` | true | `e130eef99267251390bd01f72313e0bff7166bd0597521704f318d306448bbf4` | 3413 |
| `examples/history/2026-07-03_packet.json` | true | `dc36230a0f3f6708e63973421ce71dc99d7bb5eafde807a27b0c210f1168ab94` | 3372 |
| `examples/history/2026-07-10_packet.json` | true | `8255855ee91618f3016aade3859f923730536b6840452a4011988f242ae68e97` | 3666 |

## Distributions

| Kind | Path | Exists | SHA-256 | Bytes | Note |
| --- | --- | --- | --- | ---: | --- |
| wheel | `dist/news_thesis_impact_lab-0.3.0-py3-none-any.whl` | true | `0ed28a640b679d0d411303379d2911192fe808de94b84c8d39731c1b21393b93` | 21171 |  |
| sdist | `dist/news_thesis_impact_lab-0.3.0.tar.gz` | true | `f532976de2d5bdb4d28d199c5ff2e5f58ec18bb223a50a12e1815ce21cac311b` | 20250 |  |

## Regenerate

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
PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release
```

## Verify

```bash
python -m pytest -q
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab selfcheck
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json
```
```bash
python scripts/privacy_scan.py
```
```bash
git diff --check
```

## Notes

- Manifest hashes cover public inputs, docs, generated artifacts, and any built distributions under dist/.
- Wheel and sdist records use placeholders only when the corresponding distribution file is absent.
