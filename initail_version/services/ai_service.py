from typing import List
from google import genai
from domain.news_article import NewsArticle
from config.settings import Settings
from utils.exceptions import AppError

class AIService:
    """
    Google Gemini API를 사용하여 뉴스 기사들을 요약하는 서비스 클래스입니다.
    기사 내용을 바탕으로 핵심 포인트를 추출하여 한국어로 제공합니다.
    """
    
    def __init__(self):
        """
        AIService를 초기화합니다. API 키가 없으면 AppError를 발생시킵니다.
        """
        if not Settings.GEMINI_API_KEY:
            raise AppError("api_key_invalid")
        
        self.client = genai.Client(api_key=Settings.GEMINI_API_KEY)
        self.model_name = Settings.GEMINI_MODEL

    def summarize_news(self, articles: List[NewsArticle]) -> str:
        """
        제공된 뉴스 기사 리스트를 분석하여 한국어 요약문을 생성합니다.
        
        Args:
            articles (List[NewsArticle]): 요약할 뉴스 기사 리스트
            
        Returns:
            str: AI가 생성한 한국어 요약 텍스트
            
        Raises:
            AppError: API 키 오류, 할당량 초과, 서비스 장애 등 발생 시
        """
        if not articles:
            return "요약할 기사가 없습니다."

        # 뉴스 리스트 구성
        news_context = ""
        for i, article in enumerate(articles, 1):
            news_context += f"{i}. 제목: {article.title}\n   내용: {article.snippet}\n\n"

        prompt = f"""
다음 뉴스 기사들의 핵심 내용을 한국어로 요약해주세요:
- 불릿 포인트 형식으로 최대 5개 항목
- 각 항목은 1~2문장

[뉴스 목록]
{news_context}
""".strip()

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            if not response or not response.text:
                raise AppError("ai_error")
                
            return response.text

        except Exception as e:
            error_str = str(e).lower()
            if "api_key" in error_str or "invalid" in error_str or "401" in error_str:
                raise AppError("api_key_invalid")
            elif "429" in error_str or "quota" in error_str or "limit" in error_str:
                # Gemini 무료 플랜은 분당 15회 제한이 있을 수 있음을 알림
                raise AppError("rate_limit_exceeded")
            else:
                raise AppError("ai_error")

# 싱글톤 인스턴스 전역 변수
_ai_service = None

def summarize_news(articles: List[NewsArticle]) -> str:
    """
    편의를 위한 AIService 래퍼 함수입니다.
    싱글톤 인스턴스를 사용하여 뉴스 요약을 수행합니다.
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service.summarize_news(articles)
