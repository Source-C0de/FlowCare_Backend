from __future__ import annotations

from app.common import BaseModel,Optional,datetime


class GetSlotsRequest(BaseModel):
    branch_id: str
    service_type_id: str

class CreateSlotRequest(BaseModel):
    branch_id: str
    service_type_id: str
    staff_id: Optional[str] | None
    start_at: Optional[datetime] | None
    end_at: Optional[datetime] | None
    capacity: Optional[int] | None
    is_active: Optional[bool] | None
    is_booked: Optional[bool] | None

class UpdateSlotRequest(BaseModel):
    id: str
    branch_id: Optional[str] | None
    service_type_id: Optional[str] | None
    staff_id: Optional[str] | None
    start_at: Optional[str] | None
    end_at: Optional[str] | None
    capacity: Optional[int] | None
    is_active: Optional[bool] | None

class DeleteSlotRequest(BaseModel):
    id: str
