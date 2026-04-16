# State Test Cases

These files define minimal state-layer regression scenarios:

- `01_normal_persistence_case.json`
- `02_interrupted_write_recovery_case.json`
- `03_duplicate_turn_retry_case.json`
- `04_old_schema_migration_case.json`

Use with script entry points:

```bash
python scripts/validate_state.py --state-root state --session-id <SESSION_ID>
python scripts/check_state_drift.py --state-root state --session-id <SESSION_ID> --migrate
python scripts/cleanup_sessions.py --state-root state --dry-run
python scripts/security_scan_state.py --state-root state
python scripts/run_state_tests.py
```
