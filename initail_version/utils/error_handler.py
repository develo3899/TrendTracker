import streamlit as st

# 애플리케이션에서 사용하는 공통 에러 메시지 딕셔너리
ERROR_MESSAGES = {
    "api_key_invalid": "API 키를 확인해주세요. 설정된 키가 유효하지 않거나 권한이 없습니다.",
    "daily_limit_exceeded": "일일 검색 한도(100건)를 초과했습니다. 내일 다시 시도해주세요.",
    "rate_limit_exceeded": "잠시 후 다시 시도해주세요. (API 호출 속도 제한 초과)",
    "no_results": "검색 결과가 없습니다. 다른 키워드로 검색해 보세요.",
    "network_error": "네트워크 연결 또는 서버 응답에 문제가 있습니다. 잠시 후 재시도해주세요.",
    "file_error": "파일 접근 또는 저장 중 오류가 발생했습니다.",
    "empty_input": "검색어를 입력해주세요.",
    "ai_error": "AI 요약 생성 중 오류가 발생했습니다."
}

def handle_error(error_type: str, level: str = "error"):
    """
    지정된 에러 타입에 맞는 한글 메시지를 Streamlit UI로 출력합니다.
    
    Args:
        error_type (str): 에러 식별자 (ERROR_MESSAGES의 키)
        level (str): 출력 레벨 ('error', 'warning', 'info')
    """
    message = ERROR_MESSAGES.get(error_type, "알 수 없는 에러가 발생했습니다.")
    
    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    elif level == "info":
        st.info(message)
    else:
        st.write(message)
