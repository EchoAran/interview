from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class LLMConfig(BaseModel):
    api_key: str = Field(default="", description="LLM API key")
    base_url: str = Field(default="https://api.rcouyi.com/v1")
    model: str = Field(default="gpt-5")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    timeout_sec: int = Field(default=120, ge=5)

    @property
    def enabled(self) -> bool:
        return bool(self.api_key and self.model)


class RuntimeConfig(BaseModel):
    workspace_dir: str = ".spl_i"
    build_workers: int = Field(default=4, ge=1, le=32)
    use_llm_for_build: bool = True
    markdown_name: str = "SPL_RESULT.md"


class AppConfig(BaseModel):
    llm: LLMConfig = Field(default_factory=LLMConfig)
    runtime: RuntimeConfig = Field(default_factory=RuntimeConfig)

    @classmethod
    def load(cls, file_path: str | Path) -> "AppConfig":
        path = Path(file_path)
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        data = cls._normalize_legacy_keys(data)
        return cls.model_validate(data)

    @staticmethod
    def _normalize_legacy_keys(data: dict) -> dict:
        normalized = dict(data)

        llm_block = dict(normalized.get("llm") or {})
        if "OpenAI_API_Base" in normalized and "base_url" not in llm_block:
            llm_block["base_url"] = normalized["OpenAI_API_Base"]
        if "API_key_list" in normalized and "api_key" not in llm_block:
            key_list = normalized.get("API_key_list") or []
            if isinstance(key_list, list) and key_list:
                llm_block["api_key"] = str(key_list[0]).strip()
        if "model_name" in normalized and "model" not in llm_block:
            llm_block["model"] = normalized["model_name"]
        if llm_block:
            normalized["llm"] = llm_block

        return normalized
