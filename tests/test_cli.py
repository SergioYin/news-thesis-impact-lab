import json
import hashlib
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
    assert manifest["package"] == {"name": "news-thesis-impact-lab", "version": "0.2.0"}
    assert artifacts["README.md"]["sha256"] == hashlib.sha256(readme_bytes).hexdigest()
    assert artifacts["demo/gallery.html"]["exists"] is True
    assert distributions["wheel"].get("placeholder") == "not built" or distributions["wheel"].get("exists") is True
    assert distributions["sdist"].get("placeholder") == "not built" or distributions["sdist"].get("exists") is True
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
    assert "maturity/maturity_report.md" in html
    assert "../release/manifest.md" in html
    assert "release-manifest --out release" not in html
    assert "Not investment advice" in html
