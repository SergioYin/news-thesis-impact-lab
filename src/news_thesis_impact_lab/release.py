from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List

from . import __version__
from .engine import build_packet, compare_packets
from .journal import JOURNAL_BOUNDARIES, build_decision_journal, render_decision_journal_html, render_decision_journal_markdown
from .ledger import build_review_ledger
from .model import BOUNDARIES, load_events, load_portfolio, load_theses
from .promotion import write_cold_start_walkthrough, write_visual_receipt
from .render import (
    esc,
    render_compare_markdown,
    render_packet_html,
    render_packet_markdown,
    render_review_ledger_html,
    render_review_ledger_markdown,
    render_scenario_stress_html,
    render_scenario_stress_markdown,
    render_trend_history_html,
    render_trend_history_markdown,
    write_json,
)
from .scenario import build_scenario_stress, load_scenarios
from .trend import build_trend_history


DEMO_FILES = [
    Path("demo/impact_packet.json"),
    Path("demo/impact_packet.md"),
    Path("demo/index.html"),
    Path("demo/gallery.html"),
    Path("demo/compare/compare.json"),
    Path("demo/compare/compare.md"),
    Path("demo/trend/trend_history.json"),
    Path("demo/trend/trend_history.md"),
    Path("demo/trend/trend_history.html"),
    Path("demo/scenario/scenario_stress.json"),
    Path("demo/scenario/scenario_stress.md"),
    Path("demo/scenario/scenario_stress.html"),
    Path("demo/ledger/review_ledger.json"),
    Path("demo/ledger/review_ledger.md"),
    Path("demo/ledger/review_ledger.html"),
    Path("demo/journal/decision_journal.json"),
    Path("demo/journal/decision_journal.md"),
    Path("demo/journal/decision_journal.html"),
    Path("demo/visual/visual_receipt.json"),
    Path("demo/visual/visual_receipt.md"),
    Path("demo/walkthrough/walkthrough.json"),
    Path("demo/walkthrough/walkthrough.md"),
]
EVIDENCE_FILES = [
    Path("demo/evidence/evidence_hub.json"),
    Path("demo/evidence/evidence_hub.md"),
    Path("demo/evidence/evidence_hub.html"),
]
RELEASE_FILES = [
    Path("release/manifest.json"),
    Path("release/manifest.md"),
]
EXAMPLE_FILES = [
    Path("examples/events.json"),
    Path("examples/theses.json"),
    Path("examples/portfolio.json"),
    Path("examples/scenarios.json"),
    Path("examples/previous_packet.json"),
    Path("examples/review_ledger_previous.json"),
    Path("examples/history/2026-06-26_packet.json"),
    Path("examples/history/2026-07-03_packet.json"),
    Path("examples/history/2026-07-10_packet.json"),
]
BUNDLE_FILES = [
    Path("demo/bundle/bundle_manifest.json"),
    Path("demo/bundle/bundle_manifest.md"),
    Path("demo/bundle/bundle_manifest.html"),
    Path("demo/bundle/bundle_copy_list.json"),
]
KEY_ARTIFACTS = [
    Path("README.md"),
    Path("CHANGELOG.md"),
    Path("pyproject.toml"),
    Path("docs/review-packet.md"),
    Path("demo/impact_packet.json"),
    Path("demo/impact_packet.md"),
    Path("demo/index.html"),
    Path("demo/gallery.html"),
    Path("demo/compare/compare.json"),
    Path("demo/compare/compare.md"),
    Path("demo/trend/trend_history.json"),
    Path("demo/trend/trend_history.md"),
    Path("demo/trend/trend_history.html"),
    Path("demo/scenario/scenario_stress.json"),
    Path("demo/scenario/scenario_stress.md"),
    Path("demo/scenario/scenario_stress.html"),
    Path("demo/ledger/review_ledger.json"),
    Path("demo/ledger/review_ledger.md"),
    Path("demo/ledger/review_ledger.html"),
    Path("demo/journal/decision_journal.json"),
    Path("demo/journal/decision_journal.md"),
    Path("demo/journal/decision_journal.html"),
    Path("demo/visual/visual_receipt.json"),
    Path("demo/visual/visual_receipt.md"),
    Path("demo/walkthrough/walkthrough.json"),
    Path("demo/walkthrough/walkthrough.md"),
    *EXAMPLE_FILES,
]
BUNDLE_SOURCE_FILES = sorted(
    {
        Path("README.md"),
        Path("CHANGELOG.md"),
        Path("pyproject.toml"),
        Path("docs/review-packet.md"),
        Path("skills/agent/news-thesis-impact-lab/SKILL.md"),
        *DEMO_FILES,
        *EVIDENCE_FILES,
        *RELEASE_FILES,
        *EXAMPLE_FILES,
    },
    key=lambda path: path.as_posix(),
)
REGENERATE_COMMANDS = [
    "PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo",
    "PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare",
    "PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend",
    "PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario",
    "PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger",
    "PYTHONPATH=src python -m news_thesis_impact_lab decision-journal --packet demo/impact_packet.json --compare demo/compare/compare.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --ledger demo/ledger/review_ledger.json --evidence demo/evidence/evidence_hub.json --out demo/journal",
    "PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity",
    "PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html",
    "PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual",
    "PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough",
    "PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release",
    "PYTHONPATH=src python -m news_thesis_impact_lab evidence-hub --out demo/evidence",
    "PYTHONPATH=src python -m news_thesis_impact_lab bundle-export --out demo/bundle",
]
VERIFY_COMMANDS = [
    "python -m pytest -q",
    "PYTHONPATH=src python -m news_thesis_impact_lab decision-journal --packet demo/impact_packet.json --compare demo/compare/compare.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --ledger demo/ledger/review_ledger.json --evidence demo/evidence/evidence_hub.json --out demo/journal",
    "PYTHONPATH=src python -m news_thesis_impact_lab evidence-hub --out demo/evidence",
    "PYTHONPATH=src python -m news_thesis_impact_lab bundle-export --out demo/bundle",
    "PYTHONPATH=src python -m news_thesis_impact_lab bundle-inspect --manifest demo/bundle/bundle_manifest.json --format json",
    "PYTHONPATH=src python -m news_thesis_impact_lab selfcheck",
    "PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json",
    "python scripts/privacy_scan.py",
    "git diff --check",
]


def validate_release(root: Path) -> Dict[str, Any]:
    root = root.resolve()
    checks = [
        check_files_exist(root, "demo_artifacts_exist", DEMO_FILES),
        check_files_exist(root, "evidence_hub_artifacts_exist", EVIDENCE_FILES),
        check_files_exist(root, "release_artifacts_exist", RELEASE_FILES),
        check_files_exist(root, "example_files_exist", EXAMPLE_FILES),
        check_files_exist(root, "bundle_artifacts_exist", BUNDLE_FILES),
        check_demo_boundaries(root),
        check_evidence_hub_no_js(root),
        check_bundle_no_js(root),
        check_journal_no_js(root),
        check_journal_no_recommendation_language(root),
        check_demo_deterministic(root),
        check_evidence_hub_deterministic(root),
        check_release_manifest_deterministic(root),
        check_bundle_deterministic(root),
        check_bundle_inspect(root),
        check_referenced_example_files(root),
    ]
    passed = all(check["ok"] for check in checks)
    return {"ok": passed, "checks": checks}


def check_files_exist(root: Path, name: str, paths: Iterable[Path]) -> Dict[str, Any]:
    missing = [path.as_posix() for path in paths if not (root / path).is_file()]
    return {"name": name, "ok": not missing, "missing": missing}


def check_demo_boundaries(root: Path) -> Dict[str, Any]:
    missing: Dict[str, List[str]] = {}
    for path in DEMO_FILES:
        full_path = root / path
        expected = JOURNAL_BOUNDARIES if path.as_posix().startswith("demo/journal/") else BOUNDARIES
        if not full_path.is_file():
            missing[path.as_posix()] = expected[:]
            continue
        text = full_path.read_text(encoding="utf-8")
        absent = [boundary for boundary in expected if boundary not in text]
        if absent:
            missing[path.as_posix()] = absent
    return {"name": "demo_boundaries_present", "ok": not missing, "missing_boundaries": missing}


def check_journal_no_recommendation_language(root: Path) -> Dict[str, Any]:
    paths = [
        Path("demo/journal/decision_journal.json"),
        Path("demo/journal/decision_journal.md"),
        Path("demo/journal/decision_journal.html"),
    ]
    findings: Dict[str, List[str]] = {}
    for path in paths:
        full_path = root / path
        if not full_path.is_file():
            findings[path.as_posix()] = ["missing"]
            continue
        words = full_path.read_text(encoding="utf-8").lower().replace("-", " ").split()
        found = sorted({term for term in ("buy", "sell", "hold") if term in words})
        if found:
            findings[path.as_posix()] = found
    return {"name": "decision_journal_no_recommendation_language", "ok": not findings, "findings": findings}


def check_journal_no_js(root: Path) -> Dict[str, Any]:
    html_path = root / "demo/journal/decision_journal.html"
    if not html_path.is_file():
        return {"name": "decision_journal_no_js", "ok": False, "path": "demo/journal/decision_journal.html"}
    return {
        "name": "decision_journal_no_js",
        "ok": "<script" not in html_path.read_text(encoding="utf-8").lower(),
        "path": "demo/journal/decision_journal.html",
    }


def check_demo_deterministic(root: Path) -> Dict[str, Any]:
    if any(not (root / path).is_file() for path in EXAMPLE_FILES):
        return {"name": "demo_artifacts_deterministic", "ok": False, "changed": [], "error": "missing example input"}

    with tempfile.TemporaryDirectory(prefix="news-thesis-impact-lab-") as tmp:
        tmp_path = Path(tmp)
        packet = build_packet(
            load_events(read_json(root / "examples/events.json")),
            load_theses(read_json(root / "examples/theses.json")),
            load_portfolio(read_json(root / "examples/portfolio.json")),
        )
        write_json(tmp_path / "impact_packet.json", packet)
        (tmp_path / "impact_packet.md").write_text(render_packet_markdown(packet), encoding="utf-8")
        (tmp_path / "index.html").write_text(render_packet_html(packet), encoding="utf-8")

        compare = compare_packets(packet, read_json(root / "examples/previous_packet.json"))
        compare_dir = tmp_path / "compare"
        compare_dir.mkdir()
        write_json(compare_dir / "compare.json", compare)
        (compare_dir / "compare.md").write_text(render_compare_markdown(compare), encoding="utf-8")

        trend_dir = tmp_path / "trend"
        trend_dir.mkdir()
        history_records = [
            {"name": path.stem, "path": path.relative_to(root).as_posix(), "packet": read_json(path)}
            for path in sorted((root / "examples/history").glob("*.json"))
        ]
        history = build_trend_history(history_records)
        write_json(trend_dir / "trend_history.json", history)
        (trend_dir / "trend_history.md").write_text(render_trend_history_markdown(history), encoding="utf-8")
        (trend_dir / "trend_history.html").write_text(render_trend_history_html(history), encoding="utf-8")

        scenario_dir = tmp_path / "scenario"
        scenario_dir.mkdir()
        stress = build_scenario_stress(packet, load_scenarios(read_json(root / "examples/scenarios.json")))
        write_json(scenario_dir / "scenario_stress.json", stress)
        (scenario_dir / "scenario_stress.md").write_text(render_scenario_stress_markdown(stress), encoding="utf-8")
        (scenario_dir / "scenario_stress.html").write_text(render_scenario_stress_html(stress), encoding="utf-8")

        ledger_dir = tmp_path / "ledger"
        ledger_dir.mkdir()
        ledger = build_review_ledger(packet, history, stress, read_json(root / "examples/review_ledger_previous.json"))
        write_json(ledger_dir / "review_ledger.json", ledger)
        (ledger_dir / "review_ledger.md").write_text(render_review_ledger_markdown(ledger), encoding="utf-8")
        (ledger_dir / "review_ledger.html").write_text(render_review_ledger_html(ledger), encoding="utf-8")

        journal_dir = tmp_path / "journal"
        journal_dir.mkdir()
        evidence_hub = read_json(root / "demo/evidence/evidence_hub.json") if (root / "demo/evidence/evidence_hub.json").is_file() else {}
        journal = build_decision_journal(packet, compare, history, stress, ledger, evidence_hub)
        write_json(journal_dir / "decision_journal.json", journal)
        (journal_dir / "decision_journal.md").write_text(render_decision_journal_markdown(journal), encoding="utf-8")
        (journal_dir / "decision_journal.html").write_text(render_decision_journal_html(journal), encoding="utf-8")

        write_demo_gallery(tmp_path / "gallery.html")
        write_visual_receipt(root, tmp_path / "visual")
        write_cold_start_walkthrough(tmp_path / "walkthrough")

        changed = [
            path.as_posix()
            for path in DEMO_FILES
            if not (root / path).is_file() or (root / path).read_bytes() != (tmp_path / path.relative_to("demo")).read_bytes()
        ]
    return {"name": "demo_artifacts_deterministic", "ok": not changed, "changed": changed}


def check_release_manifest_deterministic(root: Path) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="news-thesis-impact-lab-release-") as tmp:
        tmp_path = Path(tmp)
        write_release_manifest(root, tmp_path)
        changed = [
            path.as_posix()
            for path in RELEASE_FILES
            if not (root / path).is_file() or (root / path).read_bytes() != (tmp_path / path.relative_to("release")).read_bytes()
        ]
    return {"name": "release_manifest_deterministic", "ok": not changed, "changed": changed}


def check_evidence_hub_deterministic(root: Path) -> Dict[str, Any]:
    from .evidence import write_evidence_hub

    with tempfile.TemporaryDirectory(prefix="news-thesis-impact-lab-evidence-") as tmp:
        tmp_path = Path(tmp)
        write_evidence_hub(root, tmp_path)
        changed = [
            path.as_posix()
            for path in EVIDENCE_FILES
            if not (root / path).is_file() or (root / path).read_bytes() != (tmp_path / path.name).read_bytes()
        ]
    return {"name": "evidence_hub_deterministic", "ok": not changed, "changed": changed}


def check_evidence_hub_no_js(root: Path) -> Dict[str, Any]:
    html_path = root / "demo/evidence/evidence_hub.html"
    if not html_path.is_file():
        return {"name": "evidence_hub_no_js", "ok": False, "path": "demo/evidence/evidence_hub.html"}
    return {
        "name": "evidence_hub_no_js",
        "ok": "<script" not in html_path.read_text(encoding="utf-8").lower(),
        "path": "demo/evidence/evidence_hub.html",
    }


def check_bundle_no_js(root: Path) -> Dict[str, Any]:
    html_path = root / "demo/bundle/bundle_manifest.html"
    if not html_path.is_file():
        return {"name": "bundle_manifest_no_js", "ok": False, "path": "demo/bundle/bundle_manifest.html"}
    return {
        "name": "bundle_manifest_no_js",
        "ok": "<script" not in html_path.read_text(encoding="utf-8").lower(),
        "path": "demo/bundle/bundle_manifest.html",
    }


def check_bundle_deterministic(root: Path) -> Dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="news-thesis-impact-lab-bundle-") as tmp:
        tmp_path = Path(tmp)
        write_bundle_export(root, tmp_path)
        changed = [
            path.as_posix()
            for path in BUNDLE_FILES
            if not (root / path).is_file() or (root / path).read_bytes() != (tmp_path / path.relative_to("demo/bundle")).read_bytes()
        ]
    return {"name": "bundle_artifacts_deterministic", "ok": not changed, "changed": changed}


def check_bundle_inspect(root: Path) -> Dict[str, Any]:
    manifest_path = root / "demo/bundle/bundle_manifest.json"
    if not manifest_path.is_file():
        return {"name": "bundle_inspect_passes", "ok": False, "error": "missing bundle manifest"}
    inspection = inspect_bundle_manifest(manifest_path)
    return {
        "name": "bundle_inspect_passes",
        "ok": inspection["ok"],
        "missing": inspection["summary"]["missing"],
        "changed": inspection["summary"]["changed"],
        "error": inspection.get("error"),
    }


def check_referenced_example_files(root: Path) -> Dict[str, Any]:
    referenced = sorted(find_example_references(root))
    missing = [path for path in referenced if not (root / path).is_file()]
    return {"name": "referenced_example_files_exist", "ok": not missing, "referenced": referenced, "missing": missing}


def find_example_references(root: Path) -> set[str]:
    references: set[str] = set()
    for path in [root / "README.md", root / "docs/review-packet.md", root / "skills/agent/news-thesis-impact-lab/SKILL.md"]:
        if not path.is_file():
            continue
        for token in path.read_text(encoding="utf-8").replace("\\", "/").split():
            cleaned = token.strip("`'\"(),.:;")
            if "*" not in cleaned and cleaned.startswith("examples/") and cleaned.endswith(".json"):
                references.add(cleaned)
    return references


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_release_manifest(root: Path, out: Path) -> Dict[str, Any]:
    manifest = build_release_manifest(root)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "manifest.json", manifest)
    (out / "manifest.md").write_text(render_release_manifest_markdown(manifest), encoding="utf-8")
    return manifest


def write_bundle_export(root: Path, out: Path) -> Dict[str, Any]:
    root = root.resolve()
    out.mkdir(parents=True, exist_ok=True)
    artifacts_root = out / "artifacts"
    manifest = build_bundle_manifest(root, out)
    copy_list = {
        "schema_version": "1.0",
        "generated_at": manifest["generated_at"],
        "package": manifest["package"],
        "copy_root": "artifacts",
        "items": [
            {
                "source_path": artifact["source_path"],
                "bundle_path": artifact["bundle_path"],
                "sha256": artifact["sha256"],
                "bytes": artifact["bytes"],
                "role": artifact["role"],
                "package_boundary": artifact["package_boundary"],
                "safety_boundary_tags": artifact["safety_boundary_tags"],
            }
            for artifact in manifest["artifacts"]
        ],
    }
    for artifact in manifest["artifacts"]:
        source = root / artifact["source_path"]
        target = out / artifact["bundle_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    write_json(out / "bundle_manifest.json", manifest)
    (out / "bundle_manifest.md").write_text(render_bundle_manifest_markdown(manifest), encoding="utf-8")
    (out / "bundle_manifest.html").write_text(render_bundle_manifest_html(manifest), encoding="utf-8")
    write_json(out / "bundle_copy_list.json", copy_list)
    return manifest


def build_bundle_manifest(root: Path, out: Path | None = None) -> Dict[str, Any]:
    root = root.resolve()
    artifacts = [bundle_artifact_record(root, path) for path in BUNDLE_SOURCE_FILES]
    return {
        "schema_version": "1.0",
        "bundle_type": "plain-file-agent-reuse-packet",
        "generated_at": "2026-07-10",
        "package": {"name": "news-thesis-impact-lab", "version": __version__},
        "manifest_files": [
            "bundle_manifest.json",
            "bundle_manifest.md",
            "bundle_manifest.html",
            "bundle_copy_list.json",
        ],
        "artifact_root": "artifacts",
        "finance_safety_boundaries": BOUNDARIES,
        "global_safety_boundary_tags": safety_boundary_tags(),
        "artifacts": artifacts,
        "commands": {
            "regenerate": REGENERATE_COMMANDS,
            "inspect": "PYTHONPATH=src python -m news_thesis_impact_lab bundle-inspect --manifest demo/bundle/bundle_manifest.json --format json",
            "verify": VERIFY_COMMANDS,
        },
        "notes": [
            "Bundle files are copied as plain files under artifacts/; no zip or archive is created.",
            "The manifest validates bundled copies through bundle_path and keeps source_path for checkout-level regeneration.",
            "The bundle contains public local demo, example, release, documentation, and agent skill artifacts only.",
            "The bundle preserves research-only boundaries: no live data, no advice, no broker access, and no order behavior.",
        ],
    }


def bundle_artifact_record(root: Path, relative_path: Path) -> Dict[str, Any]:
    path = root / relative_path
    data = path.read_bytes() if path.is_file() else b""
    return {
        "source_path": relative_path.as_posix(),
        "bundle_path": (Path("artifacts") / relative_path).as_posix(),
        "exists": path.is_file(),
        "sha256": hashlib.sha256(data).hexdigest() if data else None,
        "bytes": len(data) if data else None,
        "role": bundle_role(relative_path),
        "regenerate_command": command_to_regenerate(relative_path.as_posix()),
        "package_boundary": package_boundary(relative_path),
        "safety_boundary_tags": safety_boundary_tags(),
    }


def inspect_bundle_manifest(manifest_path: Path) -> Dict[str, Any]:
    manifest_path = manifest_path.resolve()
    try:
        manifest = read_json(manifest_path)
    except Exception as exc:
        return {
            "ok": False,
            "manifest": str(manifest_path),
            "error": str(exc),
            "summary": {"total": 0, "present": [], "missing": [], "changed": []},
        }
    base = manifest_path.parent
    present: List[str] = []
    missing: List[str] = []
    changed: List[Dict[str, Any]] = []
    for artifact in manifest.get("artifacts", []):
        bundle_path = artifact.get("bundle_path") or artifact.get("source_path")
        expected_hash = artifact.get("sha256")
        path = base / bundle_path
        if not path.is_file():
            missing.append(bundle_path)
            continue
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            changed.append(
                {
                    "path": bundle_path,
                    "expected_sha256": expected_hash,
                    "actual_sha256": actual_hash,
                }
            )
        else:
            present.append(bundle_path)
    ok = not missing and not changed
    return {
        "ok": ok,
        "manifest": str(manifest_path),
        "package": manifest.get("package", {}),
        "summary": {
            "total": len(manifest.get("artifacts", [])),
            "present": present,
            "missing": missing,
            "changed": changed,
        },
        "finance_safety_boundaries": manifest.get("finance_safety_boundaries", []),
    }


def build_release_manifest(root: Path) -> Dict[str, Any]:
    root = root.resolve()
    return {
        "schema_version": "1.0",
        "package": {"name": "news-thesis-impact-lab", "version": __version__},
        "generated_at": "2026-07-10",
        "finance_safety_boundaries": BOUNDARIES,
        "key_artifacts": [artifact_record(root, path) for path in KEY_ARTIFACTS],
        "distributions": distribution_records(root),
        "commands": {
            "regenerate": REGENERATE_COMMANDS,
            "verify": VERIFY_COMMANDS,
        },
        "notes": [
            "Manifest hashes cover public inputs, docs, generated artifacts, and current-version distributions under dist/.",
            "Wheel and sdist records use placeholders only when the corresponding distribution file is absent.",
        ],
    }


def artifact_record(root: Path, relative_path: Path) -> Dict[str, Any]:
    path = root / relative_path
    record: Dict[str, Any] = {
        "path": relative_path.as_posix(),
        "exists": path.is_file(),
        "sha256": None,
        "bytes": None,
    }
    if path.is_file():
        data = path.read_bytes()
        record["sha256"] = hashlib.sha256(data).hexdigest()
        record["bytes"] = len(data)
    return record


def distribution_records(root: Path) -> List[Dict[str, Any]]:
    dist = root / "dist"
    wheels = sorted(dist.glob(f"news_thesis_impact_lab-{__version__}-*.whl")) if dist.is_dir() else []
    sdists = sorted(dist.glob(f"news_thesis_impact_lab-{__version__}.tar.gz")) if dist.is_dir() else []
    records = [distribution_record(root, "wheel", path) for path in wheels]
    records.extend(distribution_record(root, "sdist", path) for path in sdists)
    if not wheels:
        records.append(distribution_placeholder("wheel"))
    if not sdists:
        records.append(distribution_placeholder("sdist"))
    return records


def distribution_record(root: Path, kind: str, path: Path) -> Dict[str, Any]:
    relative_path = path.relative_to(root)
    data = path.read_bytes()
    return {
        "kind": kind,
        "path": relative_path.as_posix(),
        "exists": True,
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }


def distribution_placeholder(kind: str) -> Dict[str, Any]:
    if kind == "wheel":
        path = f"dist/news_thesis_impact_lab-{__version__}-py3-none-any.whl"
    else:
        path = f"dist/news_thesis_impact_lab-{__version__}.tar.gz"
    return {
        "kind": kind,
        "path": path,
        "exists": False,
        "sha256": None,
        "bytes": None,
        "placeholder": "not built",
        "build_command": "python -m build",
    }


def distribution_suffix(kind: str) -> str:
    if kind == "wheel":
        return "py3-none-any.whl"
    return "tar.gz"


def command_to_regenerate(path_key: str) -> str:
    command_by_prefix = {
        "demo/impact_packet": REGENERATE_COMMANDS[0],
        "demo/index.html": REGENERATE_COMMANDS[0],
        "demo/compare/": REGENERATE_COMMANDS[1],
        "demo/trend/": REGENERATE_COMMANDS[2],
        "demo/scenario/": REGENERATE_COMMANDS[3],
        "demo/ledger/": REGENERATE_COMMANDS[4],
        "demo/journal/": REGENERATE_COMMANDS[5],
        "demo/maturity/": REGENERATE_COMMANDS[6],
        "demo/gallery.html": REGENERATE_COMMANDS[7],
        "demo/visual/": REGENERATE_COMMANDS[8],
        "demo/walkthrough/": REGENERATE_COMMANDS[9],
        "release/manifest": REGENERATE_COMMANDS[10],
        "demo/evidence/": REGENERATE_COMMANDS[11],
        "demo/bundle/": REGENERATE_COMMANDS[12],
    }
    for prefix, command in command_by_prefix.items():
        if path_key.startswith(prefix):
            return command
    if path_key.startswith("examples/"):
        return "static fixture input; edit local JSON then rerun regenerate commands"
    if path_key in {"README.md", "CHANGELOG.md", "pyproject.toml", "docs/review-packet.md"}:
        return "maintained source documentation or package metadata"
    if path_key.startswith("skills/"):
        return "maintained agent skill documentation"
    return "not generated by a public CLI command"


def bundle_role(path: Path) -> str:
    key = path.as_posix()
    if key.startswith("examples/"):
        return "fixture input for deterministic reproduction"
    if key.startswith("release/"):
        return "release manifest evidence"
    if key.startswith("demo/evidence/"):
        return "reviewer evidence hub"
    if key.startswith("demo/bundle/"):
        return "bundle metadata"
    if key.startswith("demo/maturity/"):
        return "release readiness gate evidence"
    if key.startswith("demo/walkthrough/"):
        return "cold-start reproduction guide"
    if key.startswith("demo/visual/"):
        return "static visual and boundary receipt"
    if key.startswith("demo/ledger/"):
        return "repeated-use review ledger"
    if key.startswith("demo/journal/"):
        return "research meeting decision journal draft"
    if key.startswith("demo/scenario/"):
        return "illustrative scenario stress review"
    if key.startswith("demo/trend/"):
        return "multi-period trend review"
    if key.startswith("demo/compare/"):
        return "packet comparison evidence"
    if key.startswith("demo/"):
        return "primary demo artifact"
    if key.startswith("docs/"):
        return "review documentation"
    if key.startswith("skills/"):
        return "agent reuse skill"
    if key == "README.md":
        return "public entrypoint documentation"
    if key == "CHANGELOG.md":
        return "release history"
    if key == "pyproject.toml":
        return "package metadata"
    return "public support artifact"


def package_boundary(path: Path) -> str:
    key = path.as_posix()
    if key.startswith("demo/"):
        return "demo"
    if key.startswith("examples/"):
        return "examples"
    if key.startswith("release/"):
        return "release"
    if key.startswith("docs/"):
        return "docs"
    if key.startswith("skills/"):
        return "agent-skill"
    return "package-root"


def safety_boundary_tags() -> List[str]:
    return ["static-local", "no-live-data", "non-advice", "no-broker", "no-orders", "human-review"]


def render_release_manifest_markdown(manifest: Dict[str, Any]) -> str:
    lines = [
        "# Release Manifest",
        "",
        f"Package: {manifest['package']['name']} {manifest['package']['version']}",
        f"Generated: {manifest['generated_at']}",
        "",
        "## Finance Safety Boundaries",
        "",
        *[f"- {boundary}" for boundary in manifest["finance_safety_boundaries"]],
        "",
        "## Key Artifacts",
        "",
        "| Path | Exists | SHA-256 | Bytes |",
        "| --- | --- | --- | ---: |",
    ]
    for artifact in manifest["key_artifacts"]:
        lines.append(
            f"| `{artifact['path']}` | {str(artifact['exists']).lower()} | "
            f"`{artifact['sha256'] or 'missing'}` | {artifact['bytes'] or 0} |"
        )
    lines.extend(["", "## Distributions", "", "| Kind | Path | Exists | SHA-256 | Bytes | Note |", "| --- | --- | --- | --- | ---: | --- |"])
    for distribution in manifest["distributions"]:
        lines.append(
            f"| {distribution['kind']} | `{distribution['path']}` | {str(distribution['exists']).lower()} | "
            f"`{distribution['sha256'] or 'missing'}` | {distribution['bytes'] or 0} | "
            f"{distribution.get('placeholder', '')} |"
        )
    lines.extend(["", "## Regenerate", ""])
    lines.extend(f"```bash\n{command}\n```" for command in manifest["commands"]["regenerate"])
    lines.extend(["", "## Verify", ""])
    lines.extend(f"```bash\n{command}\n```" for command in manifest["commands"]["verify"])
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in manifest["notes"])
    lines.append("")
    return "\n".join(lines)


def render_bundle_manifest_markdown(manifest: Dict[str, Any]) -> str:
    lines: List[str] = [
        "# Bundle Manifest",
        "",
        f"Package: {manifest['package']['name']} {manifest['package']['version']}",
        f"Generated: {manifest['generated_at']}",
        f"Bundle type: {manifest['bundle_type']}",
        f"Artifact root: `{manifest['artifact_root']}`",
        "",
        "## Finance Safety Boundaries",
        "",
        *[f"- {boundary}" for boundary in manifest["finance_safety_boundaries"]],
        "",
        "## Boundary Tags",
        "",
        *[f"- `{tag}`" for tag in manifest["global_safety_boundary_tags"]],
        "",
        "## Artifacts",
        "",
        "| Source path | Bundle path | Role | Package boundary | Safety tags | Regenerate | SHA-256 | Bytes |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: |",
    ]
    for artifact in manifest["artifacts"]:
        lines.append(
            f"| `{artifact['source_path']}` | `{artifact['bundle_path']}` | {artifact['role']} | "
            f"{artifact['package_boundary']} | {', '.join(artifact['safety_boundary_tags'])} | "
            f"`{artifact['regenerate_command']}` | `{artifact['sha256'] or 'missing'}` | {artifact['bytes'] or 0} |"
        )
    lines.extend(["", "## Inspect", "", f"```bash\n{manifest['commands']['inspect']}\n```", "", "## Notes", ""])
    lines.extend(f"- {note}" for note in manifest["notes"])
    lines.append("")
    return "\n".join(lines)


def render_bundle_manifest_html(manifest: Dict[str, Any]) -> str:
    boundaries = "".join(f"<li>{esc(boundary)}</li>" for boundary in manifest["finance_safety_boundaries"])
    tags = "".join(f"<li><code>{esc(tag)}</code></li>" for tag in manifest["global_safety_boundary_tags"])
    rows = "".join(
        "<tr>"
        f"<td><code>{esc(artifact['source_path'])}</code></td>"
        f"<td><code>{esc(artifact['bundle_path'])}</code></td>"
        f"<td>{esc(artifact['role'])}</td>"
        f"<td>{esc(artifact['package_boundary'])}</td>"
        f"<td>{esc(', '.join(artifact['safety_boundary_tags']))}</td>"
        f"<td><code>{esc(artifact['regenerate_command'])}</code></td>"
        f"<td><code>{esc(artifact['sha256'] or 'missing')}</code></td>"
        f"<td>{artifact['bytes'] or 0}</td>"
        "</tr>"
        for artifact in manifest["artifacts"]
    )
    notes = "".join(f"<li>{esc(note)}</li>" for note in manifest["notes"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Bundle Manifest</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1280px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 1.75rem; }}
    table {{ border-collapse: collapse; width: 100%; background: white; margin-top: 0.75rem; }}
    th, td {{ border: 1px solid #d8dee8; padding: 0.6rem; vertical-align: top; text-align: left; }}
    th {{ background: #e9eef5; }}
    code {{ white-space: normal; overflow-wrap: anywhere; }}
    .note {{ background: #fff; border: 1px solid #d8dee8; padding: 1rem; margin: 1rem 0; }}
  </style>
</head>
<body>
<main>
  <h1>Bundle Manifest</h1>
  <p>Package {esc(manifest['package']['name'])} {esc(manifest['package']['version'])}; generated {esc(manifest['generated_at'])}. Plain files are copied under <code>{esc(manifest['artifact_root'])}</code>.</p>
  <section class="note"><h2>Finance Safety Boundaries</h2><ul>{boundaries}</ul><h2>Boundary Tags</h2><ul>{tags}</ul></section>
  <h2>Artifacts</h2>
  <table><thead><tr><th>Source path</th><th>Bundle path</th><th>Role</th><th>Package boundary</th><th>Safety tags</th><th>Regenerate</th><th>SHA-256</th><th>Bytes</th></tr></thead><tbody>{rows}</tbody></table>
  <h2>Inspect</h2>
  <pre><code>{esc(manifest['commands']['inspect'])}</code></pre>
  <h2>Notes</h2>
  <ul>{notes}</ul>
</main>
</body>
</html>
"""


def render_bundle_inspection_markdown(inspection: Dict[str, Any]) -> str:
    lines = [
        "# Bundle Inspection",
        "",
        f"Manifest: `{inspection['manifest']}`",
        f"Status: {'passed' if inspection['ok'] else 'failed'}",
        f"Total artifacts: {inspection['summary']['total']}",
        f"Present artifacts: {len(inspection['summary']['present'])}",
        f"Missing artifacts: {len(inspection['summary']['missing'])}",
        f"Changed artifacts: {len(inspection['summary']['changed'])}",
        "",
        "## Missing",
        "",
    ]
    lines.extend(f"- `{path}`" for path in inspection["summary"]["missing"] or ["none"])
    lines.extend(["", "## Changed", ""])
    if inspection["summary"]["changed"]:
        lines.extend(
            f"- `{item['path']}` expected `{item['expected_sha256']}` actual `{item['actual_sha256']}`"
            for item in inspection["summary"]["changed"]
        )
    else:
        lines.append("- none")
    lines.extend(["", "## Finance Safety Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in inspection.get("finance_safety_boundaries", []))
    lines.append("")
    return "\n".join(lines)


def write_demo_gallery(out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_demo_gallery(), encoding="utf-8")


def render_demo_gallery() -> str:
    boundaries = "".join(f"<li>{esc(boundary)}</li>" for boundary in BOUNDARIES)
    quickstart = "\n".join(
        [
            "PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo",
            "PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare",
            "PYTHONPATH=src python -m news_thesis_impact_lab trend-history --packets examples/history/*.json --out demo/trend",
            "PYTHONPATH=src python -m news_thesis_impact_lab scenario-stress --packet demo/impact_packet.json --scenarios examples/scenarios.json --out demo/scenario",
            "PYTHONPATH=src python -m news_thesis_impact_lab review-ledger --packet demo/impact_packet.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --previous examples/review_ledger_previous.json --out demo/ledger",
            "PYTHONPATH=src python -m news_thesis_impact_lab decision-journal --packet demo/impact_packet.json --compare demo/compare/compare.json --trend demo/trend/trend_history.json --scenario demo/scenario/scenario_stress.json --ledger demo/ledger/review_ledger.json --evidence demo/evidence/evidence_hub.json --out demo/journal",
            "PYTHONPATH=src python -m news_thesis_impact_lab visual-receipt --out demo/visual",
            "PYTHONPATH=src python -m news_thesis_impact_lab cold-start-walkthrough --out demo/walkthrough",
            "PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release",
            "PYTHONPATH=src python -m news_thesis_impact_lab evidence-hub --out demo/evidence",
            "PYTHONPATH=src python -m news_thesis_impact_lab bundle-export --out demo/bundle",
            "PYTHONPATH=src python -m news_thesis_impact_lab bundle-inspect --manifest demo/bundle/bundle_manifest.json --format json",
            "PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json",
        ]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>news-thesis-impact-lab Demo Gallery</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 0; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 2rem; }}
    h1 {{ font-size: 2rem; margin: 0 0 0.5rem; }}
    h2 {{ font-size: 1.15rem; margin-top: 2rem; }}
    p {{ line-height: 1.55; max-width: 760px; }}
    a {{ color: #2458a8; }}
    .grid {{ display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }}
    .card {{ background: #fff; border: 1px solid #d8dee8; border-radius: 6px; padding: 1rem; }}
    .card strong {{ display: block; margin-bottom: 0.35rem; }}
    pre {{ background: #1f2933; color: #f7f8fa; padding: 1rem; overflow-x: auto; white-space: pre-wrap; }}
    ul {{ padding-left: 1.25rem; }}
  </style>
</head>
<body>
<main>
  <h1>news-thesis-impact-lab Demo Gallery</h1>
  <p>Static, local, research-only finance packet artifacts for reviewing how news catalysts touch thesis claims, exposure notes, warnings, and human review prompts.</p>

  <h2>Demo Artifacts</h2>
  <section class="grid" aria-label="Demo artifact links">
    <a class="card" href="impact_packet.md"><strong>Impact Packet</strong>Markdown review packet with affected tickers, warnings, and prompts.</a>
    <a class="card" href="index.html"><strong>Impact Packet HTML</strong>No-JavaScript table view for quick scanning.</a>
    <a class="card" href="compare/compare.md"><strong>Compare Report</strong>Current versus previous packet deltas.</a>
    <a class="card" href="trend/trend_history.md"><strong>Trend History</strong>Multi-period score direction, warning persistence, exposure trend, and review queue.</a>
    <a class="card" href="trend/trend_history.html"><strong>Trend History HTML</strong>No-JavaScript table view for history review.</a>
    <a class="card" href="scenario/scenario_stress.md"><strong>Scenario Stress</strong>Illustrative macro, sector, and company shock overlap with thesis prompts.</a>
    <a class="card" href="scenario/scenario_stress.html"><strong>Scenario Stress HTML</strong>No-JavaScript table view for stress review.</a>
    <a class="card" href="ledger/review_ledger.md"><strong>Review Ledger</strong>Repeated-use issue ledger with carry-forward, resolved status, severity, stale flags, and evidence links.</a>
    <a class="card" href="ledger/review_ledger.html"><strong>Review Ledger HTML</strong>No-JavaScript table view for ledger review.</a>
    <a class="card" href="journal/decision_journal.md"><strong>Decision Journal</strong>Research meeting draft with thesis questions, evidence excerpts, risk flags, assumptions, placeholder decisions, and follow-up blanks.</a>
    <a class="card" href="journal/decision_journal.html"><strong>Decision Journal HTML</strong>No-JavaScript table view for research meeting preparation.</a>
    <a class="card" href="visual/visual_receipt.md"><strong>Visual Receipt</strong>Static capture receipt with hashes, no-script checks, and boundary checks.</a>
    <a class="card" href="walkthrough/walkthrough.md"><strong>Cold-Start Walkthrough</strong>Two-to-five minute first-user path with commands and failure modes.</a>
    <a class="card" href="evidence/evidence_hub.md"><strong>Evidence Hub</strong>Reviewer matrix with artifact purpose, gates, hashes, no-script checks, boundary coverage, and limitations.</a>
    <a class="card" href="bundle/bundle_manifest.md"><strong>Bundle Manifest</strong>Plain-file agent reuse bundle with hashes, roles, regenerate commands, package boundaries, and safety tags.</a>
    <a class="card" href="bundle/bundle_copy_list.json"><strong>Bundle Copy List</strong>Deterministic copy list for public artifacts under the bundle artifacts directory.</a>
    <a class="card" href="maturity/maturity_report.md"><strong>Maturity Report</strong>Release and promotion readiness gates.</a>
    <a class="card" href="../release/manifest.md"><strong>Release Manifest</strong>Hashes, commands, boundaries, and distribution placeholders.</a>
  </section>

  <h2>Quickstart</h2>
  <pre><code>{esc(quickstart)}</code></pre>

  <h2>Finance Safety Boundaries</h2>
  <ul>{boundaries}</ul>
</main>
</body>
</html>
"""
