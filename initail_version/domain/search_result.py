from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import pandas as pd
from .news_article import NewsArticle

@dataclass
class SearchResult:
    """
    한 번의 검색 수행 결과(키워드, 기사 리스트, AI 요약)를 관리하는 데이터 클래스입니다.
    
    Attributes:
        search_key (str): 검색 고유 키 (키워드-timestamp 형식)
        search_time (datetime): 검색 수행 시각
        keyword (str): 검색어
        articles (List[NewsArticle]): 검색된 뉴스 기사 리스트
        ai_summary (str): AI가 요약한 핵심 내용
    """
    search_key: str              # PK, "키워드-yyyymmddhhmm" 형식
    search_time: datetime         # 검색 실행 시간
    keyword: str                  # 검색 키워드
    articles: List[NewsArticle]   # 뉴스 기사 리스트
    ai_summary: str               # AI 요약 결과

    def to_dataframe(self) -> pd.DataFrame:
        """
        검색 결과를 pandas DataFrame으로 변환합니다. 
        CSV 저장을 위해 'Long format'(기사 1건당 1행)으로 구조화하며 총 8개의 컬럼을 생성합니다.
        
        Returns:
            pd.DataFrame: 8개 컬럼(search_key, search_time, keyword, article_index, title, url, snippet, ai_summary)을 가진 데이터프레임
        """
        data = []
        for i, article in enumerate(self.articles, 1):
            data.append({
                "search_key": self.search_key,
                "search_time": self.search_time,
                "keyword": self.keyword,
                "article_index": i,
                "title": article.title,
                "url": article.url,
                "snippet": article.snippet,
                "ai_summary": self.ai_summary
            })
        
        if not data:
            # 기사가 없는 경우에도 구조 유지를 위해 빈 데이터프레임 반환 (8개 컬럼 정의)
            return pd.DataFrame(columns=[
                "search_key", "search_time", "keyword", "article_index",
                "title", "url", "snippet", "ai_summary"
            ])
            
        return pd.DataFrame(data)
