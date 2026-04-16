# State Lifecycle Management

This document defines operational lifecycle from first turn to delayed deletion.

## 1. Session Initialization

Trigger:
- First run with no resolved `conversation_id -> session_id` mapping.

Actions:
1. Generate `session_id` by system rule.
2. Create `state/sessions/{session_id}/`.
3. Initialize `framework.json` with `schema_version=2.0.0`.
4. Initialize empty `history.json`.
5. Initialize `metadata.json` with:
   - `last_turn_id = null`
   - `last_successful_commit = null`
   - `write_attempt_count = 0`
   - `truncation_count = 0`
   - `truncated_fields = []`
   - `status = active`
6. Write `conversation_index.json`.
7. Create first checkpoint `checkpoints/v1/`.

## 2. Runtime Commit Cycle

For each turn:
1. Build deterministic `turn_id`.
2. Check duplicate (`history[-1].turn_id == turn_id`) to avoid retry pollution.
3. Execute transactional commit (`scripts/commit_state.py`):
   - temp write
   - validation
   - checkpoint
   - rename
   - commit marker update
4. Run state validation (`scripts/validate_state.py`).

## 3. Drift Check and Migration

At load time:
1. Compare `metadata.schema_version` with target schema version.
2. If mismatch, run `scripts/check_state_drift.py --migrate`.
3. If migration fails, rollback from latest checkpoint and block runtime until valid.

## 4. Completion and Closure

When interview reaches complete:
1. Generate final summary.
2. Mark `metadata.status = closed`, set `closed_at`.
3. Keep recent checkpoints for audit and recovery.
4. Do not hard-delete immediately.

## 5. Archive and Deletion

Maintenance policy:
- No access >= 30 days: archive session.
- No access >= 90 days: deletion candidate.

Execution entry:
- `scripts/cleanup_sessions.py`

## 6. Failure Recovery

- Commit interrupted: recover from latest successful `commit.json`.
- Partial state corruption: rollback from latest checkpoint.
- Missing checkpoint: initialize new clean session and mark old as quarantine candidate.
