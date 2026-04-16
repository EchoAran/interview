# State Cleanup Procedures

This document defines two-phase cleanup and structured lifecycle logging.

## Two-Phase Policy

Phase A: Close
- Mark `metadata.status = closed`.
- Record `metadata.closed_at`.
- Keep latest summary and checkpoints.
- Keep `conversation_index` mapping removed after closure.

Phase B: Delayed cleanup
- Move only already-closed sessions to `state/archive/` after inactivity threshold.
- Delete archived sessions only after longer retention window.

## Default Time Rules

- Archive threshold: 30 days without access.
- Delete threshold: 90 days without access.
- Emergency mode may shorten thresholds under storage pressure.

## Cleanup Log Contract

`state/sessions/cleanup.log` uses JSONL rows:

```json
{
  "session_id": "20260415_093000_A1B2C3",
  "closed_at": "2026-04-15T10:00:00Z",
  "deleted_at": null,
  "reason": "idle_30_days_archive_threshold",
  "result": "archived"
}
```

Required fields:
- `session_id`
- `closed_at`
- `deleted_at`
- `reason`
- `result`

## Failure Handling

- If archive or delete fails:
  - set `cleanup_pending = true`
  - set `cleanup_pending_reason`
  - keep session in current location
  - retry on next maintenance run

## Execution Entry

Use:
- `python scripts/cleanup_sessions.py --state-root state`
- Optional `--dry-run` for audit-only mode
