from pydantic import BaseModel


class BaseRequest(BaseModel):
    """
    모든 요청(Request) 모델의 베이스 클래스입니다.
    공통 설정을 위해 사용됩니다.
    """
    model_config = {"frozen": True}
