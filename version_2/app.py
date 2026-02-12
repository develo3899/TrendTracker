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
from services.search_service import search_news
from services.ai_service import summarize_news
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
        page_icon="🔍",
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
    keyword = render_search_form()

    # 5.2 검색 버튼 클릭 처리
    if keyword:
        try:
            st.session_state.current_mode = "new_search"
            st.session_state.selected_key = None 
            
            # 뉴스 검색
            with show_loading(f"🔍 '{keyword}' 관련 뉴스를 검색하고 있습니다..."):
                articles = search_news(keyword, num_results)
            
            if not articles:
                st.info("검색 결과가 없습니다.")
                st.session_state.last_result = None
            else:
                # AI 요약
                with show_loading("🤖 AI가 핵심 내용을 요약하고 있습니다..."):
                    summary = summarize_news(articles)
                
                # 저장 중 상태 표시
                with show_loading("💾 결과를 저장하고 있습니다..."):
                    # 결과 객체 생성 및 저장
                    search_time = datetime.now()
                    search_key = generate_search_key(keyword)
                    
                    result = SearchResult(
                        search_key=search_key,
                        search_time=search_time,
                        keyword=keyword,
                        articles=articles,
                        ai_summary=summary
                    )
                    
                    # 데이터베이스(CSV) 저장
                    repository.save(result)
                    st.session_state.last_result = result
                
                st.success(f"'{keyword}' 검색 및 요약 완료! {len(articles)}건의 뉴스를 찾았습니다.")
                
        except AppError as e:
            handle_error(e.error_type)
        except Exception as e:
            st.error(f"예기치 못한 에러가 발생했습니다: {e}")

    # 5.3 결과 표시 영역
    
    if st.session_state.current_mode == "new_search" and st.session_state.last_result:
        res = st.session_state.last_result
        render_summary(f"'{res.keyword}' 키워드 분석 결과", res.ai_summary)
        render_news_list(res.articles)
        
    elif st.session_state.current_mode == "history" and st.session_state.selected_key:
        res = repository.find_by_key(st.session_state.selected_key)
        if res:
            display_title = f"과거 검색 기록: {res.keyword}"
            render_summary(display_title, res.ai_summary)
            render_news_list(res.articles)
        else:
            st.error("해당 기록을 불러올 수 없습니다.")
    
    elif st.session_state.current_mode == "new_search" and not st.session_state.last_result:
        # 초기 화면 (검색 전 또는 결과 없을 때)
        if not search_keys:
            st.markdown("""
            <div style="text-align: center; padding: 2rem 0;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">✨ Trend Tracker</h1>
                <p style="font-size: 1.2rem; opacity: 0.8;">당신의 궁금증을 AI와 함께 실시간 트렌드로 분석해보세요.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            ### 👋 환영합니다! Trend Tracker를 시작해 보세요.
            
            아직 검색 기록이 없습니다. **상단 입력창**에 관심 있는 키워드를 입력하여 첫 번째 트렌드 분석을 시작해 보세요!
            
            **사용 팁:**
            - 왼쪽 사이드바에서 **검색 건수**를 조절할 수 있습니다 (최대 10건).
            - 검색된 결과물은 자동으로 저장되어 나중에 다시 볼 수 있습니다.
            - "AI 로봇", "금리 전망"과 같이 구체적인 키워드가 좋습니다.
            """)
        else:
            st.markdown("""
            ### 🚀 새로운 트렌드를 검색해 보세요!
            
            알고 싶은 키워드를 입력하면 **최신 뉴스**와 함께 **AI 요약**을 제공해 드립니다.
            과거 기록을 보려면 왼쪽 사이드바의 **검색 기록** 메뉴를 이용해 주세요.
            """)

if __name__ == "__main__":
    main()
