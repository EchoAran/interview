# AgentScope Skill Chatbox

基于 AgentScope 构建的双端 Chatbox（CLI + Web），系统 Agent 支持挂载并使用 `skills`。

## 目录结构

```text
agentscope_chatbox/
  core.py                 # 核心服务：模型配置、skill 注册、会话对话
  cli.py                  # CLI 入口
  web.py                  # Web 服务入口（内置 HTTPServer）
  static/index.html       # Chatbox 前端
  skills/
    general_assistant/
      SKILL.md            # 示例 skill
```

## 运行前准备

1. 安装 AgentScope 依赖（建议在虚拟环境中）：

```bash
pip install -e ./agentscope
```

2. 在项目根目录创建 `.env`（使用 OpenAI 兼容第三方接口）：

```dotenv
OPENAI_BASE_URL=https://your-openai-compatible-endpoint/v1
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=your_model_name
```

说明：
- 这三个字段为必填；
- 程序启动时会自动读取 `e:\PycharmProjects\interview\.env`；
- 同名配置以 `.env` 为准，避免被外部系统环境变量干扰。

## 启动 CLI

```bash
python agentscope_chatbox/cli.py
```

可选参数：

```bash
python agentscope_chatbox/cli.py --skill-root agentscope_chatbox/skills --session-id demo
```

CLI 命令：

- `/skills` 查看已挂载 skill
- `/reset` 清空当前会话
- `/exit` 退出

## 启动 Web

```bash
python agentscope_chatbox/web.py --host 127.0.0.1 --port 8080
```

打开浏览器访问：`http://127.0.0.1:8080`

## 如何新增 skill

在 `agentscope_chatbox/skills` 下创建新目录并放置 `SKILL.md`：

```markdown
---
name: your_skill_name
description: skill 描述
---

# Skill Content
...
```

系统会自动发现 `skills` 根目录下所有包含 `SKILL.md` 的目录并挂载。

## 设计说明

- 使用 `Toolkit.register_agent_skill` 挂载 skills；
- 系统默认为 agent 注入 `view_text_file / execute_python_code / execute_shell_command`，保证 skill 可被读取和执行；
- 为避免跨事件循环状态问题，服务端每轮对话会重建 agent，并回放该会话历史，确保 CLI 与 Web 行为一致。
