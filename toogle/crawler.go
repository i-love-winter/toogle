 package main

import (
	"fmt"
	"github.com/gocolly/colly"
)

// create a map to store visited urls to ensure that you don't visit the same url twice
var visitedurls = make(map[string]bool)

func main() {
	// define the seed url
	seedurl := "https://www.example.com" // change this to the seedurl you want to use

	// call the crawl function
	crawl(seedurl, 0)
}

func crawl(currenturl string, maxdepth int) {
	// create a new collector
	c := colly.NewCollector(
		colly.MaxDepth(maxdepth),
	)

	// extract and log the page title
	c.OnHTML("title", func(e *colly.HTMLElement) {
		fmt.Println("Page Title:", e.Text)
	})

	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		// get absolute URL
		link := e.Request.AbsoluteURL(e.Attr("href"))
		// check if current URL has already been visited
		if link != "" && !visitedurls[link] {
			// add current URL to visitedURLs
			visitedurls[link] = true
			fmt.Println("Found link:", link)
			// visit current URL
			e.Request.Visit(link)
		}
	})

	// add an OnRequest callback to track progress
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Crawling", r.URL)
	})

	// handle errors
	c.OnError(func(e *colly.Response, err error) {
		fmt.Println("Request URL:", e.Request.URL, "failed with response:", e, "\nError:", err)
	})

	// visit the seed url
	err := c.Visit(currenturl)
	if err != nil {
		fmt.Println("Error visiting page:", err)
	}
}
