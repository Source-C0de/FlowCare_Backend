import asyncio
import uuid
from datetime import datetime, timedelta
from sqlalchemy.future import select
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.slot_model import Slot
from app.infrastructure.models.branch_model import Branch
from app.infrastructure.models.service_type_model import ServiceType
from app.infrastructure.models.staff_profile_model import StaffProfile

async def seed_slots():
    async with AsyncSessionLocal() as db:
        # 1. Ensure at least one branch exists
        result = await db.execute(select(Branch))
        branch = result.scalars().first()
        if not branch:
            branch = Branch(
                uid=uuid.uuid4(),
                id="br_suhar_1",
                name="Sohar Main Branch",
                city="Sohar",
                address="Main Street, Sohar",
                phone="+96812345678",
                timezone="Asia/Muscat",
                is_active=True
            )
            db.add(branch)
            await db.commit()
            print("✅ Branch created.")
        else:
            print(f"✅ Using existing branch: {branch.id}")

        # 2. Ensure at least one service type exists
        result = await db.execute(select(ServiceType).where(ServiceType.branch_id == branch.id))
        service_type = result.scalars().first()
        if not service_type:
            service_type = ServiceType(
                uid=uuid.uuid4(),
                id="test_update_1",
                branch_id=branch.id,
                name="Consultation",
                description="General consultation service",
                duration_minutes=30,
                is_active=True
            )
            db.add(service_type)
            await db.commit()
            print("✅ Service type created.")
        else:
            print(f"✅ Using existing service type: {service_type.id}")

        # 3. Get any staff profile if available
        result = await db.execute(select(StaffProfile).where(StaffProfile.branch_id == branch.id))
        staff = result.scalars().first()
        staff_id = staff.id if staff else None
        if staff:
            print(f"✅ Using existing staff: {staff.full_name}")
        else:
            print("⚠️ No staff profile found. Slots will be created without staff_id.")

        # 4. Generate Slots for the next 2 days
        base_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        
        slots_count = 0
        for day_offset in range(2):
            for hour_offset in range(8):  # 8 AM to 4 PM
                start_time = base_time + timedelta(days=day_offset, hours=hour_offset)
                end_time = start_time + timedelta(minutes=30)
                
                slot_id = f"slot_{branch.id}_{start_time.strftime('%Y%m%d_%H%M')}"
                
                # Check if slot already exists
                check_result = await db.execute(select(Slot).where(Slot.id == slot_id))
                if not check_result.scalars().first():
                    slot = Slot(
                        uid=uuid.uuid4(),
                        id=slot_id,
                        branch_id=branch.id,
                        service_type_id=service_type.id,
                        staff_id=staff_id,
                        start_time=start_time,
                        end_time=end_time,
                        is_booked=False,
                        is_active=True
                    )
                    db.add(slot)
                    slots_count += 1
        
        if slots_count > 0:
            await db.commit()
            print(f"✅ Seeded {slots_count} slots successfully!")
        else:
            print("✅ No new slots were added (already exist).")

if __name__ == "__main__":
    asyncio.run(seed_slots())
