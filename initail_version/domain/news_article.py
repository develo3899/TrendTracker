from dataclasses import dataclass

@dataclass
class NewsArticle:
    """
    개별 뉴스 기사의 정보를 담는 데이터 클래스입니다.
    
    Attributes:
        title (str): 기사 제목
        url (str): 기사 원본 링크 URL
        snippet (str): 기사 내용 요약 또는 스니펫
        pub_date (str): 기사 발행일 정보
    """
    title: str     # 기사 제목
    url: str       # 기사 URL
    snippet: str   # 기사 스니펫
    pub_date: str  # 발행일
