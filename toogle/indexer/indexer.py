import sqlite3

# connect to the database
con = sqlite3.connect('../crawler/crawl_data.db')
cursor = con.cursor()

# find all accounts of the word 'aggregated' in all pages and print results
cursor.execute("SELECT * FROM pages WHERE text = ?", ('aggregated',))
print(cursor.fetchall())

