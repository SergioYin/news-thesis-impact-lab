from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Dict, List

from .journal import JOURNAL_BOUNDARIES
from .maturity import RATIONALE, SCORES
from .model import BOUNDARIES
from .asset import HEALTH_FILES
from .release import DEMO_FILES, REGENERATE_COMMANDS
from .render import esc, write_json


EVIDENCE_FILES = [
    Path("demo/evidence/evidence_hub.json"),
    Path("demo/evidence/evidence_hub.md"),
    Path("demo/evidence/evidence_hub.html"),
]

EVIDENCE_INPUTS = [path for path in DEMO_FILES if not path.as_posix().startswith("demo/evidence/")] + HEALTH_FILES + [
    Path("demo/maturity/maturity_report.json"),
    Path("demo/maturity/maturity_report.md"),
    Path("release/manifest.json")
]


ARTIFACT_CLASSIFICATION = {
    "demo/impact_packet.json": (
        "packet-json",
        "Which tickers are affected by local catalysts, and why?",
        "user_value",
        "core deterministic demo evidence",
        "primary reviewer workflow evidence",
    ),
    "demo/impact_packet.md": (
        "packet-markdown",
        "Can a reviewer read the catalyst-to-thesis packet without tooling?",
        "showcase",
        "public review artifact",
        "human-readable reviewer packet",
    ),
    "demo/index.html": (
        "packet-html",
        "Can the packet be scanned as static no-JavaScript HTML?",
        "showcase",
        "static HTML boundary evidence",
        "visual review surface",
    ),
    "demo/gallery.html": (
        "gallery-html",
        "Where does a reviewer start when inspecting the public artifact set?",
        "showcase",
        "artifact navigation evidence",
        "promotion entry point",
    ),
    "demo/compare/compare.json": (
        "compare-json",
        "What changed versus the previous static packet?",
        "evidence",
        "deterministic comparison evidence",
        "change-review evidence",
    ),
    "demo/compare/compare.md": (
        "compare-markdown",
        "Can packet changes be reviewed without parsing JSON?",
        "evidence",
        "human-readable comparison evidence",
        "change-review narrative",
    ),
    "demo/trend/trend_history.json": (
        "trend-json",
        "How did ticker status, scores, warnings, and exposure change across periods?",
        "evidence",
        "multi-period evidence",
        "repeat-review signal",
    ),
    "demo/trend/trend_history.md": (
        "trend-markdown",
        "Can multi-period drift be reviewed without tooling?",
        "showcase",
        "trend review evidence",
        "repeat-review narrative",
    ),
    "demo/trend/trend_history.html": (
        "trend-html",
        "Can trend history be scanned as static no-JavaScript HTML?",
        "showcase",
        "static HTML trend evidence",
        "visual review surface",
    ),
    "demo/scenario/scenario_stress.json": (
        "scenario-json",
        "Which illustrative stresses overlap with thesis and exposure language?",
        "user_value",
        "scenario coverage evidence",
        "stress-review evidence",
    ),
    "demo/scenario/scenario_stress.md": (
        "scenario-markdown",
        "Can scenario stress prompts be reviewed without parsing JSON?",
        "showcase",
        "scenario review evidence",
        "stress-review narrative",
    ),
    "demo/scenario/scenario_stress.html": (
        "scenario-html",
        "Can stress review be scanned as static no-JavaScript HTML?",
        "showcase",
        "static HTML stress evidence",
        "visual review surface",
    ),
    "demo/ledger/review_ledger.json": (
        "ledger-json",
        "Which review issues are new, open, watch, resolved, stale, or severe?",
        "user_value",
        "repeat-use state evidence",
        "ongoing review evidence",
    ),
    "demo/ledger/review_ledger.md": (
        "ledger-markdown",
        "Can repeated-use review state be inspected without parsing JSON?",
        "showcase",
        "ledger review evidence",
        "ongoing review narrative",
    ),
    "demo/ledger/review_ledger.html": (
        "ledger-html",
        "Can review ledger status be scanned as static no-JavaScript HTML?",
        "showcase",
        "static HTML ledger evidence",
        "visual review surface",
    ),
    "demo/journal/decision_journal.json": (
        "decision-journal-json",
        "Can research meetings start from a structured non-recommendation journal draft?",
        "user_value",
        "meeting workflow evidence",
        "research meeting handoff evidence",
    ),
    "demo/journal/decision_journal.md": (
        "decision-journal-markdown",
        "Can the research meeting draft be reviewed without parsing JSON?",
        "showcase",
        "meeting narrative evidence",
        "research meeting handoff narrative",
    ),
    "demo/journal/decision_journal.html": (
        "decision-journal-html",
        "Can the research meeting draft be scanned as static no-JavaScript HTML?",
        "showcase",
        "static HTML meeting evidence",
        "visual review surface",
    ),
    "demo/visual/visual_receipt.json": (
        "visual-receipt-json",
        "Which static HTML pages prove no-script and boundary coverage?",
        "risk",
        "no-JavaScript and boundary evidence",
        "promotion safety evidence",
    ),
    "demo/visual/visual_receipt.md": (
        "visual-receipt-markdown",
        "Can visual review checks be audited without running a browser?",
        "risk",
        "promotion receipt evidence",
        "promotion safety narrative",
    ),
    "demo/walkthrough/walkthrough.json": (
        "walkthrough-json",
        "Can a first user reproduce the artifact set quickly from local files?",
        "runnable",
        "cold-start reproducibility evidence",
        "first-user promotion evidence",
    ),
    "demo/walkthrough/walkthrough.md": (
        "walkthrough-markdown",
        "Can the cold-start path be followed without interpreting CLI internals?",
        "runnable",
        "cold-start review evidence",
        "first-user narrative",
    ),
    "demo/maturity/maturity_report.json": (
        "maturity-json",
        "Do release and promotion gates pass by rubric area?",
        "engineering",
        "release gate summary",
        "promotion gate summary",
    ),
    "demo/maturity/maturity_report.md": (
        "maturity-markdown",
        "Can readiness scoring be reviewed without parsing JSON?",
        "engineering",
        "human-readable gate summary",
        "promotion gate narrative",
    ),
    "release/manifest.json": (
        "release-manifest-json",
        "Which public artifacts, commands, hashes, and package metadata define this release?",
        "engineering",
        "release hash authority",
        "promotion audit input",
    ),
    "demo/health/asset_health.json": (
        "asset-health-json",
        "Does the source package, public artifacts, private-reference scan, and release checklist pass?",
        "engineering",
        "asset health authority",
        "release and promotion checklist input",
    ),
    "demo/health/asset_health.md": (
        "asset-health-markdown",
        "Can release health be reviewed without parsing JSON?",
        "showcase",
        "human-readable asset health evidence",
        "release and promotion checklist narrative",
    ),
    "demo/health/asset_health.html": (
        "asset-health-html",
        "Can release health be scanned as static no-JavaScript HTML?",
        "showcase",
        "static HTML asset health evidence",
        "visual release health surface",
    ),
}


def write_evidence_hub(root: Path, out: Path) -> Dict[str, Any]:
    hub = build_evidence_hub(root)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "evidence_hub.json", hub)
    (out / "evidence_hub.md").write_text(render_evidence_hub_markdown(hub), encoding="utf-8")
    (out / "evidence_hub.html").write_text(render_evidence_hub_html(hub), encoding="utf-8")
    return hub


def build_evidence_hub(root: Path) -> Dict[str, Any]:
    root = root.resolve()
    matrix = [artifact_evidence_record(root, path) for path in EVIDENCE_INPUTS]
    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-10",
        "title": "Evidence Hub",
        "description": "Reviewer-facing matrix for deterministic public demo artifacts and the release manifest.",
        "finance_safety_boundaries": BOUNDARIES,
        "rubric_scores": {
            name: {"score": score, "rationale": RATIONALE[name], "artifact_count": rubric_count(matrix, name)}
            for name, score in SCORES.items()
        },
        "release_gate_evidence": [
            item["path"] for item in matrix if item["exists"] and item["release_gate_relevance"] != "supporting context"
        ],
        "promotion_gate_evidence": [
            item["path"] for item in matrix if item["exists"] and item["promotion_gate_relevance"] != "supporting context"
        ],
        "matrix": matrix,
        "known_limitations": [
            "The hub indexes static local artifacts only; it does not fetch live market, broker, account, or news data.",
            "Hashes prove file content identity, not investment correctness or external factual completeness.",
            "Scenario stress records are illustrative research prompts, not forecasts, advice, or trade instructions.",
            "No-JavaScript checks are static text checks for script tags, not full browser rendering tests.",
        ],
    }


def artifact_evidence_record(root: Path, relative_path: Path) -> Dict[str, Any]:
    path_key = relative_path.as_posix()
    artifact_type, question, rubric, release_relevance, promotion_relevance = ARTIFACT_CLASSIFICATION.get(
        path_key,
        (
            infer_artifact_type(relative_path),
            "What public release evidence does this artifact provide?",
            "evidence",
            "supporting context",
            "supporting context",
        ),
    )
    path = root / relative_path
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    data = text.encode("utf-8") if path.is_file() else b""
    return {
        "path": path_key,
        "artifact_type": artifact_type,
        "user_question_answered": question,
        "maturity_rubric_category": rubric,
        "release_gate_relevance": release_relevance,
        "promotion_gate_relevance": promotion_relevance,
        "command_to_regenerate": command_to_regenerate(path_key),
        "exists": path.is_file(),
        "sha256": hashlib.sha256(data).hexdigest() if data else None,
        "bytes": len(data) if data else None,
        "no_js": no_js_value(relative_path, text),
        "boundary_coverage": boundary_coverage(text),
        "known_limitations": limitations_for(path_key),
    }


def infer_artifact_type(path: Path) -> str:
    suffix = path.suffix.lstrip(".") or "artifact"
    return f"{path.parent.name}-{suffix}" if path.parent.name != "." else suffix


def command_to_regenerate(path_key: str) -> str:
    command_by_prefix = {
        "demo/impact_packet": REGENERATE_COMMANDS[0],
        "demo/index.html": REGENERATE_COMMANDS[0],
        "demo/compare/": REGENERATE_COMMANDS[1],
        "demo/trend/": REGENERATE_COMMANDS[2],
        "demo/scenario/": REGENERATE_COMMANDS[3],
        "demo/ledger/": REGENERATE_COMMANDS[4],
        "demo/journal/": REGENERATE_COMMANDS[5],
        "demo/maturity/": REGENERATE_COMMANDS[6],
        "demo/health/": REGENERATE_COMMANDS[13],
        "demo/gallery.html": REGENERATE_COMMANDS[7],
        "demo/visual/": REGENERATE_COMMANDS[8],
        "demo/walkthrough/": REGENERATE_COMMANDS[9],
        "release/manifest.json": REGENERATE_COMMANDS[10],
    }
    for prefix, command in command_by_prefix.items():
        if path_key.startswith(prefix):
            return command
    return "not generated by a public CLI command"


def no_js_value(path: Path, text: str) -> bool | None:
    if path.suffix != ".html":
        return None
    return "<script" not in text.lower() if text else False


def boundary_coverage(text: str) -> Dict[str, Any]:
    boundaries = JOURNAL_BOUNDARIES if "Research meeting draft only" in text else BOUNDARIES
    present = [boundary for boundary in boundaries if boundary in text]
    missing = [boundary for boundary in boundaries if boundary not in text]
    return {
        "present_count": len(present),
        "missing_count": len(missing),
        "all_present": not missing,
        "missing": missing,
    }


def limitations_for(path_key: str) -> List[str]:
    limitations = ["Static local artifact; reviewer must inspect source inputs for research completeness."]
    if path_key.endswith(".html"):
        limitations.append("Static no-script check does not execute a browser layout engine.")
    if "scenario" in path_key:
        limitations.append("Scenario fixtures are illustrative stress prompts, not forecasts.")
    if "manifest" in path_key:
        limitations.append("Distribution entries may be placeholders until wheel and sdist files are built.")
    return limitations


def rubric_count(matrix: List[Dict[str, Any]], category: str) -> int:
    return sum(1 for item in matrix if item["exists"] and item["maturity_rubric_category"] == category)


def render_evidence_hub_markdown(hub: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Evidence Hub",
        "",
        f"Generated: {hub['generated_at']}",
        "",
        hub["description"],
        "",
        "## Rubric Summary",
        "",
        "| Area | Score | Artifact count | Rationale |",
        "| --- | ---: | ---: | --- |",
    ]
    for area, score in hub["rubric_scores"].items():
        lines.append(f"| {area} | {score['score']}/5 | {score['artifact_count']} | {score['rationale']} |")
    lines.extend(["", "## Release Gate Evidence", ""])
    lines.extend(f"- `{path}`" for path in hub["release_gate_evidence"])
    lines.extend(["", "## Promotion Gate Evidence", ""])
    lines.extend(f"- `{path}`" for path in hub["promotion_gate_evidence"])
    lines.extend(
        [
            "",
            "## Artifact Matrix",
            "",
            "| Path | Type | Question answered | Rubric | Release gate | Promotion gate | Regenerate | SHA-256 | No JS | Boundary coverage | Known limitations |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in hub["matrix"]:
        lines.append(
            f"| `{item['path']}` | {item['artifact_type']} | {item['user_question_answered']} | "
            f"{item['maturity_rubric_category']} | {item['release_gate_relevance']} | "
            f"{item['promotion_gate_relevance']} | `{item['command_to_regenerate']}` | "
            f"`{item['sha256'] or 'missing'}` | {format_no_js(item['no_js'])} | "
            f"{item['boundary_coverage']['present_count']}/{len(hub['finance_safety_boundaries'])} | "
            f"{'; '.join(item['known_limitations'])} |"
        )
    lines.extend(["", "## Finance Safety Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in hub["finance_safety_boundaries"])
    lines.extend(["", "## Known Limitations", ""])
    lines.extend(f"- {item}" for item in hub["known_limitations"])
    lines.append("")
    return "\n".join(lines)


def render_evidence_hub_html(hub: Dict[str, Any]) -> str:
    boundaries = "".join(f"<li>{esc(boundary)}</li>" for boundary in hub["finance_safety_boundaries"])
    rubric_rows = "".join(
        "<tr>"
        f"<td>{esc(area)}</td>"
        f"<td>{score['score']}/5</td>"
        f"<td>{score['artifact_count']}</td>"
        f"<td>{esc(score['rationale'])}</td>"
        "</tr>"
        for area, score in hub["rubric_scores"].items()
    )
    matrix_rows = "".join(
        "<tr>"
        f"<td><code>{esc(item['path'])}</code></td>"
        f"<td>{esc(item['artifact_type'])}</td>"
        f"<td>{esc(item['user_question_answered'])}</td>"
        f"<td>{esc(item['maturity_rubric_category'])}</td>"
        f"<td>{esc(item['release_gate_relevance'])}</td>"
        f"<td>{esc(item['promotion_gate_relevance'])}</td>"
        f"<td><code>{esc(item['command_to_regenerate'])}</code></td>"
        f"<td><code>{esc(item['sha256'] or 'missing')}</code></td>"
        f"<td>{esc(format_no_js(item['no_js']))}</td>"
        f"<td>{item['boundary_coverage']['present_count']}/{len(hub['finance_safety_boundaries'])}</td>"
        f"<td>{esc('; '.join(item['known_limitations']))}</td>"
        "</tr>"
        for item in hub["matrix"]
    )
    release_items = "".join(f"<li><code>{esc(path)}</code></li>" for path in hub["release_gate_evidence"])
    promotion_items = "".join(f"<li><code>{esc(path)}</code></li>" for path in hub["promotion_gate_evidence"])
    limitations = "".join(f"<li>{esc(item)}</li>" for item in hub["known_limitations"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Evidence Hub</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1280px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 1.75rem; }}
    table {{ border-collapse: collapse; width: 100%; background: white; margin: 0.75rem 0 1.25rem; }}
    th, td {{ border: 1px solid #d8dee8; padding: 0.6rem; vertical-align: top; text-align: left; }}
    th {{ background: #e9eef5; }}
    code {{ white-space: normal; overflow-wrap: anywhere; }}
    .note {{ background: #fff; border: 1px solid #d8dee8; padding: 1rem; margin: 1rem 0; }}
    .columns {{ display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }}
  </style>
</head>
<body>
<main>
  <h1>Evidence Hub</h1>
  <p>Generated {esc(hub['generated_at'])}. {esc(hub['description'])}</p>
  <section class="note"><h2>Finance Safety Boundaries</h2><ul>{boundaries}</ul></section>
  <h2>Rubric Summary</h2>
  <table><thead><tr><th>Area</th><th>Score</th><th>Artifacts</th><th>Rationale</th></tr></thead><tbody>{rubric_rows}</tbody></table>
  <section class="columns">
    <div><h2>Release Gate Evidence</h2><ul>{release_items}</ul></div>
    <div><h2>Promotion Gate Evidence</h2><ul>{promotion_items}</ul></div>
  </section>
  <h2>Artifact Matrix</h2>
  <table><thead><tr><th>Path</th><th>Type</th><th>Question</th><th>Rubric</th><th>Release gate</th><th>Promotion gate</th><th>Regenerate</th><th>SHA-256</th><th>No JS</th><th>Boundaries</th><th>Known limitations</th></tr></thead><tbody>{matrix_rows}</tbody></table>
  <h2>Known Limitations</h2>
  <ul>{limitations}</ul>
</main>
</body>
</html>
"""


def format_no_js(value: bool | None) -> str:
    if value is None:
        return "n/a"
    return str(value).lower()
