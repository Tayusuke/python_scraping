import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

url = "https://ja.wikipedia.org/wiki/%E6%98%9F%E5%BA%A7"
res = requests.get(url, headers=head)

howmany = 0

stars = []

if res.status_code == 200:
    print("OK")
    
    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.find_all("table", {"class": "wikitable"})

    for table in tables:
        for td in table.find_all("td"):
            a_tag = td.find("a")
            if td.find("span"):
                continue
            if a_tag and a_tag.get("href"):
                name = a_tag.text
                link = urljoin(url, a_tag.get("href"))
                print(name, link)
                stars.append((name, link))
                howmany += 1
else:
    print("Error")
    print(res.status_code)

print(howmany)

with open("stars.csv", "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["名前", "リンク"])
                    for name, link in stars:
                        writer.writerow([name, link])