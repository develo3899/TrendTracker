import time
import requests
from typing import List
from tavily import TavilyClient
from domain.news_article import NewsArticle
from config.settings import Settings
from utils.exceptions import AppError

class SearchService:
    """
    Tavily API를 연동하여 기사 검색 및 최신순 정렬을 수행하는 서비스 클래스입니다.
    네트워크 오류에 대한 재시도 로직과 상세 에러 처리를 포함합니다.
    """
    
    def __init__(self):
        """
        TavilyClient를 초기화합니다. API 키가 없으면 AppError를 발생시킵니다.
        """
        if not Settings.TAVILY_API_KEY:
            raise AppError("api_key_invalid")
        self.client = TavilyClient(api_key=Settings.TAVILY_API_KEY)

    def search_news(self, keyword: str, num_results: int = 5) -> List[NewsArticle]:
        """
        지정된 키워드로 뉴스를 검색하고 최신순으로 정렬하여 반환합니다.
        
        Args:
            keyword (str): 검색할 키워드
            num_results (int): 반환할 결과 수 (기본값 5)
            
        Returns:
            List[NewsArticle]: 검색된 뉴스 기사 리스트
            
        Raises:
            AppError: API 키 오류, 할당량 초과, 네트워크 오류 등 발생 시
        """
        retries = 1
        for attempt in range(retries + 1):
            try:
                # 검색 도메인 리스트 가져오기
                domains = Settings.SEARCH_DOMAINS
                
                # 충분한 기사를 확보하기 위해 더 많이 요청 (최신순 정렬을 위해)
                max_to_fetch = max(num_results * 3, 20)
                
                # Tavily SDK 내부적으로 requests를 사용하므로 직접 timeout 제어는 어려울 수 있으나
                # SDK가 지원하지 않는 경우 예외 처리에서 타임아웃 유형을 감지합니다.
                response = self.client.search(
                    query=keyword,
                    search_depth="advanced",
                    include_domains=domains,
                    max_results=max_to_fetch,
                    topic="news"
                )
                
                results = response.get('results', [])
                if not results:
                    return []
                
                # published_date 기준 내림차순(최신순) 정렬
                # 날짜가 없는 항목은 리스트 끝으로 이동
                sorted_results = sorted(
                    results,
                    key=lambda x: x.get('published_date') or "",
                    reverse=True
                )
                
                # 상위 num_results 만큼만 추출
                final_results = sorted_results[:num_results]
                
                articles = []
                for item in final_results:
                    articles.append(NewsArticle(
                        title=item.get('title', '제목 없음'),
                        url=item.get('url', ''),
                        snippet=item.get('content', ''),
                        pub_date=item.get('published_date', '날짜 정보 없음')
                    ))
                
                return articles

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                if attempt < retries:
                    time.sleep(1) # 잠시 대기 후 재시도
                    continue
                raise AppError("network_error")
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                if status_code == 400:
                    raise AppError("api_key_invalid") # 혹은 잘못된 요청
                elif status_code in [401, 403]:
                    raise AppError("api_key_invalid")
                elif status_code == 429:
                    raise AppError("rate_limit_exceeded")
                elif status_code >= 500:
                    raise AppError("network_error")
                else:
                    raise AppError("network_error")
            except Exception as e:
                error_msg = str(e).lower()
                if "invalid" in error_msg or "unauthorized" in error_msg or "401" in error_msg:
                    raise AppError("api_key_invalid")
                elif "limit" in error_msg or "429" in error_msg or "quota" in error_msg:
                    raise AppError("rate_limit_exceeded")
                else:
                    # 재시도 가능한 일반 오류인 경우
                    if attempt < retries:
                        continue
                    raise AppError("network_error")

# 싱글톤 인스턴스 제공을 위한 전역 변수
_search_service = None

def search_news(keyword: str, num_results: int = 5) -> List[NewsArticle]:
    """
    편의를 위한 SearchService 래퍼 함수입니다. 
    싱글톤 인스턴스를 사용하여 뉴스 검색을 수행합니다.
    """
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service.search_news(keyword, num_results)

def get_google_trends_url(keyword: str) -> str:
    """
    Google Trends 탐색 페이지 URL을 생성합니다.
    """
    import urllib.parse
    encoded_keyword = urllib.parse.quote(keyword)
    # 한국 지역(geo=KR), 최근 7일(date=now 7-d) 기준 탐색 URL
    return f"https://trends.google.com/trends/explore?q={encoded_keyword}&geo=KR&date=now%207-d"
