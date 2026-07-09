# Release Manifest

Package: news-thesis-impact-lab 0.4.0
Generated: 2026-07-10

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Key Artifacts

| Path | Exists | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| `README.md` | true | `91274e3b9705c30d6085c28d92c594b97df6cc77332d523ba6dcb36101b4efd8` | 5704 |
| `pyproject.toml` | true | `08998bb24f2a58865db111e1e81e59aca61e6af677d9034ccfe01ac2ca1048ef` | 876 |
| `docs/review-packet.md` | true | `4f25f2783d6a5649dd01f12505a597520ab51a97a6408c2b16b26eb8b1be84d7` | 3117 |
| `demo/impact_packet.json` | true | `8f598eee1faf86f0cc0f846f420ecad744d313cec958398907c44ad242fa6073` | 5780 |
| `demo/impact_packet.md` | true | `59513e6d36d7081df9484642e02740b5a8014e4a5e733636ea98505ec09ced65` | 3597 |
| `demo/index.html` | true | `593b6e4647d7b56f3f78cb4f6d4b73d80ce647bc729d61370029f2ee6906a10b` | 2940 |
| `demo/gallery.html` | true | `c4c511c9265c481c3bd58760ea509b0a8365527f46b8f77176325d1b98a883f3` | 3715 |
| `demo/compare/compare.json` | true | `aff81a073e9c644ddc280649398f1c13bfb159d81061db9c098d2be2f306ddf5` | 1439 |
| `demo/compare/compare.md` | true | `adc9ac2a4b2744593687353b0f5c3371aa83379fb0215746a1d2898f6f934787` | 712 |
| `demo/trend/trend_history.json` | true | `ff7b37f9ba163c0d7e863ac785f43e68373cff5b891e4b142c0a6e70714baa58` | 9470 |
| `demo/trend/trend_history.md` | true | `c95ffd8fe3435bea357eef8185fc782397d65e8e350c79650bba7e5d7ef92abd` | 1521 |
| `demo/trend/trend_history.html` | true | `6ee5d93b24967925391ec6d981bd5af49bc32efb2648cc89a92e7ae3ebb3186e` | 3354 |
| `demo/visual/visual_receipt.json` | true | `bf1102ad210347a31590e4c434e0ea8b134480e57ef028e2bff7f3d973b4c490` | 2496 |
| `demo/visual/visual_receipt.md` | true | `6c7e5082aa58fcf88172989ea73a85e5233ca6207346343ef099f05f8e0ecd46` | 1907 |
| `demo/walkthrough/walkthrough.json` | true | `8af84b7ffa99e8159485e05b5d4f15e43b3798a29c594980ebe366b977befdb2` | 3079 |
| `demo/walkthrough/walkthrough.md` | true | `bdcd10d54bca6f59caf89bfe0cae1a2fe452d7fee5aec7d306c78cd33572f9ec` | 2921 |
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
| wheel | `dist/news_thesis_impact_lab-0.4.0-py3-none-any.whl` | true | `3ba16da0721551050c2c4d526a52d3731b49b03e7cd8782d9ea05289c3ae532d` | 24806 |  |
| sdist | `dist/news_thesis_impact_lab-0.4.0.tar.gz` | true | `9ef4e06d2182be324fe80603b248da9e88f2ce496257bea3cb2e6725bbb23db4` | 23535 |  |

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
PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough
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

- Manifest hashes cover public inputs, docs, generated artifacts, and current-version distributions under dist/.
- Wheel and sdist records use placeholders only when the corresponding distribution file is absent.
