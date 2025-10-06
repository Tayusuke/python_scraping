import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

base_url = "http://books.toscrape.com/"
url = base_url

all_books =[]

count = 0

while url and count <= 3:
    res = requests.get(url, headers=head)
    soup = BeautifulSoup(res.text, "html.parser")
    for article in soup.select(".product_pod"):
        title = article.h3.a["title"]
        price = article.select_one(".price_color").text.strip()
        detail_url = urljoin(url, article.h3.a["href"])

        detail_res = requests.get(detail_url, headers=head)
        detail_soup = BeautifulSoup(detail_res.text, "html.parser")

        desc_tag = detail_soup.select_one("#product_description ~ p")
        description = desc_tag.text.strip() if desc_tag else "説明なし"

        category = detail_soup.select("ul.breadcrumb li a")[-1].text.strip()

        img_tag = detail_soup.select_one(".item.active img")
        img_url = urljoin(detail_url, img_tag["src"]) if img_tag else "なし"

        all_books.append((title,str(price).replace("Â£", ""),category,description,img_url))

    next_link = soup.select_one("li.next a")
    url = urljoin(url, next_link["href"]) if next_link else None
    count += 1

with open("detailed_books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["タイトル", "値", "カテゴリー", "説明", "画像"])
    for title, price, category, description, image in all_books[:50]:
        writer.writerow([title, price, category, description, image])