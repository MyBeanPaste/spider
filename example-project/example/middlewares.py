from fake_useragent import UserAgentfrom spider_daili import settingsimport randomimport base64#一个中间件就是一个类class RadomUserAgent(object):    #处理请求的函数    def __init__(self,crawler):        '''        :param crawl: 爬虫对象        '''        #获取配置文件中的配置信息        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE','random')        self.ua = UserAgent()   #实力化对象    @classmethod    def from_crawler(cls,crawler):        return cls(crawler)    def process_request(self,request,spider):        '''        :param request: 请求对象        :param spider: 蜘蛛对象        :return:        '''        request.headers.setdefault('User-Agent',getattr(self.ua, self.ua_type))# class FreeRandomProxy(object):#     def process_request(self,request,spider):#         #随机选出代理信息#         proxy = random.choice(settings.PROXIES)#         request.meta['proxy'] = 'http://'+ proxy['host']#         request.meta['proxy'] = 'httsp://'+ proxy['host']#收费class AutoRandomProxy(object):    #随机选出代理    def process_request(self, request, spider):        proxy = random.choice(settings.AUTO_PROXIES)        #设置代理的认证信息        # request.headers['Proxy-Authrization'] = b'Basic' + base64.b64decode(bytes(proxy['auth'],'utf-8'))        auth = base64.b64encode(bytes(proxy['auth'], 'utf-8'))        request.headers['Proxy-Authorization'] = b'Basic ' + auth        #设置代理ip        request.meta['proxy'] = 'http://' + proxy['host']