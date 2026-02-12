import streamlit as st
from contextlib import contextmanager

@contextmanager
def show_loading(message: str):
    """
    작업 수행 중 Streamlit 로딩 스피너를 표시합니다. 
    Context Manager로 구현되어 'with' 문과 함께 사용하며, 작업 완료 후 스피너가 사라집니다.
    
    Args:
        message (str): 로딩 중 표시할 한글 메시지
        
    Example:
        with show_loading("데이터를 처리하는 중입니다..."):
            perform_task()
    """
    with st.spinner(message):
        yield
