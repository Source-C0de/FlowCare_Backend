from __future__ import annotations
from fastapi import Depends

from app.domain.models.user import User





# async def get_current_user(current_user: User = Depends(get_current_user))