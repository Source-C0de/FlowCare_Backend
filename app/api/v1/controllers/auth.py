from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBasicCredentials


from app.infra.db.session import get_db
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
from app.infra.db.session import get_db
from app.infra.models.users import User
from app.api.v1.schemas.user_schema import (
    CreateUserRequest,
    UserRegisterResponse
)
from app.application.dtos import (
    CustomerRegisterDTO
)

from app.domain.repository.user_repo import UserRepository
from app.application.use_cases import (
    auth
)
# # from app.domain.entities import User


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201, response_model=UserRegisterResponse)
async def register(request: CreateUserRequest):
    #DTO
    dto = CustomerRegisterDTO(
        name=request.name,
        email=request.email,
        password=request.password,
        phone=request.phone,
    )
    user = await auth.RegisterUserUserCase.excute(dto)

    return UserRegisterResponse(
        id=str(user.id),
        name=user.name,
        email=user.email,
    )




    #Use_Case
    # existing = await db.execute(select(Customer).where(Customer.email == email))
    # if existing.scalar_one_or_none():
    #     raise HTTPException(status_code=400, detail="Email already registered")

    # image_path = await save_id_image(id_image)
    # customer = Customer(
    #     name=name,
    #     email=email,
    #     password_hash=hash_password(password),
    #     phone=phone,
    #     id_image_path=image_path,
    # )
    # db.add(customer)
    # await db.flush()



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


# @router.post("/login", status_code=201)
# async def login(
#     email:str,
#     password:str
# ):
#     return {"message": "Customer login successfully"}
