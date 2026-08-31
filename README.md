# OFF:ON (오프온)

퇴근 후의 기분, 피로도, 남은 시간에 따라 AI가 작은 회복 루틴을 제안하는 웹 서비스입니다.

## 기술 스택

- Frontend: HTML, CSS, Vanilla JavaScript
- Backend: Vercel Serverless Functions (Python)
- AI: OpenAI Responses API
- Deployment: Vercel

## 프로젝트 구조

```text
index.html       # 화면
css/style.css    # 반응형 스타일
js/app.js        # 질문 흐름, fetch, 결과 렌더링
api/recovery-plan.py # AI API를 호출하는 Python 함수
```

## 로컬 실행

정적 화면은 `index.html`을 브라우저에서 열어 확인할 수 있습니다. API까지 테스트하려면 Vercel CLI를 사용합니다.

```bash
npm install -g vercel
vercel dev
```

## 환경 변수

`.env` 파일에 아래 값을 설정합니다. 이 파일은 절대 GitHub에 올리지 않습니다.

```text
OPENAI_API_KEY=your_api_key
# 선택: 사용할 모델을 지정할 때만 설정
OPENAI_MODEL=gpt-4.1-mini
```

Vercel 배포 시에도 Project Settings → Environment Variables에서 `OPENAI_API_KEY`를 등록해야 합니다.

## 배포

1. GitHub에 프로젝트를 올립니다.
2. Vercel에서 해당 저장소를 Import합니다.
3. `OPENAI_API_KEY`를 환경 변수로 등록합니다.
4. Deploy를 누르고, 생성된 URL에서 질문·결과 생성 기능을 테스트합니다.

배포 URL: 배포 후 이곳에 작성

## 주의

오프온의 결과는 일상 회복을 위한 아이디어이며 의료 또는 심리 상담을 대신하지 않습니다.
