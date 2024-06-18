

settings = {'BOT_NAME' : "asunnot_scraper",
            'SPIDER_MODULES' : ["ClappScrapers.asunnot.spider"],
            'NEWSPIDER_MODULE' : "ClappScrapers.asunnot.spider",
            'ROBOTSTXT_OBEY' : False,
            'CONCURRENT_REQUESTS' : 8,  # Reduce the number of concurrent requests
            'CONCURRENT_REQUESTS_PER_DOMAIN' : 4,  # Reduce the number of concurrent requests per domain
            'CONCURRENT_REQUESTS_PER_IP' : 4,  # Reduce the number of concurrent requests per IP
            'LOG_LEVEL':'WARNING',
            'COOKIES_ENABLED' : False,
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
            'ITEM_PIPELINES' : {
                "ClappScrapers.asunnot.spider.pipelines.MergedDataPipeline": 200
            },
            'REQUEST_FINGERPRINTER_IMPLEMENTATION' : "2.7",
            'TWISTED_REACTOR' : "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            'FEED_EXPORT_ENCODING' : "utf-8",
            "CUSTOM_LOG_EXTENSION":True,
            "EXTENSIONS":{
                'scrapy.extensions.telnet.TelnetConsole': None,
                'ClappScrapers.asunnot.spider.extension.CustomLogExtension': 1,},
            'RETRY_ENABLED': True,
            'RETRY_TIMES': 5,  # Number of times to retry
            'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403, 407], 

}
