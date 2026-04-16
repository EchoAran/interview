#!/usr/bin/env python3
import argparse
import json
import shutil
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from storage_adapter import FileStorageAdapter
from state_lib.config import resolve_state_root, skill_dir_from_file
from validate_state import (
    bootstrap_current_revision,
    cross_validate,
    maybe_jsonschema_validate,
    validate_history,
    validate_metadata,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def latest_checkpoint(session_dir: Path) -> Optional[Path]:
    checkpoints = [p for p in (session_dir / "checkpoints").glob("v*") if p.is_dir() and p.name[1:].isdigit()]
    if not checkpoints:
        return None
    return sorted(checkpoints, key=lambda p: int(p.name[1:]), reverse=True)[0]


def rollback_from_checkpoint(session_dir: Path) -> bool:
    ckpt = latest_checkpoint(session_dir)
    if not ckpt:
        return False
    for name in ["framework.json", "history.json", "metadata.json", "commit.json"]:
        src = ckpt / name
        if src.exists():
            shutil.copy2(src, session_dir / name)
    return True


def hash_payload(framework: Dict[str, Any], history: List[Dict[str, Any]], metadata: Dict[str, Any]) -> str:
    payload = json.dumps(
        {"framework": framework, "history": history, "metadata": metadata},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def create_pre_migration_checkpoint(session_dir: Path, source_root: Path) -> None:
    checkpoints_dir = session_dir / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    versions = [
        int(p.name[1:])
        for p in checkpoints_dir.glob("v*")
        if p.is_dir() and p.name[1:].isdigit()
    ]
    next_v = (max(versions) + 1) if versions else 1
    target = checkpoints_dir / f"v{next_v}"
    target.mkdir(parents=True, exist_ok=True)
    for name in ["framework.json", "history.json", "metadata.json", "commit.json"]:
        src = source_root / name
        if not src.exists():
            src = session_dir / name
        if src.exists():
            shutil.copy2(src, target / name)


def migrate_framework(
    framework: Dict[str, Any], metadata: Dict[str, Any], target_schema_version: str
) -> Dict[str, Any]:
    framework["schema_version"] = target_schema_version
    framework.setdefault("session", {})
    framework["session"]["schema_version"] = target_schema_version
    framework["session"].setdefault("state_version", metadata.get("state_version", "2.0.0"))
    framework["session"].setdefault("status", "active")
    framework["session"].setdefault("cleanup_pending", False)
    framework["session"].setdefault("cleanup_pending_reason", None)

    # evidence migration
    for topic in framework.get("topics", []):
        topic_id = topic.get("id", "unknown_topic")
        for slot in topic.get("slots", []):
            old_evidence = slot.get("evidence")
            if isinstance(old_evidence, str):
                slot["evidence"] = [
                    {
                        "turn_id": metadata.get("last_turn_id", "turn_unknown"),
                        "excerpt": old_evidence,
                        "timestamp": now_iso(),
                        "confidence_note": f"migrated from string evidence in {topic_id}.{slot.get('name', 'slot')}",
                    }
                ]
            elif old_evidence is None:
                slot["evidence"] = []
            elif isinstance(old_evidence, list):
                normalized = []
                for ev in old_evidence:
                    if isinstance(ev, dict):
                        normalized.append(
                            {
                                "turn_id": ev.get("turn_id", metadata.get("last_turn_id", "turn_unknown")),
                                "excerpt": ev.get("excerpt", ev.get("quote", "")),
                                "timestamp": ev.get("timestamp") or now_iso(),
                                "confidence_note": ev.get("confidence_note", "migrated evidence item"),
                            }
                        )
                slot["evidence"] = normalized

    # open question migration
    migrated_open_questions: List[Dict[str, Any]] = []
    for idx, oq in enumerate(framework.get("open_questions", []), start=1):
        if isinstance(oq, str):
            kind = "contradiction" if oq.startswith("[CONTRADICTION]") else "general"
            migrated_open_questions.append(
                {
                    "id": f"oq_{idx:04d}",
                    "text": oq,
                    "kind": kind,
                    "related_slot_ref": None,
                    "severity": "high" if kind == "contradiction" else None,
                    "status": "open",
                }
            )
        elif isinstance(oq, dict):
            migrated_open_questions.append(oq)
    framework["open_questions"] = migrated_open_questions
    return framework


def migrate_history(history: List[Dict[str, Any]], metadata: Dict[str, Any], session_id: str) -> List[Dict[str, Any]]:
    for i, item in enumerate(history, start=1):
        if not isinstance(item, dict):
            history[i - 1] = {
                "turn": i,
                "turn_id": f"turn_{i:04d}",
                "session_id": session_id,
                "timestamp": now_iso(),
                "user_input": "",
                "agent_response": "",
                "framework_delta": {},
                "framework_snapshot": {},
            }
            continue
        item.setdefault("turn", i)
        item.setdefault("turn_id", f"turn_{int(item.get('turn', i)):04d}")
        item.setdefault("session_id", session_id)
        item.setdefault("timestamp", now_iso())
        item.setdefault("user_input", "")
        item.setdefault("agent_response", "")
        item.setdefault("framework_delta", {})
        item.setdefault("framework_snapshot", {})
    return history


def migrate_metadata_defaults(metadata: Dict[str, Any], session_id: str, target_schema_version: str) -> Dict[str, Any]:
    metadata.setdefault("session_id", session_id)
    metadata.setdefault("created_at", now_iso())
    metadata.setdefault("last_accessed", now_iso())
    metadata.setdefault("state_version", "2.0.0")
    metadata.setdefault("schema_version", target_schema_version)
    metadata.setdefault("last_turn_id", None)
    metadata.setdefault("last_successful_commit", None)
    metadata.setdefault("write_attempt_count", 0)
    metadata.setdefault("status", "active")
    metadata.setdefault("truncation_count", 0)
    metadata.setdefault("truncated_fields", [])
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description="Check and migrate state schema drift")
    parser.add_argument("--state-root", default=None)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--schema", default="assets/interview_framework_schema.json")
    parser.add_argument("--migrate", action="store_true")
    args = parser.parse_args()

    skill_dir = skill_dir_from_file(__file__)
    state_root = resolve_state_root(args.state_root, skill_dir=skill_dir)
    storage_adapter = FileStorageAdapter(state_root)
    schema = load_json(Path(args.schema))
    target_schema_version = (
        schema.get("properties", {}).get("schema_version", {}).get("const") or "2.0.0"
    )

    session_dir = storage_adapter.resolve_session_dir(session_id=args.session_id)
    current_revision_id = bootstrap_current_revision(session_dir)

    try:
        snapshot = storage_adapter.load_current(args.session_id)
    except Exception as exc:
        print(f"[ERROR] failed to load current state snapshot: {exc}")
        return 1

    revision_dir = (
        session_dir / "revisions" / snapshot.revision_id if snapshot.revision_id else session_dir
    )
    framework = snapshot.framework
    history = snapshot.history
    metadata = snapshot.metadata
    commit = snapshot.commit
    actual = metadata.get("schema_version")
    if actual == target_schema_version:
        print(f"[OK] no drift: {actual}")
        return 0

    print(f"[WARN] schema drift detected: session={actual}, target={target_schema_version}")
    if not args.migrate:
        return 1

    try:
        create_pre_migration_checkpoint(session_dir, revision_dir)
        framework = migrate_framework(framework, metadata, target_schema_version)
        history = migrate_history(history, metadata, args.session_id)
        metadata = migrate_metadata_defaults(metadata, args.session_id, target_schema_version)
        metadata["schema_version"] = target_schema_version
        metadata["last_updated"] = now_iso()

        # Post-migration validation before writing live files
        schema_msg = maybe_jsonschema_validate(framework, schema)
        errors: List[str] = []
        if schema_msg and schema_msg.startswith("schema validation failed"):
            errors.append(schema_msg)
        errors.extend(validate_history(history))
        errors.extend(validate_metadata(metadata))
        conversation_index = storage_adapter.load_conversation_index()
        errors.extend(
            cross_validate(
                framework,
                history,
                metadata,
                commit,
                conversation_index,
                snapshot.revision_id or current_revision_id,
                revision_dir if revision_dir.exists() else None,
            )
        )
        if errors:
            raise ValueError("post-migration validation failed: " + "; ".join(errors))

        migration_commit: Dict[str, Any] = {
            "session_id": args.session_id,
            "turn_id": f"system_migration_{now_iso()}",
            "state_version": metadata.get("state_version", "2.0.0"),
            "schema_version": metadata.get("schema_version", target_schema_version),
            "timestamp": now_iso(),
            "content_hash": hash_payload(framework, history, metadata),
        }
        metadata["last_successful_commit"] = migration_commit

        revision_id = storage_adapter.commit_revision(
            args.session_id, framework, history, metadata, migration_commit
        )
        if isinstance(metadata.get("last_successful_commit"), dict):
            metadata["last_successful_commit"]["revision_id"] = revision_id

        # Keep legacy live files in sync.
        write_json(session_dir / "framework.json", framework)
        write_json(session_dir / "history.json", history)
        write_json(session_dir / "metadata.json", metadata)
        write_json(session_dir / "commit.json", migration_commit)
        print(f"[INFO] migrated into revision: {revision_id}")
        print("[OK] migration completed")
        return 0
    except Exception as exc:
        print(f"[ERROR] migration failed: {exc}")
        if rollback_from_checkpoint(session_dir):
            print("[INFO] rolled back from latest checkpoint")
        else:
            print("[INFO] no checkpoint available for rollback")
        return 1


if __name__ == "__main__":
    sys.exit(main())
