from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterable, List

from .model import BOUNDARIES, unique_sorted


SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3, "severe": 4}
EXPIRY_DAYS = {"low": 30, "medium": 21, "high": 14, "severe": 7}


def build_review_ledger(
    packet: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
    previous_ledger: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    generated_at = str(packet.get("generated_at") or trend_history.get("generated_at") or scenario_stress.get("generated_at") or "")
    current_items = {item["item_key"]: item for item in current_review_items(packet, trend_history, scenario_stress, generated_at)}
    previous_items = {item["item_key"]: item for item in (previous_ledger or {}).get("items", [])}

    merged = []
    for key in sorted(set(current_items) | set(previous_items)):
        current = current_items.get(key)
        previous = previous_items.get(key)
        if current:
            merged.append(merge_active_item(current, previous, generated_at))
        elif previous:
            merged.append(resolve_previous_item(previous, generated_at))

    merged.sort(key=lambda item: (-SEVERITY_RANK[item["severity"]], item["ticker"], item["issue_type"], item["source"]))
    return {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "source_packet_generated_at": packet.get("generated_at", "unknown"),
        "source_trend_generated_at": trend_history.get("generated_at", "unknown"),
        "source_scenario_generated_at": scenario_stress.get("generated_at", "unknown"),
        "boundaries": BOUNDARIES,
        "summary": compact_summary(merged),
        "items": merged,
    }


def current_review_items(
    packet: Dict[str, Any],
    trend_history: Dict[str, Any],
    scenario_stress: Dict[str, Any],
    generated_at: str,
) -> List[Dict[str, Any]]:
    items = []
    items.extend(packet_warning_items(packet, generated_at))
    items.extend(packet_review_items(packet, generated_at))
    items.extend(trend_items(trend_history, generated_at))
    items.extend(scenario_items(scenario_stress, generated_at))
    return collapse_items(items)


def packet_warning_items(packet: Dict[str, Any], generated_at: str) -> List[Dict[str, Any]]:
    items = []
    for ticker_item in packet.get("impacted_tickers", []):
        ticker = str(ticker_item["ticker"])
        for warning in ticker_item.get("warnings", []):
            source = warning_source(warning)
            items.append(
                base_item(
                    ticker=ticker,
                    issue_type="packet_warning",
                    source=source,
                    severity="high",
                    generated_at=generated_at,
                    evidence=[{"label": warning, "path": "demo/impact_packet.json", "source": source}],
                    next_action=f"Refresh or document the static source behind {source} before relying on this review packet.",
                )
            )
    return items


def packet_review_items(packet: Dict[str, Any], generated_at: str) -> List[Dict[str, Any]]:
    items = []
    for queue_item in packet.get("review_queue", []):
        ticker = str(queue_item["ticker"])
        score = int(queue_item.get("attention_score", 0))
        if score < 60:
            continue
        items.append(
            base_item(
                ticker=ticker,
                issue_type="attention_review",
                source="impact_packet_review_queue",
                severity="high" if score >= 65 else "medium",
                generated_at=generated_at,
                evidence=[
                    {
                        "label": f"attention score {score}: {queue_item.get('prompt', '')}",
                        "path": "demo/impact_packet.json",
                        "source": "review_queue",
                    }
                ],
                next_action=f"Re-read the current {ticker} thesis claims and record whether the static catalyst changes the research note.",
            )
        )
    return items


def trend_items(trend_history: Dict[str, Any], generated_at: str) -> List[Dict[str, Any]]:
    items = []
    for warning in trend_history.get("persistent_warnings", []):
        ticker = str(warning["ticker"])
        source = warning_source(warning["warning"])
        items.append(
            base_item(
                ticker=ticker,
                issue_type="persistent_warning",
                source=source,
                severity="severe" if int(warning.get("period_count", 0)) >= 3 else "high",
                generated_at=generated_at,
                evidence=[
                    {
                        "label": f"{warning['warning']} across {warning.get('period_count', 0)} periods",
                        "path": "demo/trend/trend_history.json",
                        "source": ", ".join(warning.get("snapshots", [])),
                    }
                ],
                next_action=f"Resolve the repeated {ticker} warning with updated local evidence or mark why it remains valid.",
            )
        )
    for item in trend_history.get("next_review_queue", []):
        status = str(item.get("latest_status", ""))
        if status not in {"new", "changed"}:
            continue
        ticker = str(item["ticker"])
        items.append(
            base_item(
                ticker=ticker,
                issue_type="trend_change",
                source=status,
                severity="medium",
                generated_at=generated_at,
                evidence=[
                    {
                        "label": f"{status}; score {item.get('score_trend')}; exposure {item.get('exposure_trend')}",
                        "path": "demo/trend/trend_history.json",
                        "source": "next_review_queue",
                    }
                ],
                next_action=f"Compare the latest {ticker} packet against prior periods and update the research note if the change is material.",
            )
        )
    return items


def scenario_items(scenario_stress: Dict[str, Any], generated_at: str) -> List[Dict[str, Any]]:
    items = []
    for item in scenario_stress.get("ticker_stresses", []):
        ticker = str(item["ticker"])
        risk = str(item.get("highest_risk_level", "medium"))
        if risk not in {"high", "severe"} and int(item.get("stress_score", 0)) < 70:
            continue
        sources = item.get("exposure_overlap", {}).get("direct_ticker_scenarios", []) or [
            shock.get("scenario_id", "scenario_overlap") for shock in item.get("matched_shocks", [])[:1]
        ]
        for source in sorted(set(sources)):
            items.append(
                base_item(
                    ticker=ticker,
                    issue_type="scenario_stress",
                    source=str(source),
                    severity="severe" if risk == "severe" else "high",
                    generated_at=generated_at,
                    evidence=[
                        {
                            "label": f"{risk} risk; stress score {item.get('stress_score')}: {item.get('thesis_contradiction_prompts', [''])[0]}",
                            "path": "demo/scenario/scenario_stress.json",
                            "source": str(source),
                        }
                    ],
                    next_action=f"Document whether the {ticker} thesis still holds under the static {source} stress case.",
                )
            )
    return items


def base_item(
    ticker: str,
    issue_type: str,
    source: str,
    severity: str,
    generated_at: str,
    evidence: List[Dict[str, str]],
    next_action: str,
) -> Dict[str, Any]:
    key = item_key(ticker, issue_type, source)
    expiry_days = EXPIRY_DAYS[severity]
    return {
        "item_key": key,
        "ticker": ticker,
        "issue_type": issue_type,
        "source": source,
        "status": "new",
        "severity": severity,
        "first_seen": generated_at,
        "latest_seen": generated_at,
        "resolved_at": None,
        "evidence_links": evidence,
        "next_action": next_action,
        "expiry_days": expiry_days,
        "stale": False,
    }


def merge_active_item(current: Dict[str, Any], previous: Dict[str, Any] | None, generated_at: str) -> Dict[str, Any]:
    if not previous:
        status = "new"
        first_seen = current["first_seen"]
    else:
        previous_status = previous.get("status", "open")
        status = "watch" if previous_status == "watch" else "open"
        first_seen = previous.get("first_seen") or current["first_seen"]
    item = {**current, "status": status, "first_seen": first_seen, "latest_seen": generated_at, "resolved_at": None}
    item["stale"] = is_stale(item, generated_at)
    return item


def resolve_previous_item(previous: Dict[str, Any], generated_at: str) -> Dict[str, Any]:
    status = str(previous.get("status", "open"))
    item = dict(previous)
    if status != "resolved":
        item["status"] = "resolved"
        item["resolved_at"] = generated_at
        item["next_action"] = "Keep prior evidence for audit trail; no current packet, trend, or scenario evidence matched this issue."
    item["stale"] = False
    return item


def collapse_items(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    collapsed: Dict[str, Dict[str, Any]] = {}
    for item in items:
        existing = collapsed.get(item["item_key"])
        if not existing:
            collapsed[item["item_key"]] = item
            continue
        existing["severity"] = max([existing["severity"], item["severity"]], key=lambda severity: SEVERITY_RANK[severity])
        existing["expiry_days"] = EXPIRY_DAYS[existing["severity"]]
        existing["evidence_links"] = sorted(
            existing["evidence_links"] + item["evidence_links"],
            key=lambda evidence: (evidence["path"], evidence["source"], evidence["label"]),
        )
    return list(collapsed.values())


def compact_summary(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "total_items": len(items),
        "by_status": count_by(items, "status"),
        "by_severity": count_by(items, "severity"),
        "by_ticker": {
            ticker: {
                "total": len(ticker_items),
                "by_status": count_by(ticker_items, "status"),
                "by_severity": count_by(ticker_items, "severity"),
            }
            for ticker, ticker_items in grouped_by_ticker(items).items()
        },
        "stale_items": [item["item_key"] for item in items if item["stale"]],
        "open_item_keys": [item["item_key"] for item in items if item["status"] in {"new", "open", "watch"}],
    }


def grouped_by_ticker(items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in items:
        grouped.setdefault(item["ticker"], []).append(item)
    return dict(sorted(grouped.items()))


def count_by(items: Iterable[Dict[str, Any]], field: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for item in items:
        value = str(item[field])
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def item_key(ticker: str, issue_type: str, source: str) -> str:
    return "|".join([ticker.upper(), issue_type, source])


def warning_source(warning: str) -> str:
    return str(warning).split(":", 1)[0]


def is_stale(item: Dict[str, Any], generated_at: str) -> bool:
    if item.get("status") == "resolved":
        return False
    try:
        age = (date.fromisoformat(generated_at) - date.fromisoformat(str(item["first_seen"]))).days
    except ValueError:
        return False
    return age >= int(item.get("expiry_days", 0))


def referenced_tickers(items: Iterable[Dict[str, Any]]) -> List[str]:
    return unique_sorted(item["ticker"] for item in items)
