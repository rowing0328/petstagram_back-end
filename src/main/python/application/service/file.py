from fastapi import UploadFile

from src.main.python.core.exception.error_message import ErrorMessage
from src.main.python.domain.storage.file_storage_interface import IFileStorage


class FileService:
    def __init__(self, file_storage: IFileStorage):
        self.storage = file_storage

    def upload(self, file: UploadFile) -> str:
        return self.storage.save_image_to_temp(file)

    def confirm(self, temp_path: str, context: str) -> str:
        return self.storage.confirm_file(temp_path, context)

    def revert_file_to_temp(self, file_path: str) -> str:
        return self.storage.revert_to_temp(file_path)

    def clear_temp_files(self) -> str:
        self.storage.clear_temp_directory()

    def file_exists(self, file_path: str) -> bool:
        if not self.storage.file_exists(file_path):
            raise FileNotFoundError(ErrorMessage.FILE_NOT_FOUND)
