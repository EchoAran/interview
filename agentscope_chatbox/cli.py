from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from core import ModelConfig, SkillChatboxService, discover_skill_dirs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AgentScope Skill Chatbox CLI")
    parser.add_argument(
        "--skill-root",
        default="agentscope_chatbox/skills",
        help="skills 根目录，默认自动发现其下包含 SKILL.md 的目录",
    )
    parser.add_argument(
        "--session-id",
        default="cli-default",
        help="会话 ID，用于维持上下文记忆",
    )
    return parser.parse_args()


async def run_chat(session_id: str, service: SkillChatboxService) -> None:
    print("Skill Chatbox CLI 已启动。输入 /exit 退出，/skills 查看已挂载技能，/reset 清空当前会话。")
    while True:
        user_text = input("\n你: ").strip()
        if not user_text:
            continue
        if user_text == "/exit":
            print("已退出。")
            return
        if user_text == "/skills":
            print("已挂载 skills:")
            for name in service.list_skills():
                print(f"- {name}")
            continue
        if user_text == "/reset":
            service.reset_session(session_id)
            print(f"会话 `{session_id}` 已清空。")
            continue

        answer = await service.chat(session_id=session_id, user_text=user_text)
        print(f"Agent: {answer}")


def main() -> None:
    args = parse_args()
    skill_dirs = discover_skill_dirs(Path(args.skill_root).resolve())
    if not skill_dirs:
        raise ValueError(
            f"未发现可用 skills。请检查目录: {Path(args.skill_root).resolve()}",
        )

    service = SkillChatboxService(
        model_config=ModelConfig.from_env(),
        skill_dirs=skill_dirs,
    )
    asyncio.run(run_chat(args.session_id, service))


if __name__ == "__main__":
    main()
