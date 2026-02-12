from datetime import datetime

def generate_search_key(keyword: str) -> str:
    """
    키워드와 현재 시간을 조합하여 고유한 검색 키를 생성합니다.
    형식: "키워드-yyyymmddHHMM"
    
    Args:
        keyword (str): 검색 키워드
        
    Returns:
        str: 생성된 고유 검색 키
    """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M")
    return f"{keyword}-{timestamp}"
