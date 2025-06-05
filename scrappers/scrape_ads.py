import asyncio
from aiohttp import TCPConnector, ClientSession
from aiolimiter import AsyncLimiter
from selectolax.parser import HTMLParser
from utils import fetch_data, get_local_time, PROXIES
from db import init_pool, close_pool, fetch_db_data, execute_db_query


proxies = PROXIES[9:10]
print(proxies)

async def scrape_ads(limiter, session):
    try:
        query = """
            SELECT * 
            FROM kleinanzeigen
            WHERE views_hour_later - views >= 10
            AND views_two_later - views_hour_later >= 10;
        """
        data = await fetch_db_data(query, target="all")
    except Exception as e:
        print(f"Unexpected database error ocurred: {e}")
           
    if data:
        tasks = []
        urls = [url[1] for url in data]
        for i, url in enumerate(urls):
            proxy = proxies[i % len(proxies)]
            task = asyncio.create_task(fetch_data(limiter, session, url, proxy=proxy))
            tasks.append(task)


        items = []
        htmls = await asyncio.gather(*tasks)
        for i, html in enumerate(htmls):
            try:
                if html is None:
                    continue
                tree = HTMLParser(html)
                if tree.css("#viewad-features"): #Top pushed items
                    continue
                if tree.css("p.boxedarticle--old-price"): #Top down price 
                    continue
                title = tree.css_first("#viewad-title").text(strip=True)
                price = tree.css_first("#viewad-price").text(strip=True)
                if tree.css_first("#viewad-image"):
                    image = tree.css_first("#viewad-image").attrs.get("src", "")
                else:
                    image = "No image"
                description = tree.css_first("#viewad-description-text").text(strip=True)
                undercategory = tree.css_first("a.breadcrump-link:nth-child(3) > span:nth-child(1)").text(strip=True)

                item = (data[i][0], data[i][1], data[i][2], data[i][3], 
                        data[i][4], data[i][5], data[i][6], data[i][7], 
                        data[i][8], title, price, image, description, undercategory)
                items.append(item)
            except Exception as e:
                print(f"Unexpected error ocurred: {e}")
                continue
        try:
            if items:
                first_query = """
                    INSERT INTO results(
                        id, url, publication_time, views, scraped_at, 
                        views_hour_later, rechecked_hour_later, views_two_later, 
                        rechecked_two_later, title, price, image, description, undercategory
                    )
                    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                    ON CONFLICT (id) DO NOTHING;
                """
                await execute_db_query(first_query, items, target="many")

                second_query = """
                    INSERT INTO telegram_bot(
                        id, url, publication_time, views, scraped_at, 
                        views_hour_later, rechecked_hour_later, views_two_later, 
                        rechecked_two_later, title, price, image, description, undercategory
                    )
                    VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                    ON CONFLICT (id) DO NOTHING;
                """
                await execute_db_query(second_query, items, target="many")
                
                third_query = """
                    DELETE 
                    FROM kleinanzeigen
                    WHERE id = $1
                """
                ids_to_delete = [(id[0],) for id in items]
                await execute_db_query(third_query, ids_to_delete, target="many")
            
        except Exception as e:
            print(f"Unexpected database error ocurred: {e}")


async def main():
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15"
    headers = { "user-agent": ua }
    limiter = AsyncLimiter(len(proxies)*1, 1)
    connector = TCPConnector(ssl=False)
    async with ClientSession(
        connector=connector,
        headers=headers
    ) as session:
        await init_pool()
        await scrape_ads(limiter, session)
        await close_pool()


async def main_loop():
    while True:
        await main()
        print("sleep 10")
        await asyncio.sleep(20)

asyncio.run(main_loop())
