from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.security import HTTPBasicCredentials

# # from app.infra.core import (
# #     get_user_repo, get_storage, get_current_user, security
# # )

# from app.infra.core import (
#     security
# )
# # from app.infra.db.repositories import UserRepository
# # from app.infra.core.security import verify_password
# # from app.infrastructure.storage import StorageService
# # from app.application.use_cases.auth import RegisterCustomerUseCase
# from app.application.dtos import CustomerRegisterDTO
# # from app.domain.entities import User



router = APIRouter(prefix="/auth", tags=["Authentication"])

# # @router.post("register", response_model=CustomerRegisterDTO)
# # async def register(
# #     email: str,
# #     password: str,
# #     full_name: str,
# #     user_repo: UserRepository = Depends(get_user_repo)
# #     storage: StorageService = Depends(get_storage)
# # ):
    
    

# # @router.post("/login",response_model=LoginResponseDTO)
# # async def login(
# #     credentials: HTTPBasicCredentials = Depends(security),
# #     user_repo: UserRepository = Depends(get_user_repo)
# # ):
# #     if not credentials:
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail="Credentials required",
# #             headers={"WWW-Authenticate": "Basic"},
# #         )
# #     user = await use_case.execute(credentials.username, credentials.password)
# #     return LoginResponseDTO(
# #         user_id=user.id, email=user.email, full_name=user.full_name,
# #         role=user.role, branch_id=user.branch_id
# #     )