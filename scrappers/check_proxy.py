import httpx
from selectolax.parser import HTMLParser

url = "https://www.kleinanzeigen.de/s-haus-garten/anbieter:privat/anzeige:angebote/versand:ja/preis:100:/seite:26/c80"
proxy = "http://grib:work7315@185.241.150.134:50100"

response = httpx.get(url, proxy=proxy)

print(response.text)
print(response.status_code)

tree = HTMLParser(response.text)

domain = "https://www.kleinanzeigen.de"
urls = []
for url in tree.css("article"):
    item_id = int(url.attrs.get("data-adid", ""))
    item_url = domain + url.attrs.get("data-href", "")
    urls.append([item_id, item_url])

print(urls)
