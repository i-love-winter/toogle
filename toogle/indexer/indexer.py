import sqlite3 # database handling
import re # regular expressions
import spacy # lemmetization

# ____load custom word list____
wordlist_file = "wordlist.txt"
with open(wordlist_file, "r", encoding="utf-8") as f:
    # normalize to lowercase and strip whitespace
    valid_words = set(w.strip().lower() for w in f if w.strip())

# ____connect to existing database____
con = sqlite3.connect('../crawler/crawl_data.db')
con.text_factory = bytes
cursor = con.cursor()

# ____create new table to be indexed____

# delete old indexed_data if it exists
cursor.execute("DROP TABLE IF EXISTS indexed_data")

# create table same as pages, but text will be indexed
cursor.execute("""
CREATE TABLE indexed_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    token TEXT
)
""")

# ____stopword removal and tokenization____

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

    # keep only those that are in wordlist.txt
    matched = [w for w in words if w in valid_words]

    # insert into new table
    cursor.executemany(
        "INSERT INTO indexed_data (page_id, token) VALUES (?, ?)",
        [(rowid, w) for w in matched]
    )


# ________lemmetization_______

# load the english model to know what to lemmetize into
nlp = spacy.load("en_core_web_sm")

# find text row to lemmetize
cursor.execute("SELECT token FROM indexed_data WHERE rowid=?", (1,))
row = cursor.fetchone()

if row:
    text = row[0]
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    # lemmetize
    doc = nlp(text)
    lemmetized_text = " ".join([token.lemma_ for token in doc])
    # update rows
    cursor.execute("UPDATE indexed_data SET token=? WHERE rowid=?", (lemmetized_text, 1))

# commit and close
con.commit()
con.close()

print("database updated - tokens saved into new indexed_data table.")

