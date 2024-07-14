import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["www.timesnownews.com"]
    start_urls = ["https://www.timesnownews.com/latest-news"]

    def parse(self, response):
        # Ensure we're selecting the correct elements
        news_items = response.css("div._1W5s")
        for news in news_items:
            headline = news.css("div._16rp::text").get()
            news_link = news.css("a::attr(href)").get()
            
            if headline and news_link:
                yield {
                    'headline': headline.strip(),
                    'news_link': response.urljoin(news_link.strip())
                }

# To run the spider, use the command:
# scrapy runspider news_spider.py -o output.json
