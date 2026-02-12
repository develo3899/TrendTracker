from typing import Optional

def preprocess_keyword(raw_input: str) -> Optional[str]:
    """
    사용자가 입력한 검색어를 정제합니다. 
    앞뒤 공백을 제거하고, 빈 문자열인 경우 None을 반환하며, 100자로 길이를 제한합니다.
    
    Args:
        raw_input (str): 사용자로부터 입력받은 원본 문자열
        
    Returns:
        Optional[str]: 정제된 키워드 또는 None
    """
    if not raw_input:
        return None
    
    processed = raw_input.strip()
    
    if not processed:
        return None
    
    # 100자 제한
    if len(processed) > 100:
        processed = processed[:100]
        
    return processed
