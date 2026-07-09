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


def bullet(items: Iterable[str]) -> List[str]:
    return [f"- {item}" for item in items]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)

