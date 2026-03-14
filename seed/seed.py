import asyncio
import uuid
from sqlalchemy.future import select

from app.infrastructure.database.session import AsyncSessionLocal
from app.infrastructure.models.role_model import Role
from app.infrastructure.models.user_model import User
from app.infrastructure.security.hashing import hash_password
from app.config import settings

ROLE_TYPES = [
    "ADMIN",
    "BRANCH_MANAGER",
    "STAFF",
    "CUSTOMER"
]

async def seed_data():
    async with AsyncSessionLocal() as db:
        # 1. Seed Roles
        for role_name in ROLE_TYPES:
            result = await db.execute(select(Role).where(Role.role_type == role_name))
            existing_role = result.scalars().first()

            if not existing_role:
                role = Role(role_type=role_name)
                db.add(role)
        
        await db.commit()
        print("✅ Roles seeded successfully!")

        # 2. Seed Admin User
        admin_email = getattr(settings, "ADMIN_EMAIL", "admin@system.com")
        admin_password = getattr(settings, "ADMIN_PASSWORD", "Admin@123")
        
        result = await db.execute(select(User).where(User.email == admin_email))
        existing_admin = result.scalars().first()
        
        if not existing_admin:
            # Get the Admin role ID
            result = await db.execute(select(Role).where(Role.role_type == "ADMIN"))
            admin_role = result.scalars().first()
            
            if admin_role:
                admin_user = User(
                    id=uuid.uuid4(),
                    email=admin_email,
                    password_hash=hash_password(admin_password),
                    phone="+1234567890",
                    role_id=admin_role.id,
                    is_verified=True,
                    is_active=True
                )
                db.add(admin_user)
                await db.commit()
                print(f"✅ Admin user seeded successfully! ({admin_email})")
            else:
                print("❌ Could not find ADMIN role!")
        else:
            print(f"✅ Admin user already exists! ({admin_email})")

if __name__ == "__main__":
    asyncio.run(seed_data())