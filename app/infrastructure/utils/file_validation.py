from app.common import *
from app.config import settings

IMAGE_TYPE = ["image/jpeg", "image/png"]
ATTACHMENT_TYPE = ["application/pdf", "image/jpeg", "image/png"]



async def validate_file(file: UploadFile, allowed_type: list[str], max_size: int) -> None:
    if file.content_type not in allowed_type:
        raise HTTPException(status_code=400, detail="Invalid file type")
    content = await file.read()

    if file.size > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds limit")
    await file.seek(0)
