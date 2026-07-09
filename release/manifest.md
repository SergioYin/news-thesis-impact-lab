# Release Manifest

Package: news-thesis-impact-lab 0.5.0
Generated: 2026-07-10

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Key Artifacts

| Path | Exists | SHA-256 | Bytes |
| --- | --- | --- | ---: |
| `README.md` | true | `1823a053b1c0e03baa64bfd76f16e095ffd6602090549bb9650ced989056e747` | 6686 |
| `CHANGELOG.md` | true | `937e120893bac932ff5a5a503e7ce36fddc51e04c8c5746d816484375c155466` | 2084 |
| `pyproject.toml` | true | `5f9164d0b33aea044107c448c9f3bfd2008c3715e348d08440f47679301b2df2` | 876 |
| `docs/review-packet.md` | true | `e3c3ef0ea6c2338798e0716511c6cdf9a53a2b16ab3a669c70da64282fce1d94` | 4173 |
| `demo/impact_packet.json` | true | `8f598eee1faf86f0cc0f846f420ecad744d313cec958398907c44ad242fa6073` | 5780 |
| `demo/impact_packet.md` | true | `59513e6d36d7081df9484642e02740b5a8014e4a5e733636ea98505ec09ced65` | 3597 |
| `demo/index.html` | true | `593b6e4647d7b56f3f78cb4f6d4b73d80ce647bc729d61370029f2ee6906a10b` | 2940 |
| `demo/gallery.html` | true | `fe6664b1a37be81c8d90c686d75d253afead59742c18f6bcca0c50ddebe84ac5` | 4176 |
| `demo/compare/compare.json` | true | `aff81a073e9c644ddc280649398f1c13bfb159d81061db9c098d2be2f306ddf5` | 1439 |
| `demo/compare/compare.md` | true | `adc9ac2a4b2744593687353b0f5c3371aa83379fb0215746a1d2898f6f934787` | 712 |
| `demo/trend/trend_history.json` | true | `ff7b37f9ba163c0d7e863ac785f43e68373cff5b891e4b142c0a6e70714baa58` | 9470 |
| `demo/trend/trend_history.md` | true | `c95ffd8fe3435bea357eef8185fc782397d65e8e350c79650bba7e5d7ef92abd` | 1521 |
| `demo/trend/trend_history.html` | true | `6ee5d93b24967925391ec6d981bd5af49bc32efb2648cc89a92e7ae3ebb3186e` | 3354 |
| `demo/scenario/scenario_stress.json` | true | `83efb2d43c8cfcd30d8c63930e3993d93870e7669810e2f41b6ec0be7af7a728` | 20347 |
| `demo/scenario/scenario_stress.md` | true | `a994d02675e093fdb5405303ef8908d3dd4e59f70bf974bcc542c8c7056d8a4a` | 5879 |
| `demo/scenario/scenario_stress.html` | true | `69ce3af70beb4015c7ba2aedfd055e37be504657b0c18ce3d7ba9b400cffed2c` | 5936 |
| `demo/visual/visual_receipt.json` | true | `2b5fc8d02dc9d37a32c41c854488cfd335d352aa888644683e29324061791f3c` | 3165 |
| `demo/visual/visual_receipt.md` | true | `04ff36af090c2c8686fc1fdbab15da53aaa18004fc0754e9b02bb9cc3ef70b8a` | 2371 |
| `demo/walkthrough/walkthrough.json` | true | `26187dab2161f12cf426408026c82d4f7b9f0946e55a3d4f5e23457316ead972` | 3513 |
| `demo/walkthrough/walkthrough.md` | true | `2ff77bf15608175a3e451ec56a06ba402633e6976132d055e1ad3b8118fff99a` | 3346 |
| `examples/events.json` | true | `dc506f6452e1d37dc29ffef21ccd894c3e2b15b5e26e6e24bb2b0c5a7c3c0358` | 1410 |
| `examples/theses.json` | true | `29c80ca03dd125602cb0b19234385132fb5d2ad84c1a6442247d529c93d776c9` | 1824 |
| `examples/portfolio.json` | true | `c722c6bbe7cb29bf8f502a7d55cf7c3abac76451f3a18a9bb9ea708c268a260d` | 330 |
| `examples/scenarios.json` | true | `bd08d77d5f290d5a058dc01ee869d9f044b96013fe877529b748b0f11669b1d7` | 4578 |
| `examples/previous_packet.json` | true | `a7f6cb631961c966fb3cea925e0b99a6cf192212eb6649070fddb86eae2ce274` | 929 |
| `examples/history/2026-06-26_packet.json` | true | `e130eef99267251390bd01f72313e0bff7166bd0597521704f318d306448bbf4` | 3413 |
| `examples/history/2026-07-03_packet.json` | true | `dc36230a0f3f6708e63973421ce71dc99d7bb5eafde807a27b0c210f1168ab94` | 3372 |
| `examples/history/2026-07-10_packet.json` | true | `8255855ee91618f3016aade3859f923730536b6840452a4011988f242ae68e97` | 3666 |

## Distributions

| Kind | Path | Exists | SHA-256 | Bytes | Note |
| --- | --- | --- | --- | ---: | --- |
| wheel | `dist/news_thesis_impact_lab-0.5.0-py3-none-any.whl` | true | `909321bf2a23b8478112d4c01bcc14d7ef4f2fe2628d3f29860d8b0992e52638` | 29451 |  |
| sdist | `dist/news_thesis_impact_lab-0.5.0.tar.gz` | true | `758bcdac654baccc1863be8d5c3bf21b4ff477e964c7a2d25c9326735424093b` | 28548 |  |

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
PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario
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
