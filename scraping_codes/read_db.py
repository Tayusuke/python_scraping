import sqlite3

conn = sqlite3.connect("books.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM books ORDER BY price DESC")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.commit()
conn.close()