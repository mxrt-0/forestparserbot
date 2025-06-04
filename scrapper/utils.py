import asyncio 
import aiohttp
from datetime import datetime, timedelta 
from zoneinfo import ZoneInfo


PROXIES = [
    "http://ZANzID:Ba2nnIRrva@45.11.21.40:5500",
    "http://ZANzID:Ba2nnIRrva@45.11.21.61:5500",
    "http://ZANzID:Ba2nnIRrva@45.11.21.229:5500",
    "http://ZANzID:Ba2nnIRrva@45.11.21.233:5500",
    "http://ZANzID:Ba2nnIRrva@45.11.21.237:5500",
    "http://ZANzID:Ba2nnIRrva@45.11.21.239:5500",
    "http://ZANzID:Ba2nnIRrva@45.11.21.245:5500",
    "http://ZANzID:Ba2nnIRrva@45.15.72.3:5500",
    "http://ZANzID:Ba2nnIRrva@45.15.72.27:5500",
    "http://ZANzID:Ba2nnIRrva@45.15.72.36:5500"
]


def urls_generator():
    min_price = 100
    stock_urls = [
        # Auto, Rad & Boot
        "https://www.kleinanzeigen.de/s-auto-rad-boot/anbieter:privat/versand:ja/preis:{min_price}:/seite:{page_count}/c210",
        # Eintrittskarten & Tickets 
        "https://www.kleinanzeigen.de/s-eintrittskarten-tickets/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c231",
        # Elektronik
        "https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c161",
        # Familie, Kind & Baby
        "https://www.kleinanzeigen.de/s-familie-kind-baby/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c17",
        # Freizeit, Hobby & Nachbarschaft
        "https://www.kleinanzeigen.de/s-freizeit-nachbarschaft/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c185",
        # Haus & Garten "https://www.kleinanzeigen.de/s-haus-garten/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c80",
        # Haustiere
        "https://www.kleinanzeigen.de/s-haustiere/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c130",
        # Mode & Beauty
        "https://www.kleinanzeigen.de/s-mode-beauty/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c153",
        # Musik, Filme & Bücher 
        "https://www.kleinanzeigen.de/s-musik-film-buecher/anbieter:privat/anzeige:angebote/versand:ja/preis:{min_price}:/seite:{page_count}/c73",
    ]
    urls = []

    for page_count in range(1, 51):
        for url in stock_urls:
            formatted_url = url.format(min_price=min_price, page_count=page_count)
            urls.append(formatted_url)

    return urls


def get_local_time(timezone: str):
    current_time = datetime.now(ZoneInfo(timezone))
    return current_time.strftime("%Y-%m-%d %H:%M:%S")


def get_time_ago(hours: int, timezone: str = "Europe/Berlin"):
    current_time = get_local_time(timezone)
    current_formatted_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    time_ago = current_formatted_time - timedelta(hours=hours)
    return time_ago.strftime("%Y-%m-%d %H:%M:%S")

timeout = aiohttp.ClientTimeout(total=20)
async def fetch_data(limiter, session, url, proxy=None, id=None, retries=3, backoff_time=2, timeout=20, data_type="text"):
    while retries > 0:
        try:
            async with limiter:
                async with session.get(url, proxy=proxy, timeout=timeout) as response:
                    print(f"status: {response.status}")
                    if response.status == 200:
                        if data_type == "json":
                            return id, await response.json()
                        if id:
                            return id, await response.json()
                        return await response.text()
                    elif response.status == 404:
                        continue
                    else:
                        print(f"Unexpected status {response.status} for {url}")
                        print(await response.text())
        except aiohttp.ClientProxyConnectionError as e:
            print(f"Proxy connection error: {e}")
            print("Sleep 15 seconds")
            await asyncio.sleep(15)
        except aiohttp.ClientHttpProxyError as e:
            print(f"HTTP proxy error: {e}")
            print("Sleep 15 seconds")
            await asyncio.sleep(15)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            retries -= 1
            if retries > 0:
                await asyncio.sleep(backoff_time)
                backoff_time *= 2
            print(f"Failed to fetch {url} after retries.")
            continue

main_urls = ['https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:1/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:2/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:3/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:4/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:5/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:6/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:7/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:8/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:9/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:10/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:11/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:12/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:13/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:14/c161', 'https://www.kleinanzeigen.de/s-multimedia-elektronik/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:15/c161', 'https://www.kleinanzeigen.de/s-freizeit-nachbarschaft/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:1/c185', 'https://www.kleinanzeigen.de/s-musik-film-buecher/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:1/c73', 'https://www.kleinanzeigen.de/s-heimwerken/anbieter:privat/anzeige:angebote/preis:300:3000/seite:1/c84+heimwerken.versand_s:ja', 'https://www.kleinanzeigen.de/s-fahrraeder/anbieter:privat/anzeige:angebote/preis:300:3000/seite:1/c217+fahrraeder.versand_s:ja', 'https://www.kleinanzeigen.de/s-freizeit-nachbarschaft/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:2/c185', 'https://www.kleinanzeigen.de/s-musik-film-buecher/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:2/c73', 'https://www.kleinanzeigen.de/s-heimwerken/anbieter:privat/anzeige:angebote/preis:300:3000/seite:2/c84+heimwerken.versand_s:ja', 'https://www.kleinanzeigen.de/s-fahrraeder/anbieter:privat/anzeige:angebote/preis:300:3000/seite:2/c217+fahrraeder.versand_s:ja', 'https://www.kleinanzeigen.de/s-freizeit-nachbarschaft/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:3/c185', 'https://www.kleinanzeigen.de/s-musik-film-buecher/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:3/c73', 'https://www.kleinanzeigen.de/s-heimwerken/anbieter:privat/anzeige:angebote/preis:300:3000/seite:3/c84+heimwerken.versand_s:ja', 'https://www.kleinanzeigen.de/s-fahrraeder/anbieter:privat/anzeige:angebote/preis:300:3000/seite:3/c217+fahrraeder.versand_s:ja', 'https://www.kleinanzeigen.de/s-freizeit-nachbarschaft/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:4/c185', 'https://www.kleinanzeigen.de/s-musik-film-buecher/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:4/c73', 'https://www.kleinanzeigen.de/s-heimwerken/anbieter:privat/anzeige:angebote/preis:300:3000/seite:4/c84+heimwerken.versand_s:ja', 'https://www.kleinanzeigen.de/s-fahrraeder/anbieter:privat/anzeige:angebote/preis:300:3000/seite:4/c217+fahrraeder.versand_s:ja', 'https://www.kleinanzeigen.de/s-freizeit-nachbarschaft/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:5/c185', 'https://www.kleinanzeigen.de/s-musik-film-buecher/anbieter:privat/anzeige:angebote/versand:ja/preis:300:3000/seite:5/c73', 'https://www.kleinanzeigen.de/s-heimwerken/anbieter:privat/anzeige:angebote/preis:300:3000/seite:5/c84+heimwerken.versand_s:ja', 'https://www.kleinanzeigen.de/s-fahrraeder/anbieter:privat/anzeige:angebote/preis:300:3000/seite:5/c217+fahrraeder.versand_s:ja']
