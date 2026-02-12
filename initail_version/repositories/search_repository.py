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
            "title", "url", "snippet", "ai_summary"
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
            # 저장된 데이터가 없는 경우 컬럼 보장
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
                # 기존 데이터에 append
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
        
        # search_time 기준으로 정렬 후 고유값 추출
        # (문자열 비교여도 'yyyyMMddHHmm' 형식이면 정렬 가능)
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
        
        # 날짜 포맷 변환 (저장된 형식에 따라 처리)
        search_time_val = first_row["search_time"]
        if isinstance(search_time_val, str):
            try:
                # pandas가 자동 변환해줬을 수도 있고 문자열일 수도 있음
                search_time = pd.to_datetime(search_time_val).to_pydatetime()
            except:
                search_time = datetime.now() # fallback
        else:
            search_time = search_time_val

        # 기사 리스트 복구
        articles = []
        for _, row in result_df.sort_values("article_index").iterrows():
            articles.append(NewsArticle(
                title=str(row["title"]),
                url=str(row["url"]),
                snippet=str(row["snippet"]),
                pub_date="" # CSV 스펙에 없으므로 빈 문자열로 처리
            ))
            
        return SearchResult(
            search_key=str(first_row["search_key"]),
            search_time=search_time,
            keyword=str(first_row["keyword"]),
            articles=articles,
            ai_summary=str(first_row["ai_summary"])
        )

    def get_all_as_csv(self) -> str:
        """전체 데이터를 CSV 문자열로 반환 (다운로드용)"""
        df = self.load()
        return df.to_csv(index=False, encoding='utf-8-sig')
