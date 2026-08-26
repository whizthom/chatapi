import asyncio

from sqlalchemy import text

from app.core.database import engine


async def test_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            print("Database connection successful:", result.scalar_one())
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_connection())