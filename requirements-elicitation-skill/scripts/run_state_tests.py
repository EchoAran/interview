#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SCHEMA = ROOT / "assets" / "interview_framework_schema.json"


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def run(cmd: List[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)


def minimal_framework(session_id: str, conversation_id: str) -> Dict[str, Any]:
    return {
        "schema_version": "2.0.0",
        "phase": "runtime",
        "current_topic_id": "product_objective",
        "topics": [
            {
                "id": "product_objective",
                "label": "product objective",
                "priority": "high",
                "coverage_score": 0.8,
                "status": "partially_filled",
                "notes": [],
                "blocking_issues": [],
                "slots": [
                    {
                        "name": "core problem",
                        "value": "Need a marketplace workflow.",
                        "confidence": "confirmed",
                        "status": "filled",
                        "contradiction_severity": None,
                        "evidence": [
                            {
                                "turn_id": "turn_0001",
                                "excerpt": "Need a marketplace workflow.",
                                "timestamp": "2026-04-15T00:00:00Z",
                                "confidence_note": "explicit statement",
                            }
                        ],
                        "last_updated": "turn_0001",
                        "convergence_score": 0.7,
                        "information_density": "high",
                    }
                ],
            }
        ],
        "open_questions": [],
        "contradictions": [],
        "session": {
            "session_id": session_id,
            "conversation_id": conversation_id,
            "state_version": "2.0.0",
            "schema_version": "2.0.0",
            "status": "active",
            "closed_at": None,
            "cleanup_pending": False,
            "cleanup_pending_reason": None,
        },
        "efficiency_metrics": {
            "total_turns": 1,
            "avg_slots_filled_per_turn": 1.0,
            "estimated_completion": 0.5,
        },
    }


def minimal_history(session_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "turn": 1,
            "turn_id": "turn_0001",
            "session_id": session_id,
            "timestamp": "2026-04-15T00:00:00Z",
            "user_input": "Need a marketplace workflow.",
            "agent_response": "Who are the first users?",
            "framework_delta": {"slots_updated": ["product_objective.core problem"]},
            "framework_snapshot": {"phase": "runtime"},
        }
    ]


def minimal_metadata(session_id: str, conversation_id: str) -> Dict[str, Any]:
    return {
        "session_id": session_id,
        "conversation_id": conversation_id,
        "created_at": "2026-04-15T00:00:00Z",
        "last_accessed": "2026-04-15T00:00:00Z",
        "last_updated": "2026-04-15T00:00:00Z",
        "state_version": "2.0.0",
        "schema_version": "2.0.0",
        "last_turn_id": "turn_0001",
        "last_successful_commit": None,
        "write_attempt_count": 0,
        "status": "active",
        "truncation_count": 0,
        "truncated_fields": [],
    }


def assert_ok(cp: subprocess.CompletedProcess, name: str) -> None:
    if cp.returncode != 0:
        raise RuntimeError(f"{name} failed:\nSTDOUT:\n{cp.stdout}\nSTDERR:\n{cp.stderr}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="state-tests-") as tmp:
        tmp_root = Path(tmp)
        state_root = tmp_root / "state"
        work_root = tmp_root / "work"
        work_root.mkdir(parents=True, exist_ok=True)

        session_id = "20260415_120000_A1B2C3"
        conversation_id = "conv_state_test"

        fw_path = work_root / "framework.json"
        hi_path = work_root / "history.json"
        md_path = work_root / "metadata.json"
        write_json(fw_path, minimal_framework(session_id, conversation_id))
        write_json(hi_path, minimal_history(session_id))
        write_json(md_path, minimal_metadata(session_id, conversation_id))

        # Case 1: normal commit + validate
        cp = run(
            [
                sys.executable,
                str(SCRIPTS / "commit_state.py"),
                "--state-root",
                str(state_root),
                "--session-id",
                session_id,
                "--turn-id",
                "turn_0001",
                "--framework-file",
                str(fw_path),
                "--history-file",
                str(hi_path),
                "--metadata-file",
                str(md_path),
                "--schema",
                str(SCHEMA),
            ],
            ROOT,
        )
        assert_ok(cp, "commit_state normal")

        cp = run(
            [
                sys.executable,
                str(SCRIPTS / "validate_state.py"),
                "--state-root",
                str(state_root),
                "--schema",
                str(SCHEMA),
                "--session-id",
                session_id,
            ],
            ROOT,
        )
        assert_ok(cp, "validate_state normal")
        current_file = state_root / "sessions" / session_id / "CURRENT"
        if not current_file.exists():
            raise RuntimeError("CURRENT pointer not created after normal commit")
        revision_id = current_file.read_text(encoding="utf-8").strip()
        if not revision_id:
            raise RuntimeError("CURRENT pointer is empty")
        revision_dir = state_root / "sessions" / session_id / "revisions" / revision_id
        if not revision_dir.exists():
            raise RuntimeError("CURRENT points to missing revision directory")

        # Case 2: duplicate turn retry with same payload should still pass
        cp = run(
            [
                sys.executable,
                str(SCRIPTS / "commit_state.py"),
                "--state-root",
                str(state_root),
                "--session-id",
                session_id,
                "--turn-id",
                "turn_0001",
                "--framework-file",
                str(fw_path),
                "--history-file",
                str(hi_path),
                "--metadata-file",
                str(md_path),
                "--schema",
                str(SCHEMA),
            ],
            ROOT,
        )
        assert_ok(cp, "commit_state duplicate idempotent")

        # Case 3: interrupted commit recovery simulation
        pending = state_root / "sessions" / session_id / "pending_commit.json"
        write_json(
            pending,
            {
                "session_id": session_id,
                "turn_id": "turn_9999",
                "content_hash": "fake",
                "timestamp": "2026-04-15T00:00:00Z",
            },
        )
        cp = run(
            [
                sys.executable,
                str(SCRIPTS / "commit_state.py"),
                "--state-root",
                str(state_root),
                "--session-id",
                session_id,
                "--turn-id",
                "turn_0001",
                "--framework-file",
                str(fw_path),
                "--history-file",
                str(hi_path),
                "--metadata-file",
                str(md_path),
                "--schema",
                str(SCHEMA),
            ],
            ROOT,
        )
        assert_ok(cp, "commit_state recovery path")

        # Case 4: schema drift migration
        md_live = state_root / "sessions" / session_id / "metadata.json"
        metadata = json.loads(md_live.read_text(encoding="utf-8"))
        metadata["schema_version"] = "1.1.0"
        write_json(md_live, metadata)
        cp = run(
            [
                sys.executable,
                str(SCRIPTS / "check_state_drift.py"),
                "--state-root",
                str(state_root),
                "--session-id",
                session_id,
                "--schema",
                str(SCHEMA),
                "--migrate",
            ],
            ROOT,
        )
        assert_ok(cp, "check_state_drift migrate")
        revision_after_migrate = current_file.read_text(encoding="utf-8").strip()
        if revision_after_migrate == revision_id:
            raise RuntimeError("migration did not advance CURRENT revision pointer")

        print("[OK] all state tests passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
