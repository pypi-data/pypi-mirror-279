

settings = {'BOT_NAME' : "denmarksell_scraper",
            'SPIDER_MODULES' : ["ClappScrapers.den_boligsiden_sell.spider"],
            'NEWSPIDER_MODULE' : "ClappScrapers.den_boligsiden_sell.spider",
            # 'LOG_LEVEL':'WARNING',
            'ROBOTSTXT_OBEY' : False,
            'CONCURRENT_REQUESTS_PER_DOMAIN' : 2,
            'ITEM_PIPELINES' : {
                "ClappScrapers.den_boligsiden_sell.spider.pipelines.MergedDataPipeline": 200
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

            'REQUEST_FINGERPRINTER_IMPLEMENTATION' : "2.7",
            'TWISTED_REACTOR' : "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
            'FEED_EXPORT_ENCODING' : "utf-8",
            # "CUSTOM_LOG_EXTENSION":True,
            # "EXTENSIONS":{
            #     'scrapy.extensions.telnet.TelnetConsole': None,
            #     'ClappScrapers.asunnot.spider.extension.CustomLogExtension': 1,}
}