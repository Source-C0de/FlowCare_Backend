from __futuer__ import annotations

from app.common import *
from app.api.v1.schemas import *
from app.application.dtos import *
from app.application.use_cases import *


from app.api.dependencies import get_auth_use_case
from app.api.middleware.Rbac import require_roles


from app.config import settings

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/me", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_me(
    current_user = Depends(get_current_user)
):
    return current_user




@router.patch("/update-profile", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def update_user(
    request: UpdateUserRequest,
    current_user = Depends(get_current_user)
):
    
    return current_user