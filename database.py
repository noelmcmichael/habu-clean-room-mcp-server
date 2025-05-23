import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Render will set DATABASE_URL in the deployed environment.
# We need to ensure it uses the asyncpg driver.
RAW_DATABASE_URL = os.getenv("DATABASE_URL")

if not RAW_DATABASE_URL:
    # Fallback for local development if DATABASE_URL is not set, or if running outside Render
    # and want to use a default placeholder.
    print("WARNING: DATABASE_URL environment variable not found. Using local placeholder.")
    DATABASE_URL = "postgresql+asyncpg://user:password@host:port/dbname_placeholder"
elif RAW_DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    print(f"Adjusted DATABASE_URL to use asyncpg: {DATABASE_URL}")
elif RAW_DATABASE_URL.startswith("postgres://"): # Heroku-style URLs
    DATABASE_URL = RAW_DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    print(f"Adjusted DATABASE_URL from Heroku-style to use asyncpg: {DATABASE_URL}")
else:
    DATABASE_URL = RAW_DATABASE_URL # Assume it's already correctly formatted or a different DB

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit() # Commit if no exceptions
        except Exception:
            await session.rollback() # Rollback on error
            raise
        finally:
            await session.close()
