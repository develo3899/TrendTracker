from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import pandas as pd
from .news_article import NewsArticle

@dataclass
class SearchResult:
    """
    한 번의 검색 수행 결과(키워드, 기사 리스트, AI 요약, AI 인사이트, 트렌드 URL)를 관리합니다.
    """
    search_key: str              # PK, "키워드-yyyymmddhhmm" 형식
    search_time: datetime         # 검색 실행 시간
    keyword: str                  # 검색 키워드
    articles: List[NewsArticle] = field(default_factory=list)
    ai_summary: str = ""          # AI 요약 결과
    ai_insights: str = ""         # AI 심층 인사이트
    trends_url: str = ""          # Google Trends URL

    def to_dataframe(self) -> pd.DataFrame:
        """
        검색 결과를 pandas DataFrame으로 변환합니다. 
        """
        data = []
        # 기사가 있는 경우
        if self.articles:
            for i, article in enumerate(self.articles, 1):
                data.append({
                    "search_key": self.search_key,
                    "search_time": self.search_time,
                    "keyword": self.keyword,
                    "article_index": i,
                    "title": article.title,
                    "url": article.url,
                    "snippet": article.snippet,
                    "ai_summary": self.ai_summary,
                    "ai_insights": self.ai_insights,
                    "trends_url": self.trends_url
                })
        else:
            # 기사가 없는 경우에도 정보를 저장하기 위해 1행 생성
            data.append({
                "search_key": self.search_key,
                "search_time": self.search_time,
                "keyword": self.keyword,
                "article_index": 0,
                "title": "No Articles",
                "url": "",
                "snippet": "",
                "ai_summary": self.ai_summary,
                "ai_insights": self.ai_insights,
                "trends_url": self.trends_url
            })
            
        return pd.DataFrame(data)
