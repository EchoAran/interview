from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from ..storage_adapter import FileStorageAdapter, StateSnapshot  # package mode
except ImportError:  # pragma: no cover - script mode fallback
    from storage_adapter import FileStorageAdapter, StateSnapshot


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _hash_payload(framework: Dict[str, Any], history: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
    payload = json.dumps(
        {"framework": framework, "history": history, "metadata": metadata},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def state_load(
    *,
    state_root: Path,
    session_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
) -> StateSnapshot:
    adapter = FileStorageAdapter(state_root)
    session_dir = adapter.resolve_session_dir(session_id=session_id, conversation_id=conversation_id)
    return adapter.load_current(session_dir.name)


def state_commit(
    *,
    state_root: Path,
    session_id: str,
    turn_id: str,
    framework: Dict[str, Any],
    history: List[Dict[str, Any]],
    metadata: Dict[str, Any],
) -> str:
    adapter = FileStorageAdapter(state_root)
    commit = {
        "session_id": session_id,
        "turn_id": turn_id,
        "state_version": metadata.get("state_version", "2.0.0"),
        "schema_version": metadata.get("schema_version", "2.0.0"),
        "timestamp": _now_iso(),
        "content_hash": _hash_payload(framework, history, metadata),
    }
    metadata["last_successful_commit"] = commit
    revision_id = adapter.commit_revision(session_id, framework, history, metadata, commit)
    if isinstance(metadata.get("last_successful_commit"), dict):
        metadata["last_successful_commit"]["revision_id"] = revision_id
    return revision_id


def state_mark_closed(*, state_root: Path, session_id: str, closed_at: Optional[str] = None) -> None:
    adapter = FileStorageAdapter(state_root)
    adapter.mark_closed(session_id=session_id, closed_at=closed_at or _now_iso())
