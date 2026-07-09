# Release Manifest

Package: news-thesis-impact-lab 0.2.0
Generated: 2026-07-10

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Key Artifacts

| Path | Exists | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| `README.md` | true | `7b95a9a0b97f46aa0233b6c8411425a04f31606fd8abd15ecb7bc3bf241f7e57` | 4040 |
| `pyproject.toml` | true | `0cc0b107a96ae5e632f21755d361c4c639d29ad482468ad8a27d978d6bfbe7c3` | 876 |
| `docs/review-packet.md` | true | `41fd915b50a76ab608740f1e275b61540d489ae577991b44305088e36e280b02` | 1472 |
| `demo/impact_packet.json` | true | `8f598eee1faf86f0cc0f846f420ecad744d313cec958398907c44ad242fa6073` | 5780 |
| `demo/impact_packet.md` | true | `59513e6d36d7081df9484642e02740b5a8014e4a5e733636ea98505ec09ced65` | 3597 |
| `demo/index.html` | true | `593b6e4647d7b56f3f78cb4f6d4b73d80ce647bc729d61370029f2ee6906a10b` | 2940 |
| `demo/gallery.html` | true | `e274f095d18140d644c338490ecf5ae44185f73c1efd5aa5b789c83999396b19` | 2795 |
| `demo/compare/compare.json` | true | `aff81a073e9c644ddc280649398f1c13bfb159d81061db9c098d2be2f306ddf5` | 1439 |
| `demo/compare/compare.md` | true | `adc9ac2a4b2744593687353b0f5c3371aa83379fb0215746a1d2898f6f934787` | 712 |
| `demo/maturity/maturity_report.json` | true | `bd16373b19151b67115825f05107264cec1bddedd90b5a0cc6e0ac0990f95258` | 1226 |
| `demo/maturity/maturity_report.md` | true | `9384631fa47d56eda835b7b05fd4f141ba809caa12d153d82979a4d4ae1a2e07` | 1003 |
| `examples/events.json` | true | `dc506f6452e1d37dc29ffef21ccd894c3e2b15b5e26e6e24bb2b0c5a7c3c0358` | 1410 |
| `examples/theses.json` | true | `29c80ca03dd125602cb0b19234385132fb5d2ad84c1a6442247d529c93d776c9` | 1824 |
| `examples/portfolio.json` | true | `c722c6bbe7cb29bf8f502a7d55cf7c3abac76451f3a18a9bb9ea708c268a260d` | 330 |
| `examples/previous_packet.json` | true | `a7f6cb631961c966fb3cea925e0b99a6cf192212eb6649070fddb86eae2ce274` | 929 |

## Distributions

| Kind | Path | Exists | SHA-256 | Bytes | Note |
| --- | --- | --- | --- | ---: | --- |
| wheel | `dist/news_thesis_impact_lab-0.2.0-py3-none-any.whl` | true | `d8afaafed7799d4fcec354b58d93a19e408d9462fad50a36b4ed1ebd49af7703` | 17347 |  |
| sdist | `dist/news_thesis_impact_lab-0.2.0.tar.gz` | true | `b296fcc4e98355575cdc7b84dbb808057acd138b16eafb40265f4f35e17a4f08` | 16193 |  |

## Regenerate

```bash
PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo
```
```bash
PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare
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
