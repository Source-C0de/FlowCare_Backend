from __future__ import annotations

from app.common import BaseModel,Optional


class GetSlotsRequest(BaseModel):
    branch_id: str
    service_type_id: str
    is_active: Optional[bool] | None