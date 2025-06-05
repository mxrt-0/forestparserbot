import asyncio
from aiohttp import TCPConnector, ClientSession
from aiolimiter import AsyncLimiter
from utils import fetch_data, get_time_ago, get_local_time, PROXIES
from db import init_pool, close_pool, fetch_db_data, execute_db_query


proxies = PROXIES[6:9]
print(proxies)


async def rechecked_hour_later(limiter, session):
    try:
        query = """
            SELECT id
            FROM kleinanzeigen
            WHERE scraped_at <= $1
            AND views_hour_later IS NULL; 
        """
        hour_ago = get_time_ago(1)
        data = await fetch_db_data(query, (hour_ago,), target="all")
    except Exception as e:
        print(f"Unexpected database error ocurred: {e}")

    if data:
        tasks = []
        for i, row in enumerate(data):
            id = row[0]
            proxy = proxies[i % len(proxies)]
            url = f"https://www.kleinanzeigen.de/s-vac-inc-get.json?adId={id}"
            task = asyncio.create_task(fetch_data(limiter, session, url, proxy=proxy, id=id, data_type="json"))
            tasks.append(task)


        data_hour_later = []
        responses = await asyncio.gather(*tasks)
        for i, response in enumerate(responses):
            try:
                if response is None:
                    continue
                id, json_data = response 
                views_hour_later = json_data.get("numVisits", 0)
                rechecked_hour_later = get_local_time("Europe/Berlin")
                item = (id, views_hour_later, rechecked_hour_later)
                data_hour_later.append(item)
            except Exception as e:
                print(f"Unexpected error occured while rechecked views hour later: {e}")
                continue
        try:
            query = """
                UPDATE kleinanzeigen
                SET views_hour_later = $2, rechecked_hour_later = $3
                WHERE id = $1;
            """
            await execute_db_query(query, data_hour_later, target="many")
        except Exception as e:
            print(f"Unexpected database error ocurred: {e}")
        

async def rechecked_two_later(limiter, session):
    try:
        query = """
            SELECT id
            FROM kleinanzeigen
            WHERE rechecked_hour_later <= $1
            AND views_two_later IS NULL;
        """
        hour_ago = get_time_ago(1)
        data = await fetch_db_data(query, (hour_ago,), target="all")
    except Exception as e:
        print(f"Unexpected database error ocurred: {e}")

    if data:
        tasks = []
        for i, row in enumerate(data):
            id = row[0]
            proxy = proxies[i % len(proxies)]
            url = f"https://www.kleinanzeigen.de/s-vac-inc-get.json?adId={id}"
            task = asyncio.create_task(fetch_data(limiter, session, url, proxy=proxy, id=id, data_type="json"))
            tasks.append(task)

        data_two_later = []
        responses = await asyncio.gather(*tasks)
        for i, response in enumerate(responses):
            try:
                if response is None:
                    continue
                id, json_data = response 
                views_two_later = json_data.get("numVisits", 0)
                rechecked_two_later = get_local_time("Europe/Berlin")
                item = (id, views_two_later, rechecked_two_later)
                data_two_later.append(item)
            except Exception as e:
                print(f"Unexpected error occured while rechecked views hour later: {e}")
                continue
        try:
            query = """
                UPDATE kleinanzeigen
                SET views_two_later = $2, rechecked_two_later = $3
                WHERE id = $1;
            """
            await execute_db_query(query, data_two_later, target="many")
        except Exception as e:
            print(f"Unexpected database error ocurred: {e}")


async def main():
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15"
    headers = { "user-agent": ua }
    limiter = AsyncLimiter(len(proxies)*5, 1)
    connector = TCPConnector(ssl=False)
    async with ClientSession(
        connector=connector,
        headers=headers
    ) as session:
        await init_pool()
        await rechecked_hour_later(limiter, session)
        await rechecked_two_later(limiter, session)
        await close_pool()


async def main_loop():
    while True:
        await main()
        await asyncio.sleep(10)

asyncio.run(main_loop())
