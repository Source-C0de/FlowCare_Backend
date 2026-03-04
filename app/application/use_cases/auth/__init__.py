import uuid
from datetime import datetime
from fastapi import UploadFile, HTTPException, status
# from app.domain.entities import User, UserRole
# from app.domain.repositories import IUserRepository
# from app.domain.exceptions import ConflictException
# from app.infrastructure.security import hash_password, verify_password
# from app.infrastructure.storage import StorageService
# from app.application.dtos import CustomerRegisterDTO, LoginResponseDTO


# class RegisterCustomerUseCase:
#     def __init__(self, user_repo: IUserRepository, storage: StorageService):
#         self.user_repo = user_repo
#         self.storage = storage