import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Settings:
    """
    애플리케이션의 모든 환경 설정을 관리하는 클래스입니다.
    환경변수 로드 및 유효성 검사 기능을 수행합니다.
    """
    
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CSV_PATH = os.getenv("CSV_PATH", "data/search_history.csv")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # SEARCH_DOMAINS는 쉼표로 구분된 문자열을 리스트로 변환
    _search_domains_raw = os.getenv("SEARCH_DOMAINS", "")
    SEARCH_DOMAINS = [d.strip() for d in _search_domains_raw.split(",") if d.strip()]

    @classmethod
    def validate(cls):
        """
        필수 환경변수($TAVILY_API_KEY, $GEMINI_API_KEY)가 설정되어 있는지 확인합니다.
        설정되지 않은 경우 사용자에게 친절한 안내 메시지를 포함한 ValueError를 발생시킵니다.
        """
        missing_vars = []
        
        if not cls.TAVILY_API_KEY:
            missing_vars.append("TAVILY_API_KEY")
        if not cls.GEMINI_API_KEY:
            missing_vars.append("GEMINI_API_KEY")
            
        if missing_vars:
            error_msg = f"""
❌ 환경변수가 설정되지 않았습니다.

누락된 변수: {', '.join(missing_vars)}

설정 방법:
1. 프로젝트 루트에 .env.example 파일을 .env로 복사하세요.
2. 각 API 키를 발급받아 .env 파일에 입력하세요.

API 키 발급 안내:
- Tavily API (뉴스 검색): https://tavily.com/
- Google AI Studio (Gemini 요약): https://aistudio.google.com/
"""
            raise ValueError(error_msg)
