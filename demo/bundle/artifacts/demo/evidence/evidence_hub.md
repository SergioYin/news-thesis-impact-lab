# Evidence Hub

Generated: 2026-07-10

Reviewer-facing matrix for deterministic public demo artifacts and the release manifest.

## Rubric Summary

| Area | Score | Artifact count | Rationale |
| --- | ---: | ---: | --- |
| product | 4/5 | 0 | Clear CLI asset with bounded static research workflow and public package metadata. |
| runnable | 5/5 | 2 | Stdlib-only commands, examples, demo artifacts, scenario stress review, repeated-use review ledger, visual receipt, cold-start walkthrough, tests, selfcheck, and privacy scan. |
| user_value | 4/5 | 3 | Maps local catalysts and illustrative stress scenarios to thesis claims, exposure, warnings, confidence review, ledger status, and human prompts. |
| evidence | 4/5 | 3 | Includes deterministic demo JSON/Markdown/HTML, compare, trend, scenario stress, review ledger outputs, visual receipt, walkthrough, evidence hub, tests, and release validation. |
| engineering | 4/5 | 3 | Typed dataclasses, deterministic rendering, focused CLI surface, and no runtime dependencies. |
| showcase | 4/5 | 9 | Demo packet, compare packet, trend history, scenario stress review, review ledger, visual receipt, cold-start walkthrough, evidence hub, review doc, and agent skill show the intended workflow. |
| risk | 5/5 | 2 | Strong research-only boundaries with no live data, broker access, orders, or advice. |

## Release Gate Evidence

- `demo/impact_packet.json`
- `demo/impact_packet.md`
- `demo/index.html`
- `demo/gallery.html`
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
- `demo/maturity/maturity_report.json`
- `demo/maturity/maturity_report.md`
- `release/manifest.json`

## Promotion Gate Evidence

- `demo/impact_packet.json`
- `demo/impact_packet.md`
- `demo/index.html`
- `demo/gallery.html`
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
- `demo/maturity/maturity_report.json`
- `demo/maturity/maturity_report.md`
- `release/manifest.json`

## Artifact Matrix

| Path | Type | Question answered | Rubric | Release gate | Promotion gate | Regenerate | SHA-256 | No JS | Boundary coverage | Known limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `demo/impact_packet.json` | packet-json | Which tickers are affected by local catalysts, and why? | user_value | core deterministic demo evidence | primary reviewer workflow evidence | `PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo` | `8f598eee1faf86f0cc0f846f420ecad744d313cec958398907c44ad242fa6073` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/impact_packet.md` | packet-markdown | Can a reviewer read the catalyst-to-thesis packet without tooling? | showcase | public review artifact | human-readable reviewer packet | `PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo` | `59513e6d36d7081df9484642e02740b5a8014e4a5e733636ea98505ec09ced65` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/index.html` | packet-html | Can the packet be scanned as static no-JavaScript HTML? | showcase | static HTML boundary evidence | visual review surface | `PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo` | `593b6e4647d7b56f3f78cb4f6d4b73d80ce647bc729d61370029f2ee6906a10b` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
| `demo/gallery.html` | gallery-html | Where does a reviewer start when inspecting the public artifact set? | showcase | artifact navigation evidence | promotion entry point | `PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html` | `257d014acc8cf75e02c2b475e1b33952af4f2c63d79b64c64a73883f2cce0552` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
| `demo/compare/compare.json` | compare-json | What changed versus the previous static packet? | evidence | deterministic comparison evidence | change-review evidence | `PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare` | `aff81a073e9c644ddc280649398f1c13bfb159d81061db9c098d2be2f306ddf5` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/compare/compare.md` | compare-markdown | Can packet changes be reviewed without parsing JSON? | evidence | human-readable comparison evidence | change-review narrative | `PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare` | `adc9ac2a4b2744593687353b0f5c3371aa83379fb0215746a1d2898f6f934787` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/trend/trend_history.json` | trend-json | How did ticker status, scores, warnings, and exposure change across periods? | evidence | multi-period evidence | repeat-review signal | `PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend` | `ff7b37f9ba163c0d7e863ac785f43e68373cff5b891e4b142c0a6e70714baa58` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/trend/trend_history.md` | trend-markdown | Can multi-period drift be reviewed without tooling? | showcase | trend review evidence | repeat-review narrative | `PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend` | `c95ffd8fe3435bea357eef8185fc782397d65e8e350c79650bba7e5d7ef92abd` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/trend/trend_history.html` | trend-html | Can trend history be scanned as static no-JavaScript HTML? | showcase | static HTML trend evidence | visual review surface | `PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend` | `6ee5d93b24967925391ec6d981bd5af49bc32efb2648cc89a92e7ae3ebb3186e` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
| `demo/scenario/scenario_stress.json` | scenario-json | Which illustrative stresses overlap with thesis and exposure language? | user_value | scenario coverage evidence | stress-review evidence | `PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario` | `83efb2d43c8cfcd30d8c63930e3993d93870e7669810e2f41b6ec0be7af7a728` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Scenario fixtures are illustrative stress prompts, not forecasts. |
| `demo/scenario/scenario_stress.md` | scenario-markdown | Can scenario stress prompts be reviewed without parsing JSON? | showcase | scenario review evidence | stress-review narrative | `PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario` | `a994d02675e093fdb5405303ef8908d3dd4e59f70bf974bcc542c8c7056d8a4a` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Scenario fixtures are illustrative stress prompts, not forecasts. |
| `demo/scenario/scenario_stress.html` | scenario-html | Can stress review be scanned as static no-JavaScript HTML? | showcase | static HTML stress evidence | visual review surface | `PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario` | `69ce3af70beb4015c7ba2aedfd055e37be504657b0c18ce3d7ba9b400cffed2c` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine.; Scenario fixtures are illustrative stress prompts, not forecasts. |
| `demo/ledger/review_ledger.json` | ledger-json | Which review issues are new, open, watch, resolved, stale, or severe? | user_value | repeat-use state evidence | ongoing review evidence | `PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger` | `6925ed2362ca483ea7ff1c1a582ae5a8de13a90128894c94e2888da5bb4d5220` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/ledger/review_ledger.md` | ledger-markdown | Can repeated-use review state be inspected without parsing JSON? | showcase | ledger review evidence | ongoing review narrative | `PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger` | `a69ea4916942d63dba0ae5a9143217bed9e740eff9f86f30f263cc64f0ac416f` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/ledger/review_ledger.html` | ledger-html | Can review ledger status be scanned as static no-JavaScript HTML? | showcase | static HTML ledger evidence | visual review surface | `PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger` | `e33421e9c605deb57c62603957d753884655dab1c0435c99a981d2ba48c8e2d9` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
| `demo/visual/visual_receipt.json` | visual-receipt-json | Which static HTML pages prove no-script and boundary coverage? | risk | no-JavaScript and boundary evidence | promotion safety evidence | `PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual` | `f297538e39ed0ce71a73ca15206b78def1f63a2d7b806680aa53dfe3e89b4b69` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/visual/visual_receipt.md` | visual-receipt-markdown | Can visual review checks be audited without running a browser? | risk | promotion receipt evidence | promotion safety narrative | `PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual` | `8881dc42e9242631452e648dc1b3a88559eb6d2f0fde1e7623ea0aa003b9135a` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/walkthrough/walkthrough.json` | walkthrough-json | Can a first user reproduce the artifact set quickly from local files? | runnable | cold-start reproducibility evidence | first-user promotion evidence | `PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough` | `c2203f06d7d546669a86d094189af0addd014c1a7425fe66678712124aa9ea6d` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/walkthrough/walkthrough.md` | walkthrough-markdown | Can the cold-start path be followed without interpreting CLI internals? | runnable | cold-start review evidence | first-user narrative | `PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough` | `efb8bad3002c672616e025362645998bccb212a9510b4eb7c4bcd58ec72b32f4` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/maturity/maturity_report.json` | maturity-json | Do release and promotion gates pass by rubric area? | engineering | release gate summary | promotion gate summary | `PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity` | `f9310fca83693ff1421f4b6f652756d15f23e11c6e8adc9144cb05a5f3936fc6` | n/a | 0/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/maturity/maturity_report.md` | maturity-markdown | Can readiness scoring be reviewed without parsing JSON? | engineering | human-readable gate summary | promotion gate narrative | `PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity` | `d1b1cf6e31f86cb98945fa529da19b11110ebd7e0509cfe4ee0fe8e10bda6627` | n/a | 0/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `release/manifest.json` | release-manifest-json | Which public artifacts, commands, hashes, and package metadata define this release? | engineering | release hash authority | promotion audit input | `PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release` | `7f80b9019a7487033eb45cdbe981a8f8dba6a94ea5a4e14b832b6b73f9f5d3f7` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Distribution entries may be placeholders until wheel and sdist files are built. |

## Finance Safety Boundaries

- Static local research notes only; no live market data is fetched.
- Not investment advice and not a buy, sell, hold, or allocation recommendation.
- No broker integration, order routing, execution, or account access.
- Scores are deterministic review aids for human research triage.

## Known Limitations

- The hub indexes static local artifacts only; it does not fetch live market, broker, account, or news data.
- Hashes prove file content identity, not investment correctness or external factual completeness.
- Scenario stress records are illustrative research prompts, not forecasts, advice, or trade instructions.
- No-JavaScript checks are static text checks for script tags, not full browser rendering tests.
