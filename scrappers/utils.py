import aiofiles
import asyncio

HTTP = "http://"
SOCKS5 = "socks5://"


async def proxy_list(file_path="./scrappers/proxies.txt", proxies_type="http"):
    proxies = []
    async with aiofiles.open(file_path, mode="r") as f:
        async for line in f:
            proxy = line.strip()
            if proxy:
                if proxies_type == "socks5":
                    prefix = SOCKS5
                else:
                    prefix = HTTP
                proxies.append(prefix + line)
    return proxies
