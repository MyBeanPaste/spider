# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagou.items import LagouItem
from scrapy_redis.spiders import RedisCrawlSpider

class LagouSpider(RedisCrawlSpider):
    name = 'LaGou'
    allowed_domains = ['lagou.com']
    # start_urls = ['http://www.lagou.com/']
    redis_key = 'lagouspider:urls'
    rules = (
        # Rule(LinkExtractor(allow=r'zhaopin/\w+/?labelWords=label'), follow=True),
        Rule(LinkExtractor(allow=r'gongsi/j\d+.html', ), follow=True),
        Rule(LinkExtractor(allow=r'zhaopin/.*', ), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        item = LagouItem()
        job_url = response.url #路径
        job_comp = response.css('#job_company dt a img::attr(alt)').extract()[0]#公司名
        print()
        job_name = response.xpath('//div[@class="job-name"]/@title').extract()[0] # 工作名
        job_degree = response.xpath('//dd[@class="job_request"]/p/span[4]/text()').extract()[0].rstrip(' /')  # 学历
        money = response.xpath('//dd[@class="job_request"]/p/span[@class="salary"]/text()').extract()[0]
        if '-' in money:
            job_smoney = money.lower().replace('k','').split('-')[0]   # 工资最小数
            job_emoney = money.lower().replace('k','').split('-')[1]   # 工资最大数
        else:
            job_smoney = 0
            job_emoney = 0
        job_address = response.xpath('//dd[@class="job_request"]/p/span[2]/text()').extract()[0].lstrip('/').rstrip(' /')  # 工作地址
        job_comp_type = response.xpath('//ul[@class="c_feature"]/li[2]/text()').extract()[1].replace(r'\n ','')#公司类型
        job_business = response.xpath('//ul[@class="c_feature"]/li[1]').extract()[0].split(r'</i>')[1].split('<span class="hovertips">')[0].replace(r'\n','')
        job_date_pub = response.xpath('//p[@class="publish_time"]/text()').extract()[0].split(' ')[0]  #发布时间
        job_num = response.xpath('//ul[@class="c_feature"]/li[3]/text()').extract()[1]
        if '-' in job_num:
            job_comp_snum = job_num.split('-')[0] # 公司最小人数
            job_comp_enum = job_num.split('-')[1].replace('人','') # 公司最大人数
        elif '以上' in job_num:
            job_comp_snum = job_num.replace('人以上','')
            job_comp_enum = job_comp_snum
        else:
            job_comp_snum = 0
            job_comp_enum = 0

        job_year = response.xpath('//dd[@class="job_request"]/p/span[3]/text()').extract()[0]

        if '-' in job_year:
            job_syear = job_year.split('-')[0].replace('经验','')  # 最小经验年限
            job_eyear = job_year.split('-')[1].replace('年 /','') # 最大经验年限
        elif '以上' in job_year:
            job_syear = job_year.replace('年以上','').lstrip('经验')
            job_eyear = job_syear
        else:
            job_syear = 0
            job_eyear = 0
        job_datetime = datetime.datetime.now().strftime('%Y-%m-%d') # 爬取时间
        job_welfafe = response.xpath('//dd[@class="job-advantage"]/p/text()').extract()[0]# 公司福利
        job_people = ''  # 招聘人数
        job_desc = response.xpath('//dd[@class="job_bt"]//p/text()').extract() # 工作简介
        job_desc = str(job_desc).lstrip('[').rstrip(']').replace(r'\xa0','')
        job_request = ''  # 工作要求
        job_tag =response.xpath('//li[@class="labels"]/text()').extract()# 爬取种类分类
        job_tag = ','.join(job_tag)
        # print(job_business,job_tag)

        item['job_name'] = job_name
        item['job_degree'] = job_degree
        item['job_smoney'] = job_smoney
        item['job_emoney'] = job_emoney
        item['job_address'] = job_address
        item['job_comp_snum'] = job_comp_snum
        item['job_comp_enum'] = job_comp_enum
        item['job_syear'] = job_syear
        item['job_eyear'] = job_eyear
        item['job_datetime'] = job_datetime
        item['job_welfafe'] = job_welfafe
        item['job_people'] = job_people
        item['job_desc'] = job_desc
        item['job_request'] = job_request
        item['job_tag'] = job_tag
        item['job_url'] = job_url
        item['job_comp'] = job_comp
        item['job_comp_type'] = job_comp_type
        item['job_business'] = job_business
        item['job_date_pub'] = job_date_pub

        yield item

