from enum import Enum


class ErrorMessage(Enum):
    MEMBER_NOT_FOUND = "회원을 찾을 수 없습니다."
    MEMBER_EMAIL_DUPLICATE = "이미 사용중인 이메일입니다."
    MEMBER_INVALID_EMAIL = "이메일 형식이 올바르지 않습니다."
    MEMBER_INVALID_NICKNAME = "닉네임은 비워둘 수 없습니다."

    FEED_NOT_FOUND = "요청하신 피드를 찾을 수 없습니다."
    FEED_TYPE_NOT_FOUND = "유효하지 않은 피드 타입입니다."

    FEED_LIKE_ALREADY_EXISTS = "이미 이 피드에 좋아요를 누르셨습니다."
    FEED_LIKE_NOT_FOUND = "해당 피드에 좋아요를 누른 기록이 없습니다."

    FILE_NOT_FOUND = "요청한 파일이 존재하지 않습니다."
    FILE_INVALID_IMAGE = "유효하지 않은 이미지입니다."
    FILE_INVALID_IMAGE_EXTENSION = "지원하지 않는 이미지 형식입니다. (허용: .jpg, .jpeg, .png)"
    FILE_UPLOAD_FAILED = "파일 업로드에 실패했습니다."

    KAKAO_OAUTH_FAILED = "카카오 인증에 실패했습니다."
    GOOGLE_OAUTH_FAILED = "구글 인증에 실패했습니다."

    AUTH_NOT_LOGGED_IN = "로그인이 필요합니다."
