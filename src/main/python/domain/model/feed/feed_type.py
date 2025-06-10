from enum import Enum

from src.main.python.core.exception.error_message import ErrorMessage


class FeedType(Enum):
    """
    Feed 타입을 정의하는 Enum 클래스

    작성자: 신효승
    작성일: 2025-05-24

    - FOOD: 사료 및 간식
    - CARE: 돌봄 및 케어
    - MEDICAL: 병원 및 의료
    - GROOMING: 미용 및 목욕
    """
    FOOD = "FOOD"
    CARE = "CARE"
    MEDICAL = "MEDICAL"
    GROOMING = "GROOMING"

    @classmethod
    def from_value(cls, value: str) -> "FeedType":
        """
        문자열 값을 받아 FeedType Enum 멤버로 반환합니다.
        대소문자 구분 없이 처리합니다.
        """
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(ErrorMessage.FEED_TYPE_NOT_FOUND.value)
