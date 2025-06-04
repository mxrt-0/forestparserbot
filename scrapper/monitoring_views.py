import asyncio
from aiohttp import TCPConnector, ClientSession
from aiolimiter import AsyncLimiter
from utils import fetch_data, get_local_time, PROXIES
from db import init_pool, close_pool, fetch_db_data, execute_db_query

proxies = PROXIES[3:6]
print(proxies)

async def fetch_views(limiter, session):
    try:
        query = """
            SELECT id
            FROM kleinanzeigen
            WHERE views IS NULL;
        """
        data = await fetch_db_data(query, target="all")
    except Exception as e:
        print(f"Unexpected database error ocured: {e}")

    if data:
        tasks = []
        for i, row in enumerate(data):
            id = row[0]
            proxy = proxies[i % len(proxies)]
            url = f"https://www.kleinanzeigen.de/s-vac-inc-get.json?adId={id}"
            task = asyncio.create_task(fetch_data(limiter, session, url, proxy=proxy, id=id, data_type="json"))
            tasks.append(task)

        data_w_views = []
        responses = await asyncio.gather(*tasks)
        for i, response in enumerate(responses):
            try:
                if response is None:
                    continue
                id, json_data = response
                views = json_data.get("numVisits", 0)
                scraped_at = get_local_time("Europe/Berlin")
                item = (id, views, scraped_at)
                data_w_views.append(item)
            except Exception as e:
                print(f"Unexpected error occured while scraping views: {e}")
                continue
        try:
            query = """
                UPDATE kleinanzeigen
                SET views = $2, scraped_at = $3
                WHERE id = $1;
            """
            await execute_db_query(query, data_w_views, target="many")
        except Exception as e:
            print(f"Unexpected database error occured: {e}")


async def main():
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.1"
    headers = { "user-agent": ua }
    limiter = AsyncLimiter(len(proxies)*5, 1)
    connector = TCPConnector(ssl=False)
    async with ClientSession(
        connector=connector,
        headers=headers
    ) as session: 
        await init_pool() 
        await fetch_views(limiter, session)
        await close_pool()


async def main_loop():
    while True:
        await main()
        await asyncio.sleep(10)
asyncio.run(main_loop())
