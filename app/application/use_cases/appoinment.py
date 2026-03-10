from fastapi import uploadFile, HTTPException, status



class Appoinment:
    def __init__(
        self,
        branch_id: str,
        service_type_id: str,
        staff_id: str,
        start_time: str,
        end_time: str,
        capacity: int,
        is_active: bool
    ):
        self.branch_id = branch_id
        self.service_type_id = service_type_id
        self.staff_id = staff_id
        self.start_time = start_time
        self.end_time = end_time
        self.capacity = capacity
        self.is_active = is_active

        def book_appointment(self):

            slot_available = self.check_slot_availability()
            if not slot_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Slot is not available"
                )
            check_service_type = self.check_service_type_availability()
            if not check_service_type:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Service type is not available"
                )

            result = self.create_appointment()
            return result

            