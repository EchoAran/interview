from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional


def skill_dir_from_file(current_file: str) -> Path:
    # current_file is expected to be under <skill_dir>/scripts/state_lib/
    return Path(current_file).resolve().parents[2]


def _load_json_if_exists(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _resolve_candidate(raw_path: str, skill_dir: Path) -> Path:
    candidate = Path(raw_path).expanduser()
    if not candidate.is_absolute():
        candidate = skill_dir / candidate
    return candidate.resolve()


def resolve_state_root(
    cli_state_root: Optional[str],
    *,
    skill_dir: Path,
) -> Path:
    """Resolve state root with safe default and optional config override.

    Priority:
    1) CLI argument.
    2) skill.config.json -> state_root
    3) config/state.json -> state_root
    4) default <skill_dir>/state

    Safety:
    - resolved path must stay under one of allowed roots.
    - default allowed roots: [<skill_dir>]
    - optional config can extend allowlist with `allowed_state_roots`.
    """
    skill_config = _load_json_if_exists(skill_dir / "skill.config.json") or {}
    state_config = _load_json_if_exists(skill_dir / "config" / "state.json") or {}

    configured_state_root = skill_config.get("state_root") or state_config.get("state_root")
    selected = cli_state_root or configured_state_root or "state"
    resolved = _resolve_candidate(str(selected), skill_dir)

    allowed_roots = [skill_dir.resolve()]
    raw_allowlist = skill_config.get("allowed_state_roots") or state_config.get("allowed_state_roots")
    if isinstance(raw_allowlist, list):
        for item in raw_allowlist:
            if isinstance(item, str) and item.strip():
                allowed_roots.append(_resolve_candidate(item, skill_dir))

    if not any(resolved.is_relative_to(root) for root in allowed_roots):
        allowed = ", ".join(str(p) for p in allowed_roots)
        raise ValueError(
            f"resolved state_root is outside allowed roots: {resolved}; allowed=[{allowed}]"
        )

    resolved.mkdir(parents=True, exist_ok=True)
    return resolved
