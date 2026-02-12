import streamlit as st
from typing import List
from domain.news_article import NewsArticle

def render_summary(title: str, summary: str):
    """
    AI가 요약한 핵심 트렌드 내용을 메인 화면에 렌더링합니다.
    
    Args:
        title (str): 요약 섹션의 제목
        summary (str): AI가 생성한 요약 텍스트 (Markdown 지원)
    """
    st.subheader(f"🔍 {title} - AI 트렌드 요약")
    if summary:
        st.info(summary)
    else:
        st.warning("요약 내용을 생성하지 못했습니다.")

def render_news_list(articles: List[NewsArticle]):
    """
    검색된 뉴스 기사 리스트를 각 기사별 Expander 형식으로 렌더링합니다.
    
    Args:
        articles (List[NewsArticle]): 표시할 뉴스 기사 객체 리스트
    """
    st.subheader("📰 관련 뉴스 리스트")
    
    if not articles:
        st.write("관련 뉴스 기사가 없습니다.")
        return

    for article in articles:
        # expander 제목: 기사 제목 + (발행일)
        expander_title = f"{article.title}"
        if article.pub_date and article.pub_date != "날짜 정보 없음":
            expander_title += f" ({article.pub_date})"
            
        with st.expander(expander_title):
            if article.pub_date:
                st.caption(f"📅 발행일: {article.pub_date}")
            
            st.markdown(f"**스니펫:**\n{article.snippet}")
            st.markdown(f"[🔗 기사 보기]({article.url})")
