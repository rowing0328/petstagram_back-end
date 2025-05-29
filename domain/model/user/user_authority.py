from enum import Enum


class UserAuthority(str, Enum):
    """
    사용자 권한 Enum 클래스

    Author: 신효승
    Created: 2025-05-23

    Values:
    - member: 회원 권한
    - admin: 관리자 권한
    """
    member = "member"
    admin = "admin"
