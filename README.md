# OFF:ON (오프온)

> **업무는 OFF, 나의 회복은 ON.**

퇴근 후의 기분, 피로도, 남은 시간에 따라 AI가 지금의 나에게 맞는 현실적인 회복 루틴을 제안하는 웹 서비스입니다.

## 🌿 서비스 소개

퇴근 후에는 쉬고 싶어도 “오늘 저녁에 뭘 하지?”를 결정하는 것 자체가 부담이 될 수 있습니다.

**OFF:ON**은 사용자의 현재 상태와 남은 시간을 간단하게 입력하면, 지금 실제로 실행할 수 있는 **개인 맞춤형 회복 루틴**을 AI가 제안합니다.

더 많은 일을 하게 만드는 것이 아니라, 업무가 끝난 뒤 **나에게 필요한 회복 시간을 돌려주는 것**을 목표로 합니다.

### 🎯 타겟 사용자

- 퇴근 후 피로하지만 무엇을 하며 쉴지 결정하기 어려운 직장인
- 혼자 보내는 저녁 시간을 조금 더 의식적으로 보내고 싶은 사용자
- 거창한 자기계발보다 현실적으로 실행 가능한 회복 루틴을 원하는 사용자

## ✨ 주요 기능

- 퇴근 여부, 기분, 피로도, 남은 시간을 단계별로 입력
- Google Gemini API를 활용한 개인 맞춤형 회복 루틴 생성
- 3~5개의 구체적인 회복 단계와 실행 시간 제공
- 상태와 여유 시간에 따라 다양한 회복 행동 조합
- 데스크톱 및 모바일 반응형 화면 지원
- AI 및 API 오류 발생 시 사용자 안내 및 재시도

## 🖥️ 서비스 화면

### Desktop

| Home | Planner | AI Result |
|---|---|---|
| <img src="./outputs/screenshots/desktop-home.png" width="260"> | <img src="./outputs/screenshots/desktop-planner.png" width="260"> | <img src="./outputs/screenshots/desktop-result.png" width="260"> |

### Mobile

| Home | Planner | AI Result |
|---|---|---|
| <img src="./outputs/screenshots/mobile-home.png" width="180"> | <img src="./outputs/screenshots/mobile-planner.png" width="180"> | <img src="./outputs/screenshots/mobile-result.png" width="180"> |

## 🤖 AI 기능

### 입력

사용자는 플래너에서 다음 정보를 입력합니다.

1. 퇴근 여부
2. 현재 기분
3. 현재 피로도
4. 저녁에 사용할 수 있는 시간

### 출력

AI는 다음 정보를 포함한 회복 루틴을 생성합니다.

- 루틴 제목
- 추천 이유
- 3~5개의 회복 단계
- 단계별 예상 시간
- 구체적인 행동 설명
- 실행 팁
- 하루 마무리 메시지

### AI 동작 흐름

```text
사용자 입력
    ↓
HTML / CSS / JavaScript
    ↓
fetch('/api/recovery-plan')
    ↓
Vercel Serverless Function (Python)
    ↓
Google Gemini API
    ↓
JSON 회복 루틴
    ↓
JavaScript
    ↓
웹 화면에 결과 표시
```

프론트엔드에서 Gemini API를 직접 호출하지 않고 Python Serverless Function을 통해 요청하여 API 키를 클라이언트 코드에 노출하지 않습니다.

## 🔄 AI 활용 개발 과정

OFF:ON은 AI에게 코드를 한 번 생성하고 끝내는 방식이 아니라, 실제 서비스를 실행하고 결과를 확인하면서 문제를 발견하고 AI와 함께 개선했습니다.

### 1. 시간 배분 문제 개선

초기 테스트에서 `3시간 이상`을 선택했음에도 AI가 지나치게 짧은 루틴을 생성하는 문제가 발견되었습니다.

문제를 AI에게 설명하고 프롬프트에 시간별 목표 범위를 구체적으로 추가했습니다.

```text
1시간 이내 → 30~60분
1~2시간 → 60~100분
3시간 이상 → 90~150분
```

수정 후 실제 AI 결과를 다시 확인하여 개선 여부를 검증했습니다.

**스크린샷 (time-allocation.png)**
<img width="664" height="841" alt="04-time-allocation" src="https://github.com/user-attachments/assets/dd32ddfa-4bb3-4ee0-8875-9ac4a8a6f512" />

### 2. 추천 행동 다양화

초기 AI 결과에서 샤워, 음악 감상 등 비슷한 행동이 반복되는 문제가 발견되었습니다.

다양한 회복 행동 유형을 정의하고, 사용자의 상태에 따라 서로 다른 행동을 조합하도록 AI 프롬프트를 개선했습니다.

**스크린샷 (routine-diversity.png)**
<img width="642" height="829" alt="05-routine-diversity" src="https://github.com/user-attachments/assets/6910bf57-72d1-4ca9-bb3f-eb818fc7f8b6" />

### 3. UI 개선

실제 화면을 확인하면서 다음과 같은 UI 문제도 AI와 함께 수정했습니다.

- 메인 제목 줄바꿈
- 결과 카드 레이아웃
- 시간 표시 정렬
- 모바일 화면 가독성
- 결과 화면의 세부 간격

**스크린샷 (ui-improvement.png)**
<img width="641" height="797" alt="01-ui-improvement" src="https://github.com/user-attachments/assets/97fa397f-3367-4489-a776-c0ebce6ccec5" />

**스크린샷 (css-layout.png)**
<img width="645" height="771" alt="02-css-layout" src="https://github.com/user-attachments/assets/84ed1ab3-5fd3-465c-808b-9a65cf9e9fbb" />

**스크린샷 (css-improvement)**
<img width="646" height="789" alt="03-css-improvement" src="https://github.com/user-attachments/assets/0d3d2f07-cbea-4365-a6fb-27706a09505a" />

### AI 활용 방식

```text
AI를 활용해 코드 작성
        ↓
실제 서비스 실행
        ↓
문제 발견
        ↓
문제 원인 분석
        ↓
AI에게 수정 요청
        ↓
코드 / 프롬프트 수정
        ↓
다시 테스트
```

## 🛠 기술 스택

- **Frontend:** HTML, CSS, Vanilla JavaScript
- **Backend:** Vercel Serverless Functions (Python)
- **AI:** Google Gemini API
- **Deployment:** Vercel
- **Repository:** GitHub

## 📁 프로젝트 구조

```text
OFF-ON/
├── index.html
├── css/
│   └── style.css
├── js/
│   └── app.js
├── api/
│   └── recovery-plan.py
├── outputs/
│   ├── OFFON_PRD.md
│   ├── OFF-ON-서비스기획서.md
│   ├── screenshots/
│   └── ai-coding/
├── requirements.txt
├── vercel.json
├── README.md
└── .gitignore
```

### 주요 파일

- `index.html` : 웹 서비스의 화면 구조
- `css/style.css` : 레이아웃, 디자인 및 반응형 스타일
- `js/app.js` : 질문 흐름, 입력 검증, API 호출, 결과 화면 처리
- `api/recovery-plan.py` : Gemini API를 호출하는 Python Serverless Function
- `requirements.txt` : Python 패키지 의존성
- `vercel.json` : Vercel 배포 설정
- `.gitignore` : 환경 변수 및 불필요한 파일 관리

## ▶️ 로컬 실행

정적 화면은 `index.html`을 브라우저에서 열어 확인할 수 있습니다.

API까지 함께 테스트하려면 Vercel CLI를 사용합니다.

```bash
npm install -g vercel
vercel dev
```

## 🔐 환경 변수

로컬 개발 시 Gemini API 키를 환경 변수로 설정합니다.

```text
GEMINI_API_KEY=your_api_key
```

선택 사항:

```text
GEMINI_MODEL=gemini-3.1-flash-lite
```

API 키는 프론트엔드 코드에 직접 작성하지 않습니다.

`.env` 파일은 `.gitignore`에 포함하여 GitHub에 업로드하지 않습니다.

Vercel 배포 시에는 Project Settings → Environment Variables에서 `GEMINI_API_KEY`를 등록합니다.

## 🚀 배포

1. GitHub에 프로젝트를 업로드합니다.
2. Vercel에서 GitHub 저장소를 Import합니다.
3. `GEMINI_API_KEY`를 환경 변수에 등록합니다.
4. Deploy를 실행합니다.
5. 배포된 URL에서 네비게이션, 반응형 화면, AI 루틴 생성 기능을 테스트합니다.

### 배포 URL

https://off-on-one.vercel.app/

### GitHub

https://github.com/bomigrace-byte/OFF-ON

## 📚 프로젝트 문서

- [서비스 기획서](./outputs/OFF-ON-서비스기획서.md)
- [PRD](./outputs/OFFON_PRD.md)

## 📸 증빙 자료

### 서비스 화면

서비스의 데스크톱 및 모바일 화면과 AI 결과 화면은 `outputs/screenshots/`에 정리합니다.

### AI 코딩 과정

AI 코딩 과정은 `outputs/ai-coding/`에 정리합니다.

주요 증빙 내용:

- UI 문제 발견 및 CSS 개선
- AI 결과 시간 배분 개선
- 추천 루틴 다양화
- 결과 카드 UI 개선

AI 코딩 과정에서는 실제 서비스 테스트를 통해 발견한 문제를 AI에게 설명하고, 코드 및 프롬프트를 수정한 과정을 확인할 수 있습니다.

## ⚠️ 주의사항

OFF:ON이 제공하는 결과는 일상적인 회복을 위한 아이디어입니다.

의료적 진단이나 치료, 전문적인 심리 상담을 대신하지 않습니다.
