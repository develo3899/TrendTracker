import streamlit as st
from typing import Optional, Tuple, List
from utils.input_handler import preprocess_keyword

def render_search_form() -> Tuple[Optional[str], List[str]]:
    """
    메인 화면 상단에 검색 입력 필드와 소스 선택 옵션을 렌더링합니다.
    
    Returns:
        Tuple[Optional[str], List[str]]: (정제된 키워드, 선택된 소스 리스트)
    """
    with st.form("search_form", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        with col1:
            keyword_input = st.text_input(
                "검색어 입력",
                placeholder="ENTER TREND KEYWORD...",
                label_visibility="collapsed"
            )
        with col2:
            search_button = st.form_submit_button("ANALYZE TREND", use_container_width=True)
            
        # 검색 소스 선택 (멀티 셀렉트)
        sources = st.multiselect(
            "검색 대상 선택",
            options=[
                "최신 뉴스 (Tavily)", 
                "AI 심층 분석 (Gemini)", 
                "트렌드 지표 (Google Trends)"
            ],
            default=["최신 뉴스 (Tavily)", "AI 심층 분석 (Gemini)"],
            help="분석하고 싶은 데이터 소스를 선택하세요."
        )

        if search_button:
            processed_keyword = preprocess_keyword(keyword_input)
            if not processed_keyword:
                st.warning("검색어를 입력해주세요")
                return None, sources
            if not sources:
                st.warning("최소 하나 이상의 검색 대상을 선택해주세요")
                return None, sources
                
            return processed_keyword, sources
    
    return None, sources
