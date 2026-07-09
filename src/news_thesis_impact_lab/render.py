from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_packet_markdown(packet: Dict[str, Any]) -> str:
    lines = [
        "# News Thesis Impact Packet",
        "",
        f"Generated: {packet['generated_at']}",
        f"Freshness reference date: {packet['freshness_reference_date']}",
        "",
        "## Boundaries",
        "",
        *bullet(packet["boundaries"]),
        "",
        "## Impacted Tickers",
        "",
    ]
    for item in packet["impacted_tickers"]:
        lines.extend(
            [
                f"### {item['ticker']}",
                "",
                f"- Attention score: {item['attention_score']}",
                f"- Direction: {item['direction']}",
                f"- Confidence: {item['confidence']}",
                f"- Exposure: {item['exposure_weight']:.2%} ({item['position_label']})",
                f"- Events: {', '.join(item['event_ids']) or 'none'}",
                f"- Themes: {', '.join(item['themes']) or 'none'}",
                "",
                "Affected thesis claims:",
                *bullet(item["affected_thesis_claims"] or ["No thesis claim matched."]),
                "",
                "Next review prompts:",
                *bullet(item["next_review_prompts"]),
                "",
                "Warnings:",
                *bullet(item["warnings"] or ["None."]),
                "",
            ]
        )
    lines.extend(["## Review Queue", ""])
    for queue_item in packet["review_queue"]:
        lines.append(f"- {queue_item['ticker']} ({queue_item['attention_score']}): {queue_item['prompt']}")
    lines.append("")
    return "\n".join(lines)


def render_packet_html(packet: Dict[str, Any]) -> str:
    rows = []
    for item in packet["impacted_tickers"]:
        rows.append(
            "<tr>"
            f"<td>{esc(item['ticker'])}</td>"
            f"<td>{item['attention_score']}</td>"
            f"<td>{esc(item['direction'])}</td>"
            f"<td>{esc(item['confidence'])}</td>"
            f"<td>{item['exposure_weight']:.2%}</td>"
            f"<td>{esc('; '.join(item['next_review_prompts']))}</td>"
            f"<td>{esc('; '.join(item['warnings']) or 'None')}</td>"
            "</tr>"
        )
    boundaries = "".join(f"<li>{esc(item)}</li>" for item in packet["boundaries"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>News Thesis Impact Packet</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1120px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    table {{ border-collapse: collapse; width: 100%; background: white; }}
    th, td {{ border: 1px solid #d8dee8; padding: 0.65rem; vertical-align: top; text-align: left; }}
    th {{ background: #e9eef5; }}
    .note {{ background: #fff; border: 1px solid #d8dee8; padding: 1rem; margin: 1rem 0; }}
  </style>
</head>
<body>
<main>
  <h1>News Thesis Impact Packet</h1>
  <p>Generated {esc(packet['generated_at'])}; source freshness reference {esc(packet['freshness_reference_date'])}.</p>
  <section class="note"><h2>Boundaries</h2><ul>{boundaries}</ul></section>
  <table>
    <thead><tr><th>Ticker</th><th>Score</th><th>Direction</th><th>Confidence</th><th>Exposure</th><th>Review prompts</th><th>Warnings</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</main>
</body>
</html>
"""


def render_compare_markdown(compare: Dict[str, Any]) -> str:
    lines = [
        "# Impact Packet Compare",
        "",
        f"Generated: {compare['generated_at']}",
        "",
        "## Boundaries",
        "",
        *bullet(compare["boundaries"]),
        "",
        "## Deltas",
        "",
    ]
    for item in compare["deltas"]:
        lines.append(
            f"- {item['ticker']}: {item['status']}; score delta {item['attention_score_delta']}; "
            f"direction {item['previous_direction']} -> {item['current_direction']}; "
            f"exposure {item['previous_exposure_weight']:.2%} -> {item['current_exposure_weight']:.2%}"
        )
    lines.append("")
    return "\n".join(lines)


def render_trend_history_markdown(history: Dict[str, Any]) -> str:
    lines = [
        "# Trend History",
        "",
        f"Generated: {history['generated_at']}",
        f"Periods: {history['history_period_count']}",
        "",
        "## Boundaries",
        "",
        *bullet(history["boundaries"]),
        "",
        "## Snapshots",
        "",
    ]
    for snapshot in history["snapshots"]:
        lines.append(
            f"- {snapshot['generated_at']} `{snapshot['name']}`: {snapshot['impacted_ticker_count']} impacted tickers"
        )
    lines.extend(["", "## Ticker Trends", ""])
    for item in history["ticker_histories"]:
        lines.append(
            f"- {item['ticker']}: latest {item['latest_attention_score']} ({item['latest_status']}); "
            f"score {item['score_trend']} ({item['score_delta_from_first_seen']:+}); "
            f"direction {item['latest_direction']}; exposure {item['exposure_trend']} "
            f"({item['exposure_delta_from_first_seen']:+.2%})"
        )
    lines.extend(["", "## Persistent Warnings", ""])
    if history["persistent_warnings"]:
        for warning in history["persistent_warnings"]:
            lines.append(
                f"- {warning['ticker']}: {warning['warning']} "
                f"({warning['period_count']} periods: {', '.join(warning['snapshots'])})"
            )
    else:
        lines.append("- None.")
    lines.extend(["", "## Next Review Queue", ""])
    if history["next_review_queue"]:
        for item in history["next_review_queue"]:
            lines.append(
                f"- {item['ticker']} ({item['latest_attention_score']}, {item['latest_status']}, "
                f"{item['score_trend']}): {item['prompt']}"
            )
    else:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def render_trend_history_html(history: Dict[str, Any]) -> str:
    boundaries = "".join(f"<li>{esc(item)}</li>" for item in history["boundaries"])
    snapshot_rows = "".join(
        "<tr>"
        f"<td>{esc(snapshot['generated_at'])}</td>"
        f"<td>{esc(snapshot['name'])}</td>"
        f"<td>{snapshot['impacted_ticker_count']}</td>"
        "</tr>"
        for snapshot in history["snapshots"]
    )
    trend_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{item['latest_attention_score']}</td>"
        f"<td>{esc(item['latest_status'])}</td>"
        f"<td>{esc(item['score_trend'])} ({item['score_delta_from_first_seen']:+})</td>"
        f"<td>{esc(item['latest_direction'])}</td>"
        f"<td>{esc(item['exposure_trend'])} ({item['exposure_delta_from_first_seen']:+.2%})</td>"
        f"<td>{len(item['persistent_warnings'])}</td>"
        "</tr>"
        for item in history["ticker_histories"]
    )
    queue_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{item['latest_attention_score']}</td>"
        f"<td>{esc(item['latest_status'])}</td>"
        f"<td>{esc(item['score_trend'])}</td>"
        f"<td>{esc(item['exposure_trend'])}</td>"
        f"<td>{item['persistent_warning_count']}</td>"
        f"<td>{esc(item['prompt'])}</td>"
        "</tr>"
        for item in history["next_review_queue"]
    )
    warnings = "".join(
        f"<li><strong>{esc(item['ticker'])}</strong>: {esc(item['warning'])} "
        f"({item['period_count']} periods: {esc(', '.join(item['snapshots']))})</li>"
        for item in history["persistent_warnings"]
    ) or "<li>None.</li>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Trend History</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1160px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 1.75rem; }}
    table {{ border-collapse: collapse; width: 100%; background: white; margin: 0.75rem 0 1.25rem; }}
    th, td {{ border: 1px solid #d8dee8; padding: 0.65rem; vertical-align: top; text-align: left; }}
    th {{ background: #e9eef5; }}
    .note {{ background: #fff; border: 1px solid #d8dee8; padding: 1rem; margin: 1rem 0; }}
  </style>
</head>
<body>
<main>
  <h1>Trend History</h1>
  <p>Generated {esc(history['generated_at'])}; {history['history_period_count']} packet periods.</p>
  <section class="note"><h2>Boundaries</h2><ul>{boundaries}</ul></section>
  <h2>Snapshots</h2>
  <table><thead><tr><th>Generated</th><th>Name</th><th>Impacted tickers</th></tr></thead><tbody>{snapshot_rows}</tbody></table>
  <h2>Ticker Trends</h2>
  <table><thead><tr><th>Ticker</th><th>Latest score</th><th>Status</th><th>Score trend</th><th>Direction</th><th>Exposure trend</th><th>Persistent warnings</th></tr></thead><tbody>{trend_rows}</tbody></table>
  <h2>Persistent Warnings</h2>
  <ul>{warnings}</ul>
  <h2>Next Review Queue</h2>
  <table><thead><tr><th>Ticker</th><th>Score</th><th>Status</th><th>Score trend</th><th>Exposure trend</th><th>Persistent warnings</th><th>Prompt</th></tr></thead><tbody>{queue_rows}</tbody></table>
</main>
</body>
</html>
"""


def render_scenario_stress_markdown(stress: Dict[str, Any]) -> str:
    lines = [
        "# Scenario Stress Review",
        "",
        f"Generated: {stress['generated_at']}",
        f"Source packet generated: {stress['source_packet_generated_at']}",
        f"Scenarios: {stress['scenario_count']}",
        "",
        "## Boundaries",
        "",
        *bullet(stress["boundaries"]),
        "",
        "## Scenario Coverage",
        "",
    ]
    for scenario in stress["scenario_results"]:
        lines.append(
            f"- {scenario['name']} (`{scenario['scenario_id']}`): {scenario['highest_risk_level']} risk; "
            f"{len(scenario['matched_tickers'])} matched tickers ({', '.join(scenario['matched_tickers']) or 'none'})"
        )
    lines.extend(["", "## Ticker Stress Flags", ""])
    for item in stress["ticker_stresses"]:
        lines.extend(
            [
                f"### {item['ticker']}",
                "",
                f"- Stress score: {item['stress_score']}",
                f"- Highest risk: {item['highest_risk_level']}",
                f"- Current packet read: {item['current_direction']} / {item['current_confidence']}",
                f"- Exposure: {item['exposure_weight']:.2%}",
                f"- Confidence downgrade suggestion: {item['confidence_downgrade_suggestion']['from']} -> {item['confidence_downgrade_suggestion']['to']} ({item['confidence_downgrade_suggestion']['reason']})",
                "",
                "Stress flags:",
                *bullet(item["stress_flags"]),
                "",
                "Exposure overlap:",
                *bullet(
                    [
                        f"Direct ticker scenarios: {', '.join(item['exposure_overlap']['direct_ticker_scenarios']) or 'none'}",
                        f"Matched tags: {', '.join(item['exposure_overlap']['matched_tags']) or 'none'}",
                        f"Risk levels: {', '.join(item['exposure_overlap']['risk_levels']) or 'none'}",
                    ]
                ),
                "",
                "Thesis contradiction prompts:",
                *bullet(item["thesis_contradiction_prompts"]),
                "",
            ]
        )
    lines.extend(["## Next Review Queue", ""])
    for item in stress["next_review_queue"]:
        lines.append(f"- {item['ticker']} ({item['stress_score']}, {item['highest_risk_level']}): {item['prompt']}")
    if not stress["next_review_queue"]:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def render_scenario_stress_html(stress: Dict[str, Any]) -> str:
    boundaries = "".join(f"<li>{esc(item)}</li>" for item in stress["boundaries"])
    scenario_rows = "".join(
        "<tr>"
        f"<td>{esc(item['name'])}</td>"
        f"<td>{esc(item['scenario_id'])}</td>"
        f"<td>{esc(item['highest_risk_level'])}</td>"
        f"<td>{item['shock_count']}</td>"
        f"<td>{esc(', '.join(item['matched_tickers']) or 'none')}</td>"
        "</tr>"
        for item in stress["scenario_results"]
    )
    ticker_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{item['stress_score']}</td>"
        f"<td>{esc(item['highest_risk_level'])}</td>"
        f"<td>{item['exposure_weight']:.2%}</td>"
        f"<td>{esc('; '.join(item['stress_flags']))}</td>"
        f"<td>{esc('; '.join(item['thesis_contradiction_prompts']))}</td>"
        f"<td>{esc(item['confidence_downgrade_suggestion']['from'])} -> {esc(item['confidence_downgrade_suggestion']['to'])}</td>"
        "</tr>"
        for item in stress["ticker_stresses"]
    )
    queue_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{item['stress_score']}</td>"
        f"<td>{esc(item['highest_risk_level'])}</td>"
        f"<td>{esc(item['prompt'])}</td>"
        "</tr>"
        for item in stress["next_review_queue"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scenario Stress Review</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1180px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 1.75rem; }}
    table {{ border-collapse: collapse; width: 100%; background: white; margin: 0.75rem 0 1.25rem; }}
    th, td {{ border: 1px solid #d8dee8; padding: 0.65rem; vertical-align: top; text-align: left; }}
    th {{ background: #e9eef5; }}
    .note {{ background: #fff; border: 1px solid #d8dee8; padding: 1rem; margin: 1rem 0; }}
  </style>
</head>
<body>
<main>
  <h1>Scenario Stress Review</h1>
  <p>Generated {esc(stress['generated_at'])}; source packet generated {esc(stress['source_packet_generated_at'])}; {stress['scenario_count']} illustrative scenarios.</p>
  <section class="note"><h2>Boundaries</h2><ul>{boundaries}</ul></section>
  <h2>Scenario Coverage</h2>
  <table><thead><tr><th>Scenario</th><th>ID</th><th>Highest risk</th><th>Shocks</th><th>Matched tickers</th></tr></thead><tbody>{scenario_rows}</tbody></table>
  <h2>Ticker Stress Flags</h2>
  <table><thead><tr><th>Ticker</th><th>Stress score</th><th>Risk</th><th>Exposure</th><th>Flags</th><th>Contradiction prompts</th><th>Confidence suggestion</th></tr></thead><tbody>{ticker_rows}</tbody></table>
  <h2>Next Review Queue</h2>
  <table><thead><tr><th>Ticker</th><th>Stress score</th><th>Risk</th><th>Prompt</th></tr></thead><tbody>{queue_rows}</tbody></table>
</main>
</body>
</html>
"""


def render_review_ledger_markdown(ledger: Dict[str, Any]) -> str:
    lines = [
        "# Review Ledger",
        "",
        f"Generated: {ledger['generated_at']}",
        f"Source packet generated: {ledger['source_packet_generated_at']}",
        f"Source trend generated: {ledger['source_trend_generated_at']}",
        f"Source scenario generated: {ledger['source_scenario_generated_at']}",
        "",
        "## Boundaries",
        "",
        *bullet(ledger["boundaries"]),
        "",
        "## Summary",
        "",
        f"- Total items: {ledger['summary']['total_items']}",
        f"- By status: {format_counts(ledger['summary']['by_status'])}",
        f"- By severity: {format_counts(ledger['summary']['by_severity'])}",
        f"- Stale items: {', '.join(ledger['summary']['stale_items']) or 'none'}",
        "",
        "## Ticker Summary",
        "",
        "| Ticker | Total | Status | Severity |",
        "| --- | ---: | --- | --- |",
    ]
    for ticker, summary in ledger["summary"]["by_ticker"].items():
        lines.append(
            f"| {ticker} | {summary['total']} | {format_counts(summary['by_status'])} | "
            f"{format_counts(summary['by_severity'])} |"
        )
    lines.extend(["", "## Review Items", ""])
    for item in ledger["items"]:
        lines.extend(
            [
                f"### {item['ticker']} - {item['issue_type']} - {item['source']}",
                "",
                f"- Key: `{item['item_key']}`",
                f"- Status: {item['status']}",
                f"- Severity: {item['severity']}",
                f"- First seen: {item['first_seen']}",
                f"- Latest seen: {item['latest_seen']}",
                f"- Resolved at: {item['resolved_at'] or 'not resolved'}",
                f"- Expiry days: {item['expiry_days']}",
                f"- Stale: {str(item['stale']).lower()}",
                f"- Next action: {item['next_action']}",
                "",
                "Evidence links:",
            ]
        )
        for evidence in item["evidence_links"]:
            lines.append(f"- `{evidence['path']}` [{evidence['source']}]: {evidence['label']}")
        lines.append("")
    return "\n".join(lines)


def render_review_ledger_html(ledger: Dict[str, Any]) -> str:
    boundaries = "".join(f"<li>{esc(item)}</li>" for item in ledger["boundaries"])
    ticker_rows = "".join(
        "<tr>"
        f"<td>{esc(ticker)}</td>"
        f"<td>{summary['total']}</td>"
        f"<td>{esc(format_counts(summary['by_status']))}</td>"
        f"<td>{esc(format_counts(summary['by_severity']))}</td>"
        "</tr>"
        for ticker, summary in ledger["summary"]["by_ticker"].items()
    )
    item_rows = "".join(
        "<tr>"
        f"<td>{esc(item['ticker'])}</td>"
        f"<td>{esc(item['issue_type'])}</td>"
        f"<td>{esc(item['source'])}</td>"
        f"<td>{esc(item['status'])}</td>"
        f"<td>{esc(item['severity'])}</td>"
        f"<td>{esc(item['first_seen'])}</td>"
        f"<td>{esc(item['latest_seen'])}</td>"
        f"<td>{esc(item['resolved_at'] or 'not resolved')}</td>"
        f"<td>{item['expiry_days']}</td>"
        f"<td>{str(item['stale']).lower()}</td>"
        f"<td>{esc(item['next_action'])}</td>"
        f"<td>{esc('; '.join(evidence['path'] + ' [' + evidence['source'] + ']: ' + evidence['label'] for evidence in item['evidence_links']))}</td>"
        "</tr>"
        for item in ledger["items"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Review Ledger</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1240px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 1.75rem; }}
    table {{ border-collapse: collapse; width: 100%; background: white; margin: 0.75rem 0 1.25rem; }}
    th, td {{ border: 1px solid #d8dee8; padding: 0.65rem; vertical-align: top; text-align: left; }}
    th {{ background: #e9eef5; }}
    .note {{ background: #fff; border: 1px solid #d8dee8; padding: 1rem; margin: 1rem 0; }}
  </style>
</head>
<body>
<main>
  <h1>Review Ledger</h1>
  <p>Generated {esc(ledger['generated_at'])}; tracks repeated static research review items from packet, trend, and scenario artifacts.</p>
  <section class="note"><h2>Boundaries</h2><ul>{boundaries}</ul></section>
  <section class="note"><h2>Summary</h2><p>Total items: {ledger['summary']['total_items']}; status: {esc(format_counts(ledger['summary']['by_status']))}; severity: {esc(format_counts(ledger['summary']['by_severity']))}; stale: {esc(', '.join(ledger['summary']['stale_items']) or 'none')}.</p></section>
  <h2>Ticker Summary</h2>
  <table><thead><tr><th>Ticker</th><th>Total</th><th>Status</th><th>Severity</th></tr></thead><tbody>{ticker_rows}</tbody></table>
  <h2>Review Items</h2>
  <table><thead><tr><th>Ticker</th><th>Issue type</th><th>Source</th><th>Status</th><th>Severity</th><th>First seen</th><th>Latest seen</th><th>Resolved at</th><th>Expiry days</th><th>Stale</th><th>Next action</th><th>Evidence</th></tr></thead><tbody>{item_rows}</tbody></table>
</main>
</body>
</html>
"""


def format_counts(counts: Dict[str, int]) -> str:
    return ", ".join(f"{name}: {count}" for name, count in counts.items()) or "none"


def bullet(items: Iterable[str]) -> List[str]:
    return [f"- {item}" for item in items]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)
