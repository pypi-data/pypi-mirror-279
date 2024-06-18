settings = {
    "BOT_NAME": "huurdatascraper",
    "SPIDER_MODULES": ["ClappScrapers.den_rental.spider"],
    "NEWSPIDER_MODULE": "ClappScrapers.den_rental.spider",
    "ROBOTSTXT_OBEY": False,
    "ITEM_PIPELINES": {
        "ClappScrapers.den_rental.spider.pipelines.MergedDataPipeline": 100,
    },
    'COOKIES_ENABLED' : False,
    'LOG_LEVEL':'WARNING',
    'CONCURRENT_REQUESTS' : 8,  # Reduce the number of concurrent requests
    'CONCURRENT_REQUESTS_PER_DOMAIN' : 4,  # Reduce the number of concurrent requests per domain
    'CONCURRENT_REQUESTS_PER_IP' : 4,  # Reduce the number of concurrent requests per IP
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
        'ClappScrapers.den_rental.spider.extension.CustomLogExtension': 1,},
    'RETRY_ENABLED': True,
    'RETRY_TIMES': 5,  # Number of times to retry
    'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403, 407],
}