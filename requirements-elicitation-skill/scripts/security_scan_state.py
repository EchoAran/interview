#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

from state_lib.config import resolve_state_root, skill_dir_from_file


PATTERNS = [
    re.compile(r"(?i)\bapi[_-]?key\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"),
    re.compile(r"(?i)\btoken\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]{12,}"),
    re.compile(r"(?i)\bpassword\b\s*[:=]\s*['\"]?.{6,}"),
    re.compile(r"(?i)\bsecret\b\s*[:=]\s*['\"]?.{6,}"),
    re.compile(r"(?i)\baws[_-]?access[_-]?key[_-]?id\b"),
    re.compile(r"(?i)\b-----BEGIN (?:RSA|EC|OPENSSH|PRIVATE) KEY-----"),
]


def scan_file(path: Path) -> List[Tuple[int, str]]:
    hits: List[Tuple[int, str]] = []
    text = path.read_text(encoding="utf-8", errors="ignore")
    for i, line in enumerate(text.splitlines(), start=1):
        for pattern in PATTERNS:
            if pattern.search(line):
                hits.append((i, line.strip()))
                break
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan state files for sensitive content")
    parser.add_argument("--state-root", default=None)
    args = parser.parse_args()

    skill_dir = skill_dir_from_file(__file__)
    root = resolve_state_root(args.state_root, skill_dir=skill_dir)
    if not root.exists():
        print(f"[OK] state root not found: {root}")
        return 0

    files = list(root.rglob("*.json")) + list(root.rglob("*.jsonl")) + list(root.rglob("cleanup.log"))
    findings = []
    for file_path in files:
        hits = scan_file(file_path)
        for line_no, content in hits:
            findings.append((file_path, line_no, content))

    if findings:
        print("[ERROR] sensitive content findings:")
        for file_path, line_no, content in findings:
            print(f" - {file_path}:{line_no}: {content}")
        return 1

    print(f"[OK] no sensitive pattern matched in {len(files)} scanned files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
