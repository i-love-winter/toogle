# toogle

## A custom search engine I'm making

Simple search engine complete with a web crawler and an indexer written in Go and Python, respectively. The crawler scans the web for various web pages and their data, and the indexer removes stopwords,
lemmetizes, and formats all of the data. There is also a query processor with a search function with synonym expansion and lemmetization. See [psuedocode](/pseudo.code) for more information on my plans for 
how the project works (and how it will work). 

Do note that it only runs on python 3.7 to 3.12

## Dependencies

You will need an up-to-date installation of:

  [NLTK](https://www.nltk.org/install.html)

  [Go](https://go.dev/doc/install)

  [Python](https://python.org)

  [Git](https://github.com/git-guides/install-git)

  [SpaCy](https://spacy.io/)

  [SQLite3](https://docs.python.org/3/library/sqlite3.html)

  [sklearn](https://scikit-learn.org/)

  [Xcode devtools (mac only)](https://developer.apple.com/xcode/)

  Note that after installing nltk, you will need to run ```nltk.download('wordnet')``` to install wordnet
  
## How to run:

### ______LINUX, MAC OS & WINDOWS______
1. Git clone and cd into the crawler directory
2. Run ```go mod tidy```
4. Run ```go run crawler.go``` 
5. Cd into the indexer directory and run
     ```python indexer.py```
6. Cd into the query processor directory and run
     ```python query.py```


## Accesing the database

Do expect the crawler to take a while, it is literally scanning and saving descriptions and titles from every single website ever created. You can however stop it whenever
you want with Ctrl + C and it will have updated the database for the websites that have already been scanned

When running the indexer, as it is $$O(n)$$, the longer you run the crawler for, the longer the indexer will run for. 

Hope you enjoy!
