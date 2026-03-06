import asyncio
from sqlalchemy.ext.asyncio import AsyncSession as AsyncSessionLocal
from sqlalchemy.future import select
from app.infra.db.session import AsyncSessionLocal
from app.infra.models.role import Role


roles = ["admin", "staff", "customer", "branch_manager"]


async def seed_roles():
    async with AsyncSessionLocal() as db:  # AsyncSession
        for role_name in roles:
            result = await db.execute(select(Role).where(Role.name == role_name))
            existing_role = result.scalars().first()

            if not existing_role:
                role = Role(name=role_name)
                db.add(role)

        await db.commit()
    print("Roles seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_roles())