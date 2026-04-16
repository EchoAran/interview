# -*- coding: utf-8 -*-
"""The main entry point of the ReAct agent example."""
import asyncio
import os

from agentscope.agent import ReActAgent, UserAgent
from agentscope.formatter import OpenAIChatFormatter
from agentscope.memory import InMemoryMemory
from agentscope.model import OpenAIChatModel
from agentscope.tool import (
    Toolkit,
    execute_shell_command,
    execute_python_code,
    view_text_file,
)


async def main() -> None:
    """The main entry point for the ReAct agent example."""
    openai_base_url = os.environ.get("OPENAI_BASE_URL")
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    openai_model = os.environ.get("OPENAI_MODEL")

    if not openai_base_url or not openai_api_key or not openai_model:
        raise ValueError(
            "Please set OPENAI_BASE_URL, OPENAI_API_KEY and OPENAI_MODEL "
            "before running this example.",
        )

    toolkit = Toolkit()

    toolkit.register_tool_function(execute_shell_command)
    toolkit.register_tool_function(execute_python_code)
    toolkit.register_tool_function(view_text_file)

    agent = ReActAgent(
        name="Friday",
        sys_prompt="You are a helpful assistant named Friday.",
        model=OpenAIChatModel(
            api_key=openai_api_key,
            model_name=openai_model,
            stream=True,
            client_kwargs={"base_url": openai_base_url},
        ),
        formatter=OpenAIChatFormatter(),
        toolkit=toolkit,
        memory=InMemoryMemory(),
    )

    user = UserAgent("User")

    msg = None
    while True:
        msg = await user(msg)
        if msg.get_text_content() == "exit":
            break
        msg = await agent(msg)


asyncio.run(main())
