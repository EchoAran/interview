#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import shutil
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
    read_current_revision,
    validate_history,
    validate_metadata,
)


SESSION_ID_PATTERN = re.compile(r"^\d{8}_\d{6}_[A-Z0-9]{6}$")
MAX_USER_INPUT_CHARS = 20000
MAX_EVIDENCE_ITEMS_PER_SLOT = 50
MAX_HISTORY_TURNS = 1000
MAX_HISTORY_BYTES = 5_000_000


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


def write_json_atomic(path: Path, data: Any) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    write_json(tmp, data)
    tmp.replace(path)


def hash_payload(framework: Any, history: Any, metadata: Any) -> str:
    payload = json.dumps(
        {"framework": framework, "history": history, "metadata": metadata},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def latest_checkpoint_version(checkpoints_dir: Path) -> int:
    versions: List[int] = []
    for item in checkpoints_dir.glob("v*"):
        if item.is_dir() and item.name[1:].isdigit():
            versions.append(int(item.name[1:]))
    return max(versions) if versions else 0


def create_checkpoint(session_dir: Path, keep: int) -> None:
    checkpoints_dir = session_dir / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    next_v = latest_checkpoint_version(checkpoints_dir) + 1
    target = checkpoints_dir / f"v{next_v}"
    target.mkdir(parents=True, exist_ok=True)
    revision_id = read_current_revision(session_dir)
    source_root = (session_dir / "revisions" / revision_id) if revision_id else session_dir
    for name in ["framework.json", "history.json", "metadata.json", "commit.json"]:
        src = source_root / name
        if not src.exists():
            src = session_dir / name
        if src.exists():
            shutil.copy2(src, target / name)

    # Keep last N versions
    versions = sorted([p for p in checkpoints_dir.glob("v*") if p.is_dir()], key=lambda p: int(p.name[1:]))
    while len(versions) > keep:
        old = versions.pop(0)
        shutil.rmtree(old, ignore_errors=True)


def rollback_from_latest_checkpoint(session_dir: Path) -> bool:
    checkpoints_dir = session_dir / "checkpoints"
    candidates = [
        p for p in checkpoints_dir.glob("v*") if p.is_dir() and p.name[1:].isdigit()
    ]
    if not candidates:
        return False
    latest = sorted(candidates, key=lambda p: int(p.name[1:]), reverse=True)[0]
    for name in ["framework.json", "history.json", "metadata.json", "commit.json"]:
        src = latest / name
        if src.exists():
            shutil.copy2(src, session_dir / name)
    return True


def restore_from_current_revision(session_dir: Path) -> bool:
    revision_id = read_current_revision(session_dir)
    if not revision_id:
        return False
    revision_dir = session_dir / "revisions" / revision_id
    if not revision_dir.exists():
        return False
    for name in ["framework.json", "history.json", "metadata.json", "commit.json"]:
        src = revision_dir / name
        if src.exists():
            shutil.copy2(src, session_dir / name)
    return True


def recover_incomplete_commit(session_dir: Path) -> None:
    pending = session_dir / "pending_commit.json"
    if not pending.exists():
        return
    if restore_from_current_revision(session_dir):
        pending.unlink(missing_ok=True)
        print("[WARN] recovered from incomplete commit via CURRENT revision")
        return
    if rollback_from_latest_checkpoint(session_dir):
        pending.unlink(missing_ok=True)
        print("[WARN] recovered from incomplete commit via latest checkpoint")
        return
    raise RuntimeError("pending_commit.json exists but no checkpoint available for recovery")


def load_json_if_exists(path: Path) -> Optional[Any]:
    return load_json(path) if path.exists() else None


def persist_commit_artifact(
    session_dir: Path,
    commit: Dict[str, Any],
    framework: Dict[str, Any],
    history: List[Dict[str, Any]],
    metadata: Dict[str, Any],
) -> str:
    commit_id = f"{commit['timestamp'].replace(':', '').replace('-', '')}_{commit['turn_id']}_{commit['content_hash'][:8]}"
    commit_dir = session_dir / "commits" / commit_id
    commit_dir.mkdir(parents=True, exist_ok=True)
    write_json(commit_dir / "framework.json", framework)
    write_json(commit_dir / "history.json", history)
    write_json(commit_dir / "metadata.json", metadata)
    write_json(commit_dir / "commit.json", commit)
    manifest = {
        "session_id": commit["session_id"],
        "current_commit_id": commit_id,
        "turn_id": commit["turn_id"],
        "content_hash": commit["content_hash"],
        "updated_at": now_iso(),
    }
    write_json_atomic(session_dir / "manifest.json", manifest)
    return commit_id


def enforce_limits(framework: Dict[str, Any], history: List[Dict[str, Any]], metadata: Dict[str, Any]) -> None:
    truncated_fields = metadata.get("truncated_fields")
    if not isinstance(truncated_fields, list):
        truncated_fields = []
    truncation_count = int(metadata.get("truncation_count", 0))

    # user_input length limit
    for item in history:
        if "session_id" not in item:
            item["session_id"] = metadata.get("session_id", "")
        user_input = item.get("user_input")
        if isinstance(user_input, str) and len(user_input) > MAX_USER_INPUT_CHARS:
            item["user_input"] = user_input[:MAX_USER_INPUT_CHARS]
            truncation_count += 1
            truncated_fields.append("history.user_input")

    # evidence list limit
    for topic in framework.get("topics", []):
        if not isinstance(topic, dict):
            continue
        for slot in topic.get("slots", []):
            if not isinstance(slot, dict):
                continue
            evidence = slot.get("evidence")
            if isinstance(evidence, list) and len(evidence) > MAX_EVIDENCE_ITEMS_PER_SLOT:
                slot["evidence"] = evidence[-MAX_EVIDENCE_ITEMS_PER_SLOT:]
                truncation_count += 1
                truncated_fields.append(f"slot.evidence.{topic.get('id')}.{slot.get('name')}")

    # history turn limit
    if len(history) > MAX_HISTORY_TURNS:
        history[:] = history[-MAX_HISTORY_TURNS:]
        truncation_count += 1
        truncated_fields.append("history.turns")

    # history bytes limit
    while len(json.dumps(history, ensure_ascii=False).encode("utf-8")) > MAX_HISTORY_BYTES and len(history) > 1:
        history.pop(0)
        truncation_count += 1
        truncated_fields.append("history.bytes")

    metadata["truncation_count"] = truncation_count
    metadata["truncated_fields"] = truncated_fields


def validate_session_id(session_id: str) -> None:
    if not SESSION_ID_PATTERN.match(session_id):
        raise ValueError(f"invalid session_id format: {session_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Transactional state commit for one session")
    parser.add_argument("--state-root", default=None)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--turn-id", required=True)
    parser.add_argument("--framework-file", required=True)
    parser.add_argument("--history-file", required=True)
    parser.add_argument("--metadata-file", required=True)
    parser.add_argument("--schema", default="assets/interview_framework_schema.json")
    parser.add_argument("--schema-version", default="2.0.0")
    parser.add_argument("--keep-checkpoints", type=int, default=5)
    args = parser.parse_args()

    try:
        validate_session_id(args.session_id)
    except ValueError as exc:
        print(f"[ERROR] {exc}")
        return 1

    skill_dir = skill_dir_from_file(__file__)
    state_root = resolve_state_root(args.state_root, skill_dir=skill_dir)
    storage_adapter = FileStorageAdapter(state_root)
    session_dir = state_root / "sessions" / args.session_id
    temp_dir = state_root / "temp" / args.session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    temp_dir.mkdir(parents=True, exist_ok=True)
    recover_incomplete_commit(session_dir)

    framework = load_json(Path(args.framework_file))
    history = load_json(Path(args.history_file))
    metadata = load_json(Path(args.metadata_file))
    schema = load_json(Path(args.schema))

    history_last_turn_id = None
    if isinstance(history, list) and history:
        last_item = history[-1]
        if isinstance(last_item, dict):
            history_last_turn_id = last_item.get("turn_id")
    if not isinstance(history_last_turn_id, str):
        print("[ERROR] history must contain at least one turn with a valid turn_id")
        return 1
    if args.turn_id != history_last_turn_id:
        print(
            f"[ERROR] args.turn_id ({args.turn_id}) must match history last turn_id ({history_last_turn_id})"
        )
        return 1

    conversation_id = metadata.get("conversation_id")
    if not isinstance(conversation_id, str) or not conversation_id:
        print("[ERROR] metadata.conversation_id is required")
        return 1

    # Retry/duplicate protection
    current_revision_id = bootstrap_current_revision(session_dir)
    existing_history_path = (
        session_dir / "revisions" / current_revision_id / "history.json"
        if current_revision_id
        else session_dir / "history.json"
    )
    existing_commit_path = (
        session_dir / "revisions" / current_revision_id / "commit.json"
        if current_revision_id
        else session_dir / "commit.json"
    )
    existing_history = load_json_if_exists(existing_history_path)
    existing_commit = load_json_if_exists(existing_commit_path)

    write_attempt_count = int(metadata.get("write_attempt_count", 0)) + 1
    metadata["write_attempt_count"] = write_attempt_count
    metadata["schema_version"] = args.schema_version
    metadata["last_turn_id"] = history_last_turn_id
    metadata["last_accessed"] = now_iso()
    metadata["last_updated"] = now_iso()
    enforce_limits(framework, history, metadata)

    content_hash = hash_payload(framework, history, metadata)

    if existing_history_path.exists():
        if isinstance(existing_history, list) and existing_history:
            if existing_history[-1].get("turn_id") == args.turn_id:
                existing_hash = (
                    existing_commit.get("content_hash")
                    if isinstance(existing_commit, dict)
                    else None
                )
                if existing_hash == content_hash:
                    # True idempotent retry: update metadata retry counters/access timestamps only.
                    metadata_path = (
                        session_dir / "revisions" / current_revision_id / "metadata.json"
                        if current_revision_id
                        else session_dir / "metadata.json"
                    )
                    if metadata_path.exists():
                        live_metadata = load_json(metadata_path)
                        if isinstance(live_metadata, dict):
                            live_metadata["write_attempt_count"] = int(
                                live_metadata.get("write_attempt_count", 0)
                            ) + 1
                            live_metadata["last_accessed"] = now_iso()
                            live_metadata["last_updated"] = now_iso()
                            write_json(metadata_path, live_metadata)
                    print(f"[OK] idempotent duplicate turn detected and acknowledged: {args.turn_id}")
                    return 0
                print(
                    "[WARN] duplicate turn_id with different payload detected; continuing corrective commit"
                )

    # Pre-commit validation before touching live files
    errors: List[str] = []
    schema_msg = maybe_jsonschema_validate(framework, schema)
    if schema_msg and schema_msg.startswith("schema validation failed"):
        errors.append(schema_msg)
    errors.extend(validate_history(history))
    errors.extend(validate_metadata(metadata))
    errors.extend(
        cross_validate(
            framework,
            history,
            metadata,
            None,
            {conversation_id: args.session_id},
            current_revision_id,
            (session_dir / "revisions" / current_revision_id) if current_revision_id else None,
        )
    )
    if errors:
        print("[ERROR] pre-commit validation failed:")
        for err in errors:
            print(f" - {err}")
        return 1

    # Ensure conversation index mapping is valid before commit
    try:
        storage_adapter.upsert_conversation_mapping(conversation_id, args.session_id)
    except Exception as exc:
        print(f"[ERROR] conversation index update failed: {exc}")
        return 1

    commit = {
        "session_id": args.session_id,
        "turn_id": args.turn_id,
        "state_version": metadata.get("state_version", "2.0.0"),
        "schema_version": args.schema_version,
        "timestamp": now_iso(),
        "content_hash": content_hash,
    }
    metadata["last_successful_commit"] = commit

    # Create checkpoint before commit
    create_checkpoint(session_dir, keep=max(3, min(5, args.keep_checkpoints)))

    # Transactional write into state/temp/{session_id}
    tmp_framework = temp_dir / "framework.json.tmp"
    tmp_history = temp_dir / "history.json.tmp"
    tmp_metadata = temp_dir / "metadata.json.tmp"
    write_json(tmp_framework, framework)
    write_json(tmp_history, history)
    write_json(tmp_metadata, metadata)

    # Minimal "all files ready" gate then atomic replace into session dir
    for p in [tmp_framework, tmp_history, tmp_metadata]:
        if not p.exists() or p.stat().st_size == 0:
            print(f"[ERROR] tmp file invalid: {p}")
            return 1

    pending_commit_path = session_dir / "pending_commit.json"
    write_json_atomic(
        pending_commit_path,
        {"session_id": args.session_id, "turn_id": args.turn_id, "content_hash": content_hash, "timestamp": now_iso()},
    )

    try:
        # 1) write new revision and atomically switch CURRENT first (authoritative read path)
        revision_id = storage_adapter.commit_revision(
            args.session_id, framework, history, metadata, commit
        )
        persist_commit_artifact(session_dir, commit, framework, history, metadata)
        if isinstance(metadata.get("last_successful_commit"), dict):
            metadata["last_successful_commit"]["revision_id"] = revision_id

        # 2) best-effort legacy mirror refresh for compatibility/debug only (non-authoritative)
        try:
            tmp_framework.replace(session_dir / "framework.json")
            tmp_history.replace(session_dir / "history.json")
            tmp_metadata.replace(session_dir / "metadata.json")
            write_json(session_dir / "commit.json", commit)
        except Exception as mirror_exc:
            print(f"[WARN] legacy mirror refresh failed after CURRENT switch: {mirror_exc}")
        pending_commit_path.unlink(missing_ok=True)
    except Exception as exc:
        print(f"[ERROR] commit replace failed: {exc}")
        if not restore_from_current_revision(session_dir):
            rollback_from_latest_checkpoint(session_dir)
        pending_commit_path.unlink(missing_ok=True)
        return 1

    print(f"[OK] committed session={args.session_id} turn_id={args.turn_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
