#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, Tuple


JsonObject = Dict[str, Any]
HistoryList = List[JsonObject]


@dataclass
class StateSnapshot:
    framework: JsonObject
    history: HistoryList
    metadata: JsonObject
    commit: Optional[JsonObject]
    revision_id: Optional[str]


class StorageAdapter(Protocol):
    """Minimal storage contract for interview state persistence."""

    def load_current(self, session_id: str) -> StateSnapshot:
        ...

    def commit_revision(
        self,
        session_id: str,
        framework: JsonObject,
        history: HistoryList,
        metadata: JsonObject,
        commit: JsonObject,
    ) -> str:
        ...

    def mark_closed(self, session_id: str, closed_at: str) -> None:
        ...

    def archive_session(self, session_id: str) -> None:
        ...

    def resolve_session_dir(
        self, session_id: Optional[str] = None, conversation_id: Optional[str] = None
    ) -> Path:
        ...

    def load_conversation_index(self) -> Dict[str, str]:
        ...

    def upsert_conversation_mapping(self, conversation_id: str, session_id: str) -> None:
        ...

    def remove_conversation_mapping(
        self, conversation_id: str, session_id: Optional[str] = None
    ) -> None:
        ...


class FileStorageAdapter:
    """Filesystem implementation of StorageAdapter.

    This keeps the current repository layout unchanged:
    `state/sessions/{session_id}/CURRENT -> revisions/r{n}/`.
    """

    def __init__(self, state_root: Path) -> None:
        self.state_root = state_root

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def _hash_payload(self, framework: JsonObject, history: HistoryList, metadata: JsonObject) -> str:
        payload = json.dumps(
            {"framework": framework, "history": history, "metadata": metadata},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _load_json(self, path: Path) -> Any:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _write_json(self, path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
            f.write("\n")

    def _write_text_atomic(self, path: Path, text: str) -> None:
        tmp = path.with_suffix(path.suffix + ".tmp")
        path.parent.mkdir(parents=True, exist_ok=True)
        with tmp.open("w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        tmp.replace(path)

    def _session_dir(self, session_id: str) -> Path:
        return self.state_root / "sessions" / session_id

    def _index_path(self) -> Path:
        return self.state_root / "conversation_index.json"

    def _current_revision_id(self, session_dir: Path) -> Optional[str]:
        current = session_dir / "CURRENT"
        if not current.exists():
            return None
        value = current.read_text(encoding="utf-8").strip()
        return value or None

    def _latest_revision_dir(self, session_dir: Path) -> Optional[Tuple[str, Path]]:
        revision_id = self._current_revision_id(session_dir)
        if not revision_id:
            return None
        revision_dir = session_dir / "revisions" / revision_id
        if not revision_dir.exists():
            return None
        return revision_id, revision_dir

    def resolve_session_dir(
        self, session_id: Optional[str] = None, conversation_id: Optional[str] = None
    ) -> Path:
        sessions_root = self.state_root / "sessions"
        if session_id:
            return sessions_root / session_id
        if conversation_id:
            index = self.load_conversation_index()
            mapped = index.get(conversation_id)
            if not isinstance(mapped, str):
                raise FileNotFoundError("conversation_id not found in conversation_index.json")
            return sessions_root / mapped
        candidates = sorted([p for p in sessions_root.glob("*") if p.is_dir()], reverse=True)
        if not candidates:
            raise FileNotFoundError("no session directory found")
        return candidates[0]

    def load_conversation_index(self) -> Dict[str, str]:
        index_path = self._index_path()
        if not index_path.exists():
            return {}
        raw = self._load_json(index_path)
        if not isinstance(raw, dict):
            return {}
        return {str(k): str(v) for k, v in raw.items()}

    def upsert_conversation_mapping(self, conversation_id: str, session_id: str) -> None:
        index = self.load_conversation_index()
        mapped = index.get(conversation_id)
        if mapped not in (None, session_id):
            raise ValueError(
                f"conversation_id already mapped to another session: {conversation_id} -> {mapped}"
            )
        index[conversation_id] = session_id
        self._write_json(self._index_path(), index)

    def remove_conversation_mapping(self, conversation_id: str, session_id: Optional[str] = None) -> None:
        index = self.load_conversation_index()
        mapped = index.get(conversation_id)
        if mapped is None:
            return
        if session_id is not None and mapped != session_id:
            return
        del index[conversation_id]
        self._write_json(self._index_path(), index)

    def load_current(self, session_id: str) -> StateSnapshot:
        session_dir = self._session_dir(session_id)
        latest = self._latest_revision_dir(session_dir)
        if latest is None:
            root = session_dir
            revision_id = None
        else:
            revision_id, root = latest

        framework = self._load_json(root / "framework.json")
        history = self._load_json(root / "history.json")
        metadata = self._load_json(root / "metadata.json")
        commit_path = root / "commit.json"
        commit = self._load_json(commit_path) if commit_path.exists() else None
        return StateSnapshot(
            framework=framework,
            history=history,
            metadata=metadata,
            commit=commit,
            revision_id=revision_id,
        )

    def commit_revision(
        self,
        session_id: str,
        framework: JsonObject,
        history: HistoryList,
        metadata: JsonObject,
        commit: JsonObject,
    ) -> str:
        session_dir = self._session_dir(session_id)
        revisions_root = session_dir / "revisions"
        revisions_root.mkdir(parents=True, exist_ok=True)
        nums = [
            int(p.name[1:])
            for p in revisions_root.glob("r*")
            if p.is_dir() and p.name[1:].isdigit()
        ]
        next_n = (max(nums) if nums else 0) + 1
        revision_id = f"r{next_n:06d}"
        temp_revision = revisions_root / f".{revision_id}.tmp"
        final_revision = revisions_root / revision_id
        if temp_revision.exists():
            shutil.rmtree(temp_revision, ignore_errors=True)
        temp_revision.mkdir(parents=True, exist_ok=True)
        self._write_json(temp_revision / "framework.json", framework)
        self._write_json(temp_revision / "history.json", history)
        self._write_json(temp_revision / "metadata.json", metadata)
        self._write_json(temp_revision / "commit.json", commit)
        temp_revision.replace(final_revision)
        self._write_text_atomic(session_dir / "CURRENT", revision_id + "\n")
        return revision_id

    def mark_closed(self, session_id: str, closed_at: str) -> None:
        snapshot = self.load_current(session_id)
        session = snapshot.framework.get("session", {})
        session["status"] = "closed"
        session["closed_at"] = closed_at
        snapshot.framework["session"] = session
        snapshot.metadata["status"] = "closed"
        snapshot.metadata["closed_at"] = closed_at
        snapshot.metadata["last_accessed"] = closed_at
        snapshot.metadata["last_updated"] = closed_at
        commit = {
            "session_id": session_id,
            "turn_id": f"system_close_{closed_at}",
            "state_version": snapshot.metadata.get("state_version", "2.0.0"),
            "schema_version": snapshot.metadata.get("schema_version", "2.0.0"),
            "timestamp": self._now_iso(),
            "content_hash": self._hash_payload(snapshot.framework, snapshot.history, snapshot.metadata),
        }
        snapshot.metadata["last_successful_commit"] = commit
        revision_id = self.commit_revision(
            session_id, snapshot.framework, snapshot.history, snapshot.metadata, commit
        )
        snapshot.metadata["last_successful_commit"]["revision_id"] = revision_id
        session_dir = self._session_dir(session_id)
        self._write_json(session_dir / "revisions" / revision_id / "metadata.json", snapshot.metadata)

    def mark_cleanup_pending(self, session_id: str, reason: str, timestamp: Optional[str] = None) -> None:
        at = timestamp or self._now_iso()
        snapshot = self.load_current(session_id)
        snapshot.metadata["cleanup_pending"] = True
        snapshot.metadata["cleanup_pending_reason"] = reason
        snapshot.metadata["last_updated"] = at
        session = snapshot.framework.get("session", {})
        session["cleanup_pending"] = True
        session["cleanup_pending_reason"] = reason
        session.setdefault("status", snapshot.metadata.get("status", "active"))
        snapshot.framework["session"] = session
        commit = {
            "session_id": session_id,
            "turn_id": f"system_cleanup_{at}",
            "state_version": snapshot.metadata.get("state_version", "2.0.0"),
            "schema_version": snapshot.metadata.get("schema_version", "2.0.0"),
            "timestamp": self._now_iso(),
            "content_hash": self._hash_payload(snapshot.framework, snapshot.history, snapshot.metadata),
        }
        snapshot.metadata["last_successful_commit"] = commit
        revision_id = self.commit_revision(
            session_id, snapshot.framework, snapshot.history, snapshot.metadata, commit
        )
        snapshot.metadata["last_successful_commit"]["revision_id"] = revision_id
        session_dir = self._session_dir(session_id)
        self._write_json(session_dir / "revisions" / revision_id / "metadata.json", snapshot.metadata)

    def archive_session(self, session_id: str) -> None:
        src = self._session_dir(session_id)
        dst = self.state_root / "archive" / session_id
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.exists():
            src.replace(dst)
