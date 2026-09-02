# OFF:ON (오프온)

> 업무는 OFF, 나의 회복은 ON.

퇴근 후의 기분, 피로도, 남은 시간에 따라 AI가 지금의 나에게 맞는 현실적인 회복 루틴을 제안하는 웹 서비스입니다.

## 서비스 소개

OFF:ON은 퇴근 후 무언가를 더 해내야 한다는 부담 대신,
현재의 상태와 남은 시간을 바탕으로 오늘 나에게 필요한 회복 방법을 제안합니다.

### 주요 기능

- 퇴근 여부, 기분, 피로도, 남은 시간을 단계별로 입력
- Google Gemini API를 활용한 개인 맞춤형 회복 루틴 생성
- 3~5개의 구체적인 회복 단계와 실행 시간 제공
- 상태와 여유 시간에 따라 다양한 회복 행동 조합
- 데스크톱 및 모바일 반응형 화면 지원
- AI 및 API 오류 발생 시 사용자 안내

## 기술 스택

- Frontend: HTML, CSS, Vanilla JavaScript
- Backend: Vercel Serverless Functions (Python)
- AI: Google Gemini API
- Deployment: Vercel

## 프로젝트 구조

    OFF-ON/
    ├── index.html
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    ├── api/
    │   └── recovery-plan.py
    ├── outputs/
    │   └── OFFON_PRD.md
    ├── requirements.txt
    ├── vercel.json
    └── .gitignore

### 주요 파일 설명

- `index.html`: 웹 서비스의 화면 구성
- `css/style.css`: 반응형 디자인 및 스타일
- `js/app.js`: 질문 흐름, API 호출, 결과 화면 처리
- `api/recovery-plan.py`: Gemini API를 호출하는 Python Serverless Function
- `outputs/OFFON_PRD.md`: 서비스 기획서
- `requirements.txt`: Python 패키지 의존성
- `vercel.json`: Vercel 배포 설정
- `.gitignore`: 환경 변수 등 Git에서 제외할 파일 설정

## AI 동작 방식

사용자가 플래너에서 다음 정보를 입력합니다.

1. 퇴근 여부
2. 현재 기분
3. 현재 피로도
4. 저녁에 사용할 수 있는 시간

입력된 정보는 프론트엔드에서 `/api/recovery-plan`으로 전달됩니다.

Python Serverless Function이 Google Gemini API를 호출하고,
AI가 생성한 회복 루틴을 JSON 형태로 반환합니다.

반환된 결과는 프론트엔드에서 회복 루틴 카드 형태로 표시됩니다.

    사용자 입력
        ↓
    HTML / JavaScript
        ↓
    fetch('/api/recovery-plan')
        ↓
    Vercel Serverless Function (Python)
        ↓
    Google Gemini API
        ↓
    JSON 회복 루틴
        ↓
    웹 화면에 결과 표시

## 로컬 실행

정적 화면은 `index.html`을 브라우저에서 열어 확인할 수 있습니다.

API까지 함께 테스트하려면 Vercel CLI를 사용합니다.

    npm install -g vercel
    vercel dev

## 환경 변수

로컬 개발 시 `.env` 파일에 Gemini API 키를 설정합니다.

    GEMINI_API_KEY=your_api_key

선택 사항:

    GEMINI_MODEL=gemini-3.1-flash-lite

API 키는 프론트엔드 코드에 직접 작성하지 않습니다.

`.env` 파일은 `.gitignore`에 포함하여 GitHub에 업로드하지 않습니다.

Vercel 배포 시에는 Project Settings → Environment Variables에서
`GEMINI_API_KEY`를 등록해야 합니다.

## 배포

1. GitHub에 프로젝트를 업로드합니다.
2. Vercel에서 GitHub 저장소를 Import합니다.
3. `GEMINI_API_KEY`를 환경 변수에 등록합니다.
4. Deploy를 실행합니다.
5. 배포된 URL에서 플래너와 AI 루틴 생성 기능을 테스트합니다.

### 배포 URL

https://off-on-one.vercel.app/

### GitHub

https://github.com/bomigrace-byte/OFF-ON

## 주의사항

OFF:ON이 제공하는 결과는 일상적인 회복을 위한 아이디어입니다.

의료적 진단이나 치료, 전문적인 심리 상담을 대신하지 않습니다.
