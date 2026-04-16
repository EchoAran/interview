# State Management

This document defines the transaction-safe persistence model for stateful interview execution.

Execution profiles:
- Profile S (Scripted Persistence): recommended; use bundled scripts/library as deterministic state engine.
- Profile T (Tool-only Persistence): compatibility fallback; host manually orchestrates file transaction steps.

## Storage Layout

```text
<state_root>/
├── conversation_index.json                 # {conversation_id: session_id}
├── sessions/
│   ├── {session_id}/
│   │   ├── CURRENT                         # active revision pointer (single line)
│   │   ├── revisions/
│   │   │   ├── r000001/
│   │   │   │   ├── framework.json
│   │   │   │   ├── history.json
│   │   │   │   ├── metadata.json
│   │   │   │   └── commit.json
│   │   │   └── ...
│   │   ├── framework.json                  # legacy mirror (optional compatibility)
│   │   ├── history.json                    # legacy mirror (optional compatibility)
│   │   ├── metadata.json                   # legacy mirror (optional compatibility)
│   │   ├── commit.json                     # legacy mirror (optional compatibility)
│   │   └── checkpoints/
│   │       ├── v1/
│   │       ├── v2/
│   │       └── ...
│   └── cleanup.log                         # structured JSONL
├── temp/
│   └── {session_id}/                       # transactional temp write area
└── archive/                                # closed sessions kept for delayed cleanup
```

Default `state_root` is `<skill_dir>/state`.
Override may come from `skill.config.json`, `config/state.json`, or runtime `--state-root`.
Resolved path must pass allowlist validation.

## Session Identity Rules

- Session IDs must be system-generated only, with format `{YYYYMMDD_HHMMSS}_{A-Z0-9(6)}`.
- User input must never participate in session path construction.
- Runtime must resolve a single active mapping `conversation_id -> session_id` via `conversation_index.json`.
- If mapping ambiguity exists, runtime must quarantine extra candidates and keep only one active session.

## Transaction Commit Protocol

Every state-changing turn must commit with all-or-nothing semantics:

1. Prepare write payload for `framework.json`, `history.json`, `metadata.json`.
2. Validate payload before write (schema + cross-file consistency).
3. Write temp files into `state/temp/{session_id}/`:
   - `framework.json.tmp`
   - `history.json.tmp`
   - `metadata.json.tmp`
4. If any temp file fails validation, abort commit and keep prior state untouched.
5. Snapshot current state to `checkpoints/v{n}/` before replacing live files.
6. Write a complete immutable revision under `state/sessions/{session_id}/revisions/{revision_id}/`.
7. Atomically switch `state/sessions/{session_id}/CURRENT` to `{revision_id}`.
8. Update `commit.json` marker and refresh optional legacy mirror files as best-effort compatibility cache.

`commit.json` required fields:
- `session_id`
- `turn_id`
- `state_version`
- `schema_version`
- `timestamp`
- `content_hash`

## Idempotency and Retry Rules

- Each turn must carry a stable `turn_id`.
- Use `turn_id + content_hash` as idempotency key.
- If `turn_id` is same and `content_hash` is same, treat as idempotent retry.
- If `turn_id` is same but `content_hash` differs, treat as corrective retry and allow commit.
- Track retry pressure in `metadata.write_attempt_count`.

## Concurrency and Re-entry Rules

- Same `session_id` must be write-serialized.
- Use host queueing or adapter lock before commit-critical operations.
- Prefer host-generated stable `turn_id` for retries and reconnects.
- On reconnect/re-entry, load from `CURRENT` before computing any write delta.

## Snapshot and Recovery

- Keep checkpoints for the latest 3 to 5 committed versions.
- On corruption or migration failure, rollback from latest checkpoint.
- Read path must resolve from `CURRENT` first; direct root-level mirrors are fallback only.
- Root-level mirror files are not atomic commit targets and must not be used as authoritative read source.
- Recovery order:
  1. Resolve `CURRENT` revision and validate revision files
  2. If invalid, rollback to latest checkpoint
  3. If no checkpoint exists, initialize a fresh session

## Two-Phase Cleanup Policy

- On completion, mark session `status=closed` first, do not hard-delete immediately.
- Keep summary and latest checkpoints for delayed cleanup.
- Move stale closed sessions to `state/archive/`.
- Delete only after retention threshold via maintenance job.

## Guardrails

- All persistence must use JSON serialization (`json.dump`) with UTF-8.
- String concatenation write patterns are not allowed.
- Enforce hard size limits for input text, evidence list, and history file.
- Record truncation events in metadata fields (`truncated_fields`, `truncation_count`).

## Storage adapter contract

To keep interview logic portable across runtimes, implement persistence behind a minimal adapter interface:
- `load_current(session_id) -> framework, history, metadata, commit, revision_id`
- `commit_revision(session_id, framework, history, metadata, commit) -> revision_id`
- `mark_closed(session_id, closed_at)`
- `mark_cleanup_pending(session_id, reason, timestamp?)`
- `archive_session(session_id)`
- `resolve_session_dir(session_id?, conversation_id?) -> session_dir`
- `upsert_conversation_mapping(conversation_id, session_id)`
- `remove_conversation_mapping(conversation_id, session_id?)`

Current repository default is file-based implementation (`scripts/storage_adapter.py`, `FileStorageAdapter`).
Future adapters (SQLite, KV, object storage) should implement the same contract without changing interview core logic.

## Tooling Entry Points

- `scripts/commit_state.py`
- `scripts/validate_state.py`
- `scripts/check_state_drift.py`
- `scripts/security_scan_state.py`
- `scripts/cleanup_sessions.py`
- `scripts/storage_adapter.py`
- `scripts/state_doctor.py`
- `scripts/state_lib/`
