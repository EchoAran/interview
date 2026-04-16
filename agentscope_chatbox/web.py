from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from core import ModelConfig, SkillChatboxService, discover_skill_dirs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AgentScope Skill Chatbox Web")
    parser.add_argument("--host", default="127.0.0.1", help="监听地址")
    parser.add_argument("--port", type=int, default=8080, help="监听端口")
    parser.add_argument(
        "--skill-root",
        default="agentscope_chatbox/skills",
        help="skills 根目录",
    )
    return parser.parse_args()


def build_handler(service: SkillChatboxService) -> type[BaseHTTPRequestHandler]:
    static_file = Path(__file__).resolve().parent / "static" / "index.html"

    class ChatHandler(BaseHTTPRequestHandler):
        def _write_json(self, status: int, payload: dict) -> None:
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _write_text(self, status: int, body: str) -> None:
            raw = body.encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path == "/":
                html = static_file.read_text(encoding="utf-8")
                raw = html.encode("utf-8")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
                return

            if path == "/api/skills":
                self._write_json(
                    HTTPStatus.OK,
                    {"skills": service.list_skills()},
                )
                return

            self._write_text(HTTPStatus.NOT_FOUND, "Not Found")

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            if path != "/api/chat":
                self._write_text(HTTPStatus.NOT_FOUND, "Not Found")
                return

            content_len = int(self.headers.get("Content-Length", "0"))
            if content_len <= 0:
                self._write_json(
                    HTTPStatus.BAD_REQUEST,
                    {"error": "请求体不能为空"},
                )
                return

            body = self.rfile.read(content_len).decode("utf-8")
            try:
                payload = json.loads(body)
                message = str(payload.get("message", "")).strip()
                session_id = str(payload.get("session_id", "web-default")).strip()
            except json.JSONDecodeError:
                self._write_json(HTTPStatus.BAD_REQUEST, {"error": "JSON 格式错误"})
                return

            if not message:
                self._write_json(
                    HTTPStatus.BAD_REQUEST,
                    {"error": "message 不能为空"},
                )
                return

            try:
                answer = service.chat_sync(session_id=session_id, user_text=message)
            except Exception as exc:  # noqa: BLE001
                self._write_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"error": f"处理失败: {exc}"},
                )
                return

            self._write_json(
                HTTPStatus.OK,
                {
                    "session_id": session_id,
                    "answer": answer,
                    "skills": service.list_skills(),
                },
            )

        def log_message(self, fmt: str, *args) -> None:
            # 保留服务端日志输出，但格式更简洁。
            print(f"[HTTP] {self.address_string()} - {fmt % args}")

    return ChatHandler


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

    server = HTTPServer((args.host, args.port), build_handler(service))
    print(f"Web Chatbox 已启动: http://{args.host}:{args.port}")
    print("按 Ctrl+C 退出。")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Web Chatbox 已关闭。")


if __name__ == "__main__":
    main()
