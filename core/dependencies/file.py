from Infrastructure.storage.local_file import LocalFileStorage
from application.service.file import FileService
from domain.storage.file_storage_interface import IFileStorage

# 싱글톤 스토리지 객체
local_file_storage_singleton = LocalFileStorage()


def get_local_file_storage() -> IFileStorage:
    return local_file_storage_singleton


# 싱글톤 FileService 객체
file_service_singleton = FileService(local_file_storage_singleton)


def get_file_service() -> FileService:
    return file_service_singleton
