from fastapi import APIRouter, UploadFile, File, Depends, status, Query
from starlette.responses import FileResponse
from urllib.parse import unquote

from core.dependencies.file import get_file_service
from core.exception.error_message import ErrorMessage

file_router = APIRouter(prefix="/file", tags=["File"])


@file_router.get(
    "/view",
    summary="이미지 파일 조회 API",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "이미지 파일 반환",
            "content": {
                "image/jpeg": {},
                "image/png": {},
                "image/webp": {},
            }
        },
        400: {
            "description": "잘못된 파일 경로",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"}
                        }
                    },
                    "examples": {
                        "file_not_found": {
                            "value": {
                                "error": ErrorMessage.FILE_NOT_FOUND.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    이미지 파일 조회 API

    - 설명: 서버에 저장된 이미지 파일을 반환합니다.
    - 쿼리 파라미터
      - file_path: 조회할 이미지 파일의 전체 경로 (URL 인코딩 필요)
    - 응답
      - 200: 이미지 파일 반환 (image/jpeg, image/png 등)
      - 400: 파일이 존재하지 않거나 잘못된 파일 경로
    """
)
def get_image(
        file_path: str = Query(..., description="이미지 파일의 전체 경로 (URL 인코딩 필요)"),
        file_service=Depends(get_file_service)
) -> FileResponse:
    file_service.file_exists(file_path)
    decoded_path = unquote(file_path).strip('"')
    return FileResponse(decoded_path, media_type="image/jpeg")


@file_router.post(
    "/upload-file",
    summary="파일 업로드 API",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "파일 업로드 성공",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "temp_path": {"type": "string"}
                        }
                    },
                    "example": {
                        "temp_path": "/tmp/filename.jpg"
                    }
                }
            }
        },
        400: {
            "description": "파일 업로드 실패",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"}
                        }
                    },
                    "examples": {
                        "upload_failed": {
                            "value": {
                                "error": ErrorMessage.FILE_UPLOAD_FAILED.value
                            }
                        }
                    }
                }
            }
        }
    },
    description="""
    파일 업로드 API

    - 설명: 파일을 서버에 업로드하고 임시 경로를 반환합니다.
    - 요청
      - file: 업로드할 파일 (multipart/form-data)
    - 응답
      - 200: 파일 업로드 성공, 임시 파일 경로 반환
      - 400: 파일 업로드 실패
    """
)
def upload_file(
        file: UploadFile = File(..., description="업로드할 파일"),
        file_service=Depends(get_file_service)
):
    temp_path = file_service.upload(file)
    return {"temp_path": temp_path}
