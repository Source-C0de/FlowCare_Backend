from sqlalchemy.ext.asyncio import create_async_engine , AsyncSession , async_sessionmaker
from app.config import Settings



engine = create_async_engine(
    Settings.DATABASE_URL
    echo= Settings.Debug
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()