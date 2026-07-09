from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

from .render import esc, write_json


JOURNAL_BOUNDARIES = [
    "Static local research notes only; no live market data is fetched.",
    "Research meeting draft only; no investment recommendation or allocation instruction.",
    "No broker integration, order routing, execution, or account access.",
    "Review decisions are editable research-process placeholders for human notes.",
]

JOURNAL_FORBIDDEN_TERMS = ["buy", "sell", "hold"]


def write_decision_journal(
    impact_packet: Dict[str, Any],
    compare_report: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
    review_ledger: Dict[str, Any],
    evidence_hub: Dict[str, Any],
    out: Path,
) -> Dict[str, Any]:
    journal = build_decision_journal(
        impact_packet,
        compare_report,
        trend_history,
        scenario_stress,
        review_ledger,
        evidence_hub,
    )
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "decision_journal.json", journal)
    (out / "decision_journal.md").write_text(render_decision_journal_markdown(journal), encoding="utf-8")
    (out / "decision_journal.html").write_text(render_decision_journal_html(journal), encoding="utf-8")
    return journal


def build_decision_journal(
    impact_packet: Dict[str, Any],
    compare_report: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
    review_ledger: Dict[str, Any],
    evidence_hub: Dict[str, Any],
) -> Dict[str, Any]:
    generated_at = str(impact_packet.get("generated_at") or "2026-07-10")
    tickers = ordered_tickers(impact_packet, review_ledger)
    thesis_questions = build_thesis_questions(impact_packet, trend_history, scenario_stress)
    evidence_excerpts = build_evidence_excerpts(impact_packet, compare_report, trend_history, scenario_stress, review_ledger)
    risk_flags = build_risk_flags(impact_packet, trend_history, scenario_stress, review_ledger)
    unresolved_assumptions = build_unresolved_assumptions(impact_packet, trend_history, scenario_stress, evidence_hub)
    decisions = build_review_decisions(tickers, review_ledger, risk_flags)
    checklist = build_follow_up_checklist(decisions, unresolved_assumptions)
    journal = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "title": "Decision Journal Draft",
        "meeting_type": "research_review",
        "no_recommendation_statement": "This draft records research questions and process placeholders only; it does not provide investment recommendations, allocation instructions, account actions, or execution instructions.",
        "boundaries": JOURNAL_BOUNDARIES,
        "source_artifacts": {
            "impact_packet": "demo/impact_packet.json",
            "compare_report": "demo/compare/compare.json",
            "trend_history": "demo/trend/trend_history.json",
            "scenario_stress": "demo/scenario/scenario_stress.json",
            "review_ledger": "demo/ledger/review_ledger.json",
            "evidence_hub": "demo/evidence/evidence_hub.json",
        },
        "source_generated_at": {
            "impact_packet": impact_packet.get("generated_at", "unknown"),
            "compare_report": compare_report.get("generated_at", "unknown"),
            "trend_history": trend_history.get("generated_at", "unknown"),
            "scenario_stress": scenario_stress.get("generated_at", "unknown"),
            "review_ledger": review_ledger.get("generated_at", "unknown"),
            "evidence_hub": evidence_hub.get("generated_at", "unknown"),
        },
        "meeting_fields": {
            "meeting_date": "",
            "facilitator": "",
            "participants": [],
            "prepared_by": "",
        },
        "thesis_questions": thesis_questions,
        "evidence_excerpts": evidence_excerpts,
        "risk_flags": risk_flags,
        "unresolved_assumptions": unresolved_assumptions,
        "review_decisions": decisions,
        "follow_up_checklist": checklist,
    }
    assert_no_forbidden_terms(journal)
    return journal


def ordered_tickers(packet: Dict[str, Any], ledger: Dict[str, Any]) -> List[str]:
    seen: List[str] = []
    for item in packet.get("impacted_tickers", []):
        ticker = str(item.get("ticker", ""))
        if ticker and ticker not in seen:
            seen.append(ticker)
    for item in ledger.get("items", []):
        ticker = str(item.get("ticker", ""))
        if ticker and ticker not in seen:
            seen.append(ticker)
    return seen


def build_thesis_questions(
    packet: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
) -> List[Dict[str, Any]]:
    trend_prompts = {item["ticker"]: item.get("prompt", "") for item in trend_history.get("next_review_queue", [])}
    stress_prompts = {item["ticker"]: item.get("prompt", "") for item in scenario_stress.get("next_review_queue", [])}
    questions = []
    for item in packet.get("impacted_tickers", []):
        ticker = str(item["ticker"])
        prompts = list(item.get("next_review_prompts", []))
        if trend_prompts.get(ticker):
            prompts.append(trend_prompts[ticker])
        if stress_prompts.get(ticker):
            prompts.append(stress_prompts[ticker])
        questions.append(
            {
                "ticker": ticker,
                "primary_question": f"What local evidence would change the current {ticker} thesis wording?",
                "supporting_questions": unique_limited(prompts, 4),
                "affected_claims": item.get("affected_thesis_claims", [])[:3],
                "owner": "",
                "due_date": "",
            }
        )
    return questions


def build_evidence_excerpts(
    packet: Dict[str, Any],
    compare_report: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
    review_ledger: Dict[str, Any],
) -> List[Dict[str, Any]]:
    excerpts = []
    for item in packet.get("impacted_tickers", [])[:6]:
        excerpts.append(
            {
                "source": "impact_packet",
                "path": "demo/impact_packet.json",
                "ticker": item["ticker"],
                "excerpt": f"attention {item['attention_score']}; direction {item['direction']}; confidence {item['confidence']}; prompts {join_short(item.get('next_review_prompts', []), 2)}",
            }
        )
    for item in compare_report.get("deltas", [])[:6]:
        excerpts.append(
            {
                "source": "compare_report",
                "path": "demo/compare/compare.json",
                "ticker": item["ticker"],
                "excerpt": f"{item['status']} delta; attention score delta {item['attention_score_delta']}; direction {item['previous_direction']} to {item['current_direction']}",
            }
        )
    for item in trend_history.get("persistent_warnings", [])[:6]:
        excerpts.append(
            {
                "source": "trend_history",
                "path": "demo/trend/trend_history.json",
                "ticker": item["ticker"],
                "excerpt": f"{item['warning']} across {item['period_count']} periods",
            }
        )
    for item in scenario_stress.get("ticker_stresses", [])[:6]:
        excerpts.append(
            {
                "source": "scenario_stress",
                "path": "demo/scenario/scenario_stress.json",
                "ticker": item["ticker"],
                "excerpt": f"stress score {item['stress_score']}; highest risk {item['highest_risk_level']}; flags {join_short(item.get('stress_flags', []), 2)}",
            }
        )
    for item in review_ledger.get("items", [])[:8]:
        excerpts.append(
            {
                "source": "review_ledger",
                "path": "demo/ledger/review_ledger.json",
                "ticker": item["ticker"],
                "excerpt": f"{item['issue_type']} status {item['status']}; severity {item['severity']}; next research step {item['next_action']}",
            }
        )
    return excerpts


def build_risk_flags(
    packet: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
    review_ledger: Dict[str, Any],
) -> List[Dict[str, Any]]:
    flags = []
    for item in packet.get("impacted_tickers", []):
        for warning in item.get("warnings", []):
            flags.append(flag(item["ticker"], "source_warning", "high", warning, "demo/impact_packet.json"))
    for item in trend_history.get("persistent_warnings", []):
        severity = "severe" if int(item.get("period_count", 0)) >= 3 else "high"
        flags.append(flag(item["ticker"], "persistent_warning", severity, item["warning"], "demo/trend/trend_history.json"))
    for item in scenario_stress.get("ticker_stresses", []):
        risk = str(item.get("highest_risk_level", ""))
        if risk in {"high", "severe"}:
            flags.append(
                flag(
                    item["ticker"],
                    "scenario_overlap",
                    risk,
                    f"stress score {item.get('stress_score')}; {join_short(item.get('stress_flags', []), 2)}",
                    "demo/scenario/scenario_stress.json",
                )
            )
    for item in review_ledger.get("items", []):
        if item.get("stale") or item.get("severity") in {"high", "severe"}:
            flags.append(
                flag(
                    item["ticker"],
                    "ledger_item",
                    item.get("severity", "medium"),
                    f"{item['issue_type']} is {item['status']}; stale {str(item.get('stale', False)).lower()}",
                    "demo/ledger/review_ledger.json",
                )
            )
    return flags[:24]


def flag(ticker: str, category: str, severity: str, description: str, path: str) -> Dict[str, str]:
    return {
        "ticker": ticker,
        "category": category,
        "severity": severity,
        "description": description,
        "evidence_path": path,
    }


def build_unresolved_assumptions(
    packet: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
    evidence_hub: Dict[str, Any],
) -> List[Dict[str, str]]:
    assumptions = []
    for item in packet.get("impacted_tickers", []):
        if item.get("warnings"):
            assumptions.append(
                {
                    "topic": f"{item['ticker']} source freshness",
                    "assumption": "Static source freshness is sufficient for a research meeting draft.",
                    "test": f"Refresh or annotate warnings: {join_short(item['warnings'], 2)}",
                    "owner": "",
                    "due_date": "",
                }
            )
    if trend_history.get("persistent_warnings"):
        assumptions.append(
            {
                "topic": "Persistent warning treatment",
                "assumption": "Repeated warnings can remain open until local evidence is updated.",
                "test": "Review persistent warning rows and record whether each remains valid.",
                "owner": "",
                "due_date": "",
            }
        )
    if scenario_stress.get("scenario_results"):
        assumptions.append(
            {
                "topic": "Scenario fixture scope",
                "assumption": "Illustrative stress fixtures are adequate prompts for the meeting agenda.",
                "test": "Confirm whether any missing sector or company stress case should be added locally.",
                "owner": "",
                "due_date": "",
            }
        )
    missing_boundaries = [
        item["path"]
        for item in evidence_hub.get("matrix", [])
        if item.get("boundary_coverage", {}).get("missing_count", 0)
    ]
    if missing_boundaries:
        assumptions.append(
            {
                "topic": "Boundary coverage",
                "assumption": "Every public artifact should carry explicit research boundaries.",
                "test": f"Inspect boundary coverage gaps: {', '.join(missing_boundaries[:4])}",
                "owner": "",
                "due_date": "",
            }
        )
    return assumptions[:12]


def build_review_decisions(
    tickers: List[str],
    review_ledger: Dict[str, Any],
    risk_flags: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    risk_by_ticker: Dict[str, List[Dict[str, str]]] = {}
    for item in risk_flags:
        risk_by_ticker.setdefault(item["ticker"], []).append(item)
    ledger_by_ticker: Dict[str, List[Dict[str, Any]]] = {}
    for item in review_ledger.get("items", []):
        ledger_by_ticker.setdefault(item["ticker"], []).append(item)

    decisions = []
    for ticker in tickers:
        decisions.append(
            {
                "ticker": ticker,
                "decision_placeholder": "research_decision_pending",
                "allowed_research_labels": [
                    "confirm_thesis_wording",
                    "request_source_refresh",
                    "defer_pending_local_evidence",
                    "close_issue_as_addressed",
                ],
                "meeting_note": "",
                "owner": "",
                "due_date": "",
                "linked_risk_flags": [item["category"] for item in risk_by_ticker.get(ticker, [])[:4]],
                "linked_ledger_items": [item["item_key"] for item in ledger_by_ticker.get(ticker, [])[:4]],
            }
        )
    return decisions


def build_follow_up_checklist(
    decisions: List[Dict[str, Any]],
    assumptions: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    checklist = [
        {
            "item": "Fill meeting date, facilitator, participants, and prepared-by fields.",
            "owner": "",
            "due_date": "",
            "done": False,
        },
        {
            "item": "Record one research-process label for each ticker decision placeholder.",
            "owner": "",
            "due_date": "",
            "done": False,
        },
        {
            "item": "Assign owners and dates for unresolved assumptions.",
            "owner": "",
            "due_date": "",
            "done": False,
        },
        {
            "item": "Confirm evidence excerpts cite local artifacts only.",
            "owner": "",
            "due_date": "",
            "done": False,
        },
        {
            "item": "Re-run validation after editing local inputs or generated artifacts.",
            "owner": "",
            "due_date": "",
            "done": False,
        },
    ]
    for decision in decisions[:6]:
        checklist.append(
            {
                "item": f"Complete research note for {decision['ticker']}.",
                "owner": "",
                "due_date": "",
                "done": False,
            }
        )
    if assumptions:
        checklist.append(
            {
                "item": "Resolve or explicitly defer each assumption listed in the meeting draft.",
                "owner": "",
                "due_date": "",
                "done": False,
            }
        )
    return checklist


def render_decision_journal_markdown(journal: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Decision Journal Draft",
        "",
        f"Generated: {journal['generated_at']}",
        f"Meeting type: {journal['meeting_type']}",
        "",
        journal["no_recommendation_statement"],
        "",
        "## Boundaries",
        "",
    ]
    lines.extend(f"- {item}" for item in journal["boundaries"])
    lines.extend(
        [
            "",
            "## Meeting Fields",
            "",
            f"- Meeting date: {journal['meeting_fields']['meeting_date']}",
            f"- Facilitator: {journal['meeting_fields']['facilitator']}",
            f"- Participants: {', '.join(journal['meeting_fields']['participants'])}",
            f"- Prepared by: {journal['meeting_fields']['prepared_by']}",
            "",
            "## Thesis Questions",
            "",
        ]
    )
    for item in journal["thesis_questions"]:
        lines.extend(
            [
                f"### {item['ticker']}",
                "",
                f"- Primary question: {item['primary_question']}",
                f"- Owner: {item['owner']}",
                f"- Due date: {item['due_date']}",
                "- Supporting questions:",
                *[f"  - {question}" for question in item["supporting_questions"]],
                "- Affected claims:",
                *[f"  - {claim}" for claim in item["affected_claims"] or ["none"]],
                "",
            ]
        )
    lines.extend(["## Evidence Excerpts", ""])
    for item in journal["evidence_excerpts"]:
        lines.append(f"- `{item['path']}` [{item['source']}] {item['ticker']}: {item['excerpt']}")
    lines.extend(["", "## Risk Flags", ""])
    for item in journal["risk_flags"]:
        lines.append(f"- {item['ticker']} {item['category']} ({item['severity']}): {item['description']} (`{item['evidence_path']}`)")
    lines.extend(["", "## Unresolved Assumptions", ""])
    for item in journal["unresolved_assumptions"]:
        lines.append(f"- {item['topic']}: {item['assumption']} Test: {item['test']} Owner: {item['owner']} Due: {item['due_date']}")
    lines.extend(["", "## Review Decisions", ""])
    for item in journal["review_decisions"]:
        lines.append(
            f"- {item['ticker']}: {item['decision_placeholder']}; labels {', '.join(item['allowed_research_labels'])}; "
            f"owner `{item['owner']}`; due `{item['due_date']}`; note `{item['meeting_note']}`"
        )
    lines.extend(["", "## Follow-Up Checklist", ""])
    for item in journal["follow_up_checklist"]:
        marker = "x" if item["done"] else " "
        lines.append(f"- [{marker}] {item['item']} Owner: {item['owner']} Due: {item['due_date']}")
    lines.append("")
    return "\n".join(lines)


def render_decision_journal_html(journal: Dict[str, Any]) -> str:
    boundaries = "".join(f"<li>{esc(item)}</li>" for item in journal["boundaries"])
    question_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{esc(item['primary_question'])}</td>"
        f"<td>{esc('; '.join(item['supporting_questions']))}</td>"
        f"<td>{esc('; '.join(item['affected_claims']) or 'none')}</td>"
        f"<td>{esc(item['owner'])}</td>"
        f"<td>{esc(item['due_date'])}</td>"
        "</tr>"
        for item in journal["thesis_questions"]
    )
    evidence_rows = "".join(
        "<tr>"
        f"<td><code>{esc(item['path'])}</code></td>"
        f"<td>{esc(item['source'])}</td>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{esc(item['excerpt'])}</td>"
        "</tr>"
        for item in journal["evidence_excerpts"]
    )
    risk_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{esc(item['category'])}</td>"
        f"<td>{esc(item['severity'])}</td>"
        f"<td>{esc(item['description'])}</td>"
        f"<td><code>{esc(item['evidence_path'])}</code></td>"
        "</tr>"
        for item in journal["risk_flags"]
    )
    assumption_rows = "".join(
        "<tr>"
        f"<td>{esc(item['topic'])}</td>"
        f"<td>{esc(item['assumption'])}</td>"
        f"<td>{esc(item['test'])}</td>"
        f"<td>{esc(item['owner'])}</td>"
        f"<td>{esc(item['due_date'])}</td>"
        "</tr>"
        for item in journal["unresolved_assumptions"]
    )
    decision_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{esc(item['decision_placeholder'])}</td>"
        f"<td>{esc(', '.join(item['allowed_research_labels']))}</td>"
        f"<td>{esc(item['owner'])}</td>"
        f"<td>{esc(item['due_date'])}</td>"
        f"<td>{esc(item['meeting_note'])}</td>"
        f"<td>{esc(', '.join(item['linked_ledger_items']) or 'none')}</td>"
        "</tr>"
        for item in journal["review_decisions"]
    )
    checklist = "".join(
        f"<li>{esc(item['item'])} Owner: {esc(item['owner'])} Due: {esc(item['due_date'])}</li>"
        for item in journal["follow_up_checklist"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Decision Journal Draft</title>
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
  </style>
</head>
<body>
<main>
  <h1>Decision Journal Draft</h1>
  <p>Generated {esc(journal['generated_at'])}. {esc(journal['no_recommendation_statement'])}</p>
  <section class="note"><h2>Boundaries</h2><ul>{boundaries}</ul></section>
  <section class="note"><h2>Meeting Fields</h2><p>Meeting date: {esc(journal['meeting_fields']['meeting_date'])}; facilitator: {esc(journal['meeting_fields']['facilitator'])}; prepared by: {esc(journal['meeting_fields']['prepared_by'])}.</p></section>
  <h2>Thesis Questions</h2>
  <table><thead><tr><th>Ticker</th><th>Primary question</th><th>Supporting questions</th><th>Affected claims</th><th>Owner</th><th>Due date</th></tr></thead><tbody>{question_rows}</tbody></table>
  <h2>Evidence Excerpts</h2>
  <table><thead><tr><th>Path</th><th>Source</th><th>Ticker</th><th>Excerpt</th></tr></thead><tbody>{evidence_rows}</tbody></table>
  <h2>Risk Flags</h2>
  <table><thead><tr><th>Ticker</th><th>Category</th><th>Severity</th><th>Description</th><th>Evidence</th></tr></thead><tbody>{risk_rows}</tbody></table>
  <h2>Unresolved Assumptions</h2>
  <table><thead><tr><th>Topic</th><th>Assumption</th><th>Test</th><th>Owner</th><th>Due date</th></tr></thead><tbody>{assumption_rows}</tbody></table>
  <h2>Review Decisions</h2>
  <table><thead><tr><th>Ticker</th><th>Placeholder</th><th>Labels</th><th>Owner</th><th>Due date</th><th>Meeting note</th><th>Ledger links</th></tr></thead><tbody>{decision_rows}</tbody></table>
  <h2>Follow-Up Checklist</h2>
  <ul>{checklist}</ul>
</main>
</body>
</html>
"""


def assert_no_forbidden_terms(value: Any) -> None:
    text = flatten_text(value).lower()
    found = [term for term in JOURNAL_FORBIDDEN_TERMS if term in text.split()]
    if found:
        raise ValueError("decision journal contains disallowed recommendation language: " + ", ".join(found))


def flatten_text(value: Any) -> str:
    if isinstance(value, dict):
        return " ".join(flatten_text(item) for item in value.values())
    if isinstance(value, list):
        return " ".join(flatten_text(item) for item in value)
    return str(value)


def unique_limited(values: Iterable[str], limit: int) -> List[str]:
    result = []
    for value in values:
        text = str(value)
        if text and text not in result:
            result.append(text)
        if len(result) >= limit:
            break
    return result


def join_short(values: Iterable[str], limit: int) -> str:
    items = unique_limited(values, limit)
    return "; ".join(items) if items else "none"
