from __future__ import annotations

import argparse
import json
from pathlib import Path

from spl_system.core.config import AppConfig
from spl_system.core.service import SPLProjectService


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SPL markdown from a config file.")
    parser.add_argument("--config", default="settings.yaml", help="Path to the YAML config file.")
    parser.add_argument("--url", required=True, help="Git repository URL.")
    parser.add_argument("--commit", default=None, help="Optional git ref override.")
    parser.add_argument("--project-name", default=None, help="Optional project name override.")
    parser.add_argument("--markdown-name", default=None, help="Optional markdown output filename.")
    parser.add_argument("--use-llm-for-build", default=None, choices=["true", "false"], help="Override LLM usage.")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = AppConfig.load(config_path)
    source_commit = args.commit
    source_project_name = args.project_name
    markdown_name = args.markdown_name or config.runtime.markdown_name
    if args.use_llm_for_build is None:
        use_llm_for_build = config.runtime.use_llm_for_build
    else:
        use_llm_for_build = args.use_llm_for_build.lower() == "true"

    service = SPLProjectService.from_config(config, base_dir=Path(__file__).resolve().parent)
    build_result = service.generate_markdown_only(
        repo_url=args.url,
        commit=source_commit,
        project_name=source_project_name,
        use_llm_for_build=use_llm_for_build,
        markdown_name=markdown_name,
    )
    print(json.dumps(build_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
