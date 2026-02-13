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

    def get_ai_insights(self, keyword: str) -> str:
        """
        특정 키워드에 대해 Gemini의 자체 지식을 바탕으로 깊이 있는 트렌드 분석을 수행합니다.
        """
        prompt = f"""
전문가적인 시각에서 '{keyword}'에 대한 현재 트렌드와 미래 전망을 분석해주세요.
다음 구조로 한국어로 답변해주세요:
1. 🌟 현재 위상: 이 키워드가 현재 시장이나 사회에서 어떤 위치에 있는지
2. 💡 핵심 동력: 이 트렌드를 이끄는 주요 요인들
3. 🚀 미래 전망: 향후 1~2년 내의 발전 방향
4. ⚠️ 주의점: 관련하여 주목해야 할 리스크나 한계점

답변은 친절하고 전문적인 톤으로 작성해주세요.
""".strip()

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text if response and response.text else "인사이트를 생성할 수 없습니다."
        except Exception as e:
            return f"AI 인사이트 로드 중 오류 발생: {str(e)}"

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

def get_ai_insights(keyword: str) -> str:
    """
    편의를 위한 AIService 래퍼 함수입니다.
    Gemini의 자체 지식으로 트렌드 분석을 수행합니다.
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service.get_ai_insights(keyword)
