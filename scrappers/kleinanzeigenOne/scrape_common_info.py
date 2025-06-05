import asyncio
from aiohttp import TCPConnector, ClientSession
from aiolimiter import AsyncLimiter
from selectolax.parser import HTMLParser

from scrappers.kleinanzeigenOne.utils import fetch_raw_data, urls_generator
from scrappers.utils import proxy_list
from bot.database.database import execute_raw_query, fetch_raw_data


async def fetch_urls(urls, limiter, session, proxies):
    tasks = []
    for i, url in enumerate(urls):
        proxy = proxies[i % len(proxies)]
        task = asyncio.create_task(fetch_raw_data(limiter, session, url, proxy=proxy))
        tasks.append(task)
    htmls = await asyncio.gather(*tasks)
    return htmls


async def scrape_urls(urls, limiter, session, proxies):
    htmls = fetch_urls(urls, limiter, session, proxies)
    domain = "https://www.kleinanzeigen.de"

    links = []
    created_at = []
    cards_info = []
    for html in htmls:
        try:
            if html is None:
                continue
            tree = HTMLParser(html)
            for link in tree.css("article"):
                id = int(link.attrs.get("data-adid", ""))
                url = domain + link.attrs.get("data-href", "")
                links.append([id, url])
            for time in tree.css("div.aditem-main--top--right"):
                card_created_at = time.text(strip=True)
                created_at.append(card_created_at)
        except Exception as e:
            print(f"Unexpected error ocurred while scraping page: {e}")
            continue

        for i in range(len(created_at)):
            try:
                if created_at[i] != "" and "Heute" in created_at[i]:
                    cards_info.append((links[i][0], links[i][1], created_at[i]))
            except Exception as e:
                print(f"Unexpected error ocurred while deleting pushed cards: {e}")
                continue
        try:
            query = """
                INSERT INTO kleinanzeigenOne(id, url, scraped_at)
                VALUES($1, $2, $3)
                ON CONFLICT (id) DO NOTHING;
            """
            await execute_raw_query(query, values=cards_info, target="many")
        except Exception as e:
            print(f"Unexpected database error ocurred: {e}")


async def fetch_views(limiter, session, proxies):
    cards_info = None
    try:
        query = """
            SELECT id
            FROM kleinanzeigenOne
            WHERE views IS NULL;
        """
        cards_info = await fetch_raw_data(query, target="all")
    except Exception as e:
        print(
            "Unexpected database error ocured "
            f"while fetching instances without views: {e}"
        )

    if cards_info:
        tasks = []
        views_url = "https://www.kleinanzeigen.de/s-vac-inc-get.json?adId={id}"
        for i, card_id in enumerate(cards_info):
            proxy = proxies[i % len(proxies)]
            task = asyncio.create_task(
                fetch_raw_data(
                    limiter,
                    session,
                    views_url.format(id=card_id[0]),
                    proxy=proxy,
                    id=card_id[0],
                    data_type="json",
                )
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
    return responses


async def scrape_views(proxies, limiter, session):
        responses = await  fetch_views(proxies, limiter, session)
        cards_w_views = []
        for i, response in enumerate(responses):
            try:
                if response is None:
                    continue
                id, json_data = response
                views = json_data.get("numVisits", 0)
                scraped_at = get_local_time("Europe/Berlin")
                cards_w_views.append((id, views, scraped_at))
            except Exception as e:
                print(f"Unexpected error occured while scraping views: {e}")
                continue
        try:
            query = """
                UPDATE kleinanzeigenOne
                SET views = $2, scraped_at = $3
                WHERE id = $1;
            """
            await execute_raw_query(query, values=cards_w_views, target="many")
        except Exception as e:
            print(f"Unexpected database error occured: {e}")


async def main_loop():
    proxies = proxy_list[0:11]
    ua = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.3"
    )
    headers = {"user-agent": ua}
    limiter = AsyncLimiter(len(proxies) * 5, 1)
    connector = TCPConnector(ssl=False)
    urls = urls_generator()
    iterations_delay = 30

    async with ClientSession(connector=connector, headers=headers) as session:
        while True:
            await asyncio.gather(
                scrape_urls(urls, proxies, limiter, session)
                scrape_views(proxies, limiter, session)
            )
            await asyncio.sleep(iterations_delay)
