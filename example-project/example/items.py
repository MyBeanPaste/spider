# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AynuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WuYijobsItem(scrapy.Item):
    job_url = scrapy.Field()  #路径
    job_comp = scrapy.Field() #公司名
    job_name = scrapy.Field() #工作名
    job_degree = scrapy.Field() #学历
    job_smoney = scrapy.Field() #工资最小数
    job_emoney = scrapy.Field() #工资最大数
    job_address = scrapy.Field() #工作地址
    job_comp_type = scrapy.Field() #公司类型
    job_comp_snum = scrapy.Field() #公司最小人数
    job_comp_enum = scrapy.Field() #公司最大人数
    job_business = scrapy.Field()  #公司主营
    job_syear = scrapy.Field()  #最小经验年限
    job_eyear = scrapy.Field()  #最大经验年限
    job_date_pub = scrapy.Field() #工作发布时间
    job_datetime = scrapy.Field() #爬取时间
    job_welfafe = scrapy.Field() #公司福利
    job_people = scrapy.Field() #招聘人数
    job_desc = scrapy.Field() # 工资简介
    job_request = scrapy.Field() #工资要求
    job_tag = scrapy.Field() #爬取种类分类

# class LagouItem(scrapy.Item):
#     job_url = scrapy.Field()  #路径
#     job_comp = scrapy.Field() #公司名
#     job_name = scrapy.Field() #工作名
#     job_degree = scrapy.Field() #学历
#     job_smoney = scrapy.Field() #工资最小数
#     job_emoney = scrapy.Field() #工资最大数
#     job_address = scrapy.Field() #工作地址
#     job_comp_type = scrapy.Field() #公司类型
#     job_comp_snum = scrapy.Field() #公司最小人数
#     job_comp_enum = scrapy.Field() #公司最大人数
#     job_business = scrapy.Field()  #公司主营
#     job_syear = scrapy.Field()  #最小经验年限
#     job_eyear = scrapy.Field()  #最大经验年限
#     job_date_pub = scrapy.Field() #工作发布时间
#     job_datetime = scrapy.Field() #爬取时间
#     job_welfafe = scrapy.Field() #公司福利
#     job_people = scrapy.Field() #招聘人数
#     job_desc = scrapy.Field() # 工资简介
#     job_request = scrapy.Field() #工资要求
#     job_tag = scrapy.Field() #爬取种类分类