from __future__ import annotations

from datetime import date
from typing import Any, Dict, Iterable, List

from .model import BOUNDARIES, Event, Position, Thesis, parse_date, unique_sorted

CONFIDENCE_POINTS = {"low": 1, "medium": 2, "high": 3}
FRESHNESS_REFERENCE_DATE = date(2026, 7, 10)
STALE_DAYS = 14


def build_packet(events: List[Event], theses: Dict[str, Thesis], portfolio: Dict[str, Position]) -> Dict[str, Any]:
    tickers = sorted({ticker.upper() for event in events for ticker in event.tickers} | set(theses) | set(portfolio))
    impacted = []
    for ticker in tickers:
        related_events = [event for event in events if ticker in {t.upper() for t in event.tickers}]
        thesis = theses.get(ticker)
        position = portfolio.get(ticker)
        if not related_events and not position:
            continue
        direction = infer_direction(related_events)
        confidence = infer_confidence(related_events)
        warnings = source_warnings(related_events, ticker, thesis)
        affected_claims = affected_thesis_claims(thesis, related_events)
        score = attention_score(related_events, thesis, position, warnings)
        impacted.append(
            {
                "ticker": ticker,
                "attention_score": score,
                "direction": direction,
                "confidence": confidence,
                "exposure_weight": round(position.weight, 4) if position else 0.0,
                "position_label": position.label if position else "not in portfolio",
                "event_ids": [event.event_id for event in related_events],
                "themes": unique_sorted(theme for event in related_events for theme in event.themes),
                "affected_thesis_claims": affected_claims,
                "risks": thesis.risks if thesis else [],
                "opportunities": thesis.opportunities if thesis else [],
                "next_review_prompts": review_prompts(ticker, related_events, thesis, position, warnings),
                "warnings": warnings,
            }
        )
    impacted.sort(key=lambda item: (-item["attention_score"], item["ticker"]))
    packet = {
        "schema_version": "1.0",
        "generated_at": "2026-07-10",
        "freshness_reference_date": FRESHNESS_REFERENCE_DATE.isoformat(),
        "boundaries": BOUNDARIES,
        "source_event_count": len(events),
        "portfolio_weight_total": round(sum(position.weight for position in portfolio.values()), 4),
        "impacted_tickers": impacted,
        "review_queue": [
            {
                "ticker": item["ticker"],
                "attention_score": item["attention_score"],
                "prompt": item["next_review_prompts"][0] if item["next_review_prompts"] else "Review static thesis notes.",
            }
            for item in impacted
            if item["attention_score"] >= 40 or item["warnings"]
        ],
    }
    return packet


def infer_direction(events: Iterable[Event]) -> str:
    joined = " ".join(" ".join(event.impact_hints).lower() for event in events)
    positive = sum(token in joined for token in ("tailwind", "positive", "accelerate", "margin", "demand"))
    negative = sum(token in joined for token in ("headwind", "negative", "delay", "regulatory", "supply"))
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    if positive or negative:
        return "mixed"
    return "unclear"


def infer_confidence(events: Iterable[Event]) -> str:
    points = [CONFIDENCE_POINTS.get(event.confidence, 2) for event in events]
    if not points:
        return "low"
    average = sum(points) / len(points)
    if average >= 2.5:
        return "high"
    if average <= 1.5:
        return "low"
    return "medium"


def source_warnings(events: Iterable[Event], ticker: str, thesis: Thesis | None) -> List[str]:
    warnings = []
    for event in events:
        age = (FRESHNESS_REFERENCE_DATE - parse_date(event.source_date)).days
        if age > STALE_DAYS:
            warnings.append(f"{event.event_id}: source is {age} days old")
    if thesis is None:
        warnings.append(f"{ticker}: no thesis file entry")
    return sorted(warnings)


def affected_thesis_claims(thesis: Thesis | None, events: Iterable[Event]) -> List[str]:
    if thesis is None:
        return []
    event_parts = []
    for event in events:
        event_parts.extend([event.summary.lower(), " ".join(event.themes).lower(), " ".join(event.impact_hints).lower()])
    event_text = " ".join(event_parts)
    matched = []
    for claim in thesis.claims:
        claim_terms = {term.strip(".,:;").lower() for term in claim.split() if len(term.strip(".,:;")) > 4}
        if claim_terms and any(term in event_text for term in claim_terms):
            matched.append(claim)
    return matched or thesis.claims[:1]


def attention_score(events: List[Event], thesis: Thesis | None, position: Position | None, warnings: List[str]) -> int:
    event_points = sum(14 + (3 * len(event.impact_hints)) + CONFIDENCE_POINTS.get(event.confidence, 2) for event in events)
    thesis_points = 8 if thesis else 0
    exposure_points = int(round((position.weight if position else 0.0) * 120))
    warning_points = min(12, len(warnings) * 4)
    return min(100, event_points + thesis_points + exposure_points + warning_points)


def review_prompts(
    ticker: str,
    events: List[Event],
    thesis: Thesis | None,
    position: Position | None,
    warnings: List[str],
) -> List[str]:
    prompts = []
    if events:
        prompts.append(f"Review whether {ticker} thesis sensitivities still match events {', '.join(event.event_id for event in events)}.")
    if position and position.weight > 0:
        prompts.append(f"Check static exposure note for {ticker} at {position.weight:.1%} portfolio weight.")
    if thesis and thesis.risks:
        prompts.append(f"Re-read risk note: {thesis.risks[0]}")
    if warnings:
        prompts.append(f"Resolve warning before relying on packet: {warnings[0]}")
    return prompts or [f"Add a thesis note before interpreting {ticker} impact."]


def compare_packets(current: Dict[str, Any], previous: Dict[str, Any]) -> Dict[str, Any]:
    current_by_ticker = {item["ticker"]: item for item in current.get("impacted_tickers", [])}
    previous_by_ticker = {item["ticker"]: item for item in previous.get("impacted_tickers", [])}
    tickers = sorted(set(current_by_ticker) | set(previous_by_ticker))
    deltas = []
    for ticker in tickers:
        cur = current_by_ticker.get(ticker)
        old = previous_by_ticker.get(ticker)
        deltas.append(
            {
                "ticker": ticker,
                "status": delta_status(cur, old),
                "attention_score_delta": (cur or {}).get("attention_score", 0) - (old or {}).get("attention_score", 0),
                "current_direction": (cur or {}).get("direction", "absent"),
                "previous_direction": (old or {}).get("direction", "absent"),
                "current_exposure_weight": (cur or {}).get("exposure_weight", 0.0),
                "previous_exposure_weight": (old or {}).get("exposure_weight", 0.0),
            }
        )
    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-10",
        "boundaries": BOUNDARIES,
        "delta_count": len(deltas),
        "deltas": sorted(deltas, key=lambda item: (-abs(item["attention_score_delta"]), item["ticker"])),
    }


def delta_status(current: Dict[str, Any] | None, previous: Dict[str, Any] | None) -> str:
    if current and not previous:
        return "new"
    if previous and not current:
        return "removed"
    if current == previous:
        return "unchanged"
    return "changed"
