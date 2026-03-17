import asyncio
import json
import os
import sys
import uuid
from datetime import datetime, timedelta
from typing import Dict, List

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import select
from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.role_model import Role
from app.infrastructure.models.branch_model import Branch
from app.infrastructure.models.service_type_model import ServiceType
from app.infrastructure.models.user_model import User
from app.infrastructure.models.staff_profile_model import StaffProfile
from app.infrastructure.models.customer_profile_model import CustomerProfile
from app.infrastructure.models.staff_service_type_model import StaffServiceType
from app.infrastructure.models.slot_model import Slot
from app.infrastructure.models.appointment_model import Appointment
from app.infrastructure.security.hashing import hash_password

JSON_FILE = "example.json"

# Utility: Create a stable UUID from a string
def to_uuid(id_str: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_DNS, f"flowcare.{id_str}")

async def seed_from_json():
    if not os.path.exists(JSON_FILE):
        print(f"File {JSON_FILE} not found.")
        return

    with open(JSON_FILE, "r") as f:
        data = json.load(f)

    async with AsyncSessionLocal() as session:
        # 1. Roles (Fallback defaults if not in JSON)
        print("Seeding roles...")
        roles_to_seed = [
            {"id": 1, "name": "ADMIN"},
            {"id": 2, "name": "BRANCH_MANAGER"},
            {"id": 3, "name": "STAFF"},
            {"id": 4, "name": "CUSTOMER"}
        ]
        for r in roles_to_seed:
            stmt = select(Role).where(Role.id == r["id"])
            if not (await session.execute(stmt)).scalars().first():
                session.add(Role(id=r["id"], role_type=r["name"]))
        await session.commit()

        # 2. Branches
        print("Seeding branches...")
        branch_map = {} # Maps JSON ID to SQL Model
        for b_data in data.get("branches", []):
            stmt = select(Branch).where(Branch.id == b_data["id"])
            branch = (await session.execute(stmt)).scalars().first()
            if not branch:
                branch = Branch(
                    uid=to_uuid(b_data["id"]),
                    id=b_data["id"],
                    name=b_data["name"],
                    city=b_data["city"],
                    address=b_data["address"],
                    timezone="Asia/Muscat",
                    is_active=True
                )
                session.add(branch)
            branch_map[b_data["id"]] = branch
        await session.commit()

        # 3. ServiceTypes
        print("Seeding service types...")
        for s_data in data.get("service_types", []):
            stmt = select(ServiceType).where(ServiceType.id == s_data["id"])
            if not (await session.execute(stmt)).scalars().first():
                st = ServiceType(
                    uid=to_uuid(s_data["id"]),
                    id=s_data["id"],
                    branch_id=s_data["branch_id"],
                    name=s_data["name"],
                    description=s_data["description"],
                    duration_minutes=s_data["duration_minutes"],
                    is_active=True
                )
                session.add(st)
        await session.commit()

        # 4. Users (Unified Seeding)
        print("Seeding users (Admin, Managers, Staff, Customers)...")
        users_flat = []
        for cat, list_users in data.get("users", {}).items():
            for u in list_users:
                u["category"] = cat 
                users_flat.append(u)

        user_role_map = {
            "admin": 1,
            "branch_managers": 2,
            "staff": 3,
            "customers": 4
        }

        for u_data in users_flat:
            stmt = select(User).where(User.email == u_data["email"])
            user = (await session.execute(stmt)).scalars().first()
            if not user:
                user = User(
                    id=to_uuid(u_data["id"]),
                    email=u_data["email"],
                    password_hash=hash_password(u_data["password"]),
                    role_id=user_role_map.get(u_data["category"], 4),
                    is_active=True,
                    is_verified=True,
                    phone=u_data.get("phone")
                )
                session.add(user)
                await session.flush() # Ensure ID is set

                # If staff/manager, create Profile
                if u_data["category"] in ["staff", "branch_managers"]:
                    stmt_profile = select(StaffProfile).where(StaffProfile.user_id == user.id)
                    if not (await session.execute(stmt_profile)).scalars().first():
                        profile = StaffProfile(
                            user_id=user.id,
                            username=u_data["username"],
                            full_name=u_data["full_name"],
                            role=u_data["role"],
                            branch_id=u_data.get("branch_id"),
                            is_active=True
                        )
                        session.add(profile)
                
                # If customer, create Profile
                if u_data["category"] == "customers":
                    stmt_cust = select(CustomerProfile).where(CustomerProfile.customer_email == user.email)
                    if not (await session.execute(stmt_cust)).scalars().first():
                        cust_profile = CustomerProfile(
                            customer_email=user.email,
                            user_name=u_data["username"],
                            first_name=u_data.get("full_name", "").split(" ")[0],
                            last_name=" ".join(u_data.get("full_name", "").split(" ")[1:]),
                            id_image_path="uploads/id_images/seed_default.jpg"
                        )
                        session.add(cust_profile)

        await session.commit()

        # 5. Staff Service Types
        print("Seeding staff service type assignments...")
        for sst_data in data.get("staff_service_types", []):
            staff_user_id = to_uuid(sst_data["staff_id"])
            # We need the profile ID or staff user sequence ID?
            # Looking at our model: StaffServiceType connects to staff_id (Integer from Profile) or User?
            # Let's check StaffServiceType model.
            stmt_staff_profile = select(StaffProfile).where(StaffProfile.user_id == staff_user_id)
            staff_profile = (await session.execute(stmt_staff_profile)).scalars().first()
            if staff_profile:
                stmt_exist = select(StaffServiceType).where(
                    StaffServiceType.staff_id == staff_profile.id,
                    StaffServiceType.service_type_id == sst_data["service_type_id"]
                )
                if not (await session.execute(stmt_exist)).scalars().first():
                    sst = StaffServiceType(
                        uid=uuid.uuid4(),
                        staff_id=staff_profile.id,
                        service_type_id=sst_data["service_type_id"],
                        is_active=True
                    )
                    session.add(sst)
        await session.commit()

        # 6. Slots (Generate for next 3-7 days)
        print("Seeding slots (Dynamic schedule for next 7 days)...")
        # I'll use some from JSON as templates but create fresh ones for the future
        for day_offset in range(1, 8): # Next 7 days
            target_date = datetime.now() + timedelta(days=day_offset)
            # Create a few slots per branch per service type
            for b_id, branch in branch_map.items():
                # Get some service types for this branch
                stmt_st = select(ServiceType).where(ServiceType.branch_id == b_id)
                branch_services = (await session.execute(stmt_st)).scalars().all()
                
                for bs in branch_services:
                    for hour in [9, 11, 14]: # 9AM, 11AM, 2PM
                        start_at = target_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                        end_at = start_at + timedelta(minutes=bs.duration_minutes)
                        
                        slot_id = f"slot_{b_id}_{bs.id}_{start_at.strftime('%Y%m%d%H%M')}"
                        
                        stmt_slot = select(Slot).where(Slot.id == slot_id)
                        if not (await session.execute(stmt_slot)).scalars().first():
                            # Optional: assign any staff from this branch who can do this service
                            stmt_staff = select(StaffProfile).where(
                                StaffProfile.branch_id == b_id
                            ).limit(1)
                            staff_p = (await session.execute(stmt_staff)).scalars().first()
                            
                            new_slot = Slot(
                                uid=uuid.uuid4(),
                                id=slot_id,
                                branch_id=b_id,
                                service_type_id=bs.id,
                                staff_id=staff_p.id if staff_p else None,
                                start_time=start_at,
                                end_time=end_at,
                                is_booked=False,
                                is_active=True
                            )
                            session.add(new_slot)
        await session.commit()

        print("Seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_from_json())
