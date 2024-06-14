settings = {
   "BOT_NAME": "huurdatascraper",
   "SPIDER_MODULES": ["ClappScrapers.den_rental.spider"],
   "NEWSPIDER_MODULE": "ClappScrapers.den_rental.spider",
   "ROBOTSTXT_OBEY": False,
   "ITEM_PIPELINES": {
       "ClappScrapers.den_rental.spider.pipelines.MergedDataPipeline": 100,
   },
   'DOWNLOADER_MIDDLEWARES' : {
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
                'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
            },
   'FAKEUSERAGENT_PROVIDERS' : [
                'scrapy_fake_useragent.providers.FakeUserAgentProvider',
                'scrapy_fake_useragent.providers.FakerProvider',  
                'scrapy_fake_useragent.providers.FixedUserAgentProvider',
            ],
   "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
   "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
   "FEED_EXPORT_ENCODING": "utf-8",
    "CUSTOM_LOG_EXTENSION":True,
    "EXTENSIONS":{
        'scrapy.extensions.telnet.TelnetConsole': None,
        'ClappScrapers.den_rental.spider.extension.CustomLogExtension': 1,}
}