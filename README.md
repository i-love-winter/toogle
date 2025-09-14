# toogle

## A custom search engine I'm making :p

Currently, it is just a web crawler written in go, but see the [psuedocode](/psuedo.code) for more information on my plans for how the project works (and how it will work)

## Dependencies

You will need an up-to-date installation of:
  [Go](https://go.dev/doc/install)
  [Git](https://github.com/git-guides/install-git)

## How to run:

### ______LINUX & MAC OS______
1. Git clone and cd into the directory and the directory inside
2. Run ```make```
3. Run ```go run crawler.go``` 
4. And you're done!

### ___________WINDOWS___________

1. Git clone and cd int
2. Run these commands:
  ```
    go mod tidy
	  go fmt crawler.go
  ```

## Accesing the database

Do expect the crawler to take a while, it is literally scanning and saving descriptions and titles from every single website ever created. You can however stop it whenever you want with Ctrl + C and it will have updated the database for the websites that have already been scanned

The data will be stored in a SQLite 3 database named crawl_data.db, and it can be viewed through any SQlite gui, but I prefer to use [SQLiteStudio](https://sqlitestudio.pl/). The data can be viweed by:
1. First pressing database up the top of SQLiteStudio, and pressing add a database.
2. Then ensure these options are selected, with the file area being the location of your crawl_data.db file:
   
   ![SQLiteStudio add a database screen](https://raw.githubusercontent.com/i-love-winter/toogle/refs/heads/main/add%20a%20database.png)
3. Hit okay, then click the down arrows in the bar on the left until you get the pages database
4. Then select data, and that's all the data you've crawled!
5. Good job!

