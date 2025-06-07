from bot.database.database import execute_raw_query
from bot.database.utils import KleinanzeigenOneUtilities


async def users():
    query = """
        CREATE TABLE IF NOT EXISTS users(
            user_id BIGINT PRIMARY KEY,
            refferer_id BIGINT,
            current_balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0,
            total_balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0,
            refferer_balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0,
            total_referrer_balance NUMERIC(8,2) CHECK (balance >= 0) DEFAULT 0,
            subscription_expired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_banned BOOLEAN DEFAULT FALSE
        )
    """
    await execute_raw_query(query)


async def kleinanzeigen_one():
    query = """
        CREATE TABLE IF NOT EXISTS kleinanzeigen_one(
            id BIGINT NOT NULL,
            url TEXT NOT NULL,
            views INT,
            created_at TEXT NOT NULL,
            scraped_at TEXT,
        )
    """
    await execute_raw_query(query)


async def kleinanzeigen_one_preferences():
    subcategories = KleinanzeigenOneUtilities.concatenate_subcategories()
    banwords = KleinanzeigenOneUtilities.concatenate_banwords()
    query = f"""
        CREATE TABLE IF NOT EXISTS kleinanzeigen_one_preferences(
            user_id BIGINT PRIMARY KEY,
            subcategories TEXT DEFAULT {subcategories},
            banwords TEXT DEFAULT {banwords},
            check_count SMALLINT 2,
            check_every SMALLINT DEFAULT 30,
            min_view_count SMALLINT DEFAULT 10,
            max_view_count SMALLINT DEFAULT 40,
            min_price_range SMALLINT DEFAULT 100,
            max_price_range SMALLINT DEFAULT 1000
        )
    """
    await execute_raw_query(query)


async def init_tables()
    await users()
    await kleinanzeigen_one()
    await kleinanzeigen_one_preferences()
