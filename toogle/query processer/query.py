import sqlite3
import spacy

nlp = spacy.load("en_core_web_sm")

DB_PATH = "../crawler/crawl_data.db"

def to_lemma(text):  # define lemmatization function
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

def search(processed_text):
    # search
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT page_id FROM indexed_data WHERE indexed_data MATCH ?;", (processed_text,))
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

def get_urls(matching_ids):
    # return urls
    if not matching_ids:
        return []
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    placeholders = ",".join("?" for _ in matching_ids)
    cursor.execute(f"SELECT url FROM pages WHERE rowid IN ({placeholders})", tuple(matching_ids))
    urls = [row[0] for row in cursor.fetchall()]
    conn.close()
    return urls

if __name__ == "__main__":
    while True:
        try:
            query = input("\nEnter a search term (Ctrl+C to quit): ").strip().lower()
        except KeyboardInterrupt:
            print("\nThanks for using toogle!")
            break

        if not query:
            continue

        processed = to_lemma(query)
        ids = search(processed)
        urls = get_urls(ids)

        if not urls:
            print(f"No pages found containing '{query}'.")
        else:
            print("\nMatching URLs:")
            for url in urls:
                print("  ", url)
