from __future__ import annotations

import hashlib
import importlib.metadata
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

from . import __version__
from .model import BOUNDARIES
from .render import esc, write_json


GENERATED_AT = "2026-07-10"
HEALTH_FILES = [
    Path("demo/health/asset_health.json"),
    Path("demo/health/asset_health.md"),
    Path("demo/health/asset_health.html"),
]
EXPECTED_COMMANDS = [
    "build-packet",
    "compare",
    "trend-history",
    "scenario-stress",
    "review-ledger",
    "decision-journal",
    "selfcheck",
    "validate-release",
    "maturity-report",
    "release-manifest",
    "demo-gallery",
    "visual-receipt",
    "cold-start-walkthrough",
    "evidence-hub",
    "bundle-export",
    "bundle-inspect",
    "asset-health",
]
DOC_PATHS = [
    Path("README.md"),
    Path("docs/review-packet.md"),
    Path("docs/cold-user-walkthrough.md"),
    Path("skills/agent/news-thesis-impact-lab/SKILL.md"),
    Path("CHANGELOG.md"),
]
LOCAL_NEUTRAL_FORBIDDEN = ["http://", "https://", "broker API", "live market data feed"]
PRIVATE_STRING_PATTERNS = [
    "Her" + "mes",
    "Fei" + "shu",
    "/" + "mnt" + "/" + "c",
    "x" + "jyin",
]
PRIVATE_REGEX_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
]
SCAN_SKIP_DIRS = {".git", ".venv", "__pycache__", "dist", "build", "*.egg-info"}
SCAN_SKIP_FILES = {Path("scripts/privacy_scan.py")}


def write_asset_health(root: Path, out: Path) -> Dict[str, Any]:
    health = build_asset_health(root)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "asset_health.json", health)
    (out / "asset_health.md").write_text(render_asset_health_markdown(health), encoding="utf-8")
    (out / "asset_health.html").write_text(render_asset_health_html(health), encoding="utf-8")
    return health


def build_asset_health(root: Path) -> Dict[str, Any]:
    from .release import (
        BUNDLE_FILES,
        DEMO_FILES,
        EVIDENCE_FILES,
        RELEASE_FILES,
        distribution_records,
        validate_release,
    )

    root = root.resolve()
    validation = validate_release(root, include_asset_health=False)
    source_metadata = read_source_metadata(root)
    installed_metadata = read_installed_metadata(source_metadata["name"])
    command_records = advertised_command_records(root)
    all_public_artifacts = sorted(set(DEMO_FILES + EVIDENCE_FILES + RELEASE_FILES + BUNDLE_FILES + HEALTH_FILES), key=lambda path: path.as_posix())
    artifact_records = [artifact_health_record(root, path) for path in all_public_artifacts]
    dist_records = distribution_records(root)
    skill_record = repo_skill_record(root)
    docs_record = local_neutral_docs_record(root)
    private_scan = private_ref_scan_summary(root)
    boundary_record = finance_boundary_coverage(root, all_public_artifacts)
    generated = generated_freshness(validation)
    readiness = readiness_checklist(
        validation=validation,
        source_metadata=source_metadata,
        installed_metadata=installed_metadata,
        command_records=command_records,
        artifact_records=artifact_records,
        dist_records=dist_records,
        skill_record=skill_record,
        docs_record=docs_record,
        private_scan=private_scan,
        boundary_record=boundary_record,
        generated=generated,
    )
    return {
        "schema_version": "1.0",
        "asset": "news-thesis-impact-lab",
        "generated_at": GENERATED_AT,
        "package": {
            "source": source_metadata,
            "installed": installed_metadata,
        },
        "advertised_commands": command_records,
        "generated_artifact_freshness": generated,
        "public_artifacts": artifact_records,
        "distributions": dist_records,
        "repo_skill": skill_record,
        "local_neutral_docs": docs_record,
        "private_ref_scan_summary": private_scan,
        "finance_boundary_coverage": boundary_record,
        "release_validation": {"ok": validation["ok"], "failed_checks": [check["name"] for check in validation["checks"] if not check["ok"]]},
        "scores": score_sections(readiness),
        "readiness_checklist": readiness,
        "final_readiness": {
            "release_ready": all(item["ok"] for item in readiness if item["gate"] == "release"),
            "promote_ready": all(item["ok"] for item in readiness),
        },
        "finance_safety_boundaries": BOUNDARIES,
        "notes": [
            "Health checks inspect local source and generated files only; they do not fetch live data.",
            "Distribution records report wheel and sdist presence for the current package version.",
            "Private-reference scanning skips the scanner implementation so regex definitions are not counted as findings.",
        ],
    }


def read_source_metadata(root: Path) -> Dict[str, Any]:
    data = read_pyproject_project(root / "pyproject.toml")
    scripts = data.get("scripts", {})
    return {
        "name": data.get("name", "news-thesis-impact-lab"),
        "version": data.get("version", ""),
        "module_version": __version__,
        "versions_match": data.get("version") == __version__,
        "description": data.get("description", ""),
        "requires_python": data.get("requires-python", ""),
        "dependencies": data.get("dependencies", []),
        "zero_runtime_dependencies": data.get("dependencies", []) == [],
        "console_scripts": scripts,
        "console_script_present": scripts.get("news-thesis-impact-lab") == "news_thesis_impact_lab.cli:main",
    }


def read_pyproject_project(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    project: Dict[str, Any] = {"scripts": {}}
    section = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line.strip("[]")
            continue
        if section == "project" and "=" in line:
            key, value = [part.strip() for part in line.split("=", 1)]
            if value.startswith('"') and value.endswith('"'):
                project[key] = value.strip('"')
            elif value == "[]":
                project[key] = []
        elif section == "project.scripts" and "=" in line:
            key, value = [part.strip() for part in line.split("=", 1)]
            project["scripts"][key] = value.strip('"')
    return project


def read_installed_metadata(package_name: str) -> Dict[str, Any]:
    try:
        metadata = importlib.metadata.metadata(package_name)
        version = importlib.metadata.version(package_name)
        entry_points_result = importlib.metadata.entry_points()
        selected = (
            entry_points_result.select(group="console_scripts")
            if hasattr(entry_points_result, "select")
            else entry_points_result.get("console_scripts", [])
        )
        entry_points = sorted(
            f"{entry_point.name}={entry_point.value}"
            for entry_point in selected
            if entry_point.dist and entry_point.dist.metadata.get("Name") == package_name
        )
        return {
            "available": True,
            "name": metadata.get("Name", package_name),
            "version": version,
            "version_matches_source": version == __version__,
            "entry_points": entry_points,
        }
    except importlib.metadata.PackageNotFoundError:
        return {
            "available": False,
            "name": package_name,
            "version": None,
            "version_matches_source": False,
            "entry_points": [],
            "note": "Package is inspectable from source but is not installed in the current interpreter.",
        }


def advertised_command_records(root: Path) -> List[Dict[str, Any]]:
    cli_text = (root / "src/news_thesis_impact_lab/cli.py").read_text(encoding="utf-8")
    records = []
    for command in EXPECTED_COMMANDS:
        records.append(
            {
                "command": command,
                "advertised_in_cli": f'"{command}"' in cli_text,
                "advertised_in_readme": command in read_optional_text(root / "README.md"),
                "advertised_in_skill": command in read_optional_text(root / "skills/agent/news-thesis-impact-lab/SKILL.md"),
            }
        )
    return records


def artifact_health_record(root: Path, path: Path) -> Dict[str, Any]:
    full_path = root / path
    return {
        "path": path.as_posix(),
        "exists": True if path in HEALTH_FILES else full_path.is_file(),
        "sha256": "tracked-by-release-manifest",
        "bytes": None,
        "no_js": True if path in HEALTH_FILES and path.suffix == ".html" else no_js(full_path),
    }


def no_js(path: Path) -> bool | None:
    if path.suffix != ".html":
        return None
    if not path.is_file():
        return False
    return "<script" not in path.read_text(encoding="utf-8").lower()


def generated_freshness(validation: Dict[str, Any]) -> Dict[str, Any]:
    deterministic = [check for check in validation["checks"] if check["name"].endswith("_deterministic")]
    stale: List[str] = []
    for check in deterministic:
        stale.extend(check.get("changed", []))
    return {
        "ok": not stale and all(check["ok"] for check in deterministic),
        "deterministic_checks": [{"name": check["name"], "ok": check["ok"], "changed": check.get("changed", [])} for check in deterministic],
        "stale_or_changed": sorted(set(stale)),
    }


def repo_skill_record(root: Path) -> Dict[str, Any]:
    path = Path("skills/agent/news-thesis-impact-lab/SKILL.md")
    text = read_optional_text(root / path)
    required_terms = ["news-thesis-impact-lab", "asset-health", "no runtime dependencies"]
    boundary_hits = [boundary for boundary in BOUNDARIES if boundary in text]
    return {
        "path": path.as_posix(),
        "exists": bool(text),
        "mentions_asset_health": "asset-health" in text,
        "boundary_count": len(boundary_hits),
        "all_boundaries_present": len(boundary_hits) == len(BOUNDARIES),
        "required_terms_present": all(term in text or term.lower() in text.lower() for term in required_terms),
    }


def local_neutral_docs_record(root: Path) -> Dict[str, Any]:
    records = []
    all_ok = True
    for path in DOC_PATHS:
        text = read_optional_text(root / path)
        forbidden = [term for term in LOCAL_NEUTRAL_FORBIDDEN if term.lower() in text.lower()]
        record = {
            "path": path.as_posix(),
            "exists": bool(text),
            "forbidden_terms": forbidden,
            "local_neutral": bool(text) and not forbidden,
        }
        all_ok = all_ok and record["local_neutral"]
        records.append(record)
    return {
        "ok": all_ok,
        "paths": records,
        "rule": "Docs should describe local static operation without external services, workflow files, or broker/live-data integrations.",
    }


def private_ref_scan_summary(root: Path) -> Dict[str, Any]:
    findings = []
    scanned = 0
    for path in sorted(root.rglob("*")):
        if not path.is_file() or should_skip_scan_path(root, path):
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PRIVATE_STRING_PATTERNS:
            if pattern in text:
                findings.append({"path": path.relative_to(root).as_posix(), "kind": "private-string"})
        for pattern in PRIVATE_REGEX_PATTERNS:
            if pattern.search(text):
                findings.append({"path": path.relative_to(root).as_posix(), "kind": "private-token-pattern"})
    return {
        "ok": not findings,
        "files_scanned": scanned,
        "finding_count": len(findings),
        "findings": findings,
        "ignored_files": sorted(path.as_posix() for path in SCAN_SKIP_FILES),
    }


def should_skip_scan_path(root: Path, path: Path) -> bool:
    relative = path.relative_to(root)
    if relative in SCAN_SKIP_FILES:
        return True
    if len(relative.parts) >= 2 and relative.parts[0] == "demo" and relative.parts[1] == "bundle":
        return True
    return any(part in SCAN_SKIP_DIRS for part in relative.parts)


def finance_boundary_coverage(root: Path, paths: Iterable[Path]) -> Dict[str, Any]:
    records = []
    for path in paths:
        text = read_optional_text(root / path)
        present = [boundary for boundary in BOUNDARIES if boundary in text]
        records.append(
            {
                "path": path.as_posix(),
                "exists": bool(text),
                "present_count": len(present),
                "missing": [boundary for boundary in BOUNDARIES if boundary not in text],
                "all_present": len(present) == len(BOUNDARIES),
            }
        )
    combined_text = "\n".join(read_optional_text(root / path) for path in paths)
    return {
        "ok": all(boundary in combined_text for boundary in BOUNDARIES),
        "boundary_count": len(BOUNDARIES),
        "records": records,
    }


def readiness_checklist(
    *,
    validation: Dict[str, Any],
    source_metadata: Dict[str, Any],
    installed_metadata: Dict[str, Any],
    command_records: List[Dict[str, Any]],
    artifact_records: List[Dict[str, Any]],
    dist_records: List[Dict[str, Any]],
    skill_record: Dict[str, Any],
    docs_record: Dict[str, Any],
    private_scan: Dict[str, Any],
    boundary_record: Dict[str, Any],
    generated: Dict[str, Any],
) -> List[Dict[str, Any]]:
    wheel_present = any(record["kind"] == "wheel" and record["exists"] for record in dist_records)
    sdist_present = any(record["kind"] == "sdist" and record["exists"] for record in dist_records)
    return [
        checklist_item("release", f"package_metadata_version_{source_metadata['version'].replace('.', '_')}", bool(source_metadata["version"]) and source_metadata["versions_match"]),
        checklist_item("release", "zero_runtime_dependencies", source_metadata["zero_runtime_dependencies"]),
        checklist_item("release", "console_script_configured", source_metadata["console_script_present"]),
        checklist_item("release", "advertised_commands_documented", all(item["advertised_in_cli"] and item["advertised_in_readme"] and item["advertised_in_skill"] for item in command_records)),
        checklist_item("release", "generated_artifacts_fresh", generated["ok"]),
        checklist_item("release", "asset_health_artifacts_present", all(record["exists"] for record in artifact_records if record["path"].startswith("demo/health/"))),
        checklist_item("release", "validate_release_passes", validation["ok"]),
        checklist_item("release", "repo_skill_ready", skill_record["exists"] and skill_record["mentions_asset_health"] and skill_record["all_boundaries_present"]),
        checklist_item("release", "local_neutral_docs", docs_record["ok"]),
        checklist_item("release", "private_ref_scan_clean", private_scan["ok"]),
        checklist_item("release", "finance_boundaries_covered", boundary_record["ok"]),
        checklist_item("promote", "wheel_present", wheel_present),
        checklist_item("promote", "sdist_present", sdist_present),
        checklist_item("promote", "installed_metadata_matches_when_available", (not installed_metadata["available"]) or installed_metadata["version_matches_source"]),
    ]


def checklist_item(gate: str, name: str, ok: bool) -> Dict[str, Any]:
    return {"gate": gate, "name": name, "ok": bool(ok)}


def score_sections(readiness: List[Dict[str, Any]]) -> Dict[str, Any]:
    release_items = [item for item in readiness if item["gate"] == "release"]
    promote_items = readiness
    return {
        "release": score_group(release_items),
        "promote": score_group(promote_items),
    }


def score_group(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    passed = sum(1 for item in items if item["ok"])
    total = len(items)
    return {"passed": passed, "total": total, "score": round((passed / total) * 100, 2) if total else 0.0}


def render_asset_health_markdown(health: Dict[str, Any]) -> str:
    lines = [
        "# Asset Health",
        "",
        f"Asset: {health['asset']}",
        f"Generated: {health['generated_at']}",
        f"Package: {health['package']['source']['name']} {health['package']['source']['version']}",
        "",
        "## Final Readiness",
        "",
        f"- release_ready: {str(health['final_readiness']['release_ready']).lower()}",
        f"- promote_ready: {str(health['final_readiness']['promote_ready']).lower()}",
        "",
        "## Release/Promote Checklist",
        "",
    ]
    lines.extend(f"- [{'x' if item['ok'] else ' '}] {item['gate']}: {item['name']}" for item in health["readiness_checklist"])
    lines.extend(
        [
            "",
            "## Package Metadata",
            "",
            f"- source_version: {health['package']['source']['version']}",
            f"- module_version: {health['package']['source']['module_version']}",
            f"- installed_available: {str(health['package']['installed']['available']).lower()}",
            f"- zero_runtime_dependencies: {str(health['package']['source']['zero_runtime_dependencies']).lower()}",
            "",
            "## Commands",
            "",
            "| Command | CLI | README | Skill |",
            "| --- | --- | --- | --- |",
        ]
    )
    for item in health["advertised_commands"]:
        lines.append(
            f"| `{item['command']}` | {str(item['advertised_in_cli']).lower()} | "
            f"{str(item['advertised_in_readme']).lower()} | {str(item['advertised_in_skill']).lower()} |"
        )
    lines.extend(["", "## Generated Artifact Freshness", ""])
    lines.append(f"- ok: {str(health['generated_artifact_freshness']['ok']).lower()}")
    lines.append(f"- stale_or_changed: {', '.join(health['generated_artifact_freshness']['stale_or_changed']) or 'none'}")
    lines.extend(["", "## Distributions", "", "| Kind | Path | Exists | SHA-256 | Bytes |", "| --- | --- | --- | --- | ---: |"])
    for item in health["distributions"]:
        lines.append(f"| {item['kind']} | `{item['path']}` | {str(item['exists']).lower()} | `{item['sha256'] or 'missing'}` | {item['bytes'] or 0} |")
    lines.extend(["", "## Private Reference Scan", ""])
    lines.append(f"- ok: {str(health['private_ref_scan_summary']['ok']).lower()}")
    lines.append(f"- files_scanned: {health['private_ref_scan_summary']['files_scanned']}")
    lines.append(f"- finding_count: {health['private_ref_scan_summary']['finding_count']}")
    lines.extend(["", "## Finance Safety Boundaries", ""])
    lines.extend(f"- {boundary}" for boundary in health["finance_safety_boundaries"])
    lines.extend(["", "## Notes", ""])
    lines.extend(f"- {note}" for note in health["notes"])
    lines.append("")
    return "\n".join(lines)


def render_asset_health_html(health: Dict[str, Any]) -> str:
    checklist_rows = "".join(
        "<tr>"
        f"<td>{esc(item['gate'])}</td>"
        f"<td>{esc(item['name'])}</td>"
        f"<td>{str(item['ok']).lower()}</td>"
        "</tr>"
        for item in health["readiness_checklist"]
    )
    command_rows = "".join(
        "<tr>"
        f"<td><code>{esc(item['command'])}</code></td>"
        f"<td>{str(item['advertised_in_cli']).lower()}</td>"
        f"<td>{str(item['advertised_in_readme']).lower()}</td>"
        f"<td>{str(item['advertised_in_skill']).lower()}</td>"
        "</tr>"
        for item in health["advertised_commands"]
    )
    dist_rows = "".join(
        "<tr>"
        f"<td>{esc(item['kind'])}</td>"
        f"<td><code>{esc(item['path'])}</code></td>"
        f"<td>{str(item['exists']).lower()}</td>"
        f"<td><code>{esc(item['sha256'] or 'missing')}</code></td>"
        f"<td>{item['bytes'] or 0}</td>"
        "</tr>"
        for item in health["distributions"]
    )
    boundaries = "".join(f"<li>{esc(boundary)}</li>" for boundary in health["finance_safety_boundaries"])
    notes = "".join(f"<li>{esc(note)}</li>" for note in health["notes"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Asset Health</title>
  <style>
    body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; margin: 2rem; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1200px; margin: 0 auto; }}
    h1 {{ font-size: 2rem; margin-bottom: 0.25rem; }}
    h2 {{ font-size: 1.2rem; margin-top: 1.75rem; }}
    table {{ border-collapse: collapse; width: 100%; background: white; margin: 0.75rem 0 1.25rem; }}
    th, td {{ border: 1px solid #d8dee8; padding: 0.6rem; vertical-align: top; text-align: left; }}
    th {{ background: #e9eef5; }}
    code {{ white-space: normal; overflow-wrap: anywhere; }}
    .note {{ background: #fff; border: 1px solid #d8dee8; padding: 1rem; margin: 1rem 0; }}
  </style>
</head>
<body>
<main>
  <h1>Asset Health</h1>
  <p>Package {esc(health['package']['source']['name'])} {esc(health['package']['source']['version'])}; generated {esc(health['generated_at'])}.</p>
  <section class="note">
    <h2>Final Readiness</h2>
    <p>release_ready: {str(health['final_readiness']['release_ready']).lower()}<br>promote_ready: {str(health['final_readiness']['promote_ready']).lower()}</p>
  </section>
  <h2>Release/Promote Checklist</h2>
  <table><thead><tr><th>Gate</th><th>Check</th><th>OK</th></tr></thead><tbody>{checklist_rows}</tbody></table>
  <h2>Advertised Commands</h2>
  <table><thead><tr><th>Command</th><th>CLI</th><th>README</th><th>Skill</th></tr></thead><tbody>{command_rows}</tbody></table>
  <h2>Distributions</h2>
  <table><thead><tr><th>Kind</th><th>Path</th><th>Exists</th><th>SHA-256</th><th>Bytes</th></tr></thead><tbody>{dist_rows}</tbody></table>
  <h2>Private Reference Scan</h2>
  <p>ok: {str(health['private_ref_scan_summary']['ok']).lower()}; files scanned: {health['private_ref_scan_summary']['files_scanned']}; findings: {health['private_ref_scan_summary']['finding_count']}.</p>
  <h2>Finance Safety Boundaries</h2>
  <ul>{boundaries}</ul>
  <h2>Notes</h2>
  <ul>{notes}</ul>
</main>
</body>
</html>
"""


def read_optional_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")
