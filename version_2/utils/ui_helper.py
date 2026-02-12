import streamlit as st
import os

def apply_custom_css(css_file_path: str):
    """
    지정된 경로의 CSS 파일을 읽어 Streamlit 앱에 주입합니다.
    """
    if os.path.exists(css_file_path):
        with open(css_file_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS 파일을 찾을 수 없습니다: {css_file_path}")
