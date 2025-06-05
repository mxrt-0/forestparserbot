import asyncio
from db import init_pool, close_pool, execute_db_query


async def kleinanzeigen_specific_table():
    query = """
        CREATE TABLE IF NOT EXISTS kleinanzeigen_specific( 
            id BIGINT PRIMARY KEY NOT NULL, 
            url TEXT NOT NULL,
            is_checked TEXT,
            target_user TEXT
        );
    """
    await execute_db_query(query)


async def kleinanzen_table():
    query = """
        CREATE TABLE IF NOT EXISTS kleinanzeigen( 
            id BIGINT PRIMARY KEY NOT NULL, 
            url TEXT NOT NULL,
            publication_time TEXT NOT NULL,
            views SMALLINT,
            scraped_at TEXT,
            views_hour_later SMALLINT,
            rechecked_hour_later TEXT, 
            views_two_later SMALLINT, 
            rechecked_two_later TEXT,
            title TEXT,
            price TEXT,
            image TEXT,
            description TEXT,
            undercategory TEXT
        );
    """
    await execute_db_query(query)
            
async def results_table():
    query = """
        CREATE TABLE IF NOT EXISTS results(
            id BIGINT PRIMARY KEY NOT NULL, 
            url TEXT NOT NULL,
            publication_time TEXT NOT NULL,
            views SMALLINT,
            scraped_at TEXT,
            views_hour_later SMALLINT,
            rechecked_hour_later TEXT, 
            views_two_later INT, 
            rechecked_two_later TEXT,
            title TEXT,
            price TEXT,
            image TEXT,
            description TEXT,
            undercategory TEXT
        );
    """
    await execute_db_query(query)

    
async def telegram_bot_table():
    query = """                
        CREATE TABLE IF NOT EXISTS telegram_bot(
            id BIGINT PRIMARY KEY NOT NULL, 
            url TEXT NOT NULL,
            publication_time TEXT NOT NULL,
            views INT,
            scraped_at TEXT,
            views_hour_later INT,
            rechecked_hour_later TEXT, 
            views_two_later INT, 
            rechecked_two_later TEXT,
            title TEXT,
            price TEXT,
            image TEXT,
            description TEXT,
            undercategory TEXT
        );
    """
    await execute_db_query(query)

async def main():
    await init_pool()
    await kleinanzeigen_specific_table()
    await kleinanzen_table()
    await results_table()
    await telegram_bot_table()
    await close_pool()

asyncio.run(main())
