from scrapy_redis.spiders import RedisSpider


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    #爬虫名称
    name = 'myspider_redis'
    allow_domains = ['51job.com']

    #利用redis启动爬虫的钥匙
    redis_key = 'myspider:start_urls'

    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return {
            'name': response.css('title::text').extract_first(),
            'url': response.url,
        }
