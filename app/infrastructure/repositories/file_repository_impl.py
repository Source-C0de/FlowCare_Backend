from __future__ import annotations
from app.common import * 
from app.domain.interfaces.file_repository import FileRepository
from minio import Minio
from app.config import settings

class FileRepositoryImpl(FileRepository):
    def __init__(self) -> None:
        self._minio = Minio(
            endpoint=settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
    
    async def upload_file(self, file: UploadFile, folder: str) -> str:
        try:
            path_name = f"{folder}/{uuid.uuid4()}_{file.filename}"
            self._minio.put_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=path_name,
                data=file.file,
                length=file.size,
                content_type=file.content_type,
            )
            return path_name
        except Exception as e:
            raise Exception(f"Failed to upload file: {str(e)}")
    

    async def get_file(self, file_path: str) -> UploadFile:
        try:
            file = self._minio.get_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=file_path,
            )
            return file
        except Exception as e:
            raise Exception(f"Failed to get file: {str(e)}")

    async def delete_file(self, file_path: str) -> None:
        try:
            self._minio.remove_object(
                bucket_name=settings.MINIO_BUCKET_NAME,
                object_name=file_path,
            )
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")

__all__ = [
    "FileRepositoryImpl"    
]