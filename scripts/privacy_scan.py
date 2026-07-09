#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLOCKED = [
    "Her" + "mes",
    "Fei" + "shu",
    "/" + "mnt" + "/" + "c",
    "x" + "jyin",
    re.compile(r"ghp_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
]
SKIP_DIRS = {".git", ".venv", "__pycache__", "dist", "build", "*.egg-info"}


def main() -> int:
    findings = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in BLOCKED:
            if isinstance(pattern, str):
                if pattern in text:
                    findings.append(f"{path.relative_to(ROOT)}: contains {pattern}")
            elif pattern.search(text):
                findings.append(f"{path.relative_to(ROOT)}: matches {pattern.pattern}")
    if findings:
        print("privacy scan failed")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("privacy scan passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
