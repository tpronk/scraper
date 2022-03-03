# Introduction
This scraper can be used for [Discourse fora](https://www.discourse.org/). It consists of two scripts:
1. A [Scrapy SitemapSpider](https://docs.scrapy.org/en/latest/topics/spiders.html#sitemapspider) that downloads each topic and post of a given discourse forum
2. A [processing script](process_data.py) that merges topic IDs that are spread across multiple pages

# Usage
1. Have the `sitemap_urls` variable point to the sitemap of the Discourse Forum you'd like to scrape. See [this line](discourse_forum/spiders/spider.py#L7)
2. Start the spider by running the following command in the scraper/discourse_forum directory: `scrapy crawl discourse_forum -L WARNING -O data/data_parsed.pickle`
3. Once scraping has completed, process the parsed data by running `py process_data.py`

# Development
## Scrapy-related
* As a starting point, I created a scaffold Scrapy project by running: `scrapy startproject discourse_forum`. 
* There is an average interval of 3 seconds between successive requests. See [DOWNLOAD_DELAY](https://doc.scrapy.org/en/latest/topics/settings.html?highlight=download_delay#download-delay).
* HTTP requests and responses are cached via [HttpCacheMiddleware](https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#module-scrapy.downloadermiddlewares.httpcache).

## Discourse-related
* The HTML that Discourse delivers to crawlers/scrapers/spiders is different from what it delivers to a standard web-browser.
* Obtaining answer information (i.e. "Solved by jdoe in Post #3") required parsing somewhat arcane JSON.
* Topics with many posts may be spread across multiple pages, with separate links to each in the sitemap, for example: `/topic-name/123` and `/topic_name/123?page=2`. The processing script takes care of merging multiple pages into topics.

# Example output
The JSON below is some example output (as produced by the spider or processing script).
```json
[{
  "answer_user": "fatima",
  "answer_date": "2016-11-04T11:17:12Z",
  "answer_position": 2,
  "answered": true,
  "posts": [{
    "user": "jane",
    "position": 1,
    "date": "2016-11-03T19:45:23Z",
    "text": "How much is 1 + 1?",
    "likes": 0,
    "comments": 1
  }, {
    "user": "fatima",
    "position": 2,
    "date": "2016-11-04T11:17:12Z",
    "text": "More than 1, definitely",
    "likes": 1,
    "comments": 1
  }, {
    "user": "jane",
    "position": 3,
    "date": "2016-11-05T15:58:43Z",
    "text": "Thanks!",
    "likes": 0,
    "comments": 1
  }],
  "topic_id": 1402,
  "topic_url": "https://discourse.example.com/t/math-question/1402",
  "topic_title": "Math question",
  "topic_category": "Arithmetics",
  "topic_tags": ["Addition", "Binary operators"]
}]
```
