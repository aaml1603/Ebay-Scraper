import requests
from bs4 import BeautifulSoup
from icecream import ic
import json


product = input("Enter product name: ")
words = product.split()
args = "+".join(words)

url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1312&_nkw={args}&_sacat=0&_ipg=240"
data = {"items": []}
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")
items = soup.find_all("div", class_="s-item__wrapper clearfix")
for i in items:
    title = i.find("div", class_="s-item__title").text
    subtitle = i.find("div", class_="s-item__subtitle")
    image = i.find("img")
    item_link = i.find("a", class_="s-item__link").get("href")
    url = image.get("src")
    if subtitle:
        try:
            sub_text = subtitle.find("span", class_="SECONDARY_INFO").text
        except Exception:
            sub_text = subtitle.text
    else:
        sub_text = "N/A"
    price = i.find("span", class_="s-item__price").text
    data["items"].append(
        {
            "title": title,
            "sub_text": sub_text,
            "image_url": url,
            "price": price,
            "item_link": item_link,
        }
    )
    with open("ebay_dump.json", "w") as f:
        dump = json.dumps(data, indent=4)
        f.write(dump)
