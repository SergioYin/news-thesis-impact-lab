# Evidence Hub

Generated: 2026-07-10

Reviewer-facing matrix for deterministic public demo artifacts and the release manifest.

## Rubric Summary

| Area | Score | Artifact count | Rationale |
| --- | ---: | ---: | --- |
| product | 4/5 | 0 | Clear CLI asset with bounded static research workflow and public package metadata. |
| runnable | 5/5 | 3 | Stdlib-only commands, examples, demo artifacts, scenario stress review, repeated-use review ledger, decision journal draft, visual receipt, cold-start walkthrough, asset health, tests, selfcheck, and privacy scan. |
| user_value | 4/5 | 4 | Maps local catalysts and illustrative stress scenarios to thesis claims, exposure, warnings, confidence review, ledger status, meeting-draft placeholders, and human prompts. |
| evidence | 4/5 | 3 | Includes deterministic demo JSON/Markdown/HTML, compare, trend, scenario stress, review ledger, decision journal outputs, visual receipt, walkthrough, evidence hub, asset health, tests, and release validation. |
| engineering | 4/5 | 4 | Typed dataclasses, deterministic rendering, focused CLI surface, and no runtime dependencies. |
| showcase | 4/5 | 13 | Demo packet, compare packet, trend history, scenario stress review, review ledger, decision journal, visual receipt, cold-start walkthrough, evidence hub, asset health, review doc, and agent skill show the intended workflow. |
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
- `demo/journal/decision_journal.json`
- `demo/journal/decision_journal.md`
- `demo/journal/decision_journal.html`
- `demo/visual/visual_receipt.json`
- `demo/visual/visual_receipt.md`
- `demo/walkthrough/walkthrough.json`
- `demo/walkthrough/walkthrough.md`
- `demo/health/asset_health.json`
- `demo/health/asset_health.md`
- `demo/health/asset_health.html`
- `demo/maturity/maturity_report.json`
- `demo/maturity/maturity_report.md`
- `docs/cold-user-walkthrough.md`
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
- `demo/journal/decision_journal.json`
- `demo/journal/decision_journal.md`
- `demo/journal/decision_journal.html`
- `demo/visual/visual_receipt.json`
- `demo/visual/visual_receipt.md`
- `demo/walkthrough/walkthrough.json`
- `demo/walkthrough/walkthrough.md`
- `demo/health/asset_health.json`
- `demo/health/asset_health.md`
- `demo/health/asset_health.html`
- `demo/maturity/maturity_report.json`
- `demo/maturity/maturity_report.md`
- `docs/cold-user-walkthrough.md`
- `release/manifest.json`

## Artifact Matrix

| Path | Type | Question answered | Rubric | Release gate | Promotion gate | Regenerate | SHA-256 | No JS | Boundary coverage | Known limitations |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `demo/impact_packet.json` | packet-json | Which tickers are affected by local catalysts, and why? | user_value | core deterministic demo evidence | primary reviewer workflow evidence | `PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo` | `8f598eee1faf86f0cc0f846f420ecad744d313cec958398907c44ad242fa6073` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/impact_packet.md` | packet-markdown | Can a reviewer read the catalyst-to-thesis packet without tooling? | showcase | public review artifact | human-readable reviewer packet | `PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo` | `59513e6d36d7081df9484642e02740b5a8014e4a5e733636ea98505ec09ced65` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/index.html` | packet-html | Can the packet be scanned as static no-JavaScript HTML? | showcase | static HTML boundary evidence | visual review surface | `PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo` | `593b6e4647d7b56f3f78cb4f6d4b73d80ce647bc729d61370029f2ee6906a10b` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
| `demo/gallery.html` | gallery-html | Where does a reviewer start when inspecting the public artifact set? | showcase | artifact navigation evidence | promotion entry point | `PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html` | `56cac6d6f5e14784ad06c4ec9163b53359462a46f1657b19a53a9fdbb24dfc9e` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
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
| `demo/journal/decision_journal.json` | decision-journal-json | Can research meetings start from a structured non-recommendation journal draft? | user_value | meeting workflow evidence | research meeting handoff evidence | `PYTHONPATH=src python -m news_thesis_impact_lab decision-journal --packet demo/impact_packet.json --compare demo/compare/compare.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --ledger demo/ledger/review_ledger.json --evidence demo/evidence/evidence_hub.json --out demo/journal` | `99fad44207637d183346495e15c8f4446772bcf5b47c632d2edcffabf553f66e` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/journal/decision_journal.md` | decision-journal-markdown | Can the research meeting draft be reviewed without parsing JSON? | showcase | meeting narrative evidence | research meeting handoff narrative | `PYTHONPATH=src python -m news_thesis_impact_lab decision-journal --packet demo/impact_packet.json --compare demo/compare/compare.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --ledger demo/ledger/review_ledger.json --evidence demo/evidence/evidence_hub.json --out demo/journal` | `2d39115f2189a18cb2df79714ecd1f40bb0b4e3198ccc9a23b5ebc0f2bfb1422` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/journal/decision_journal.html` | decision-journal-html | Can the research meeting draft be scanned as static no-JavaScript HTML? | showcase | static HTML meeting evidence | visual review surface | `PYTHONPATH=src python -m news_thesis_impact_lab decision-journal --packet demo/impact_packet.json --compare demo/compare/compare.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --ledger demo/ledger/review_ledger.json --evidence demo/evidence/evidence_hub.json --out demo/journal` | `8f9205c709a817392c84bae9fcb7aaf24bdc6b0fde24278989b0a9a22ef1ba35` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
| `demo/visual/visual_receipt.json` | visual-receipt-json | Which static HTML pages prove no-script and boundary coverage? | risk | no-JavaScript and boundary evidence | promotion safety evidence | `PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual` | `d495905b45aeabff2d1ff37e3eeee6c435d55610de267d5d916b99ebcce4c548` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/visual/visual_receipt.md` | visual-receipt-markdown | Can visual review checks be audited without running a browser? | risk | promotion receipt evidence | promotion safety narrative | `PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual` | `93414427c55046f64fd8d826bfb4088252c9aec845a6e4b4f45975a987ff3813` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/walkthrough/walkthrough.json` | walkthrough-json | Can a first user reproduce the artifact set quickly from local files? | runnable | cold-start reproducibility evidence | first-user promotion evidence | `PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough` | `98787839136619573de0a8f8d76d70f70a0ae69a5afb8ff17418326a486041ea` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/walkthrough/walkthrough.md` | walkthrough-markdown | Can the cold-start path be followed without interpreting CLI internals? | runnable | cold-start review evidence | first-user narrative | `PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough` | `b10c47ca31b5336b02dfaafa5b10bd6ee5db94b8ec3d1b2f69ce88da5b2a141d` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/health/asset_health.json` | asset-health-json | Does the source package, public artifacts, private-reference scan, and release checklist pass? | engineering | asset health authority | release and promotion checklist input | `PYTHONPATH=src python -m news_thesis_impact_lab asset-health --out demo/health` | `425a4ef42c6dc1cdeb4a4d4b7c263c1ab54b2e4e839de368b61c1403d2d6c0ab` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/health/asset_health.md` | asset-health-markdown | Can release health be reviewed without parsing JSON? | showcase | human-readable asset health evidence | release and promotion checklist narrative | `PYTHONPATH=src python -m news_thesis_impact_lab asset-health --out demo/health` | `fcc5329b6279c705f8b200fd57e43109e5f3a3adb65b7bca0b35b1398ca65bd9` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/health/asset_health.html` | asset-health-html | Can release health be scanned as static no-JavaScript HTML? | showcase | static HTML asset health evidence | visual release health surface | `PYTHONPATH=src python -m news_thesis_impact_lab asset-health --out demo/health` | `68c3b49ea0896f789ee31afdbbb76b0a57d2edd23b56d4c9998cf1dd879a7c06` | true | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Static no-script check does not execute a browser layout engine. |
| `demo/maturity/maturity_report.json` | maturity-json | Do release and promotion gates pass by rubric area? | engineering | release gate summary | promotion gate summary | `PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity` | `72cca030fdbee061bfd64f7bdc66e9689e3be6a77f5012c7acc10f4245fbb649` | n/a | 0/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `demo/maturity/maturity_report.md` | maturity-markdown | Can readiness scoring be reviewed without parsing JSON? | engineering | human-readable gate summary | promotion gate narrative | `PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity` | `2f7194d1f2afae3080651353f13a5655df3123cf77a0d0a1ad57670627a622d7` | n/a | 0/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `docs/cold-user-walkthrough.md` | cold-user-walkthrough-doc | Can a public first user clone, install, run, troubleshoot, and understand safety boundaries in 10 minutes? | runnable | cold-user source onboarding evidence | public comprehension evidence | `not generated by a public CLI command` | `7aa5048c12eaf37abe336f1d252522d00b84c8227b3e8140a8f045080f16d74e` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness. |
| `release/manifest.json` | release-manifest-json | Which public artifacts, commands, hashes, and package metadata define this release? | engineering | release hash authority | promotion audit input | `PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release` | `78ae54730a31d3ddd8395ca285f2a47a66075f11895a3fbdd0e610d8b66bf095` | n/a | 4/4 | Static local artifact; reviewer must inspect source inputs for research completeness.; Distribution entries may be placeholders until wheel and sdist files are built. |

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
