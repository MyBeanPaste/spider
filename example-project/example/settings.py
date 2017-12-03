# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['example.spiders']
NEWSPIDER_MODULE = 'example.spiders'

# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',

#url指纹过滤器
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#调度器
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#设置爬虫是否可以中断
SCHEDULER_PERSIST = True

#设置请求队列类型
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"#按照优先级入队列
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"#按照队列模式
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"#按照栈进行请求的调度（先进后出）
DOWNLOADER_MIDDLEWARES = {
#    'aynu.middlewares.MyCustomDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'example.middlewares.RadomUserAgent': 1,
    # 'example.middlewares.AutoRandomProxy': 1,

}
DOWNLOAD_TIMEOUT = 15

ITEM_PIPELINES = {
    'example.pipelines.ExamplePipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 400,#redis管道文件，自动把数据加载到redis
}

# LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 0

#redis服务的ip地址和端口号
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

CONCURRENT_ITEMS = 100 #并发解析
CONCURRENT_REQUEST = 16 #并发请求
# CONCURRENT_REQUEST_PER_DOMAIN = 64

# AUTO_PROXIES = [
#     {'host':'120.78.166.84:6666','auth':'alice:123456'}
# ]
