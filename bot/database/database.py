import asyncpg

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy import select, exists  insert

from bot.settings import get_settings
from models import Base

cfg = get_settings()

engine: AsyncEngine = create_async_engine(cfg.DB_URL, echo=True, future=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


pool = None


async def init_pool():
    global pool
    pool = await asyncpg.create_pool(cfg.DB_URL, min_size=1, max_size=30)
    return pool


async def close_pool():
    if pool:
        await pool.close()


async def execute_raw_query(query, values=None, target="one"):
    async with pool.acquire() as conn:
        async with conn.transaction():
            if values:
                if target == "many":
                    return await conn.executemany(query, values)
                elif target == "one":
                    return await conn.execute(query, *values)
            else:
                if target == "many":
                    return await conn.executemany(query)
                elif target == "one":
                    return await conn.execute(query)


async def fetch_raw_data(query, values=None, target="row"):
    async with pool.acquire() as conn:
        if values:
            if target == "all":
                return await conn.fetch(query, *values)  # Fetch all rows
            elif target == "row":
                return await conn.fetchrow(query, *values)  # Fetch one row
            elif target == "value":
                return await conn.fetchval(query, *values)  # Fetch a single value
        else:
            if target == "all":
                return await conn.fetch(query)  # Fetch all rows
            elif target == "row":
                return await conn.fetchrow(query)  # Fetch one row
            elif target == "value":
                return await conn.fetchval(query)  # Fetch a single value

async def fetch_data_query(table, column_name)
    async with async_session() as session:
        async with session.begin():
            stmt = select(table).where(table.c.name == column_name)
            data = await session.execute(stmt)
    return data


async def user_exists(referrer_id: int) -> bool:
    async with async_session() as session:
        async with session.begin():
            stmt = select(exists().where(User.referrer_id == referrer_id))
            result = await session.scalar(stmt)
            return result



async def create_tables(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
