import asyncio
import uuid
import sys
import os

# Add the project root to sys.path to allow imports from 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.role_model import Role
from app.infrastructure.models.branch_model import Branch
from app.infrastructure.models.service_type_model import ServiceType
from app.infrastructure.models.user_model import User
from app.infrastructure.models.staff_profile_model import StaffProfile
from app.infrastructure.security.hashing import hash_password
from sqlalchemy import select

SEED_DATA = {
  "roles": [
    {"id": 1, "name": "admin", "permissions": {"all": True}},
    {"id": 2, "name": "manager", "permissions": {"branch_scoped": True}},
    {"id": 3, "name": "staff", "permissions": {"appointments": ["read", "update"]}},
    {"id": 4, "name": "customer", "permissions": {"appointments": ["create", "read", "cancel", "reschedule"]}}
  ],
  "branches": [
    {"name": "FlowCare Muscat Central", "location": "Al Qurum, Muscat, Oman", "phone": "+968-2412-0001", "city": "Muscat", "id": "muscat-central"},
    {"name": "FlowCare Salalah Branch", "location": "Salalah City Center, Dhofar, Oman", "phone": "+968-2323-0002", "city": "Salalah", "id": "salalah-branch"},
    {"name": "FlowCare Sohar Hub", "location": "Sohar Industrial Area, Al Batinah, Oman", "phone": "+968-2685-0003", "city": "Sohar", "id": "sohar-hub"}
  ],
  "service_types": [
    {"branch_index": 0, "name": "General Consultation", "description": "General medical consultation with a doctor", "duration_minutes": 30, "id": "muscat-gen-cons"},
    {"branch_index": 0, "name": "Blood Test", "description": "Blood sample collection and analysis", "duration_minutes": 15, "id": "muscat-blood-test"},
    {"branch_index": 0, "name": "X-Ray Imaging", "description": "Digital X-Ray scan and report", "duration_minutes": 20, "id": "muscat-xray"},
    {"branch_index": 0, "name": "Pharmacy Counter", "description": "Prescription pickup and medication consultation", "duration_minutes": 10, "id": "muscat-pharmacy"},
    {"branch_index": 1, "name": "General Consultation", "description": "General medical consultation", "duration_minutes": 30, "id": "salalah-gen-cons"},
    {"branch_index": 1, "name": "Dental Care", "description": "Dental examination and treatment", "duration_minutes": 45, "id": "salalah-dental"},
    {"branch_index": 1, "name": "Eye Examination", "description": "Vision test and eye health check", "duration_minutes": 25, "id": "salalah-eye"},
    {"branch_index": 1, "name": "Physiotherapy", "description": "Physical rehabilitation and therapy sessions", "duration_minutes": 60, "id": "salalah-physio"},
    {"branch_index": 2, "name": "General Consultation", "description": "General medical consultation", "duration_minutes": 30, "id": "sohar-gen-cons"},
    {"branch_index": 2, "name": "Vaccination", "description": "Immunization and vaccination services", "duration_minutes": 15, "id": "sohar-vaccine"},
    {"branch_index": 2, "name": "Chronic Disease Management", "description": "Follow-up for chronic conditions", "duration_minutes": 40, "id": "sohar-chronic"}
  ],
  "staff": [
    {"branch_index": 0, "role_name": "manager", "role_id": 2, "name": "Sara Al Balushi", "email": "sara.manager@flowcare.om", "password": "Manager@1234", "phone": "+968-9100-0001"},
    {"branch_index": 0, "role_name": "staff",   "role_id": 3, "name": "Ahmed Al Farsi",   "email": "ahmed.staff@flowcare.om",  "password": "Staff@1234",   "phone": "+968-9100-0002"},
    {"branch_index": 0, "role_name": "staff",   "role_id": 3, "name": "Fatima Al Hinai",  "email": "fatima.staff@flowcare.om", "password": "Staff@1234",   "phone": "+968-9100-0003"},
    {"branch_index": 1, "role_name": "manager", "role_id": 2, "name": "Khalid Al Rawahi", "email": "khalid.manager@flowcare.om","password": "Manager@1234","phone": "+968-9200-0001"},
    {"branch_index": 1, "role_name": "staff",   "role_id": 3, "name": "Maha Al Zadjali",  "email": "maha.staff@flowcare.om",   "password": "Staff@1234",   "phone": "+968-9200-0002"},
    {"branch_index": 1, "role_name": "staff",   "role_id": 3, "name": "Omar Al Maskari",  "email": "omar.staff@flowcare.om",   "password": "Staff@1234",   "phone": "+968-9200-0003"},
    {"branch_index": 2, "role_name": "manager", "role_id": 2, "name": "Hessa Al Mamari",  "email": "hessa.manager@flowcare.om","password": "Manager@1234", "phone": "+968-9300-0001"},
    {"branch_index": 2, "role_name": "staff",   "role_id": 3, "name": "Yousuf Al Kindi",  "email": "yousuf.staff@flowcare.om", "password": "Staff@1234",   "phone": "+968-9300-0002"}
  ]
}

async def seed():
    async with AsyncSessionLocal() as session:
        print("Seeding roles...")
        for role_data in SEED_DATA["roles"]:
            stmt = select(Role).where(Role.id == role_data["id"])
            result = await session.execute(stmt)
            if not result.scalars().first():
                role = Role(
                    id=role_data["id"],
                    role_type=role_data["name"],
                    permissions=role_data["permissions"]
                )
                session.add(role)
        await session.commit()

        print("Seeding branches...")
        branch_entities = []
        for b_data in SEED_DATA["branches"]:
            stmt = select(Branch).where(Branch.id == b_data["id"])
            result = await session.execute(stmt)
            branch = result.scalars().first()
            if not branch:
                branch = Branch(
                    id=b_data["id"],
                    name=b_data["name"],
                    city=b_data["city"],
                    address=b_data["location"],
                    phone=b_data["phone"],
                    timezone="Asia/Muscat",
                    is_active=True
                )
                session.add(branch)
            branch_entities.append(branch)
        await session.commit()
        
        # Refresh branch entities to ensure they are attached to the session
        for b in branch_entities:
            await session.refresh(b)

        print("Seeding service types...")
        for s_data in SEED_DATA["service_types"]:
            branch = branch_entities[s_data["branch_index"]]
            stmt = select(ServiceType).where(ServiceType.id == s_data["id"])
            result = await session.execute(stmt)
            if not result.scalars().first():
                st = ServiceType(
                    id=s_data["id"],
                    branch_id=branch.id,
                    name=s_data["name"],
                    description=s_data["description"],
                    duration_minutes=s_data["duration_minutes"],
                    is_active=True
                )
                session.add(st)
        await session.commit()

        print("Seeding staff...")
        for staff_data in SEED_DATA["staff"]:
            branch = branch_entities[staff_data["branch_index"]]
            stmt = select(User).where(User.email == staff_data["email"])
            result = await session.execute(stmt)
            if not result.scalars().first():
                # Create User
                user = User(
                    id=uuid.uuid4(),
                    email=staff_data["email"],
                    password_hash=hash_password(staff_data["password"]),
                    phone=staff_data["phone"],
                    role_id=staff_data["role_id"],
                    is_verified=True,
                    is_active=True
                )
                session.add(user)
                await session.flush() # Get user.id

                # Create StaffProfile
                username = staff_data["email"].split('@')[0]
                profile = StaffProfile(
                    user_id=user.id,
                    username=username,
                    full_name=staff_data["name"],
                    role=staff_data["role_name"],
                    branch_id=branch.id,
                    is_active=True
                )
                session.add(profile)
        await session.commit()
        print("Seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
