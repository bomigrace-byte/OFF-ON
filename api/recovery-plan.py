import json
import os
from http.server import BaseHTTPRequestHandler

from google import genai
from google.genai import types


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

        if not os.environ.get("GEMINI_API_KEY"):
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
                    "items": {
                        "type": "object",
                        "properties": {
                            "minutes": {"type": "integer"},
                            "action": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["minutes", "action", "description"],
                    },
                },
                "tip": {"type": "string"},
                "closing_message": {"type": "string"},
            },
            "required": ["title", "summary", "steps", "tip", "closing_message"]
        }

        try:
            client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
            response = client.models.generate_content(
                model=os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite"),
                contents=f"{instructions}\n\n사용자 입력 JSON:\n{user_input}",
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    max_output_tokens=700,
                    temperature=0.7,
                ),
            )
            self._send_json(200, json.loads(response.text))
        except Exception as error:
            print(f"Gemini request failed: {error}")
            error_status = getattr(error, "code", "unknown")
            self._send_json(502, {
                "error": "Gemini 응답을 생성하지 못했습니다.",
                "code": f"{type(error).__name__} ({error_status})"
            })

    def do_GET(self):
        self._send_json(405, {"error": "POST 요청만 지원합니다."})
