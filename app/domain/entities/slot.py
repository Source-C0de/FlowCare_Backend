from __future__ import annotations

from app.common import BaseModel,Optional,datetime

class Slot(BaseModel):
    id: Optional[str] | None
    branch_id: Optional[str] | None
    service_type_id: Optional[str] | None
    is_active: Optional[bool] | None
    staff_id: Optional[str] | None
    start_time: Optional[datetime] | None
    end_time: Optional[datetime] | None
    is_booked: Optional[bool] | None
    capacity: Optional[int] | None