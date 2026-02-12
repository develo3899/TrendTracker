import streamlit as st
from typing import Optional
from utils.input_handler import preprocess_keyword

def render_search_form() -> Optional[str]:
    """
    메인 화면 상단에 검색 입력 필드와 버튼을 렌더링합니다.
    사용자의 입력을 전처리하여 유효한 키워드를 반환합니다.
    
    Returns:
        Optional[str]: 정제된 검색 키워드. 입력이 없거나 오류 발생 시 None 반환.
    """
    with st.container():
        col1, col2 = st.columns([4, 1])
        with col1:
            keyword_input = st.text_input(
                "검색어 입력",
                placeholder="관심 있는 트렌드 키워드를 입력하세요 (예: AI 로봇, 신재생 에너지)",
                label_visibility="collapsed"
            )
        with col2:
            search_button = st.button("검색", use_container_width=True)

    if search_button:
        processed_keyword = preprocess_keyword(keyword_input)
        if not processed_keyword:
            st.warning("검색어를 입력해주세요")
            return None
        return processed_keyword
    
    return None
