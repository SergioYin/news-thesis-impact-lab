import json
import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from news_thesis_impact_lab.trend import build_trend_history, load_packet_records


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "news_thesis_impact_lab", *args],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
        text=True,
        capture_output=True,
        check=True,
    )


def test_build_packet_outputs_expected_files(tmp_path):
    out = tmp_path / "packet"
    run_cli(
        "build-packet",
        "--events",
        "examples/events.json",
        "--theses",
        "examples/theses.json",
        "--portfolio",
        "examples/portfolio.json",
        "--out",
        str(out),
    )

    packet = json.loads((out / "impact_packet.json").read_text(encoding="utf-8"))
    assert [item["ticker"] for item in packet["impacted_tickers"]] == ["NVDA", "MSFT", "GOOGL", "AAPL"]
    assert packet["impacted_tickers"][0]["attention_score"] == 67
    assert "Not investment advice" in "\n".join(packet["boundaries"])
    assert (out / "impact_packet.md").exists()
    assert "<script" not in (out / "index.html").read_text(encoding="utf-8").lower()


def test_compare_outputs_delta(tmp_path):
    packet_out = tmp_path / "packet"
    compare_out = tmp_path / "compare"
    run_cli(
        "build-packet",
        "--events",
        "examples/events.json",
        "--theses",
        "examples/theses.json",
        "--portfolio",
        "examples/portfolio.json",
        "--out",
        str(packet_out),
    )
    run_cli(
        "compare",
        "--current",
        str(packet_out / "impact_packet.json"),
        "--previous",
        "examples/previous_packet.json",
        "--out",
        str(compare_out),
    )

    compare = json.loads((compare_out / "compare.json").read_text(encoding="utf-8"))
    statuses = {item["ticker"]: item["status"] for item in compare["deltas"]}
    assert statuses["NVDA"] == "new"
    assert statuses["MSFT"] == "changed"


def test_trend_history_calculates_statuses_warnings_and_queue():
    history_paths = sorted((ROOT / "examples/history").glob("*.json"))
    history = build_trend_history(load_packet_records(history_paths, lambda path: json.loads(path.read_text(encoding="utf-8"))))
    histories = {item["ticker"]: item for item in history["ticker_histories"]}
    queue = [item["ticker"] for item in history["next_review_queue"]]

    assert [snapshot["generated_at"] for snapshot in history["snapshots"]] == [
        "2026-06-26",
        "2026-07-03",
        "2026-07-10",
    ]
    assert histories["NVDA"]["timeline"][1]["status"] == "new"
    assert histories["AAPL"]["timeline"][-1]["status"] == "absent"
    assert histories["AAPL"]["timeline"][1]["status"] == "cleared"
    assert histories["AAPL"]["score_trend"] == "decreased"
    assert histories["MSFT"]["score_trend"] == "increased"
    assert histories["MSFT"]["exposure_trend"] == "increased"
    assert histories["GOOGL"]["exposure_trend"] == "decreased"
    assert histories["GOOGL"]["persistent_warnings"][0]["period_count"] == 3
    assert histories["GOOGL"]["persistent_warnings"][0]["warning"].endswith("source remained stale")
    assert queue[:3] == ["GOOGL", "NVDA", "MSFT"]


def test_trend_history_cli_outputs_files(tmp_path):
    out = tmp_path / "trend"
    run_cli(
        "trend-history",
        "--packets",
        "examples/history/2026-07-10_packet.json",
        "examples/history/2026-06-26_packet.json",
        "examples/history/2026-07-03_packet.json",
        "--out",
        str(out),
    )

    history = json.loads((out / "trend_history.json").read_text(encoding="utf-8"))
    markdown = (out / "trend_history.md").read_text(encoding="utf-8")
    html = (out / "trend_history.html").read_text(encoding="utf-8")

    assert history["history_period_count"] == 3
    assert [snapshot["name"] for snapshot in history["snapshots"]] == [
        "2026-06-26_packet",
        "2026-07-03_packet",
        "2026-07-10_packet",
    ]
    assert "Persistent Warnings" in markdown
    assert "Not investment advice" in markdown
    assert "<script" not in html.lower()
    assert "Trend History" in html


def test_selfcheck():
    result = run_cli("selfcheck")
    assert "selfcheck passed" in result.stdout


def test_validate_release_json_reports_expected_checks():
    result = run_cli("validate-release", "--format", "json")
    payload = json.loads(result.stdout)
    checks = {check["name"]: check for check in payload["checks"]}

    assert payload["ok"] is True
    assert checks["demo_artifacts_exist"]["ok"] is True
    assert checks["release_artifacts_exist"]["ok"] is True
    assert checks["demo_artifacts_deterministic"]["ok"] is True
    assert checks["release_manifest_deterministic"]["ok"] is True
    assert checks["demo_boundaries_present"]["ok"] is True
    assert checks["referenced_example_files_exist"]["ok"] is True
    assert "examples/events.json" in checks["referenced_example_files_exist"]["referenced"]
    assert checks["example_files_exist"]["ok"] is True
    assert "demo/visual/visual_receipt.json" not in checks["demo_artifacts_exist"]["missing"]
    assert "demo/walkthrough/walkthrough.json" not in checks["demo_artifacts_exist"]["missing"]


def test_maturity_report_writes_markdown_and_json(tmp_path):
    out = tmp_path / "maturity"
    result = run_cli("maturity-report", "--out", str(out))

    report = json.loads((out / "maturity_report.json").read_text(encoding="utf-8"))
    markdown = (out / "maturity_report.md").read_text(encoding="utf-8")
    assert "release_ready: true" in result.stdout
    assert report["gates"]["release_ready"] is True
    assert report["gates"]["promotion_ready"] is True
    assert set(report["scores"]) == {
        "product",
        "runnable",
        "user_value",
        "evidence",
        "engineering",
        "showcase",
        "risk",
    }
    assert "# Maturity Report" in markdown
    assert "failed_checks: none" in markdown


def test_release_manifest_writes_hashes_commands_and_placeholders(tmp_path):
    out = tmp_path / "release"
    result = run_cli("release-manifest", "--out", str(out))

    manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    markdown = (out / "manifest.md").read_text(encoding="utf-8")
    artifacts = {item["path"]: item for item in manifest["key_artifacts"]}
    distributions = {item["kind"]: item for item in manifest["distributions"]}
    readme_bytes = (ROOT / "README.md").read_bytes()

    assert "wrote" in result.stdout
    assert manifest["package"] == {"name": "news-thesis-impact-lab", "version": "0.4.0"}
    assert artifacts["README.md"]["sha256"] == hashlib.sha256(readme_bytes).hexdigest()
    assert artifacts["demo/gallery.html"]["exists"] is True
    assert artifacts["demo/trend/trend_history.json"]["exists"] is True
    assert artifacts["demo/visual/visual_receipt.json"]["exists"] is True
    assert artifacts["demo/walkthrough/walkthrough.json"]["exists"] is True
    assert artifacts["examples/history/2026-07-10_packet.json"]["exists"] is True
    assert distributions["wheel"].get("placeholder") == "not built" or distributions["wheel"].get("exists") is True
    assert distributions["sdist"].get("placeholder") == "not built" or distributions["sdist"].get("exists") is True
    assert "visual-receipt --out demo/visual" in "\n".join(manifest["commands"]["regenerate"])
    assert "cold-start-walkthrough --out demo/walkthrough" in "\n".join(manifest["commands"]["regenerate"])
    assert "validate-release --format json" in "\n".join(manifest["commands"]["verify"])
    assert "Not investment advice" in "\n".join(manifest["finance_safety_boundaries"])
    assert "# Release Manifest" in markdown


def test_demo_gallery_writes_static_landing_page(tmp_path):
    out = tmp_path / "gallery.html"
    run_cli("demo-gallery", "--out", str(out))

    html = out.read_text(encoding="utf-8")
    assert "<script" not in html.lower()
    assert "impact_packet.md" in html
    assert "compare/compare.md" in html
    assert "trend/trend_history.md" in html
    assert "trend/trend_history.html" in html
    assert "visual/visual_receipt.md" in html
    assert "walkthrough/walkthrough.md" in html
    assert "maturity/maturity_report.md" in html
    assert "../release/manifest.md" in html
    assert "release-manifest --out release" not in html
    assert "Not investment advice" in html


def test_visual_receipt_checks_static_html_boundaries_and_scripts(tmp_path):
    out = tmp_path / "visual"
    run_cli("visual-receipt", "--out", str(out))

    receipt = json.loads((out / "visual_receipt.json").read_text(encoding="utf-8"))
    markdown = (out / "visual_receipt.md").read_text(encoding="utf-8")
    captures = {item["path"]: item for item in receipt["captures"]}

    assert receipt["summary"]["asset_count"] == 3
    assert receipt["summary"]["all_no_script"] is True
    assert receipt["summary"]["all_boundaries_present"] is True
    assert captures["demo/index.html"]["title"] == "News Thesis Impact Packet"
    assert captures["demo/gallery.html"]["role"] == "artifact gallery entry point"
    assert captures["demo/trend/trend_history.html"]["no_script"] is True
    assert captures["demo/index.html"]["boundaries_present"] is True
    assert captures["demo/index.html"]["sha256"] == hashlib.sha256((ROOT / "demo/index.html").read_bytes()).hexdigest()
    assert "static read demo/index.html" in markdown
    assert "Not investment advice" in markdown


def test_cold_start_walkthrough_content(tmp_path):
    out = tmp_path / "walkthrough"
    run_cli("cold-start-walkthrough", "--out", str(out))

    walkthrough = json.loads((out / "walkthrough.json").read_text(encoding="utf-8"))
    markdown = (out / "walkthrough.md").read_text(encoding="utf-8")

    assert walkthrough["duration"] == "2-5 minutes"
    assert "visual-receipt --out demo/visual" in "\n".join(walkthrough["commands"])
    assert "cold-start-walkthrough --out demo/walkthrough" in "\n".join(walkthrough["commands"])
    assert "demo/visual/visual_receipt.json" in walkthrough["expected_artifacts"]
    assert "demo/walkthrough/walkthrough.md" in walkthrough["expected_artifacts"]
    assert any("no-script" in item for item in walkthrough["interpretation_guide"])
    assert any("live market data" in item for item in walkthrough["failure_modes"])
    assert "No broker integration" in "\n".join(walkthrough["boundaries"])
    assert "## Failure Modes And Boundaries" in markdown


def test_promotion_outputs_are_deterministic(tmp_path):
    first_visual = tmp_path / "first_visual"
    second_visual = tmp_path / "second_visual"
    first_walkthrough = tmp_path / "first_walkthrough"
    second_walkthrough = tmp_path / "second_walkthrough"

    run_cli("visual-receipt", "--out", str(first_visual))
    run_cli("visual-receipt", "--out", str(second_visual))
    run_cli("cold-start-walkthrough", "--out", str(first_walkthrough))
    run_cli("cold-start-walkthrough", "--out", str(second_walkthrough))

    assert (first_visual / "visual_receipt.json").read_bytes() == (second_visual / "visual_receipt.json").read_bytes()
    assert (first_visual / "visual_receipt.md").read_bytes() == (second_visual / "visual_receipt.md").read_bytes()
    assert (first_walkthrough / "walkthrough.json").read_bytes() == (second_walkthrough / "walkthrough.json").read_bytes()
    assert (first_walkthrough / "walkthrough.md").read_bytes() == (second_walkthrough / "walkthrough.md").read_bytes()
