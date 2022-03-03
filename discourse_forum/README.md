# Introduction
This scraper can be used for [https://www.discourse.org/](https://www.discourse.org/). It consists of two scripts
1. A [Scrapy SitemapSpider](https://docs.scrapy.org/en/latest/topics/spiders.html#sitemapspider) that downloads each topic and post of a given discourse forum
2. A [processing script](process_data.py) that merges topic IDs that are spread across multiple pages

# Usage
1. Have the `sitemap_urls` variable point to the sitemap of the Discourse Forum you'd like to scrape. See [this line](discourse_forum/spiders/spider.py#L7)
2. Start the spider by running the following command in the scraper/discourse_forum directory: `scrapy crawl discourse_forum -L WARNING -O data/data_parsed.pickle`
3. Once scraping completed, process the parsed data by running `py process_data.py`

# Development
* The files belonging to this scraper were created by running the following command in the scraper directory: `scrapy startproject discourse_forum`. 
* The HTML that Discourse delivers to crawlers/scrapers/spiders is different from what it delivers to a standard web-browser.
* Obtaining answer information (i.e. "Solved by jdoe in Post #3") required parsing somewhat arcane JSON.
* Topics with many posts may be spread across multiple pages, with separate links to each in the sitemap, for example: `/topic-name/123` and `/topic_name/123?page=2`. The processing script takes care of merging multiple pages into topics.

