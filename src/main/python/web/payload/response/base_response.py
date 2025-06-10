from typing import Optional
from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    message: Optional[str] = Field(None, description="응답 메시지 (처리 결과 등)")

    class Config:
        from_attributes = True  # 객체의 속성에서 값 할당 허용 (ORM 호환 등)
