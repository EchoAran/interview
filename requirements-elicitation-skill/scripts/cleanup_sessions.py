#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from storage_adapter import FileStorageAdapter
from validate_state import bootstrap_current_revision


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now_utc().strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_iso(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def log_cleanup(log_path: Path, row: Dict[str, Any]) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def archive_closed_session(
    session_dir: Path,
    dry_run: bool,
    log_path: Path,
    reason: str,
    storage_adapter: FileStorageAdapter,
) -> None:
    current_revision_id = bootstrap_current_revision(session_dir)
    revision_dir = session_dir / "revisions" / current_revision_id if current_revision_id else session_dir
    metadata_path = revision_dir / "metadata.json"
    if not metadata_path.exists():
        return
    metadata = load_json(metadata_path)
    if metadata.get("status") != "closed":
        return
    closed_at = metadata.get("closed_at") or now_iso()

    if not dry_run:
        storage_adapter.mark_closed(session_dir.name, closed_at)
        storage_adapter.mark_cleanup_pending(
            session_dir.name, reason="archived_waiting_retention_delete", timestamp=closed_at
        )
        conversation_id = metadata.get("conversation_id")
        if isinstance(conversation_id, str):
            storage_adapter.remove_conversation_mapping(conversation_id, session_id=session_dir.name)
        storage_adapter.archive_session(session_dir.name)
    log_cleanup(
        log_path,
        {
            "session_id": session_dir.name,
            "closed_at": closed_at,
            "deleted_at": None,
            "reason": reason,
            "result": "archived" if not dry_run else "dry_run_archive",
        },
    )


def delete_archived(
    session_dir: Path, dry_run: bool, log_path: Path, reason: str, storage_adapter: FileStorageAdapter
) -> None:
    deleted_at = now_iso()
    current_revision_id = bootstrap_current_revision(session_dir)
    revision_dir = session_dir / "revisions" / current_revision_id if current_revision_id else session_dir
    metadata_path = revision_dir / "metadata.json"
    if metadata_path.exists():
        metadata = load_json(metadata_path)
        conversation_id = metadata.get("conversation_id")
        if isinstance(conversation_id, str):
            if not dry_run:
                storage_adapter.remove_conversation_mapping(conversation_id, session_id=session_dir.name)
    if not dry_run:
        shutil.rmtree(session_dir, ignore_errors=True)
    log_cleanup(
        log_path,
        {
            "session_id": session_dir.name,
            "closed_at": None,
            "deleted_at": deleted_at,
            "reason": reason,
            "result": "deleted" if not dry_run else "dry_run_delete",
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive/delete stale sessions with two-phase cleanup")
    parser.add_argument("--state-root", default="state")
    parser.add_argument("--archive-days", type=int, default=30)
    parser.add_argument("--delete-days", type=int, default=90)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    state_root = Path(args.state_root)
    sessions_root = state_root / "sessions"
    archive_root = state_root / "archive"
    storage_adapter = FileStorageAdapter(state_root)
    cleanup_log = sessions_root / "cleanup.log"
    now = now_utc()

    if sessions_root.exists():
        for session_dir in [p for p in sessions_root.iterdir() if p.is_dir()]:
            current_revision_id = bootstrap_current_revision(session_dir)
            revision_dir = session_dir / "revisions" / current_revision_id if current_revision_id else session_dir
            metadata_path = revision_dir / "metadata.json"
            if not metadata_path.exists():
                continue
            metadata = load_json(metadata_path)
            last_accessed = metadata.get("last_accessed")
            if not isinstance(last_accessed, str):
                continue
            idle_days = (now - parse_iso(last_accessed)).days
            if idle_days >= args.archive_days and metadata.get("status") == "closed":
                archive_closed_session(
                    session_dir=session_dir,
                    dry_run=args.dry_run,
                    log_path=cleanup_log,
                    reason=f"idle_{idle_days}_days_archive_threshold",
                    storage_adapter=storage_adapter,
                )

    if archive_root.exists():
        for session_dir in [p for p in archive_root.iterdir() if p.is_dir()]:
            current_revision_id = bootstrap_current_revision(session_dir)
            revision_dir = session_dir / "revisions" / current_revision_id if current_revision_id else session_dir
            metadata_path = revision_dir / "metadata.json"
            if not metadata_path.exists():
                continue
            metadata = load_json(metadata_path)
            anchor = metadata.get("closed_at") or metadata.get("last_accessed")
            if not isinstance(anchor, str):
                continue
            idle_days = (now - parse_iso(anchor)).days
            if idle_days >= args.delete_days:
                delete_archived(
                    session_dir=session_dir,
                    dry_run=args.dry_run,
                    log_path=cleanup_log,
                    reason=f"idle_{idle_days}_days_delete_threshold",
                    storage_adapter=storage_adapter,
                )

    print("[OK] cleanup_sessions completed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
