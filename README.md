# toogle

## A custom search engine I'm making

Currently, it is just a web crawler and a wip indexer written in goand python, but see the [psuedocode](/pseudo.code) for more information on my plans for how the project works (and how it will work)
I am using an edited version of this [list of words](https://github.com/dwyl/english-words/blob/master/words.txt) with stopwords removed so that my indexer can sort through different words 

## Dependencies

You will need an up-to-date installation of:

  [Go](https://go.dev/doc/install)

  [Git](https://github.com/git-guides/install-git)
  
  [Python](https://python.org) 

## How to run:

### ______LINUX & MAC OS______
1. Git clone and cd into the new directory
2. Run ```make```
3. Cd into the crawler dir and run ```go run crawler.go```
4. Cd into the indexer dir and run ```python indexer.py```
5. And you're done!

## Accesing and viewing the databases

Do expect the crawler to take a while, it is literally scanning and saving descriptions and titles from every single website ever created. You can, however stop it whenever you want with Ctrl + C and it will have updated the database for the websites that have already been scanned

The data will be stored in a SQLite 3 database named crawl_data.db, and it can be viewed through any SQlite gui, but I prefer to use [SQLiteStudio](https://sqlitestudio.pl/). The data can be viweed by:
1. First pressing database up the top of SQLiteStudio, and pressing add a database.
2. Then ensure these options are selected, with the file area being the location of your crawl_data.db file:
   
   ![SQLiteStudio add a database screen](https://raw.githubusercontent.com/i-love-winter/toogle/refs/heads/main/add%20a%20database.png)
3. Hit okay, then click the down arrows in the bar on the left until you get to tables
4. Select which table you want to view
5. Then select data, and you can browse all the data that you have crawled and tokenized!
6. Good job!

