import sqlite3
import re

# ____load custom word list____
wordlist_file = "wordlist.txt"
with open(wordlist_file, "r", encoding="utf-8") as f:
    # normalize to lowercase and strip whitespace
    valid_words = set(w.strip().lower() for w in f if w.strip())

# ____connect to existing database____
con = sqlite3.connect('../crawler/crawl_data.db')
con.text_factory = bytes
cursor = con.cursor()

# delete old indexed_data if it exists
cursor.execute("DROP TABLE IF EXISTS indexed_data")

# create new tablesame schema as pages, but text will hold tokens found in wordlist.txt
cursor.execute("""
CREATE TABLE indexed_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    token TEXT
)
""")

# get rows from the pages table
cursor.execute("SELECT rowid, text FROM pages")
rows = cursor.fetchall()

for rowid, text in rows:
    try:
        decoded = text.decode("utf-8")
    except Exception:
        continue

    # split into candidate words
    words = re.findall(r'\b\w+\b', decoded.lower())

    # keep only those that are in your word list
    matched = [w for w in words if w in valid_words]

    # insert into new table
    cursor.executemany(
        "INSERT INTO indexed_data (page_id, token) VALUES (?, ?)",
        [(rowid, w) for w in matched]
    )

# commit and close
con.commit()
con.close()

print("database updated: tokens saved into 'indexed_data' table.")
