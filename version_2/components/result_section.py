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

def render_ai_insights(keyword: str, insights: str):
    """
    Gemini의 자체 지식을 바탕으로 한 심층 분석 결과를 렌더링합니다.
    """
    st.subheader(f"🤖 '{keyword}'에 대한 AI 심층 인사이트")
    if insights:
        st.write(insights)
    else:
        st.warning("인사이트를 생성할 수 없습니다.")

def render_trends_link(keyword: str, trends_url: str):
    """
    Google Trends로 이동하는 링크 섹션을 렌더링합니다.
    """
    st.subheader(f"📈 '{keyword}' 트렌드 지표 확인")
    st.markdown(f"""
    <div style="background-color: rgba(255, 140, 0, 0.1); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 140, 0, 0.2);">
        <p style="margin-bottom: 1rem;">Google Trends에서 <b>'{keyword}'</b>의 시간 흐름에 따른 관심도 변화와 지역별 통계를 확인해보세요.</p>
        <a href="{trends_url}" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #FF8C00, #FF4500); color: white; padding: 10px 20px; border-radius: 8px; text-align: center; font-weight: bold; display: inline-block;">
                Google Trends에서 확인하기 ↗
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

def render_news_list(articles: List[NewsArticle]):
    """
    검색된 뉴스 기사 리스트를 각 기사별 Expander 형식으로 렌더링합니다.
    """
    st.subheader("📰 관련 뉴스 기사")
    if not articles:
        st.info("관련 뉴스 기사가 없습니다.")
        return

    for i, article in enumerate(articles, 1):
        with st.expander(f"{i}. {article.title}"):
            st.markdown(f"**[기사 원문 보기]({article.url})**")
            st.write(article.snippet)
            if article.pub_date and article.pub_date != "날짜 정보 없음":
                st.caption(f"발행일: {article.pub_date}")
