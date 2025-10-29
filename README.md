# toogle

## A custom search engine I'm making

Simple search engine complete with a web crawler and an indexer written in Go and Python, respectively. The crawler scans the web for various web pages and their data, and the indexer removes stopwords,
lemmetizes, and formats all of the data. It also has a search function built into the indexer at current. See [psuedocode](/pseudo.code) for more information on my plans for 
how the project works (and how it will work)

## Dependencies

Do note that on windows, it seems like you have to do some shenanigans with installing cgo (even though my project doesn't use it), so I'll try and fix that up soon

You will need an up-to-date installation of:

  [Go](https://go.dev/doc/install)

  [Python](https://python.org)

  [Git](https://github.com/git-guides/install-git)

  [SpaCy](https://spacy.io/)

  [SQLite3](https://docs.python.org/3/library/sqlite3.html)

  [sklearn](https://scikit-learn.org/)

  [Xcode devtools (mac only)](https://developer.apple.com/xcode/)
  
## How to run:

### ______LINUX, MAC OS & WINDOWS______
1. Git clone and cd into the crawler directory
2. Run ```go mod tidy```
4. Run ```go run crawler.go``` 
5. Cd into the indexer directory and run
     ```python indexer.py```


## Accesing the database

Do expect the crawler to take a while, it is literally scanning and saving descriptions and titles from every single website ever created. You can however stop it whenever
you want with Ctrl + C and it will have updated the database for the websites that have already been scanned

When running the indexer, as it is $$O(n)$$, the longer you run the crawler for, the longer the indexer will run for. After the indexer has finished indexing all the data, you will be prompted with an input,
asking what you would like to search, and it will search the indexed_data database for anything matching your input. It will give the link to all pages containing your word, and will display the respective
pages' tf-idf statistics. Currently, it provides the links in byte format (b'link'), but I need to work on seperating the indexer and query processor into two different programs before I do anything else.

Hope you enjoy!
