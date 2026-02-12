import streamlit as st
from typing import List, Optional
from datetime import datetime

def render_sidebar_header():
    """애플리케이션 이름과 간단한 소개를 사이드바 최상단에 표시합니다."""
    st.sidebar.title("Trend Tracker")
    st.sidebar.markdown("키워드로 뉴스를 검색하고 AI가 요약해드립니다")
    st.sidebar.divider()

def render_settings() -> int:
    """
    뉴스 검색 건수를 설정하는 슬라이더를 사이드바에 표시합니다.
    
    Returns:
        int: 사용자가 선택한 검색 건수 (1~10)
    """
    st.sidebar.subheader("⚙️ 설정")
    num_results = st.sidebar.slider(
        "검색 건수 설정",
        min_value=1,
        max_value=10,
        value=5,
        help="검색할 뉴스 기사의 개수를 선택하세요."
    )
    return num_results

def render_info():
    """
    애플리케이션 사용법, API 한도 정보, 데이터 저장 주의사항을 
    사이드바의 Expander 형식으로 표시합니다.
    """
    with st.sidebar.expander("ℹ️ 사용법"):
        st.markdown("""
        1. 상단 입력창에 알고 싶은 **키워드**를 입력하세요.
        2. **검색** 버튼을 클릭하여 관련 뉴스를 찾아봅니다.
        3. AI가 요약한 **핵심 내용**과 **뉴스 리스트**를 확인하세요.
        """)

    with st.sidebar.expander("📊 API 한도"):
        st.info("Tavily 무료 플랜: 월 1,000건 검색 가능")

    with st.sidebar.expander("💾 데이터 저장 안내"):
        st.write("- 검색 기록은 CSV 파일(`data/search_history.csv`)에 저장됩니다.")
        st.write("- CSV 파일을 삭제하거나 경로를 변경하면 이전 검색 기록이 모두 사라집니다.")
        st.warning("중요한 기록은 CSV 다운로드 기능을 통해 백업해주세요.")

def render_history_list(search_keys: List[str], keywords_map: dict) -> Optional[str]:
    """
    저장된 과거 검색 기록 리스트를 사이드바 셀렉트박스로 표시합니다.
    
    Args:
        search_keys (List[str]): 조회된 검색 키 리스트
        keywords_map (dict): 키워드 매핑 정보 (파싱에 사용)
        
    Returns:
        Optional[str]: 사용자가 선택한 고유 search_key
    """
    st.sidebar.subheader("📜 검색 기록")
    
    if not search_keys:
        st.sidebar.info("저장된 검색 기록이 없습니다")
        return None

    # 표시용 포맷 생성: "키워드 (yyyy-mm-dd HH:MM)"
    display_options = []
    key_to_display = {}

    for key in search_keys:
        try:
            # 키워드와 timestamp 분리
            parts = key.rsplit('-', 1)
            keyword = parts[0]
            ts_str = parts[1]
            dt = datetime.strptime(ts_str, "%Y%m%d%H%M")
            display_name = f"{keyword} ({dt.strftime('%Y-%m-%d %H:%M')})"
        except:
            display_name = key
        
        display_options.append(display_name)
        key_to_display[display_name] = key

    selected_display = st.sidebar.selectbox(
        "과거 기록 불러오기",
        options=display_options,
        index=None,
        placeholder="이전 검색 기록 선택",
        label_visibility="collapsed"
    )
    
    return key_to_display.get(selected_display) if selected_display else None

def render_download_button(csv_data: str, is_empty: bool):
    """
    저장된 전체 CSV 데이터를 다운로드할 수 있는 버튼을 사이드바에 표시합니다.
    
    Args:
        csv_data (str): 전체 CSV 데이터 문자열
        is_empty (bool): 데이터 존재 여부 (비어 있으면 버튼 비활성화)
    """
    st.sidebar.divider()
    filename = f"trendtracker_export_{datetime.now().strftime('%Y%m%d')}.csv"
    
    if is_empty:
        st.sidebar.button("📥 CSV 다운로드", disabled=True, use_container_width=True)
        st.sidebar.caption("저장된 데이터가 없어 다운로드할 수 없습니다.")
    else:
        st.sidebar.download_button(
            label="📥 CSV 다운로드",
            data=csv_data,
            file_name=filename,
            mime="text/csv",
            use_container_width=True
        )
