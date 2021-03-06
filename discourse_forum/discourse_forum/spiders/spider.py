import json
import scrapy
from scrapy.spiders import SitemapSpider

class MySpider(SitemapSpider):
  name = 'discourse_forum'
  sitemap_urls = ['https://discourse.psychopy.org/sitemap.xml']

  def parse(self, response):
    print(response.url)
    # This page in parsed format
    result = {}

    # *** Topic info
    # Topic ID can be found in URL, after last slash, before "?", for example: blabla.com/topic-title/123?page=2
    result['topic_id'] = int(response.url.split('/').pop().split('?')[0]) 
    result['topic_url'] = response.url
    result['topic_title'] = response.css('#topic-title a')[0].xpath('text()').extract_first()
    result['topic_category'] = response.css('span[class="category-name"]').xpath('text()').extract_first()
    raw_tags = response.css('a[class="discourse-tag"]')
    result['topic_tags'] = [raw_tag.xpath('text()').extract_first() for raw_tag in raw_tags]
    
    # *** Answer info
    result['answer_user'] = None
    result['answer_date'] = None
    result['answer_position'] = None
    result['answered'] = False    
    # Find any JSON that might contain answer info
    json_strings = response.css('script[type="application/ld+json"]').xpath('string()').extract()
    for json_string in json_strings:
      json_data = json.loads(json_string)
      if json_data['@type'] == 'QAPage':
        try:
          result['answer_user'] = json_data['mainEntity']['acceptedAnswer']['author']['name']          
          result['answer_date'] = json_data['mainEntity']['acceptedAnswer']['dateCreated']
          result['answer_position'] = int(json_data['mainEntity']['acceptedAnswer']['url'].split('/').pop())
          result['answered'] = True
        except:
          pass

    # *** Parse each post in topic
    result['posts'] = []
    raw_posts = response.css('.topic-body')
    for raw_post in raw_posts:
      # Parse only if div is a post 
      if raw_post.xpath('@itemtype').extract_first() == 'http://schema.org/DiscussionForumPosting':
        # Username
        user = raw_post.css('span[itemprop="name"]').xpath('text()').extract_first()
        # Position
        raw_position = raw_post.css('span[itemprop="position"]').xpath('text()').extract_first()
        position = int(raw_position[1:len(raw_position)])
        # Date published
        date = raw_post.css('time[itemprop="datePublished"]').xpath('@datetime').extract_first()
        # Content of post
        text = raw_post.css('div[itemprop="articleBody"]').xpath('string()').extract_first()
        # Likes and comments
        raw_interaction_stats = raw_post.css('div[itemprop="interactionStatistic"]')
        for raw_interaction_stat in raw_interaction_stats:
          interaction_type = raw_interaction_stat.css('meta[itemprop="interactionType"]').xpath('@content').extract_first()
          interaction_value = int(raw_interaction_stat.css('meta[itemprop="userInteractionCount"]').xpath('@content').extract_first())
          if interaction_type == 'http://schema.org/LikeAction':
            likes = interaction_value
          else:
            comments = interaction_value
        # Add post
        result['posts'].append({
          'user': user,
          'position': position,
          'date': date,
          'text': text,
          'likes': likes,
          'comments': comments,
        })
    #print(result)
    yield result

