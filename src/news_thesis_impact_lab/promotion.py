from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Dict, List

from .model import BOUNDARIES
from .render import write_json


VISUAL_ASSETS = [
    {
        "path": Path("demo/index.html"),
        "route": "demo/index.html",
        "role": "impact packet scan view",
        "review_notes": "Confirm impacted tickers, warnings, review prompts, and finance boundaries are visible without JavaScript.",
    },
    {
        "path": Path("demo/gallery.html"),
        "route": "demo/gallery.html",
        "role": "artifact gallery entry point",
        "review_notes": "Confirm first-screen artifact links, quickstart, and finance boundaries are visible without JavaScript.",
    },
    {
        "path": Path("demo/trend/trend_history.html"),
        "route": "demo/trend/trend_history.html",
        "role": "trend history scan view",
        "review_notes": "Confirm multi-period status, persistent warning, review queue, and finance boundaries are visible without JavaScript.",
    },
    {
        "path": Path("demo/scenario/scenario_stress.html"),
        "route": "demo/scenario/scenario_stress.html",
        "role": "scenario stress scan view",
        "review_notes": "Confirm scenario coverage, ticker stress flags, contradiction prompts, confidence suggestions, and finance boundaries are visible without JavaScript.",
    },
]


WALKTHROUGH_COMMANDS = [
    "PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo",
    "PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare",
    "PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend",
    "PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario",
    "PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual",
    "PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough",
    "PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json",
]


WALKTHROUGH_ARTIFACTS = [
    "demo/impact_packet.json",
    "demo/impact_packet.md",
    "demo/index.html",
    "demo/compare/compare.json",
    "demo/compare/compare.md",
    "demo/trend/trend_history.json",
    "demo/trend/trend_history.md",
    "demo/trend/trend_history.html",
    "demo/scenario/scenario_stress.json",
    "demo/scenario/scenario_stress.md",
    "demo/scenario/scenario_stress.html",
    "demo/visual/visual_receipt.json",
    "demo/visual/visual_receipt.md",
    "demo/walkthrough/walkthrough.json",
    "demo/walkthrough/walkthrough.md",
]


def write_visual_receipt(root: Path, out: Path) -> Dict[str, Any]:
    receipt = build_visual_receipt(root)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "visual_receipt.json", receipt)
    (out / "visual_receipt.md").write_text(render_visual_receipt_markdown(receipt), encoding="utf-8")
    return receipt


def build_visual_receipt(root: Path) -> Dict[str, Any]:
    root = root.resolve()
    captures = [visual_capture_record(root, asset) for asset in VISUAL_ASSETS]
    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-10",
        "capture_type": "static_html_receipt",
        "description": "Deterministic static capture receipt for promotion review; no screenshots, browser automation, network, or JavaScript execution required.",
        "finance_safety_boundaries": BOUNDARIES,
        "captures": captures,
        "summary": {
            "asset_count": len(captures),
            "all_no_script": all(capture["no_script"] for capture in captures),
            "all_boundaries_present": all(capture["boundaries_present"] for capture in captures),
        },
    }


def visual_capture_record(root: Path, asset: Dict[str, Any]) -> Dict[str, Any]:
    relative_path = asset["path"]
    path = root / relative_path
    data = path.read_bytes() if path.is_file() else b""
    text = data.decode("utf-8") if data else ""
    title = extract_title(text) if text else "missing"
    missing_boundaries = [boundary for boundary in BOUNDARIES if boundary not in text]
    return {
        "title": title,
        "role": asset["role"],
        "route": asset["route"],
        "path": relative_path.as_posix(),
        "exists": path.is_file(),
        "bytes": len(data) if data else None,
        "sha256": hashlib.sha256(data).hexdigest() if data else None,
        "no_script": "<script" not in text.lower() if text else False,
        "boundaries_present": not missing_boundaries,
        "missing_boundaries": missing_boundaries,
        "capture_command": f"static read {relative_path.as_posix()}",
        "review_notes": asset["review_notes"],
    }


def extract_title(html: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return "untitled"
    return re.sub(r"\s+", " ", match.group(1)).strip()


def render_visual_receipt_markdown(receipt: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Visual Receipt",
        "",
        f"Generated: {receipt['generated_at']}",
        f"Capture type: {receipt['capture_type']}",
        "",
        receipt["description"],
        "",
        "## Summary",
        "",
        f"- asset_count: {receipt['summary']['asset_count']}",
        f"- all_no_script: {str(receipt['summary']['all_no_script']).lower()}",
        f"- all_boundaries_present: {str(receipt['summary']['all_boundaries_present']).lower()}",
        "",
        "## Captures",
        "",
        "| Title | Role | Route | Path | Bytes | SHA-256 | No script | Boundaries | Capture command |",
        "| --- | --- | --- | --- | ---: | --- | --- | --- | --- |",
    ]
    for capture in receipt["captures"]:
        lines.append(
            f"| {capture['title']} | {capture['role']} | `{capture['route']}` | `{capture['path']}` | "
            f"{capture['bytes'] or 0} | `{capture['sha256'] or 'missing'}` | "
            f"{str(capture['no_script']).lower()} | {str(capture['boundaries_present']).lower()} | "
            f"`{capture['capture_command']}` |"
        )
    lines.extend(["", "## Review Notes", ""])
    lines.extend(f"- `{capture['path']}`: {capture['review_notes']}" for capture in receipt["captures"])
    lines.extend(["", "## Finance Safety Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in receipt["finance_safety_boundaries"])
    lines.append("")
    return "\n".join(lines)


def write_cold_start_walkthrough(out: Path) -> Dict[str, Any]:
    walkthrough = build_cold_start_walkthrough()
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "walkthrough.json", walkthrough)
    (out / "walkthrough.md").write_text(render_walkthrough_markdown(walkthrough), encoding="utf-8")
    return walkthrough


def build_cold_start_walkthrough() -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-10",
        "title": "Cold-Start Walkthrough",
        "audience": "First user reviewing the public demo from a clean checkout.",
        "duration": "2-5 minutes",
        "goal": "Generate the local packet, compare, trend, scenario stress, visual receipt, walkthrough, and release validation evidence without network, broker, order, or advice behavior.",
        "commands": WALKTHROUGH_COMMANDS,
        "expected_artifacts": WALKTHROUGH_ARTIFACTS,
        "interpretation_guide": [
            "Start with demo/gallery.html for the linked artifact set and finance boundaries.",
            "Read demo/impact_packet.md as a research triage packet; attention scores rank review urgency, not trades.",
            "Use demo/compare/compare.md to spot changes versus the previous static packet.",
            "Use demo/trend/trend_history.md to review score direction, warning persistence, exposure trend, and next review queue.",
            "Use demo/scenario/scenario_stress.md to review illustrative macro, sector, and company shock overlap against thesis language.",
            "Use demo/visual/visual_receipt.md to confirm static HTML pages pass no-script checks and retain boundaries.",
            "Treat validate-release JSON as the promotion gate summary; every check should be true before publishing.",
        ],
        "failure_modes": [
            "Missing example JSON files cause packet, compare, trend, and validation commands to fail.",
            "Edited generated files cause deterministic release validation to report changed artifacts.",
            "Removing finance boundaries from public artifacts causes boundary validation to fail.",
            "Adding script tags to static demo HTML causes the visual receipt no-script summary to fail.",
            "Using live market data, broker integrations, orders, or advice language is outside project scope.",
        ],
        "boundaries": BOUNDARIES,
    }


def render_walkthrough_markdown(walkthrough: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Cold-Start Walkthrough",
        "",
        f"Generated: {walkthrough['generated_at']}",
        f"Audience: {walkthrough['audience']}",
        f"Duration: {walkthrough['duration']}",
        "",
        walkthrough["goal"],
        "",
        "## Commands",
        "",
    ]
    lines.extend(f"```bash\n{command}\n```" for command in walkthrough["commands"])
    lines.extend(["", "## Expected Artifacts", ""])
    lines.extend(f"- `{artifact}`" for artifact in walkthrough["expected_artifacts"])
    lines.extend(["", "## Interpretation Guide", ""])
    lines.extend(f"- {item}" for item in walkthrough["interpretation_guide"])
    lines.extend(["", "## Failure Modes And Boundaries", ""])
    lines.extend(f"- {item}" for item in walkthrough["failure_modes"])
    lines.extend(["", "## Finance Safety Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in walkthrough["boundaries"])
    lines.append("")
    return "\n".join(lines)
