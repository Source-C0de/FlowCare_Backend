import asyncio
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionLocal
from sqlalchemy.future import select
from app.infra.db.session import AsyncSessionLocal
from app.infra.models.roles import Role


role_type = [
    "admin",
    "branch_manager",
    "staff",
    "customer"
]


async def seed_roles():
    async with AsyncSessionLocal() as db:  # AsyncSession
        for role_name in role_type:
            result = await db.execute(select(Role).where(Role.name == role_name.upper()))
            existing_role = result.scalars().first()

            if not existing_role:
                role = Role(name=role_name)
                db.add(role)

        await db.commit()
    print("Roles seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_roles())


# Reset Only the Sequence
# ALTER SEQUENCE roles_id_seq RESTART WITH 1;


# TRUNCATE with Cascade (If FK exists)
# TRUNCATE TABLE roles RESTART IDENTITY CASCADE;