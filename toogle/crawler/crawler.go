package main

import (
	"bytes"
	"database/sql"
	"fmt"
	"log"
	"strings"

	"github.com/gocolly/colly"
	_ "github.com/mattn/go-sqlite3"
	"golang.org/x/net/html"
)

// create a map to store visited urls to ensure that you don't visit the same url twice
var visitedurls = make(map[string]bool)

// extractText recursively gets all visible text from HTML nodes
func extractText(n *html.Node) string {
	if n.Type == html.TextNode {
		return strings.TrimSpace(n.Data)
	}
	var result string
	for c := n.FirstChild; c != nil; c = c.NextSibling {
		result += extractText(c) + " "
	}
	return strings.Join(strings.Fields(result), " ")
}

func main() {
	// create the SQLite database
	db, err := sql.Open("sqlite3", "./crawl_data.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// create table if it doesn't exist
	createTable := `
    CREATE TABLE IF NOT EXISTS pages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        title TEXT,
        description TEXT,
				text TEXT
    );`
	if _, err := db.Exec(createTable); err != nil {
		log.Fatal(err)
	}

	// define the seed url
	seedurl := "https://en.wikipedia.org/wiki/Chicago_rat_hole"

	// call the crawl function
	crawl(seedurl, 0, db)
}

func crawl(currenturl string, maxdepth int, db *sql.DB) {
	// create a new collector
	c := colly.NewCollector(
		colly.MaxDepth(maxdepth),
	)

	// variables to hold data for each page
	var pageTitle, pageDescription string

	// extract the page title
	c.OnHTML("title", func(e *colly.HTMLElement) {
		pageTitle = strings.TrimSpace(e.Text)
	})

	// extract meta description
	c.OnHTML(`meta[name="description"]`, func(e *colly.HTMLElement) {
		pageDescription = strings.TrimSpace(e.Attr("content"))
	})

	c.OnScraped(func(r *colly.Response) {
		pageURL := r.Request.URL.String()

		// Parse HTML and extract text
		doc, err := html.Parse(bytes.NewReader(r.Body))
		if err != nil {
			log.Println("HTML parse error:", err)
			return
		}
		pageText := extractText(doc)

		fmt.Printf("Saving: %s\n", pageURL)

		_, err = db.Exec(
			`INSERT OR IGNORE INTO pages (url, title, description, text) VALUES (?, ?, ?, ?)`,
			pageURL, pageTitle, pageDescription, pageText,
		)
		if err != nil {
			log.Println("DB insert error:", err)
		}

		// reset for next page
		pageTitle = ""
		pageDescription = ""
	})

	// find and visit links
	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		link := e.Request.AbsoluteURL(e.Attr("href"))
		if link != "" && !visitedurls[link] {
			visitedurls[link] = true
			fmt.Println("Found link:", link)
			e.Request.Visit(link)
		}
	})

	// track progress
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Crawling", r.URL)
	})

	// handle errors
	c.OnError(func(e *colly.Response, err error) {
		fmt.Println("Request URL:", e.Request.URL, "failed with response:", e, "\nError:", err)
	})

	// visit the seed url
	if err := c.Visit(currenturl); err != nil {
		fmt.Println("Error visiting page:", err)
	}
}
