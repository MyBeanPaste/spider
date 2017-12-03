# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from example.items import WuYijobsItem
import datetime
from scrapy_redis.spiders import RedisCrawlSpider



class WuyijobSpider(RedisCrawlSpider):
    name = 'wuyijob'
    allowed_domains = ['51job.com']
    # start_urls = ['http://www.51job.com']

    redis_key = 'wuyijobspider:urls'

    rules = (
        Rule(LinkExtractor(allow=r'http://www.51job.com/[a-z]+/$'), follow=True),
        Rule(LinkExtractor(allow=r'jobs.51job.com/[a-z]+/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        print(response.url)
        item = WuYijobsItem()
        # item = {}
        job_url = response.url
        job_comp = response.xpath('//p[@class="cname"]/a/text()').extract()[0]#公司名
        job_name = response.xpath('//div[@class="cn"]/h1/text()').extract()[0]#工作名
        job_degree = response.xpath('//div[@class="t1"]/span[@class="sp4"][2]/text()').extract()[0]#学历
        if '招' in job_degree:
            job_degree = ''
            job_people = response.xpath('//div[@class="t1"]/span[@class="sp4"][2]/text()').extract()[0].lstrip('招').rstrip('人')  # 招聘人数
        else:
            job_people = response.xpath('//div[@class="t1"]/span[@class="sp4"][3]/text()').extract()[0].lstrip('招').rstrip('人') # 招聘人数
        money = response.xpath('//div[@class="cn"]/strong/text()').extract()
        # print(money)
        if len(money) > 0:
            money = money[0]
            if '月' in money:
                if '万' in money:
                    job_smoney = money.split('-')[0]
                    job_smoney = float(job_smoney)*10

                    job_emoney = money.split('-')[1].rstrip(r'万/月')
                    job_emoney = float(job_emoney)*10
                elif '千/月' in money:
                    job_smoney = money.split('-')[0]
                    job_emoney = money.split('-')[1].rstrip(r'千/月')

                else:
                    job_smoney = 0
                    job_emoney = 0
            elif '万/年' in money:
                job_smoney = money.split('-')[0]
                job_smoney =round(float(job_smoney)/12)

                job_emoney = money.split('-')[1].rstrip(r'万/年')
                job_emoney = round(float(job_emoney)/12)
            # else:
            #     job_smoney = 0
            #     job_emoney = 0
            # print(job_smoney,job_emoney)

            elif '天' in money:
                job_emoney = money.rstrip(r'元/天')
                job_emoney = float(job_emoney)*0.03
                job_smoney = 0
        else:
            job_smoney = 0
            job_emoney = 0
        job_address = response.xpath('//span[@class="lname"]/text()').extract()[0]#公司地址
        job_comp_type = response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('|')[0].strip()#公司类型
        job_num= response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('|')#公司人数
        if len(job_num) >= 1:
            job_business = response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('|')[2].strip()  # 公司主营
            job_num = job_num[1]
            if ' 少于' in job_num:
                job_comp_snum = 0
                job_comp_enum = 50
            elif '以上' in job_num:
                job_comp_snum = 10000
                job_comp_enum = 10000
            elif '-' in job_num:
                job_comp_snum = job_num.split('-')[0].strip()
                job_comp_enum = job_num.split('-')[1].replace('人','').strip()
        else:
            job_comp_snum = 0
            job_comp_enum = 0
            job_business = response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('|')[1].strip()


        # if job_num == '':
        #     job_business = response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('|')[1].strip()#公司主营
        # else:
        #     job_business = response.xpath('//p[@class="msg ltype"]/text()').extract()[0].split('|')[2].strip()

        job_year = response.xpath('//div[@class="t1"]/span[1]/text()').extract()[0]#工作经验
        if '-' in job_year:
            job_syear = job_year.split('-')[0]
            job_eyear = job_year.split('-')[1].replace('年经验','')
        elif '无' in job_year:
            job_syear = 0
            job_eyear = 0
        elif '以上' in job_year:
            job_syear = job_year.replace('年以上经验','')
            job_eyear = job_year.replace('年以上经验','')
        else:
            job_syear = job_year.replace('年经验','')
            job_eyear = job_year.replace('年经验','')

        if job_degree == '':
            job_date_pub = response.xpath('//div[@class="t1"]/span[@class="sp4"][3]/text()').extract()[0].replace('发布','')#发布时间
        else:
            job_date_pub = response.xpath('//div[@class="t1"]/span[@class="sp4"][4]/text()').extract()[0].replace('发布','')#发布时间

        job_datetime = datetime.datetime.now().strftime('%Y-%m-%d')

        job_welfafe = response.xpath('//p[@class="t2"]/span/text()').extract()#公司福利
        if len(job_welfafe) != 0:
            job_welfafe = str(job_welfafe).lstrip('[').rstrip(']')
        else:
            job_welfafe = ''


        job_desc = response.xpath('//div[@class="bmsg job_msg inbox"]/text()').extract()[2:-4]
        job_desc = str(job_desc).lstrip('[').rstrip(']').replace(r' \xa0','').replace(r'\t','')
        job_request = ''
        job_tag = response.xpath('//p[@class="fp"]/span[2]/text()').extract()[0]
        if job_tag:
            job_tag = job_tag
        else:
            job_tag = ''

        item['job_url'] = job_url
        item['job_comp'] = job_comp
        item['job_name'] = job_name
        item['job_degree'] = job_degree
        item['job_smoney'] = job_smoney
        item['job_emoney'] = job_emoney
        item['job_address'] = job_address
        item['job_comp_type'] = job_comp_type
        item['job_comp_snum'] = job_comp_snum
        item['job_comp_enum'] = job_comp_enum
        item['job_business'] = job_business
        item['job_syear'] = job_syear
        item['job_eyear'] = job_syear
        item['job_date_pub'] = job_date_pub
        item['job_datetime'] = job_datetime
        item['job_welfafe'] = job_welfafe
        item['job_desc'] = job_desc
        item['job_request'] = job_request
        item['job_tag'] = job_tag
        item['job_people'] = job_people

        yield item










