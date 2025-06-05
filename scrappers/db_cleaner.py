import asyncio
from utils import get_time_ago
from db import init_pool, execute_db_query, close_pool

async def clean_db():
    try:
        query = """
            DELETE 
            FROM kleinanzeigen
            WHERE scraped_at <= $1;
        """
        six_hours_ago = get_time_ago(6)
        await execute_db_query(query, (six_hours_ago,), target="one")

        print("Database was cleaned")
        print("Sleep 30 minutes")
        await asyncio.sleep(60 * 30)
            
    except Exception as e:
        print(f"Unexpected database error ocurred: {e}")


async def main():
    await init_pool()
    await clean_db()
    await close_pool()


async def main_loop():
    while True:
        await main()


asyncio.run(main_loop())
