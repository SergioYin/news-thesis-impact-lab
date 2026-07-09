from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

from .model import BOUNDARIES


def load_packet_records(paths: Iterable[Path], read_json) -> List[Dict[str, Any]]:
    records = []
    for path in paths:
        packet = read_json(path)
        records.append({"name": path.stem, "path": path.as_posix(), "packet": packet})
    return records


def build_trend_history(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    snapshots = sorted(records, key=lambda record: (record["packet"].get("generated_at", ""), record["name"]))
    if len(snapshots) < 2:
        raise ValueError("trend-history requires at least two packet files")

    normalized_snapshots = [
        {
            "name": record["name"],
            "path": record["path"],
            "generated_at": record["packet"].get("generated_at", ""),
            "impacted_ticker_count": len(record["packet"].get("impacted_tickers", [])),
        }
        for record in snapshots
    ]
    ticker_histories = [ticker_history(ticker, snapshots) for ticker in all_tickers(snapshots)]
    latest_generated_at = normalized_snapshots[-1]["generated_at"]
    return {
        "schema_version": "1.0",
        "generated_at": latest_generated_at,
        "history_period_count": len(snapshots),
        "boundaries": BOUNDARIES,
        "snapshots": normalized_snapshots,
        "ticker_histories": sorted(ticker_histories, key=lambda item: (-item["latest_attention_score"], item["ticker"])),
        "persistent_warnings": persistent_warning_records(ticker_histories),
        "next_review_queue": next_review_queue(ticker_histories),
    }


def all_tickers(snapshots: List[Dict[str, Any]]) -> List[str]:
    tickers = {
        item["ticker"]
        for snapshot in snapshots
        for item in snapshot["packet"].get("impacted_tickers", [])
        if item.get("ticker")
    }
    return sorted(tickers)


def ticker_history(ticker: str, snapshots: List[Dict[str, Any]]) -> Dict[str, Any]:
    timeline = []
    previous_item: Dict[str, Any] | None = None
    previous_present = False
    for snapshot in snapshots:
        packet_item = ticker_item(snapshot["packet"], ticker)
        present = packet_item is not None
        score = int((packet_item or {}).get("attention_score", 0))
        exposure = float((packet_item or {}).get("exposure_weight", 0.0))
        warnings = list((packet_item or {}).get("warnings", []))
        timeline.append(
            {
                "snapshot": snapshot["name"],
                "generated_at": snapshot["packet"].get("generated_at", ""),
                "present": present,
                "attention_score": score,
                "score_direction": score_direction(previous_item, packet_item),
                "status": transition_status(previous_item, packet_item, previous_present, present),
                "direction": (packet_item or {}).get("direction", "absent"),
                "exposure_weight": exposure,
                "warnings": warnings,
                "warning_count": len(warnings),
            }
        )
        previous_item = packet_item
        previous_present = present

    present_points = [point for point in timeline if point["present"]]
    latest_item = ticker_item(snapshots[-1]["packet"], ticker)
    first_present = present_points[0] if present_points else timeline[0]
    latest_present = present_points[-1] if present_points else timeline[-1]
    latest_point = timeline[-1]
    score_delta = latest_point["attention_score"] - first_present["attention_score"]
    exposure_delta = round(latest_point["exposure_weight"] - first_present["exposure_weight"], 4)
    persistent_warnings = ticker_persistent_warnings(timeline)
    return {
        "ticker": ticker,
        "first_seen": first_present["generated_at"] if present_points else None,
        "last_seen": latest_present["generated_at"] if present_points else None,
        "latest_status": timeline[-1]["status"],
        "latest_direction": (latest_item or {}).get("direction", "absent"),
        "latest_attention_score": int((latest_item or {}).get("attention_score", 0)),
        "score_delta_from_first_seen": score_delta,
        "score_trend": numeric_trend(score_delta),
        "exposure_delta_from_first_seen": exposure_delta,
        "exposure_trend": numeric_trend(exposure_delta),
        "persistent_warnings": persistent_warnings,
        "latest_review_prompt": latest_review_prompt(snapshots[-1]["packet"], latest_item, ticker),
        "timeline": timeline,
    }


def ticker_item(packet: Dict[str, Any], ticker: str) -> Dict[str, Any] | None:
    for item in packet.get("impacted_tickers", []):
        if item.get("ticker") == ticker:
            return item
    return None


def score_direction(previous: Dict[str, Any] | None, current: Dict[str, Any] | None) -> str:
    if previous is None and current is None:
        return "absent"
    if previous is None:
        return "new"
    if current is None:
        return "cleared"
    delta = int(current.get("attention_score", 0)) - int(previous.get("attention_score", 0))
    return numeric_trend(delta)


def transition_status(
    previous: Dict[str, Any] | None,
    current: Dict[str, Any] | None,
    previous_present: bool,
    present: bool,
) -> str:
    if present and not previous_present:
        return "new"
    if previous_present and not present:
        return "cleared"
    if not present:
        return "absent"
    if changed(previous, current):
        return "changed"
    return "unchanged"


def changed(previous: Dict[str, Any] | None, current: Dict[str, Any] | None) -> bool:
    if previous is None or current is None:
        return previous != current
    fields = ("attention_score", "direction", "confidence", "exposure_weight", "event_ids", "warnings")
    return any(previous.get(field) != current.get(field) for field in fields)


def numeric_trend(delta: float) -> str:
    if delta > 0:
        return "increased"
    if delta < 0:
        return "decreased"
    return "flat"


def ticker_persistent_warnings(timeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    warning_periods: Dict[str, Dict[str, Any]] = {}
    for point in timeline:
        for warning in point["warnings"]:
            key = warning_key(warning)
            record = warning_periods.setdefault(key, {"warning": key, "snapshots": [], "examples": []})
            record["snapshots"].append(point["snapshot"])
            record["examples"].append(warning)
    return [
        {
            "warning": record["warning"],
            "period_count": len(record["snapshots"]),
            "snapshots": record["snapshots"],
            "latest_example": record["examples"][-1],
        }
        for _, record in sorted(warning_periods.items())
        if len(record["snapshots"]) >= 2
    ]


def warning_key(warning: str) -> str:
    if ": source is " in warning:
        prefix = warning.split(": source is ", 1)[0]
        return f"{prefix}: source remained stale"
    return warning


def persistent_warning_records(ticker_histories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    records = []
    for history in ticker_histories:
        for warning in history["persistent_warnings"]:
            records.append({"ticker": history["ticker"], **warning})
    return sorted(records, key=lambda item: (item["ticker"], item["warning"]))


def latest_review_prompt(packet: Dict[str, Any], item: Dict[str, Any] | None, ticker: str) -> str:
    for queue_item in packet.get("review_queue", []):
        if queue_item.get("ticker") == ticker and queue_item.get("prompt"):
            return str(queue_item["prompt"])
    prompts = (item or {}).get("next_review_prompts", [])
    if prompts:
        return str(prompts[0])
    return f"Review whether {ticker} still belongs in the static research packet."


def next_review_queue(ticker_histories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    queue = []
    for history in ticker_histories:
        latest_point = history["timeline"][-1]
        include = (
            latest_point["present"]
            and (
                history["latest_status"] in {"new", "changed"}
                or bool(history["persistent_warnings"])
                or history["latest_attention_score"] >= 40
            )
        )
        if include:
            queue.append(
                {
                    "ticker": history["ticker"],
                    "latest_attention_score": history["latest_attention_score"],
                    "latest_status": history["latest_status"],
                    "score_trend": history["score_trend"],
                    "exposure_trend": history["exposure_trend"],
                    "persistent_warning_count": len(history["persistent_warnings"]),
                    "prompt": history["latest_review_prompt"],
                }
            )
    return sorted(
        queue,
        key=lambda item: (
            -item["persistent_warning_count"],
            -item["latest_attention_score"],
            item["ticker"],
        ),
    )
