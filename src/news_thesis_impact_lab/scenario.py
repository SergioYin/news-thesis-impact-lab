from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from .model import BOUNDARIES, as_list, unique_sorted


RISK_POINTS = {"low": 1, "medium": 2, "high": 3, "severe": 4}
CONFIDENCE_DOWNGRADE = {"high": "medium", "medium": "low", "low": "low"}


@dataclass(frozen=True)
class Shock:
    shock_id: str
    name: str
    category: str
    description: str
    risk_level: str
    exposure_tickers: List[str]
    exposure_tags: List[str]


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    name: str
    description: str
    shocks: List[Shock]


def load_scenarios(raw: Dict[str, Any]) -> List[Scenario]:
    scenarios = raw.get("scenarios")
    if not isinstance(scenarios, list):
        raise ValueError("scenario file must contain a scenarios list")
    parsed = []
    for scenario in scenarios:
        shocks = scenario.get("shocks")
        if not isinstance(shocks, list):
            raise ValueError("each scenario must contain a shocks list")
        parsed.append(
            Scenario(
                scenario_id=str(scenario["id"]),
                name=str(scenario["name"]),
                description=str(scenario.get("description", "")),
                shocks=[load_shock(item) for item in shocks],
            )
        )
    return sorted(parsed, key=lambda item: item.scenario_id)


def load_shock(raw: Dict[str, Any]) -> Shock:
    risk_level = str(raw.get("risk_level", "medium")).lower()
    if risk_level not in RISK_POINTS:
        raise ValueError(f"unsupported risk level: {risk_level!r}")
    category = str(raw.get("category", "")).lower()
    if category not in {"macro", "sector", "company"}:
        raise ValueError(f"unsupported shock category: {category!r}")
    return Shock(
        shock_id=str(raw["id"]),
        name=str(raw["name"]),
        category=category,
        description=str(raw.get("description", "")),
        risk_level=risk_level,
        exposure_tickers=[ticker.upper() for ticker in as_list(raw.get("exposure_tickers", []), "shock.exposure_tickers")],
        exposure_tags=[tag.lower() for tag in as_list(raw.get("exposure_tags", []), "shock.exposure_tags")],
    )


def build_scenario_stress(packet: Dict[str, Any], scenarios: List[Scenario]) -> Dict[str, Any]:
    tickers = sorted(packet.get("impacted_tickers", []), key=lambda item: item.get("ticker", ""))
    scenario_results = [scenario_result(scenario, tickers) for scenario in scenarios]
    ticker_results = []
    for ticker_item in tickers:
        result = ticker_stress_result(ticker_item, scenario_results)
        if result["matched_shock_count"]:
            ticker_results.append(result)
    ticker_results.sort(key=lambda item: (-item["stress_score"], -item["exposure_weight"], item["ticker"]))
    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-10",
        "source_packet_generated_at": packet.get("generated_at", "unknown"),
        "scenario_count": len(scenarios),
        "boundaries": BOUNDARIES,
        "scenario_results": scenario_results,
        "ticker_stresses": ticker_results,
        "next_review_queue": next_review_queue(ticker_results),
    }


def scenario_result(scenario: Scenario, tickers: List[Dict[str, Any]]) -> Dict[str, Any]:
    matched_tickers = []
    max_risk = "low"
    for ticker_item in tickers:
        matches = match_shocks(ticker_item, scenario.shocks)
        if matches:
            matched_tickers.append(ticker_item["ticker"])
            max_risk = max([max_risk, *[match["risk_level"] for match in matches]], key=lambda risk: RISK_POINTS[risk])
    return {
        "scenario_id": scenario.scenario_id,
        "name": scenario.name,
        "description": scenario.description,
        "shock_count": len(scenario.shocks),
        "highest_risk_level": max_risk if matched_tickers else "none",
        "matched_tickers": sorted(matched_tickers),
        "shocks": [
            {
                "shock_id": shock.shock_id,
                "name": shock.name,
                "category": shock.category,
                "risk_level": shock.risk_level,
                "description": shock.description,
                "exposure_tickers": shock.exposure_tickers,
                "exposure_tags": shock.exposure_tags,
            }
            for shock in scenario.shocks
        ],
    }


def ticker_stress_result(ticker_item: Dict[str, Any], scenario_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    all_matches = []
    for scenario in scenario_results:
        matches = []
        for shock in scenario["shocks"]:
            match = match_shock_dict(ticker_item, shock)
            if match:
                matches.append(match)
        if matches:
            all_matches.extend(
                {
                    "scenario_id": scenario["scenario_id"],
                    "scenario_name": scenario["name"],
                    **match,
                }
                for match in matches
            )
    stress_score = min(100, sum(match["match_points"] for match in all_matches) + int(round(ticker_item.get("exposure_weight", 0.0) * 70)))
    highest_risk = highest_risk_level(match["risk_level"] for match in all_matches)
    return {
        "ticker": ticker_item["ticker"],
        "attention_score": ticker_item.get("attention_score", 0),
        "current_direction": ticker_item.get("direction", "unclear"),
        "current_confidence": ticker_item.get("confidence", "low"),
        "exposure_weight": ticker_item.get("exposure_weight", 0.0),
        "stress_score": stress_score,
        "highest_risk_level": highest_risk,
        "matched_shock_count": len(all_matches),
        "exposure_overlap": exposure_overlap(all_matches),
        "stress_flags": stress_flags(ticker_item, all_matches),
        "matched_shocks": sorted(all_matches, key=lambda item: (item["scenario_id"], item["shock_id"])),
        "thesis_contradiction_prompts": contradiction_prompts(ticker_item, all_matches),
        "confidence_downgrade_suggestion": confidence_downgrade(ticker_item, stress_score, highest_risk),
    }


def match_shocks(ticker_item: Dict[str, Any], shocks: Iterable[Shock]) -> List[Dict[str, Any]]:
    return [match for shock in shocks if (match := match_shock(ticker_item, shock))]


def match_shock(ticker_item: Dict[str, Any], shock: Shock) -> Dict[str, Any] | None:
    return match_shock_dict(
        ticker_item,
        {
            "shock_id": shock.shock_id,
            "name": shock.name,
            "category": shock.category,
            "risk_level": shock.risk_level,
            "exposure_tickers": shock.exposure_tickers,
            "exposure_tags": shock.exposure_tags,
        },
    )


def match_shock_dict(ticker_item: Dict[str, Any], shock: Dict[str, Any]) -> Dict[str, Any] | None:
    ticker = str(ticker_item["ticker"]).upper()
    direct = ticker in {str(item).upper() for item in shock.get("exposure_tickers", [])}
    text = searchable_text(ticker_item)
    tags = [tag for tag in shock.get("exposure_tags", []) if str(tag).lower() in text]
    if not direct and not tags:
        return None
    risk_level = shock["risk_level"]
    points = RISK_POINTS[risk_level] * 7
    points += 6 if direct else 0
    points += min(6, len(tags) * 2)
    return {
        "shock_id": shock["shock_id"],
        "shock_name": shock["name"],
        "category": shock["category"],
        "risk_level": risk_level,
        "direct_ticker_match": direct,
        "matched_tags": sorted(tags),
        "match_points": points,
    }


def searchable_text(ticker_item: Dict[str, Any]) -> str:
    parts = [
        ticker_item.get("position_label", ""),
        ticker_item.get("direction", ""),
        " ".join(ticker_item.get("themes", [])),
        " ".join(ticker_item.get("affected_thesis_claims", [])),
        " ".join(ticker_item.get("risks", [])),
        " ".join(ticker_item.get("opportunities", [])),
        " ".join(ticker_item.get("next_review_prompts", [])),
    ]
    return " ".join(str(part).lower() for part in parts)


def highest_risk_level(levels: Iterable[str]) -> str:
    levels = list(levels)
    if not levels:
        return "none"
    return max(levels, key=lambda risk: RISK_POINTS[risk])


def exposure_overlap(matches: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "direct_ticker_scenarios": sorted({match["scenario_id"] for match in matches if match["direct_ticker_match"]}),
        "matched_tags": unique_sorted(tag for match in matches for tag in match["matched_tags"]),
        "risk_levels": unique_sorted(match["risk_level"] for match in matches),
    }


def stress_flags(ticker_item: Dict[str, Any], matches: List[Dict[str, Any]]) -> List[str]:
    flags = []
    if any(match["direct_ticker_match"] for match in matches):
        flags.append("direct ticker shock exposure")
    if any(match["matched_tags"] for match in matches):
        flags.append("scenario tags overlap thesis, themes, or position label")
    if any(match["risk_level"] in {"high", "severe"} for match in matches):
        flags.append("high-risk stress case intersects the thesis")
    if ticker_item.get("direction") == "positive" and any(match["risk_level"] in {"high", "severe"} for match in matches):
        flags.append("current positive read has adverse stress overlap")
    if ticker_item.get("warnings"):
        flags.append("existing packet warning remains unresolved under stress review")
    return flags or ["matched illustrative stress case"]


def contradiction_prompts(ticker_item: Dict[str, Any], matches: List[Dict[str, Any]]) -> List[str]:
    ticker = ticker_item["ticker"]
    prompts = []
    if ticker_item.get("direction") == "positive":
        prompts.append(f"Test whether the current positive read for {ticker} still holds under the matched stress shocks.")
    elif ticker_item.get("direction") == "negative":
        prompts.append(f"Check whether matched stress shocks add a separate reason for {ticker} thesis pressure or duplicate an existing concern.")
    else:
        prompts.append(f"Clarify whether matched stress shocks turn the current {ticker} read into a directional thesis question.")
    for tag in exposure_overlap(matches)["matched_tags"][:3]:
        prompts.append(f"Re-read the {ticker} thesis language that depends on `{tag}` and mark what evidence would confirm or weaken it.")
    return prompts


def confidence_downgrade(ticker_item: Dict[str, Any], stress_score: int, highest_risk: str) -> Dict[str, Any]:
    current = ticker_item.get("confidence", "low")
    if highest_risk in {"high", "severe"} or stress_score >= 55:
        suggested = CONFIDENCE_DOWNGRADE.get(current, "low")
        reason = f"{highest_risk} scenario overlap with stress score {stress_score}"
    else:
        suggested = current
        reason = "stress overlap does not cross downgrade threshold"
    return {"from": current, "to": suggested, "reason": reason}


def next_review_queue(ticker_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    queue = []
    for item in ticker_results:
        if item["stress_score"] >= 40 or item["highest_risk_level"] in {"high", "severe"}:
            queue.append(
                {
                    "ticker": item["ticker"],
                    "stress_score": item["stress_score"],
                    "highest_risk_level": item["highest_risk_level"],
                    "prompt": item["thesis_contradiction_prompts"][0],
                }
            )
    return sorted(queue, key=lambda item: (-item["stress_score"], item["ticker"]))
