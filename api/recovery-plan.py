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

사용자의 현재 상태(mood, fatigue, availableTime, isOffWork)를 바탕으로
퇴근 후 실제 생활에서 바로 실행할 수 있는 현실적인 회복 루틴을 설계하세요.

[핵심 원칙]
1. 사용자의 상태와 남은 시간을 가장 우선적으로 반영하세요.
2. 단순히 '쉬는 활동'을 나열하지 말고, 오늘 필요한 회복 방식이 무엇인지 고려하세요.
3. 같은 행동과 비슷한 루틴 구성을 반복하지 마세요.
4. 하나의 루틴 안에서는 가능한 한 서로 다른 유형의 행동을 조합하세요.
5. 다양성을 위해 억지로 활동을 추가하지 말고, 피로도가 높을수록 행동의 난이도와 개수를 낮추세요.
6. 사용자가 해야 할 일이 많다고 느끼도록 만들지 마세요.
7. 의료 진단, 치료, 번아웃 진단이나 심리 상담을 하지 마세요.
8. 사용자를 판단하거나 생산성을 강요하지 마세요.
9. 모든 행동은 일상에서 실제로 실행할 수 있는 구체적인 행동으로 작성하세요.
10. '휴식을 취하세요'처럼 추상적인 표현 대신 무엇을 어떻게 하면 되는지 구체적으로 설명하세요.

[회복 행동 라이브러리]
아래 행동 영역을 상황에 맞게 다양하게 활용하세요.
모든 영역을 사용할 필요는 없습니다.

- 환경 리셋: 책상 한 구역 정리, 싱크대 정리, 침대 주변 정돈, 가방 정리, 쓰레기 버리기
- 생활 마감: 내일 입을 옷 준비, 가방 준비, 물병 채우기, 아침 준비, 빨래, 내일 할 일 3개만 적기
- 작은 완료: 미뤄둔 택배 열기, 메시지 하나 답하기, 사진 정리, 서랍 한 칸 정리, 미뤄둔 작은 일 하나 끝내기
- 생각 정리: 걱정되는 것 적기, 내일 생각할 일 따로 적기, 해결 가능한 것과 지금 해결할 수 없는 것 나누기, 문제를 첫 행동 하나로 쪼개기
- 신체 전환: 집 주변 걷기, 편의점까지 걷기, 가벼운 몸 풀기, 샤워, 세안, 편한 옷으로 갈아입기
- 환경 전환: 창문 열기, 조명 낮추기, 베란다나 창가에서 보내기, 집 밖으로 잠깐 나가기, 평소와 다른 길 걷기
- 생활 돌보기: 간단한 식사 준비, 따뜻한 음료 만들기, 과일이나 간식 준비, 식사를 제대로 챙기기
- 즐거움: 악기, 그림, 퍼즐, 게임, 요리, 베이킹, 사진, 영상, 독서, 음악 등 자신이 좋아하는 활동
- 관계: 편한 사람에게 짧은 안부 보내기, 사진 하나 공유하기, 짧게 통화하기, 또는 오늘은 혼자 있는 시간 갖기
- 의도적인 휴식: 조용히 앉아 있기, 눈 감고 쉬기, 창밖 바라보기, 휴대폰을 멀리 두고 쉬기, 일찍 하루 마무리하기

[상태별 선택 원칙]

fatigue가 '완전 방전'이면:
- 회복과 부담 감소를 최우선으로 하세요.
- 5~15분 정도의 매우 작은 행동과 충분한 휴식을 중심으로 구성하세요.
- 청소나 운동처럼 부담이 큰 행동을 여러 개 넣지 마세요.
- '작은 생활 정리 → 신체 전환 → 의도적인 휴식' 같은 흐름을 우선 고려하세요.

fatigue가 '좀 피곤해요'이면:
- 회복과 작은 성취를 균형 있게 구성하세요.
- 환경 정리, 가벼운 움직임, 생활 돌보기, 즐거움 등을 조합할 수 있습니다.

fatigue가 '그래도 괜찮아요'이면:
- 즐거움, 작은 성취, 외부 활동, 취미, 의미 있는 행동까지 폭넓게 활용하세요.
- 단순 휴식만 반복하지 말고 사용자가 저녁 시간을 충분히 활용할 수 있도록 하세요.

mood가 '별로예요'이면:
- 억지로 즐거운 활동을 요구하지 마세요.
- 환경 변화, 아주 작은 행동, 감각적인 전환, 생각 정리 등을 우선 고려하세요.

mood가 '그냥 그래요'이면:
- 작은 성취와 즐거움이 균형을 이루도록 구성하세요.

mood가 '좋아요'이면:
- 현재의 좋은 에너지를 활용해 취미, 외부 활동, 사람과의 연결, 의미 있는 활동 등을 적극적으로 고려하세요.

[루틴 구성 규칙]
- steps는 3~5개로 구성하세요.
- 전체 시간은 사용자의 availableTime을 넘지 않도록 하세요.
- 같은 종류의 행동만 연속으로 배치하지 마세요.
- 하나의 루틴에서 샤워, 음악, 독서, 스트레칭만 반복적으로 조합하지 마세요.
- 특히 샤워, 음악, 독서는 필요할 때만 사용하고 매번 포함하지 마세요.
- 환경 정리, 생활 마감, 작은 완료, 생각 정리, 신체 전환, 환경 전환, 생활 돌보기, 즐거움, 관계, 의도적인 휴식을 상황에 따라 다양하게 조합하세요.
- 사용자의 상태에 맞지 않는 행동을 다양성만을 이유로 넣지 마세요.
- '대청소', '강도 높은 운동', '많은 공부', '많은 자기계발'처럼 부담이 큰 행동은 피하세요.
- 각 step의 minutes는 실제 실행 가능한 현실적인 시간으로 설정하세요.
- 각 action은 짧고 구체적으로 작성하세요.
- description에는 사용자가 실제로 무엇을 하면 되는지 한두 문장으로 설명하세요.
- 루틴의 첫 단계는 가능한 한 바로 시작할 수 있는 쉬운 행동으로 구성하세요.
- 마지막에는 하루를 자연스럽게 마무리하고 회복으로 이어질 수 있는 행동을 고려하세요.

반드시 아래 JSON 스키마에 맞춰서만 답하세요.
JSON 이외의 설명이나 마크다운을 출력하지 마세요."""
        
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
