import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS books")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,                            
    price REAL,                            
    stock TEXT                             
)
""")

import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/catalogue/page-1.html"
res = requests.get(url)
res.encoding = res.apparent_encoding
soup = BeautifulSoup(res.text, "html.parser")

books = []

for article in soup.select(".product_pod"):
    title = article.h3.a["title"]
    price = article.select_one(".price_color").text.strip()
    stock = article.select_one(".instock.availability").text.strip()
    books.append((title, str(price).replace("£", ""), stock))

cursor.executemany("INSERT INTO books (title, price, stock) VALUES (?, ?, ?)", books)

conn.commit()
conn.close()