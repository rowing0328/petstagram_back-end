import os
import shutil

from uuid import uuid4
from fastapi import UploadFile
from PIL import Image

from core.exception.error_message import ErrorMessage
from domain.storage.file_storage_interface import IFileStorage


class LocalFileStorage(IFileStorage):

    _BASE_DIR = os.getenv("FILE_STORAGE_BASE_DI")
    _TEMP_DIR = os.path.join(_BASE_DIR, "temp")

    def __init__(self):
        os.makedirs(self._TEMP_DIR, exist_ok=True)

    def _generate_unique_filename(self, extension: str, directory: str) -> str:
        while True:
            filename = f"{uuid4().hex}{extension}"
            if not os.path.exists(os.path.join(directory, filename)):
                return filename

    def _generate_jpeg_image(self, upload_file: UploadFile) -> Image.Image:
        try:
            image = Image.open(upload_file.file)
        except Exception:
            raise ValueError(ErrorMessage.FILE_INVALID_IMAGE.value)
        return image.convert("RGB")

    def _move_with_unique_name(self, src_path: str, dest_dir: str) -> str:
        extension = os.path.splitext(src_path)[1].lower()
        filename = os.path.basename(src_path)
        destination_path = os.path.join(dest_dir, filename)

        if os.path.exists(destination_path):
            filename = self._generate_unique_filename(extension, dest_dir)
            destination_path = os.path.join(dest_dir, filename)

        shutil.move(src_path, destination_path)
        return destination_path

    def save_image_to_temp(self, file: UploadFile) -> str:
        image = self._generate_jpeg_image(file)

        filename = self._generate_unique_filename(".jpeg", self._TEMP_DIR)
        file_path = os.path.join(self._TEMP_DIR, filename)

        image.save(file_path, format="JPEG", quality=85)

        return file_path

    def confirm_file(self, temp_path: str, context: str) -> str:
        if not os.path.exists(temp_path):
            raise FileNotFoundError(ErrorMessage.FILE_NOT_FOUND)

        target_dir = os.path.join(self._BASE_DIR, context)
        os.makedirs(target_dir, exist_ok=True)

        return self._move_with_unique_name(temp_path, target_dir)

    def revert_to_temp(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(ErrorMessage.FILE_NOT_FOUND)

        return self._move_with_unique_name(file_path, self._TEMP_DIR)

    def clear_temp_directory(self):
        for filename in os.listdir(self._TEMP_DIR):
            file_path = os.path.join(self._TEMP_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def file_exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)
