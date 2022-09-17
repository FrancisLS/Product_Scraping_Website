# Allinit - A Product Scraping Website
My senior project application

Languages: Python, HTML, CSS
Frameworks: Scrapy, Flask, Bootstrap
APIs: ScraperAPI, ScrapyRT

This project allows the user to search and scrape for products in multiple online shopping websites,
save the results into a temporary JSON file, and show all the product results in one Results Page.
User can filter through these results either by searching, name, price, number of reviews, and which
website it came from. Future plans for bookmarking search results and alerting if the bookmarked 
search results are currently lower in price.

I used the Scrapy framework to create and run the scrapers (spiders) used by my website. ScraperAPI is a
proxy API used to safely to get the product data in online shopping websites. ScrapyRT is an HTTP API 
that allows the user to start the Scrapy spiders when clicking the "Search" button in the website 
using GET request instead of manually in the command line ScrapyRT also temporarily stores the scraped 
data into a JSON file in a localhost URL link for reading by the Results Page. Flask and Bootstrap are 
used to design the website itself.
