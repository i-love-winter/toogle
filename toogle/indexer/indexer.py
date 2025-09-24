print(f"\033[1;95m ROW_N0 | NUMBER OF OCCURENCES ") # print a sort of legend
time.sleep(5) # wait to allow user to see legend

con = sqlite3.connect('../crawler/crawl_data.db')
con.text_factory = bytes   # fetch TEXT as raw bytes
cursor = con.cursor()

cursor.execute("SELECT rowid, text FROM pages")
rows = cursor.fetchall()

search_word = b"test"  # bytes now

for rowid, text in rows:
    try:
        decoded = text.decode("utf-8")  # try to decode
    except Exception:
        continue  # skip rows that aren’t valid UTF-8

    count = decoded.lower().count(search_word.decode().lower())
    if count > 0:
        # \033[1m = bold, \033[95m = purple, \033[0m = reset
        print(f"\033[1;95m{rowid}\033[0m) {count}")
