import os
import pandas as pd
import logging
from typing import List, Optional
from domain.search_result import SearchResult
from domain.news_article import NewsArticle
from datetime import datetime

# 로깅 설정
logger = logging.getLogger(__name__)

class SearchRepository:
    """CSV 파일을 사용하여 검색 기록을 관리하는 리포지토리"""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.columns = [
            "search_key", "search_time", "keyword", "article_index",
            "title", "url", "snippet", "ai_summary", "ai_insights", "trends_url"
        ]
        # data/ 폴더가 없으면 자동 생성
        directory = os.path.dirname(csv_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def load(self) -> pd.DataFrame:
        """CSV 파일에서 데이터를 로드. 파일이 없으면 빈 데이터프레임 반환"""
        if not os.path.exists(self.csv_path):
            return pd.DataFrame(columns=self.columns)
        
        try:
            df = pd.read_csv(self.csv_path)
            if df.empty:
                return pd.DataFrame(columns=self.columns)
            return df
        except Exception as e:
            logger.warning(f"CSV 로드 실패: {e}")
            return pd.DataFrame(columns=self.columns)

    def save(self, search_result: SearchResult) -> bool:
        """SearchResult를 CSV 파일에 추가 저장"""
        try:
            new_df = search_result.to_dataframe()
            
            if os.path.exists(self.csv_path):
                existing_df = pd.read_csv(self.csv_path)
                final_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                final_df = new_df
                
            final_df.to_csv(self.csv_path, index=False, encoding='utf-8-sig')
            return True
        except Exception as e:
            logger.error(f"CSV 저장 실패: {e}")
            return False

    def get_all_keys(self) -> List[str]:
        """모든 고유 search_key 리스트를 최신순으로 반환"""
        df = self.load()
        if df.empty:
            return []
        
        df_sorted = df.sort_values(by="search_time", ascending=False)
        keys = df_sorted["search_key"].unique().tolist()
        return keys

    def find_by_key(self, search_key: str) -> Optional[SearchResult]:
        """search_key로 특정 검색 결과 조회"""
        df = self.load()
        if df.empty:
            return None
        
        result_df = df[df["search_key"] == search_key]
        if result_df.empty:
            return None
        
        # 첫 번째 행에서 기본 정보 추출
        first_row = result_df.iloc[0]
        
        # 안전한 가져오기 (이전 버전 CSV 호환성)
        ai_insights = str(first_row.get("ai_insights", ""))
        trends_url = str(first_row.get("trends_url", ""))
        
        # 날짜 포맷 변환
        search_time_val = first_row["search_time"]
        if isinstance(search_time_val, str):
            try:
                search_time = pd.to_datetime(search_time_val).to_pydatetime()
            except:
                search_time = datetime.now()
        else:
            search_time = search_time_val

        # 기사 리스트 복구 (article_index가 0인 것은 기사가 없는 placeholder)
        articles = []
        for _, row in result_df.sort_values("article_index").iterrows():
            if row["article_index"] > 0:
                articles.append(NewsArticle(
                    title=str(row["title"]),
                    url=str(row["url"]),
                    snippet=str(row["snippet"]),
                    pub_date=""
                ))
            
        return SearchResult(
            search_key=str(first_row["search_key"]),
            search_time=search_time,
            keyword=str(first_row["keyword"]),
            articles=articles,
            ai_summary=str(first_row["ai_summary"]),
            ai_insights=ai_insights,
            trends_url=trends_url
        )

    def get_all_as_csv(self) -> str:
        """전체 데이터를 CSV 문자열로 반환 (다운로드용)"""
        df = self.load()
        return df.to_csv(index=False, encoding='utf-8-sig')
