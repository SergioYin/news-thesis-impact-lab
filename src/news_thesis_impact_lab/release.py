from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List

from . import __version__
from .engine import build_packet, compare_packets
from .model import BOUNDARIES, load_events, load_portfolio, load_theses
from .render import esc, render_compare_markdown, render_packet_html, render_packet_markdown, write_json


DEMO_FILES = [
    Path("demo/impact_packet.json"),
    Path("demo/impact_packet.md"),
    Path("demo/index.html"),
    Path("demo/gallery.html"),
    Path("demo/compare/compare.json"),
    Path("demo/compare/compare.md"),
]
RELEASE_FILES = [
    Path("release/manifest.json"),
    Path("release/manifest.md"),
]
EXAMPLE_FILES = [
    Path("examples/events.json"),
    Path("examples/theses.json"),
    Path("examples/portfolio.json"),
    Path("examples/previous_packet.json"),
]
KEY_ARTIFACTS = [
    Path("README.md"),
    Path("pyproject.toml"),
    Path("docs/review-packet.md"),
    Path("demo/impact_packet.json"),
    Path("demo/impact_packet.md"),
    Path("demo/index.html"),
    Path("demo/gallery.html"),
    Path("demo/compare/compare.json"),
    Path("demo/compare/compare.md"),
    Path("demo/maturity/maturity_report.json"),
    Path("demo/maturity/maturity_report.md"),
    *EXAMPLE_FILES,
]
REGENERATE_COMMANDS = [
    "PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo",
    "PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare",
    "PYTHONPATH=src python -m news_thesis_impact_lab maturity-report --out demo/maturity",
    "PYTHONPATH=src python -m news_thesis_impact_lab demo-gallery --out demo/gallery.html",
    "PYTHONPATH=src python -m news_thesis_impact_lab release-manifest --out release",
]
VERIFY_COMMANDS = [
    "python -m pytest -q",
    "PYTHONPATH=src python -m news_thesis_impact_lab selfcheck",
    "PYTHONPATH=src python -m news_thesis_impact_lab validate-release --format json",
    "python scripts/privacy_scan.py",
    "git diff --check",
]


def validate_release(root: Path) -> Dict[str, Any]:
    root = root.resolve()
    checks = [
        check_files_exist(root, "demo_artifacts_exist", DEMO_FILES),
        check_files_exist(root, "release_artifacts_exist", RELEASE_FILES),
        check_files_exist(root, "example_files_exist", EXAMPLE_FILES),
        check_demo_boundaries(root),
        check_demo_deterministic(root),
        check_release_manifest_deterministic(root),
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
        if not full_path.is_file():
            missing[path.as_posix()] = BOUNDARIES[:]
            continue
        text = full_path.read_text(encoding="utf-8")
        absent = [boundary for boundary in BOUNDARIES if boundary not in text]
        if absent:
            missing[path.as_posix()] = absent
    return {"name": "demo_boundaries_present", "ok": not missing, "missing_boundaries": missing}


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
        write_demo_gallery(tmp_path / "gallery.html")

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
            if cleaned.startswith("examples/") and cleaned.endswith(".json"):
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
            "Manifest hashes cover public inputs, docs, generated artifacts, and any built distributions under dist/.",
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
    wheels = sorted(dist.glob("*.whl")) if dist.is_dir() else []
    sdists = sorted(dist.glob("*.tar.gz")) if dist.is_dir() else []
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
    return {
        "kind": kind,
        "path": f"dist/news_thesis_impact_lab-{__version__}.{distribution_suffix(kind)}",
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


def write_demo_gallery(out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_demo_gallery(), encoding="utf-8")


def render_demo_gallery() -> str:
    boundaries = "".join(f"<li>{esc(boundary)}</li>" for boundary in BOUNDARIES)
    quickstart = "\n".join(
        [
            "PYTHONPATH=src python -m news_thesis_impact_lab build-packet --events examples/events.json --theses examples/theses.json --portfolio examples/portfolio.json --out demo",
            "PYTHONPATH=src python -m news_thesis_impact_lab compare --current demo/impact_packet.json --previous examples/previous_packet.json --out demo/compare",
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
