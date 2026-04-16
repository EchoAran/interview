from __future__ import annotations

import shutil
from pathlib import Path
import platform
import re
import subprocess
from typing import Optional

from .models import SourceHandle, stable_hash


class SourceResolver:
    def __init__(self, workspace_dir: str | Path):
        self.workspace_dir = Path(workspace_dir)
        self.sources_dir = self.workspace_dir / "sources"
        self.sources_dir.mkdir(parents=True, exist_ok=True)

    def normalize_git_url(self, repo_url: str) -> str:
        text = repo_url.strip()
        text = text.rstrip("/")
        text = re.sub(r"\.git$", "", text)
        return text

    def resolve_git(
        self,
        repo_url: str,
        commit: Optional[str] = None,
        project_name: Optional[str] = None,
    ) -> SourceHandle:
        normalized_url = self.normalize_git_url(repo_url)
        source_hash = stable_hash(normalized_url)
        checkout_dir = self.sources_dir / f"git_{source_hash[:16]}"
        if checkout_dir.exists():
            shutil.rmtree(checkout_dir, ignore_errors=True)
        self._run_git(["git", "clone", repo_url.strip(), str(checkout_dir)])
        requested_ref = commit or "HEAD"
        self._run_git(["git", "-C", str(checkout_dir), "checkout", requested_ref])
        resolved_commit = self._run_git(["git", "-C", str(checkout_dir), "rev-parse", "HEAD"]).strip()

        name = project_name or Path(normalized_url).name or resolved_commit[:8]
        project_id = f"git:{source_hash[:16]}:{resolved_commit[:12]}"
        return SourceHandle(
            source_type="git",
            display_name=name,
            project_root=checkout_dir,
            cache_key=normalized_url,
            project_id=project_id,
            normalized_source=normalized_url,
            commit=resolved_commit,
            metadata={
                "repo_url": repo_url,
                "normalized_repo_url": normalized_url,
                "checkout_dir": str(checkout_dir),
                "requested_ref": requested_ref,
                "resolved_commit": resolved_commit,
            },
        )

    def _run_git(self, command: list[str]) -> str:
        run_cmd = command
        if platform.system().lower().startswith("win") and command and command[0].lower() == "git":
            # Force long-path support for this invocation to reduce Windows filename-too-long failures.
            run_cmd = ["git", "-c", "core.longpaths=true", *command[1:]]
        proc = subprocess.run(run_cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            stderr = proc.stderr.strip() or proc.stdout.strip()
            raise RuntimeError(f"Git command failed: {' '.join(command)}\n{stderr}")
        return proc.stdout.strip()
