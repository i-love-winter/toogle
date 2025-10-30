import sqlite3 # database handling
import re # regular expressions
import spacy # lemmetization

def to_lemma(text): # define lemmetization function
    tp = nlp(text)
    processed_text = ""
    for word in tp:
        processed_text = processed_text + word.lemma_ + " "
    return processed_text

# ____load custom word list____
wordlist_file = "wordlist.txt"
with open(wordlist_file, "r", encoding="utf-8") as f:
    # normalize to lowercase and strip
    valid_words = set(w.strip().lower() for w in f if w.strip())

# ____connect to existing database____
con = sqlite3.connect('../crawler/crawl_data.db')
con.text_factory = bytes
cursor = con.cursor()

# ____create new table to be indexed____
cursor.execute("DROP TABLE IF EXISTS indexed_data")
cursor.execute("""
CREATE VIRTUAL TABLE indexed_data USING fts5(page_id UNINDEXED, token)
""")

# ________preprocessing_______

# get rows from the pages table
cursor.execute("SELECT rowid, text FROM pages")
rows = cursor.fetchall()

# load spacy model
nlp = spacy.load("en_core_web_sm")

for rowid, text in rows:
    try:
        decoded = text.decode("utf-8")
    except Exception:
        continue

    # split into candidate words
    words = re.findall(r'\b\w+\b', decoded.lower())

    # keep only those that are in wordlist.txt
    filtered_words = [w for w in words if w in valid_words]

    # lemmatize the filtered words
    lemma_str = to_lemma(" ".join(filtered_words))

    # insert into indexed_data table
    cursor.execute(
        "INSERT INTO indexed_data (page_id, token) VALUES (?, ?)",
        (rowid, lemma_str)
    )

# ________searching indexed_data with tf-idf________

documents = []
page_ids = []

for rowid, text in rows:
    ...
    documents.append(lemma_str)
    page_ids.append(rowid)

from sklearn.feature_extraction.text import TfidfVectorizer # tf-idf

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

search_query = input("Enter a word to search for: ").strip().lower()

processed_text = to_lemma(search_query)

cursor.execute("""
SELECT page_id FROM indexed_data WHERE indexed_data MATCH ?;
""", (processed_text,))
matching_rows = cursor.fetchall()
matching_ids = list(row[0] for row in matching_rows)

# return urls corresponding to those ids
if matching_ids:
    placeholders = ",".join("?" for _ in matching_ids)
    cursor.execute(
        f"SELECT url FROM pages WHERE rowid IN ({placeholders})",
        tuple(matching_ids)   # convert set → tuple
    )
    url_rows = cursor.fetchall()

    for (url,) in url_rows:
        print(url)
else:
    print(f"\nNo pages found containing the word {search_query}.")

feature_names = vectorizer.get_feature_names_out()

for doc_index, page_id in enumerate(page_ids):
    if page_id in matching_ids:
        row = tfidf_matrix.getrow(doc_index)
        scores = zip(row.indices, row.data)
        print(f"\nTF-IDF scores for page_id {page_id}:")
        for token_index, score in scores:
            token = feature_names[token_index]
            print(f"  {token}: {score:.4f}")


# commit and close
con.commit()
con.close()
