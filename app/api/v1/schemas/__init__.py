from .user_schemas import *
from .auth_schemas import *
from .appointment_schemas import *
from .branch_schemas import *
from .service_type_schemas import *
from .slot_schemas import *
from .audit_shcemas import *
from .common import *

# from . import user_schemas
# from . import auth_schemas
# from . import appointment_schemas
# from . import branch_schemas
# from . import service_type_schemas
# from . import slot_schemas
# from . import audit_shcemas

__all__ = (
    user_schemas.__all__ +
    auth_schemas.__all__ +
    appointment_schemas.__all__ +
    branch_schemas.__all__ +
    service_type_schemas.__all__ +
    slot_schemas.__all__ +
    audit_shcemas.__all__ +
    common.__all__
)
