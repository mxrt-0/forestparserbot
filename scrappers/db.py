import asyncio
import asyncpg 

DB_URL = "postgresql://postgres:Mort20051996%21@localhost/fractalparser"
pool = None

async def init_pool():
    global pool
    pool = await asyncpg.create_pool(DB_URL, min_size=1, max_size=30) 
    return pool

async def close_pool():
    if pool:
        await pool.close()


async def execute_db_query(query, params=None, target="one"):
    async with pool.acquire() as conn:
        async with conn.transaction():
            if params:
                if target == "many":
                    return await conn.executemany(query, params)
                elif target == "one":
                    return await conn.execute(query, *params)
            else:
                if target == "many":
                    return await conn.executemany(query)
                elif target == "one":
                    return await conn.execute(query)

async def fetch_db_data(query, params=None, target="row"):
    async with pool.acquire() as conn:
        if params:
            if target == "all":
                return await conn.fetch(query, *params)  # Fetch all rows
            elif target == "row":
                return await conn.fetchrow(query, *params)  # Fetch one row
            elif target == "value":
                return await conn.fetchval(query, *params)  # Fetch a single value
        else:
            if target == "all":
                return await conn.fetch(query)  # Fetch all rows
            elif target == "row":
                return await conn.fetchrow(query)  # Fetch one row
            elif target == "value":
                return await conn.fetchval(query)  # Fetch a single value

        
