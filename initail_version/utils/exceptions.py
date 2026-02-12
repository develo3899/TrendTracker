class AppError(Exception):
    """
    Trend Tracker 애플리케이션의 커스텀 예외 클래스입니다.
    API 키 오류, 할당량 초과, 네트워크 장애 등 비즈니스 로직 상의 에러를 구분하기 위해 사용합니다.
    
    Attributes:
        error_type (str): 에러의 종류를 나타내는 식별자
    """
    def __init__(self, error_type: str):
        self.error_type = error_type
        super().__init__(error_type)
