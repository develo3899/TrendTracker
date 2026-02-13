import streamlit as st
from datetime import datetime
from config.settings import Settings
from domain.search_result import SearchResult
from repositories.search_repository import SearchRepository
from components.search_form import render_search_form
from components.sidebar import (
    render_sidebar_header, render_settings, render_info, 
    render_history_list, render_download_button
)
from components.result_section import render_summary, render_news_list
from components.loading import show_loading
from services.search_service import search_news, get_google_trends_url
from services.ai_service import summarize_news, get_ai_insights
from components.result_section import render_summary, render_news_list, render_ai_insights, render_trends_link
from utils.key_generator import generate_search_key
from utils.exceptions import AppError
from utils.ui_helper import apply_custom_css
from utils.error_handler import handle_error

def init_session_state():
    """애플리케이션 명시적 상태 관리를 위한 session_state 초기화"""
    if "current_mode" not in st.session_state:
        st.session_state.current_mode = "new_search"
    if "selected_key" not in st.session_state:
        st.session_state.selected_key = None
    if "last_result" not in st.session_state:
        st.session_state.last_result = None

def main():
    """
    애플리케이션의 메인 진입점입니다. 
    UI 렌더링, 사용자 흐름 및 API 연동을 조율합니다.
    """
    # 1. 페이지 설정
    st.set_page_config(
        page_title="Trend Tracker",
        page_icon="🔥",
        layout="wide"
    )
    apply_custom_css("styles/main.css")

    # 2. 필수 환경변수 검증
    try:
        Settings.validate()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # 3. 초기화
    init_session_state()
    repository = SearchRepository(Settings.CSV_PATH)

    # 4. 사이드바 영역
    with st.sidebar:
        render_sidebar_header()
        num_results = render_settings()
        render_info()
        st.divider()
        
        # 검색 기록 목록 조회
        search_keys = repository.get_all_keys()
        history_key = render_history_list(search_keys, {})
        
        # 모드 전환 감지 (기록 선택 시)
        if history_key and history_key != st.session_state.selected_key:
            st.session_state.current_mode = "history"
            st.session_state.selected_key = history_key
            st.session_state.last_result = None 
            st.rerun()

        # CSV 다운로드
        csv_data = repository.get_all_as_csv()
        render_download_button(csv_data, len(search_keys) == 0)

    # 5. 메인 영역
    
    # 5.1 검색 폼
    keyword, selected_sources = render_search_form()

    # 5.2 검색 버튼 클릭 처리
    if keyword:
        try:
            st.session_state.current_mode = "new_search"
            st.session_state.selected_key = None 
            
            articles = []
            summary = ""
            insights = ""
            trends_url = ""

            with st.status("🚀 통합 트렌드 분석 중...", expanded=True) as status:
                # 1. 뉴스 검색 및 요약
                if "최신 뉴스 (Tavily)" in selected_sources:
                    status.write(f"🔍 '{keyword}' 관련 뉴스 검색 중...")
                    articles = search_news(keyword, num_results)
                    if articles:
                        status.write("🤖 AI 뉴스 요약 생성 중...")
                        summary = summarize_news(articles)
                
                # 2. Gemini 인사이트
                if "AI 심층 분석 (Gemini)" in selected_sources:
                    status.write("🧠 Gemini AI 심층 트렌드 분석 중...")
                    insights = get_ai_insights(keyword)
                
                # 3. Google Trends
                if "트렌드 지표 (Google Trends)" in selected_sources:
                    status.write(f"📈 Google Trends '{keyword}' 데이터 분석 중...")
                    trends_url = get_google_trends_url(keyword)
                
                status.update(label="✅ 분석 완료!", state="complete", expanded=False)

            # 결과 객체 생성 및 저장
            search_time = datetime.now()
            search_key = generate_search_key(keyword)
            
            result = SearchResult(
                search_key=search_key,
                search_time=search_time,
                keyword=keyword,
                articles=articles,
                ai_summary=summary,
                ai_insights=insights,
                trends_url=trends_url
            )
            
            # 데이터베이스(CSV) 저장
            repository.save(result)
            st.session_state.last_result = result
                
            st.success(f"'{keyword}' 트렌드 분석이 완료되었습니다!")
                
        except AppError as e:
            handle_error(e.error_type)
        except Exception as e:
            st.error(f"예기치 못한 에러가 발생했습니다: {e}")

    # 5.3 결과 표시 영역
    if (st.session_state.current_mode == "new_search" and st.session_state.last_result) or \
       (st.session_state.current_mode == "history" and st.session_state.selected_key):
        
        if st.session_state.current_mode == "history":
            res = repository.find_by_key(st.session_state.selected_key)
        else:
            res = st.session_state.last_result
            
        if res:
            st.divider()
            st.markdown(f"## 🏷️ 검색 키워드: **{res.keyword}**")
            
            # 탭을 사용하여 결과 분리 표시
            tab1, tab2, tab3 = st.tabs(["📊 통합 리포트", "📰 관련 뉴스", "🧠 AI 인사이트"])
            
            with tab1:
                render_summary(res.keyword, res.ai_summary)
                if res.trends_url:
                    render_trends_link(res.keyword, res.trends_url)
            
            with tab2:
                render_news_list(res.articles)
            
            with tab3:
                render_ai_insights(res.keyword, res.ai_insights)
        else:
            st.error("해당 기록을 불러올 수 없습니다.")
    
    elif st.session_state.current_mode == "new_search" and not st.session_state.last_result:
        # Boutique Style Landing Page
        st.markdown(f"""
        <div style="text-align: center; padding: 6rem 0;">
            <p style="letter-spacing: 5px; font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; text-transform: uppercase; font-family: 'Inter', sans-serif;">Advanced Analytics Hub</p>
            <h1 style="border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 2rem 0; display: inline-block; width: 100%;">TREND TRACKER</h1>
            <p style="font-size: 1.2rem; margin-top: 2rem; color: #000 !important; font-style: italic; font-family: 'Cormorant Garamond', serif;">Exploring insights across news, AI, and global trends with clinical precision.</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("---")
        st.info("💡 위 입력창에 키워드를 입력하고 분석할 소스를 선택한 뒤 '통합 트렌드 검색'을 누르세요.")

if __name__ == "__main__":
    main()
