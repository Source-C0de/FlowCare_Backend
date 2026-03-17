"""Application-layer Data Transfer Objects."""

# from app.application.dtos.auth_dto import UserRegisterDTO, UserLoginDTO
# from app.application.dtos.appointment_dto import AppointmentDTO
from . import auth_dto
from . import appointment_dto
from . import service_type_dto
from . import slot_dto
from . import branch_dto
from . import audit_dto
from . import common_dto

from .auth_dto import *
from .appointment_dto import *
from .service_type_dto import *
from .slot_dto import *
from .branch_dto import *
from .audit_dto import *
from .common_dto import *

# __all__ = [
#     # "UserRegisterDTO", 
#     # "UserLoginDTO",
#     # "AppointmentDTO",
#     # "ServiceTypeDTO",
#     # "BranchDTO"
# ]


__all__ = (
    auth_dto.__all__ +
    appointment_dto.__all__ +
    service_type_dto.__all__ +
    slot_dto.__all__ +
    branch_dto.__all__ +
    audit_dto.__all__ +
    common_dto.__all__
)
