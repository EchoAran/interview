from __future__ import annotations

from pathlib import Path
from typing import Optional

try:
    from ..storage_adapter import FileStorageAdapter  # package mode
    from ..validate_state import (  # package mode
        cross_validate,
        maybe_jsonschema_validate,
        validate_history,
        validate_metadata,
    )
except ImportError:  # pragma: no cover - script mode fallback
    from storage_adapter import FileStorageAdapter
    from validate_state import (
        cross_validate,
        maybe_jsonschema_validate,
        validate_history,
        validate_metadata,
    )


def state_doctor(
    *,
    state_root: Path,
    action: str,
    session_id: Optional[str] = None,
    conversation_id: Optional[str] = None,
    schema_path: Optional[Path] = None,
) -> int:
    """Single state diagnostics entry.

    Supported actions:
    - validate: validate current snapshot against schema and cross-file rules.
    - repair: reserved; currently behaves like validate and returns non-zero on failure.
    - migrate: reserved; hand off to check_state_drift.py for full migration flow.
    """
    adapter = FileStorageAdapter(state_root)
    session_dir = adapter.resolve_session_dir(session_id=session_id, conversation_id=conversation_id)
    snapshot = adapter.load_current(session_dir.name)
    conversation_index = adapter.load_conversation_index()

    schema_errors = []
    if schema_path and schema_path.exists():
        import json

        with schema_path.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        schema_msg = maybe_jsonschema_validate(snapshot.framework, schema)
        if schema_msg and schema_msg.startswith("schema validation failed"):
            schema_errors.append(schema_msg)

    errors = []
    errors.extend(schema_errors)
    errors.extend(validate_history(snapshot.history))
    errors.extend(validate_metadata(snapshot.metadata))
    errors.extend(
        cross_validate(
            snapshot.framework,
            snapshot.history,
            snapshot.metadata,
            snapshot.commit,
            conversation_index,
            snapshot.revision_id,
            (session_dir / "revisions" / snapshot.revision_id) if snapshot.revision_id else None,
        )
    )

    normalized = action.strip().lower()
    if normalized in {"validate", "repair"}:
        return 0 if not errors else 1
    if normalized == "migrate":
        # Migration is implemented in check_state_drift.py to preserve checkpoint/rollback flow.
        return 0 if not errors else 1
    raise ValueError(f"unsupported action: {action}")
