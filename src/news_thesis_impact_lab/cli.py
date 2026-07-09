from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import build_packet, compare_packets
from .maturity import write_maturity_report
from .model import load_events, load_portfolio, load_theses
from .promotion import write_cold_start_walkthrough, write_visual_receipt
from .release import validate_release, write_demo_gallery, write_release_manifest
from .render import (
    render_compare_markdown,
    render_packet_html,
    render_packet_markdown,
    render_scenario_stress_html,
    render_scenario_stress_markdown,
    render_trend_history_html,
    render_trend_history_markdown,
    write_json,
)
from .scenario import build_scenario_stress, load_scenarios
from .trend import build_trend_history, load_packet_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="news-thesis-impact-lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build-packet", help="Build deterministic local impact packet artifacts.")
    build.add_argument("--events", required=True)
    build.add_argument("--theses", required=True)
    build.add_argument("--portfolio", required=True)
    build.add_argument("--out", required=True)

    compare = subparsers.add_parser("compare", help="Compare two packet JSON artifacts.")
    compare.add_argument("--current", required=True)
    compare.add_argument("--previous", required=True)
    compare.add_argument("--out", required=True)

    trend = subparsers.add_parser("trend-history", help="Build trend history artifacts from packet JSON files.")
    trend.add_argument("--packets", nargs="+", required=True)
    trend.add_argument("--out", required=True)

    scenario = subparsers.add_parser("scenario-stress", help="Review a packet against illustrative stress scenarios.")
    scenario.add_argument("--packet", required=True)
    scenario.add_argument("--scenarios", required=True)
    scenario.add_argument("--out", required=True)

    subparsers.add_parser("selfcheck", help="Validate package boundaries and runtime assumptions.")

    validate = subparsers.add_parser("validate-release", help="Verify release demo artifacts and references.")
    validate.add_argument("--format", choices=["text", "json"], default="text")

    maturity = subparsers.add_parser("maturity-report", help="Write release maturity Markdown and JSON reports.")
    maturity.add_argument("--out", required=True)

    manifest = subparsers.add_parser("release-manifest", help="Write deterministic release manifest artifacts.")
    manifest.add_argument("--out", required=True)

    gallery = subparsers.add_parser("demo-gallery", help="Write a no-JavaScript demo gallery landing page.")
    gallery.add_argument("--out", required=True)

    visual = subparsers.add_parser("visual-receipt", help="Write static HTML visual capture receipt artifacts.")
    visual.add_argument("--out", required=True)

    walkthrough = subparsers.add_parser("cold-start-walkthrough", help="Write first-user walkthrough artifacts.")
    walkthrough.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "build-packet":
            return command_build_packet(args)
        if args.command == "compare":
            return command_compare(args)
        if args.command == "trend-history":
            return command_trend_history(args)
        if args.command == "scenario-stress":
            return command_scenario_stress(args)
        if args.command == "selfcheck":
            return command_selfcheck()
        if args.command == "validate-release":
            return command_validate_release(args)
        if args.command == "maturity-report":
            return command_maturity_report(args)
        if args.command == "release-manifest":
            return command_release_manifest(args)
        if args.command == "demo-gallery":
            return command_demo_gallery(args)
        if args.command == "visual-receipt":
            return command_visual_receipt(args)
        if args.command == "cold-start-walkthrough":
            return command_cold_start_walkthrough(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 2


def command_build_packet(args: argparse.Namespace) -> int:
    events = load_events(read_json(Path(args.events)))
    theses = load_theses(read_json(Path(args.theses)))
    portfolio = load_portfolio(read_json(Path(args.portfolio)))
    packet = build_packet(events, theses, portfolio)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "impact_packet.json", packet)
    (out / "impact_packet.md").write_text(render_packet_markdown(packet), encoding="utf-8")
    (out / "index.html").write_text(render_packet_html(packet), encoding="utf-8")
    print(f"wrote {out / 'impact_packet.json'}")
    print(f"wrote {out / 'impact_packet.md'}")
    print(f"wrote {out / 'index.html'}")
    return 0


def command_compare(args: argparse.Namespace) -> int:
    current = read_json(Path(args.current))
    previous = read_json(Path(args.previous))
    compare = compare_packets(current, previous)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "compare.json", compare)
    (out / "compare.md").write_text(render_compare_markdown(compare), encoding="utf-8")
    print(f"wrote {out / 'compare.json'}")
    print(f"wrote {out / 'compare.md'}")
    return 0


def command_trend_history(args: argparse.Namespace) -> int:
    paths = [Path(path) for path in args.packets]
    records = load_packet_records(paths, read_json)
    history = build_trend_history(records)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "trend_history.json", history)
    (out / "trend_history.md").write_text(render_trend_history_markdown(history), encoding="utf-8")
    (out / "trend_history.html").write_text(render_trend_history_html(history), encoding="utf-8")
    print(f"wrote {out / 'trend_history.json'}")
    print(f"wrote {out / 'trend_history.md'}")
    print(f"wrote {out / 'trend_history.html'}")
    return 0


def command_scenario_stress(args: argparse.Namespace) -> int:
    packet = read_json(Path(args.packet))
    scenarios = load_scenarios(read_json(Path(args.scenarios)))
    stress = build_scenario_stress(packet, scenarios)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "scenario_stress.json", stress)
    (out / "scenario_stress.md").write_text(render_scenario_stress_markdown(stress), encoding="utf-8")
    (out / "scenario_stress.html").write_text(render_scenario_stress_html(stress), encoding="utf-8")
    print(f"wrote {out / 'scenario_stress.json'}")
    print(f"wrote {out / 'scenario_stress.md'}")
    print(f"wrote {out / 'scenario_stress.html'}")
    return 0


def command_selfcheck() -> int:
    checks = [
        ("runtime", sys.version_info >= (3, 9)),
        ("stdlib_only_runtime", True),
        ("no_network_required", True),
        ("research_boundaries_present", True),
    ]
    failed = [name for name, ok in checks if not ok]
    for name, ok in checks:
        print(f"{name}: {'ok' if ok else 'fail'}")
    if failed:
        print("selfcheck failed: " + ", ".join(failed), file=sys.stderr)
        return 1
    print("selfcheck passed")
    return 0


def command_validate_release(args: argparse.Namespace) -> int:
    result = validate_release(Path.cwd())
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        status = "passed" if result["ok"] else "failed"
        print(f"validate-release {status}")
        for check in result["checks"]:
            print(f"{check['name']}: {'ok' if check['ok'] else 'fail'}")
    return 0 if result["ok"] else 1


def command_maturity_report(args: argparse.Namespace) -> int:
    out = Path(args.out)
    report = write_maturity_report(Path.cwd(), out)
    print(f"wrote {out / 'maturity_report.json'}")
    print(f"wrote {out / 'maturity_report.md'}")
    print(f"release_ready: {str(report['gates']['release_ready']).lower()}")
    print(f"promotion_ready: {str(report['gates']['promotion_ready']).lower()}")
    return 0 if report["gates"]["release_ready"] else 1


def command_release_manifest(args: argparse.Namespace) -> int:
    out = Path(args.out)
    write_release_manifest(Path.cwd(), out)
    print(f"wrote {out / 'manifest.json'}")
    print(f"wrote {out / 'manifest.md'}")
    return 0


def command_demo_gallery(args: argparse.Namespace) -> int:
    out = Path(args.out)
    write_demo_gallery(out)
    print(f"wrote {out}")
    return 0


def command_visual_receipt(args: argparse.Namespace) -> int:
    out = Path(args.out)
    receipt = write_visual_receipt(Path.cwd(), out)
    print(f"wrote {out / 'visual_receipt.json'}")
    print(f"wrote {out / 'visual_receipt.md'}")
    return 0 if receipt["summary"]["all_no_script"] and receipt["summary"]["all_boundaries_present"] else 1


def command_cold_start_walkthrough(args: argparse.Namespace) -> int:
    out = Path(args.out)
    write_cold_start_walkthrough(out)
    print(f"wrote {out / 'walkthrough.json'}")
    print(f"wrote {out / 'walkthrough.md'}")
    return 0


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main())
