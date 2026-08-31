import json
import os
from http.server import BaseHTTPRequestHandler

from openai import OpenAI


REQUIRED_FIELDS = {"isOffWork", "mood", "fatigue", "availableTime"}


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "잘못된 요청 형식입니다."})
            return

        if not REQUIRED_FIELDS.issubset(payload):
            self._send_json(400, {"error": "필수 질문에 모두 답해 주세요."})
            return

        if not os.environ.get("OPENAI_API_KEY"):
            self._send_json(500, {"error": "서버 환경 변수가 설정되지 않았습니다."})
            return

        instructions = """당신은 '오프온'의 회복 루틴 플래너입니다.
사용자에게 일상에서 바로 할 수 있는, 부담 없고 구체적인 저녁 회복 루틴을 한국어로 제안하세요.
의료 진단, 치료 조언, 번아웃 진단은 하지 마세요. 사용자를 판단하거나 압박하지 마세요.
반드시 JSON 스키마에 맞춰서만 답하세요. steps는 3~5개이고, 전체 시간은 사용자의 availableTime에 맞춰야 합니다."""
        user_input = json.dumps(payload, ensure_ascii=False)
        schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "summary": {"type": "string"},
                "steps": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 5,
                    "items": {
                        "type": "object",
                        "properties": {
                            "minutes": {"type": "integer"},
                            "action": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["minutes", "action", "description"],
                        "additionalProperties": False,
                    },
                },
                "tip": {"type": "string"},
                "closing_message": {"type": "string"},
            },
            "required": ["title", "summary", "steps", "tip", "closing_message"],
            "additionalProperties": False,
        }

        try:
            client = OpenAI()
            response = client.responses.create(
                model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
                instructions=instructions,
                input=user_input,
                max_output_tokens=800,
                text={"format": {"type": "json_schema", "name": "recovery_plan", "strict": True, "schema": schema}},
            )
            self._send_json(200, json.loads(response.output_text))
        except Exception:
            self._send_json(502, {"error": "AI 응답을 생성하지 못했습니다."})

    def do_GET(self):
        self._send_json(405, {"error": "POST 요청만 지원합니다."})
