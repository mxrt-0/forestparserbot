import asyncio
from aiohttp import TCPConnector, ClientSession 
from aiolimiter import AsyncLimiter
from selectolax.parser import HTMLParser
from utils import fetch_data, urls_generator, PROXIES
from db import init_pool, close_pool, execute_db_query


proxies = PROXIES[0:3]
print(proxies)


async def monitoring_urls(limiter, session): 
    main_urls = urls_generator()
    tasks = []
    for i, url in enumerate(main_urls):
        proxy = proxies[i % len(proxies)]
        task = asyncio.create_task(fetch_data(limiter, session, url, proxy=proxy))
        tasks.append(task)
    htmls = await asyncio.gather(*tasks)

    urls = []
    publication_times = []
    domain = "https://www.kleinanzeigen.de"
    
    for html in htmls:
        try:
            if html is None:
                continue
            tree = HTMLParser(html)
            for url in tree.css("article"):
                item_id = int(url.attrs.get("data-adid", ""))
                item_url = domain + url.attrs.get("data-href", "")
                urls.append([item_id, item_url])

            for time in tree.css("div.aditem-main--top--right"):
                item_publication_time = time.text(strip=True)
                publication_times.append(item_publication_time)
        except Exception as e:
            print(f"Unexpected error ocurred while scrape page: {e}")
            continue 

        data = []
        for i in range(len(urls)):
            if publication_times[i] != "" and "Heute" in publication_times[i]:
                data.append((urls[i][0], urls[i][1], publication_times[i]))

        try:
            query = """
                INSERT INTO kleinanzeigen(id, url, publication_time) 
                VALUES($1, $2, $3)
                ON CONFLICT (id) DO NOTHING;
            """ 
            await execute_db_query(query, params=data, target="many")
        except Exception as e:
            print(f"Unexpected database error ocurred: {e}")


async def main():
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3"
    headers = { "user-agent": ua }
    limiter = AsyncLimiter(len(proxies)*5, 1)
    connector = TCPConnector(ssl=False)
    async with ClientSession(
        connector=connector, 
        headers=headers
    ) as session:
        await init_pool()
        await monitoring_urls(limiter, session)
        await close_pool()

async def main_loop(): 
    while True:
        await main()
        await asyncio.sleep(20)
        

asyncio.run(main_loop())
