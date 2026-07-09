from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, Iterable, List


BOUNDARIES = [
    "Static local research notes only; no live market data is fetched.",
    "Not investment advice and not a buy, sell, hold, or allocation recommendation.",
    "No broker integration, order routing, execution, or account access.",
    "Scores are deterministic review aids for human research triage.",
]


@dataclass(frozen=True)
class Event:
    event_id: str
    date: str
    source: str
    source_date: str
    tickers: List[str]
    themes: List[str]
    summary: str
    impact_hints: List[str]
    confidence: str


@dataclass(frozen=True)
class Thesis:
    ticker: str
    claims: List[str]
    sensitivities: List[str]
    risks: List[str]
    opportunities: List[str]


@dataclass(frozen=True)
class Position:
    ticker: str
    weight: float
    label: str


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"invalid ISO date: {value!r}") from exc


def as_list(value: Any, field: str) -> List[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{field} must be a list of strings")
    return sorted(value)


def load_events(raw: Dict[str, Any]) -> List[Event]:
    events = raw.get("events")
    if not isinstance(events, list):
        raise ValueError("events file must contain an events list")
    parsed = []
    for item in events:
        parsed.append(
            Event(
                event_id=str(item["id"]),
                date=str(item["date"]),
                source=str(item["source"]),
                source_date=str(item.get("source_date", item["date"])),
                tickers=as_list(item["tickers"], "event.tickers"),
                themes=as_list(item.get("themes", []), "event.themes"),
                summary=str(item["summary"]),
                impact_hints=as_list(item.get("impact_hints", []), "event.impact_hints"),
                confidence=str(item.get("confidence", "medium")).lower(),
            )
        )
    return sorted(parsed, key=lambda e: (e.date, e.event_id))


def load_theses(raw: Dict[str, Any]) -> Dict[str, Thesis]:
    theses = raw.get("theses")
    if not isinstance(theses, list):
        raise ValueError("theses file must contain a theses list")
    parsed = {}
    for item in theses:
        ticker = str(item["ticker"]).upper()
        parsed[ticker] = Thesis(
            ticker=ticker,
            claims=as_list(item.get("claims", []), "thesis.claims"),
            sensitivities=as_list(item.get("sensitivities", []), "thesis.sensitivities"),
            risks=as_list(item.get("risks", []), "thesis.risks"),
            opportunities=as_list(item.get("opportunities", []), "thesis.opportunities"),
        )
    return dict(sorted(parsed.items()))


def load_portfolio(raw: Dict[str, Any]) -> Dict[str, Position]:
    positions = raw.get("positions")
    if not isinstance(positions, list):
        raise ValueError("portfolio file must contain a positions list")
    parsed = {}
    for item in positions:
        ticker = str(item["ticker"]).upper()
        parsed[ticker] = Position(
            ticker=ticker,
            weight=float(item.get("weight", 0.0)),
            label=str(item.get("label", ticker)),
        )
    return dict(sorted(parsed.items()))


def unique_sorted(values: Iterable[str]) -> List[str]:
    return sorted({str(value) for value in values if str(value)})

