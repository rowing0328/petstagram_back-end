from abc import ABC, abstractmethod
from fastapi import UploadFile


class IFileStorage(ABC):

    @abstractmethod
    def save_image_to_temp(self, file: UploadFile) -> str:
        pass

    @abstractmethod
    def confirm_file(self, temp_path: str, context: str) -> str:
        pass

    @abstractmethod
    def revert_to_temp(self, file_path: str) -> str:
        pass

    @abstractmethod
    def clear_temp_directory(self):
        pass

    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        pass
