from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .release import validate_release
from .render import write_json


SCORES = {
    "product": 4,
    "runnable": 5,
    "user_value": 4,
    "evidence": 4,
    "engineering": 4,
    "showcase": 4,
    "risk": 5,
}


RATIONALE = {
    "product": "Clear CLI asset with bounded static research workflow and public package metadata.",
    "runnable": "Stdlib-only commands, examples, demo artifacts, scenario stress review, repeated-use review ledger, decision journal draft, visual receipt, cold-start walkthrough, asset health, tests, selfcheck, and privacy scan.",
    "user_value": "Maps local catalysts and illustrative stress scenarios to thesis claims, exposure, warnings, confidence review, ledger status, meeting-draft placeholders, and human prompts.",
    "evidence": "Includes deterministic demo JSON/Markdown/HTML, compare, trend, scenario stress, review ledger, decision journal outputs, visual receipt, walkthrough, evidence hub, asset health, tests, and release validation.",
    "engineering": "Typed dataclasses, deterministic rendering, focused CLI surface, and no runtime dependencies.",
    "showcase": "Demo packet, compare packet, trend history, scenario stress review, review ledger, decision journal, visual receipt, cold-start walkthrough, evidence hub, asset health, review doc, and agent skill show the intended workflow.",
    "risk": "Strong research-only boundaries with no live data, broker access, orders, or advice.",
}


def build_maturity_report(root: Path) -> Dict[str, Any]:
    validation = validate_release(root)
    gates = {
        "release_ready": validation["ok"] and min(SCORES.values()) >= 4,
        "promotion_ready": validation["ok"] and SCORES["showcase"] >= 4 and SCORES["risk"] >= 5,
    }
    return {
        "schema_version": "1.0",
        "asset": "news-thesis-impact-lab",
        "generated_at": "2026-07-10",
        "scale": "1=missing, 3=usable, 5=strong public release signal",
        "scores": SCORES,
        "rationale": RATIONALE,
        "gates": gates,
        "release_validation": {"ok": validation["ok"], "failed_checks": failed_check_names(validation)},
    }


def write_maturity_report(root: Path, out: Path) -> Dict[str, Any]:
    report = build_maturity_report(root)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "maturity_report.json", report)
    (out / "maturity_report.md").write_text(render_maturity_markdown(report), encoding="utf-8")
    return report


def render_maturity_markdown(report: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Maturity Report",
        "",
        f"Asset: {report['asset']}",
        f"Generated: {report['generated_at']}",
        f"Scale: {report['scale']}",
        "",
        "## Scores",
        "",
    ]
    for name, score in report["scores"].items():
        lines.append(f"- {name}: {score}/5 - {report['rationale'][name]}")
    lines.extend(
        [
            "",
            "## Gates",
            "",
            f"- release_ready: {str(report['gates']['release_ready']).lower()}",
            f"- promotion_ready: {str(report['gates']['promotion_ready']).lower()}",
            "",
            "## Evidence",
            "",
            f"- release_validation_ok: {str(report['release_validation']['ok']).lower()}",
            f"- failed_checks: {', '.join(report['release_validation']['failed_checks']) or 'none'}",
            "",
        ]
    )
    return "\n".join(lines)


def failed_check_names(validation: Dict[str, Any]) -> List[str]:
    return [check["name"] for check in validation["checks"] if not check["ok"]]
