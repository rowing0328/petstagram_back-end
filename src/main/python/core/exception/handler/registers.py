import logging
import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    tb = traceback.format_exc()
    logger.error(f"[{request.method}] {request.url.path} - {str(exc)}\n{tb}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": str(exc)
        }
    )


def permission_error_handler(request: Request, exc: PermissionError) -> JSONResponse:
    tb = traceback.format_exc()
    logger.error(f"[{request.method}] {request.url.path} - {str(exc)}\n{tb}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": str(exc)
        }
    )


def file_not_found_error_handler(request: Request, exc: FileNotFoundError) -> JSONResponse:
    tb = traceback.format_exc()
    logger.error(f"[{request.method}] {request.url.path} - {str(exc)}\n{tb}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": str(exc)
        }
    )

# def validation_error_handler(request: Request, exc: ValidationError) -> JSONResponse:
#     tb = traceback.format_exc()
#     logger.error(f"[{request.method}] {request.url.path} - {str(exc)}\n{tb}")
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "error": str(exc)
#         }
#     )
