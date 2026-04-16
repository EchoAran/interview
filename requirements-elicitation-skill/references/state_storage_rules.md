# State Storage Rules

This document defines file contracts, hard limits, and transaction boundaries.

## Core Files

### framework.json

- Must conform to `assets/interview_framework_schema.json`.
- Must contain:
  - `schema_version = "2.0.0"`
  - `session.session_id`
  - `session.conversation_id`
  - `session.status`
- `evidence` must be object array format only:
  - `{turn_id, excerpt, timestamp, confidence_note}`

### history.json

- Array of ordered turns.
- Required turn fields:
  - `turn` (1..N sequential)
  - `turn_id` (stable idempotency key)
  - `session_id`
  - `timestamp`
  - `user_input`
  - `agent_response`
  - `framework_delta`
  - `framework_snapshot`

### metadata.json

- Required fields:
  - `session_id`
  - `conversation_id`
  - `created_at`
  - `last_accessed`
  - `last_updated`
  - `state_version`
  - `schema_version`
  - `last_turn_id`
  - `last_successful_commit`
  - `write_attempt_count`
  - `truncation_count`
  - `truncated_fields`
  - `status` (`active|closed`)

### commit.json

- Last successful transaction pointer.
- Required fields:
  - `session_id`
  - `turn_id`
  - `state_version`
  - `schema_version`
  - `timestamp`
  - `content_hash`

### conversation_index.json

- Global map `{conversation_id: session_id}`.
- Must be updated atomically with session creation and cleanup transitions.

## Directory Rules

- `state_root` default: `<skill_dir>/state`.
- Override sources (priority high to low):
  - runtime `--state-root`
  - `skill.config.json` -> `state_root`
  - `config/state.json` -> `state_root`
- Resolved path must remain within allowlisted roots.
- Base directories:
  - `<state_root>/sessions/`
  - `<state_root>/temp/`
  - `<state_root>/archive/`
- Transaction temp path: `<state_root>/temp/{session_id}/`.
- Checkpoint path: `<state_root>/sessions/{session_id}/checkpoints/v{n}/`.
- Revision path: `<state_root>/sessions/{session_id}/revisions/r{n}/`.
- Active read pointer: `<state_root>/sessions/{session_id}/CURRENT`.

## Session ID and Path Safety

- Session ID format: `^\d{8}_\d{6}_[A-Z0-9]{6}$`.
- Any session directory name not matching this regex must be rejected.
- Path joins must be done via safe APIs (never raw string concatenation).

## Hard Limits

- `max_user_input_chars`: 20_000
- `max_evidence_items_per_slot`: 50
- `max_history_turns`: 1_000
- `max_history_bytes`: 5_000_000
- `max_session_bytes`: 10_000_000

If truncation occurs:
- increment `metadata.truncation_count`
- append human-readable reason to `metadata.truncated_fields`

## Transaction Write Rules

1. Serialize all JSON payloads with `json.dump` UTF-8.
2. Write 3 temp files:
   - `framework.json.tmp`
   - `history.json.tmp`
   - `metadata.json.tmp`
3. Validate all 3 temp files.
4. Backup current live files to a new checkpoint version.
5. Write complete revision snapshot to `revisions/r{n}`.
6. Atomically replace `CURRENT` pointer to `r{n}`.
7. Write `commit.json` (and optional live mirrors for compatibility/debug).

If step 3 fails, do not mutate live files.

## Validation Rules

### Single-file validation

- `framework.json` validates against schema.
- `history.json` is ordered and has unique `turn_id`.
- `history.turn` must be strictly increasing (monotonic), but it does not need to start from 1 after retention truncation.
- `metadata.json` includes all required operational fields.

### Cross-file validation

- Read source should be `CURRENT -> revisions/<id>/`.
- `session_id` must match across framework, history context, and metadata.
- `metadata.last_turn_id` must match `history[-1].turn_id`.
- `framework.session.status` must match `metadata.status`.
- `framework.session.schema_version` must match `metadata.schema_version`.
- If `commit.json` exists, `commit.turn_id` must match `metadata.last_turn_id`.
- If `conversation_index.json` exists, `conversation_index[metadata.conversation_id]` must match `metadata.session_id`.
- `framework.current_topic_id` must exist in `framework.topics`.
- Each `conflicted` slot must have an open contradiction question linked by `related_slot_ref`.
