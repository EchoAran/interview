from __future__ import annotations

import os
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Optional

from .builder import ProjectSPLBuilder
from .config import AppConfig, LLMConfig
from .semantic_builder import FunctionSemanticBuilder
from .sources import SourceResolver


class SPLProjectService:
    def __init__(
        self,
        base_dir: str | Path,
        llm_config: LLMConfig,
        workspace_dir: str | Path,
        build_workers: int = 4,
    ):
        self.base_dir = Path(base_dir)
        self.workspace_dir = (self.base_dir / workspace_dir).resolve()
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.sources = SourceResolver(self.workspace_dir)
        os.environ.setdefault("SPL_LLM_IO_LOG_PATH", str(self.workspace_dir / "llm_io.jsonl"))
        self.semantic_builder = FunctionSemanticBuilder(llm_config=llm_config, base_dir=self.base_dir)
        self.builder = ProjectSPLBuilder(self.semantic_builder, max_workers=build_workers)

    @classmethod
    def from_config(cls, config: AppConfig, base_dir: str | Path) -> "SPLProjectService":
        return cls(
            base_dir=base_dir,
            llm_config=config.llm,
            workspace_dir=config.runtime.workspace_dir,
            build_workers=config.runtime.build_workers,
        )

    def generate_markdown_only(
        self,
        repo_url: str,
        commit: Optional[str] = None,
        project_name: Optional[str] = None,
        use_llm_for_build: bool = True,
        markdown_name: str = "SPL_RESULT.md",
    ) -> Dict[str, Any]:
        if not repo_url.strip():
            raise ValueError("repo_url is required")
        handle = self.sources.resolve_git(
            repo_url=repo_url,
            commit=commit,
            project_name=project_name,
        )

        _, exported_spl = self.builder.build_from_source(handle, use_llm=use_llm_for_build)
        markdown_path = self.base_dir / markdown_name
        markdown_path.write_text(
            self._render_markdown(
                project_name=handle.display_name,
                source_type=handle.source_type,
                source_value=handle.normalized_source,
                commit=handle.commit,
                exported_spl=exported_spl,
            ),
            encoding="utf-8",
        )
        self._cleanup_workspace()
        return {
            "project_id": handle.project_id,
            "project_name": handle.display_name,
            "source_type": handle.source_type,
            "normalized_source": handle.normalized_source,
            "commit": handle.commit,
            "requested_ref": handle.metadata.get("requested_ref"),
            "markdown_path": str(markdown_path),
            "function_count": len(exported_spl),
        }

    def _render_markdown(
        self,
        project_name: str,
        source_type: str,
        source_value: str,
        commit: Optional[str],
        exported_spl: Dict[str, str],
    ) -> str:
        grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)
        for key, spl_text in exported_spl.items():
            module_path, qualified_name = key.split("::", 1)
            grouped[module_path].append((qualified_name, spl_text))
        for module_path in grouped:
            grouped[module_path].sort(key=lambda item: item[0])

        sorted_modules = sorted(grouped.keys())
        total_modules = len(sorted_modules)
        total_functions = len(exported_spl)

        lines: list[str] = []
        lines.append("# SPL Report")
        lines.append("")
        lines.append("## Project Overview")
        lines.append("")
        lines.append(f"- project_name: {project_name}")
        lines.append(f"- source_type: {source_type}")
        lines.append(f"- source: {source_value}")
        lines.append(f"- commit: {commit or 'N/A'}")
        lines.append(f"- module_count: {total_modules}")
        lines.append(f"- function_count: {total_functions}")
        lines.append("")
        lines.append("## Reading Guide")
        lines.append("")
        lines.append("- 先看 `Module Index`，快速定位模块。")
        lines.append("- 再看 `Function Index`，快速跳转到函数。")
        lines.append("- 每个函数都提供可折叠的 SPL 代码块，减少滚动干扰。")
        lines.append("")
        lines.append("## Module Index")
        lines.append("")
        for module_path in sorted_modules:
            module_anchor = self._anchor_id("module", module_path)
            lines.append(f"- [{module_path}](#{module_anchor}) ({len(grouped[module_path])} functions)")
        lines.append("")
        lines.append("## Function Index")
        lines.append("")
        for module_path in sorted_modules:
            lines.append(f"### {module_path}")
            lines.append("")
            for qualified_name, _ in grouped[module_path]:
                function_anchor = self._anchor_id("fn", f"{module_path}::{qualified_name}")
                lines.append(f"- [{qualified_name}](#{function_anchor})")
            lines.append("")

        lines.append("## SPL Details")
        lines.append("")
        for module_path in sorted_modules:
            module_anchor = self._anchor_id("module", module_path)
            lines.append(f'<a id="{module_anchor}"></a>')
            lines.append(f"### Module: {module_path}")
            lines.append("")
            lines.append(f"- function_count: {len(grouped[module_path])}")
            lines.append("")
            for qualified_name, spl_text in grouped[module_path]:
                function_anchor = self._anchor_id("fn", f"{module_path}::{qualified_name}")
                line_count = len(spl_text.splitlines())
                lines.append(f'<a id="{function_anchor}"></a>')
                lines.append(f"#### Function: {qualified_name}")
                lines.append("")
                lines.append(f"- key: `{module_path}::{qualified_name}`")
                lines.append(f"- spl_line_count: {line_count}")
                lines.append("")
                lines.append("<details>")
                lines.append("<summary>View SPL</summary>")
                lines.append("")
                lines.append("```spl")
                lines.append(spl_text.rstrip())
                lines.append("```")
                lines.append("")
                lines.append("</details>")
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    def _anchor_id(self, prefix: str, value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower()).strip("-")
        if not slug:
            slug = "item"
        return f"{prefix}-{slug}"

    def _cleanup_workspace(self) -> None:
        for entry in self.workspace_dir.iterdir():
            if entry.name == "llm_io.jsonl":
                entry.unlink(missing_ok=True)
                continue
            if entry.is_dir():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                entry.unlink(missing_ok=True)
