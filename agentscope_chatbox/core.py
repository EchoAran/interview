from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOCAL_AGENTSCOPE_SRC = PROJECT_ROOT / "agentscope" / "src"
if LOCAL_AGENTSCOPE_SRC.exists():
    sys.path.insert(0, str(LOCAL_AGENTSCOPE_SRC))

from agentscope.agent import ReActAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.message import Msg
from agentscope.model import OpenAIChatModel
from agentscope.tool import (
    Toolkit,
    execute_python_code,
    execute_shell_command,
    view_text_file,
)


DEFAULT_SYSTEM_PROMPT = """你是一个稳定、可靠的智能助手。

你具备已挂载的 skills，必须优先使用 skills 中的指令来回答任务。
如果任务信息不足，先通过可用工具读取 skill 目录下的 SKILL.md 及相关文件，再行动。

要求：
1. 不要臆断 skill 内容；
2. 尽量复用已挂载 skill 的约束、步骤和输出格式；
3. 给出答案时先满足正确性，再追求简洁性。
"""


@dataclass(frozen=True)
class ModelConfig:
    model_name: str
    api_key: str
    base_url: str
    stream: bool = False

    @classmethod
    def from_env(cls) -> "ModelConfig":
        # 按用户预期：以项目根目录 .env 为准，避免被外部系统环境变量污染。
        load_dotenv(PROJECT_ROOT / ".env", override=True)

        base_url = (os.getenv("OPENAI_BASE_URL") or "").strip()
        api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
        model_name = (os.getenv("OPENAI_MODEL") or "").strip()

        # 兼容误填 "Bearer xxx" 的情况，OpenAI SDK 会自行补 Bearer。
        if api_key.lower().startswith("bearer "):
            api_key = api_key[7:].strip()

        missing = []
        if not base_url:
            missing.append("OPENAI_BASE_URL")
        if not api_key:
            missing.append("OPENAI_API_KEY")
        if not model_name:
            missing.append("OPENAI_MODEL")

        if missing:
            raise ValueError(
                "未检测到完整的 OpenAI 兼容配置，请在项目根目录 `.env` 中设置："
                f"{', '.join(missing)}",
            )

        return cls(
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            stream=False,
        )


def load_dotenv(env_path: Path, override: bool = False) -> None:
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue

        if value and len(value) >= 2 and value[0] == value[-1] and value[0] in (
            "'",
            '"',
        ):
            value = value[1:-1]

        if override:
            os.environ[key] = value
        else:
            os.environ.setdefault(key, value)


def discover_skill_dirs(skill_root: Path) -> list[Path]:
    if not skill_root.exists():
        return []

    found: list[Path] = []
    if (skill_root / "SKILL.md").exists():
        found.append(skill_root)

    for child in sorted(skill_root.iterdir()):
        if child.is_dir() and (child / "SKILL.md").exists():
            found.append(child)
    return found


class SkillChatboxService:
    def __init__(
        self,
        model_config: ModelConfig,
        skill_dirs: list[Path],
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    ) -> None:
        self.model_config = model_config
        self.skill_dirs = [p.resolve() for p in skill_dirs]
        self.system_prompt = system_prompt
        self._sessions: dict[str, list[dict[str, Any]]] = {}

        # 预检 skills，启动阶段就暴露错误，避免运行中才失败。
        _ = self._build_toolkit()

    def list_skills(self) -> list[str]:
        return [p.name for p in self.skill_dirs]

    def reset_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    async def chat(self, session_id: str, user_text: str) -> str:
        agent = self._build_agent()
        history = self._sessions.setdefault(session_id, [])

        if history:
            await agent.observe([Msg.from_dict(item) for item in history])

        user_msg = Msg(name="user", content=user_text, role="user")
        reply = await agent(user_msg)

        history.append(user_msg.to_dict())
        history.append(reply.to_dict())
        return reply.get_text_content() or ""

    def chat_sync(self, session_id: str, user_text: str) -> str:
        return asyncio.run(self.chat(session_id=session_id, user_text=user_text))

    def _build_toolkit(self) -> Toolkit:
        toolkit = Toolkit()
        toolkit.register_tool_function(view_text_file)
        toolkit.register_tool_function(execute_python_code)
        toolkit.register_tool_function(execute_shell_command)

        for skill_dir in self.skill_dirs:
            toolkit.register_agent_skill(str(skill_dir))
        return toolkit

    def _build_agent(self) -> ReActAgent:
        toolkit = self._build_toolkit()
        model = OpenAIChatModel(
            model_name=self.model_config.model_name,
            api_key=self.model_config.api_key,
            stream=self.model_config.stream,
            client_kwargs={"base_url": self.model_config.base_url},
        )
        formatter = OpenAIChatFormatter()

        return ReActAgent(
            name="SkillChatboxAgent",
            sys_prompt=self.system_prompt,
            model=model,
            formatter=formatter,
            toolkit=toolkit,
            memory=InMemoryMemory(),
        )
