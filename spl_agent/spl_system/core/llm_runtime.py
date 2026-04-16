from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from openai import OpenAI

from .config import AppConfig, LLMConfig

logger = logging.getLogger("spl_system.llm")


def resolve_config_path(config_path: str | Path | None = None) -> Path:
    if config_path is not None:
        return Path(config_path)
    env_path = os.getenv("SPL_CONFIG_PATH")
    if env_path:
        return Path(env_path)
    return Path("settings.yaml")


def load_runtime_llm_config(config_path: str | Path | None = None) -> LLMConfig:
    path = resolve_config_path(config_path)
    if path.exists():
        return AppConfig.load(path).llm
    return LLMConfig()


def create_openai_client(
    llm_config: Optional[LLMConfig] = None,
    config_path: str | Path | None = None,
) -> Tuple[OpenAI, LLMConfig]:
    config = llm_config or load_runtime_llm_config(config_path)
    base_url = (config.base_url or "").rstrip("/")
    if base_url and not base_url.endswith("/v1"):
        base_url = f"{base_url}/v1"
    normalized = config.model_copy(update={"base_url": base_url or config.base_url})
    return OpenAI(api_key=normalized.api_key, base_url=normalized.base_url), normalized


def _llm_log_path() -> Path:
    env_path = (os.getenv("SPL_LLM_IO_LOG_PATH") or "").strip()
    if env_path:
        path = Path(env_path)
    else:
        path = Path(".spl_cache") / "llm_io.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _write_llm_event(event: Dict[str, Any]) -> None:
    payload = dict(event)
    payload["timestamp"] = datetime.now(timezone.utc).isoformat()
    line = json.dumps(payload, ensure_ascii=False)
    with _llm_log_path().open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def chat_completion_with_logging(
    client: OpenAI,
    llm_config: LLMConfig,
    messages: List[Dict[str, Any]],
    *,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    timeout: Optional[int] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    call_id = str(uuid4())
    request_payload = {
        "model": model or llm_config.model,
        "messages": messages,
        "temperature": llm_config.temperature if temperature is None else temperature,
        "timeout": llm_config.timeout_sec if timeout is None else timeout,
    }
    meta = {
        "call_id": call_id,
        "base_url": llm_config.base_url,
        "context": context or {},
    }
    _write_llm_event({"event": "request", **meta, "payload": request_payload})
    logger.info("spl_llm_request call_id=%s context=%s", call_id, json.dumps(meta["context"], ensure_ascii=False))
    try:
        response = client.chat.completions.create(
            model=request_payload["model"],
            messages=request_payload["messages"],
            temperature=request_payload["temperature"],
            timeout=request_payload["timeout"],
        )
        raw = response.model_dump() if hasattr(response, "model_dump") else {}
        _write_llm_event({"event": "response", **meta, "response": raw})
        logger.info("spl_llm_response call_id=%s", call_id)
        return response
    except Exception as exc:
        _write_llm_event(
            {"event": "error", **meta, "error_type": type(exc).__name__, "error_message": str(exc)}
        )
        logger.exception("spl_llm_error call_id=%s", call_id)
        raise
