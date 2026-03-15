from __future__ import annotations

from app.common import * 

class FileRepository(ABC):


    @abstractmethod
    async def upload_file(self, file: UploadFile, folder: str) -> str:
        pass
    @abstractmethod
    async def get_file(self, file_path: str) -> UploadFile:
        pass
    @abstractmethod
    async def delete_file(self, file_path: str) -> None:
        pass

__all__ = [
    "FileRepository"    
]