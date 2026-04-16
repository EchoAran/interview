# Integration Guide

This guide explains how to integrate the requirements elicitation skill into different host runtimes without binding to any specific framework.

## Integration Tiers

### Tier 0: Minimal (read-only fallback)

Use when host cannot provide reliable persistence.

- Supports interview reasoning only.
- No durable state continuity guarantee across restarts.
- Suitable for quick demos, not production use.

Required host capabilities:
- read markdown/json files
- send/receive multi-turn messages

### Tier 1: Tool-only Persistence (Profile T)

Use when host can read/write files but cannot run bundled scripts/functions.

- Host must implement mechanical transaction steps.
- Higher implementation burden on host and orchestration prompts.
- Must emit risk caveat when atomic guarantees are weak.

Required host capabilities:
- `read_text`, `write_text`, `atomic_write` (or `write_tmp + replace`)
- `mkdir_p`, `exists`, `list_dir`

### Tier 2: Scripted Persistence (Profile S, recommended)

Use when host can execute controlled Python entry points.

- Deterministic commit/validate/cleanup behavior.
- Lowest drift risk between hosts.
- Recommended for production deployment.

Required host capabilities:
- all Tier 1 capabilities, or equivalent
- controlled Python execution for bundled state modules/scripts

## Atomic Operations Contract

Expose (or emulate) these operations in host tooling:

- `state_load(conversation_id|session_id) -> snapshot`
- `state_commit(turn_id, framework, history, metadata) -> revision_id`
- `state_mark_closed(session_id, closed_at?)`
- `state_doctor(session_id|conversation_id, action)`

Reference implementation:
- `scripts/state_lib/atomic_ops.py`
- `scripts/state_lib/doctor.py`

## Design Decisions (Portability/Consistency)

This section documents two portability-oriented decisions used by the current implementation.

### 1) Import strategy for state library modules

- `state_lib` uses package-first imports (for package execution) with script-mode fallback imports.
- This keeps both integration styles workable:
  - package mode: host imports modules/functions directly
  - script mode: host executes `python scripts/<entry>.py`
- For long-term maintenance, prefer package mode in host integrations.

### 2) Commit consistency for revision metadata

- `revision_id` is written during `commit_revision(...)` itself.
- `commit.json` and `metadata.last_successful_commit.revision_id` are materialized in the same revision write path.
- Avoid relying on a second metadata rewrite after `CURRENT` pointer switch.
- This reduces post-switch race windows and improves cross-host consistency.

## State Root Resolution

Default:
- `<skill_dir>/state`

Optional override:
- `skill.config.json` -> `state_root`
- `config/state.json` -> `state_root`
- runtime `--state-root`

Safety:
- resolved path must stay in allowlisted roots.

## Concurrency Requirements

- One in-flight commit per `session_id`.
- Host should serialize by queue or lock.
- Host should generate stable `turn_id` for retries and reconnects.

## Host-side Pseudocode

```python
def on_user_turn(conversation_id: str, user_input: str):
    snapshot = state_load(conversation_id=conversation_id)
    plan = run_skill_reasoning(snapshot, user_input)  # LLM reasoning only
    revision_id = state_commit(
        turn_id=plan.turn_id,
        framework=plan.framework,
        history=plan.history,
        metadata=plan.metadata,
    )
    return plan.agent_utterance, revision_id
```

## Recommended Entry Points

- `scripts/commit_state.py`
- `scripts/validate_state.py`
- `scripts/check_state_drift.py`
- `scripts/cleanup_sessions.py`
- `scripts/state_doctor.py`
