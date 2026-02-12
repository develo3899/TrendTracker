# Trend Tracker: AI 기반 뉴스 트렌드 요약 웹앱

**Trend Tracker**는 특정 키워드에 대한 최신 뉴스를 검색하고, Google Gemini AI를 활용하여 핵심 내용을 신속하게 요약해 주는 Streamlit 기반 웹 애플리케이션입니다.

## 🌟 주요 기능
- **뉴스 검색**: Tavily API를 사용하여 신뢰할 수 있는 도메인에서 최신 뉴스를 가져옵니다.
- **AI 요약**: Google Gemini API를 통해 복잡한 뉴스 기사들을 단 몇 줄의 한국어로 요약합니다.
- **기록 관리**: 모든 검색 결과는 로컬 CSV 파일에 저장되어 언제든지 다시 확인할 수 있습니다.
- **데이터 내보내기**: 저장된 전체 검색 기록을 한 번의 클릭으로 CSV로 다운로드할 수 있습니다.

## 🛠️ 설치 및 실행 방법

### 1. 요구 사항
- Python 3.12 이상
- [uv](https://github.com/astral-sh/uv) (파이썬 패키지 매니저)

### 2. 의존성 설치
프로젝트 루트에서 다음 명령어를 실행하여 필요한 패키지를 설치합니다:
```bash
uv sync
```

### 3. 환경변수 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 API 키를 입력합니다:
```bash
cp .env.example .env
```
`.env` 파일 내용 예시:
```env
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key
SEARCH_DOMAINS=www.yna.co.kr,news.kbs.co.kr,news.sbs.co.kr  # 기타 원하는 도메인
CSV_PATH=data/search_history.csv
```

### 4. 앱 실행
다음 명령어로 Streamlit 서버를 실행합니다:
```bash
uv run streamlit run app.py
```

## 🔑 API 키 발급 안내

### Tavily API (뉴스 검색)
1. [Tavily 공식 홈페이지](https://tavily.com/)에 접속하여 가입합니다.
2. 대시보드에서 무료 API 키를 발급받습니다 (월 1,000건 무료).

### Google Gemini API (AI 요약)
1. [Google AI Studio](https://aistudio.google.com/)에 접속합니다.
2. "Get API key"를 클릭하여 새로운 키를 생성합니다.

## 📁 프로젝트 구조
- `app.py`: 메인 애플리케이션 진입점 및 레이아웃 정의
- `components/`: UI 구성을 위한 Streamlit 컴포넌트들
- `services/`: Tavily 검색 및 Gemini AI 요약 외부 연동 로직
- `repositories/`: CSV 파일 데이터 저장 및 관리 (DAO)
- `domain/`: 기사 및 검색 결과 데이터 모델 (Dataclasses)
- `config/`: 환경 설정 및 유효성 검사
- `utils/`: 검색 키 생성, 키워드 전처리, 공통 에러 핸들러 등

---
**주의**: 모든 검색 기록은 `data/search_history.csv` 파일에 물리적으로 저장됩니다. 해당 파일을 삭제하거나 경로를 변경하면 이전 기록을 불러올 수 없으니 주의하시기 바랍니다.
