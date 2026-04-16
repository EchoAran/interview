#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from state_lib.config import resolve_state_root, skill_dir_from_file
from state_lib.doctor import state_doctor


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified state doctor entry")
    parser.add_argument("--state-root", default=None)
    parser.add_argument("--action", choices=["validate", "repair", "migrate"], default="validate")
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--conversation-id", default=None)
    parser.add_argument("--schema", default="assets/interview_framework_schema.json")
    args = parser.parse_args()

    if not args.session_id and not args.conversation_id:
        print("[ERROR] either --session-id or --conversation-id is required")
        return 1

    skill_dir = skill_dir_from_file(__file__)
    state_root = resolve_state_root(args.state_root, skill_dir=skill_dir)
    schema_path = Path(args.schema)
    if not schema_path.is_absolute():
        schema_path = skill_dir / schema_path

    try:
        rc = state_doctor(
            state_root=state_root,
            action=args.action,
            session_id=args.session_id,
            conversation_id=args.conversation_id,
            schema_path=schema_path,
        )
    except Exception as exc:
        print(f"[ERROR] state_doctor failed: {exc}")
        return 1

    if rc == 0:
        print(f"[OK] state_doctor action={args.action} passed")
    else:
        print(f"[ERROR] state_doctor action={args.action} reported issues")
    return rc


if __name__ == "__main__":
    sys.exit(main())
