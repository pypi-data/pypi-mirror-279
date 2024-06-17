# Scrapy settings for nieuwbouwscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

settings = {
    "BOT_NAME": "nieuwbouwscraper",
    "SPIDER_MODULES": ["ClappScrapers.nieuwbouw.spider"],
    "NEWSPIDER_MODULE": "ClappScrapers.nieuwbouw.spider",
    "ROBOTSTXT_OBEY": False,
    "ITEM_PIPELINES": {
        "ClappScrapers.nieuwbouw.spider.pipelines.MergedDataPipeline": 100,
    },
    'COOKIES_ENABLED' : False,
    'LOG_LEVEL':'WARNING',
    "DOWNLOADER_MIDDLEWARES":{
        "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware":None,
        "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
        'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
        'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
    },
    "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    "FEED_EXPORT_ENCODING": "utf-8",
    "CUSTOM_LOG_EXTENSION":True,
    'FAKEUSERAGENT_PROVIDERS' : [
    'scrapy_fake_useragent.providers.FakeUserAgentProvider',
    'scrapy_fake_useragent.providers.FakerProvider',  
    'scrapy_fake_useragent.providers.FixedUserAgentProvider',
    ],
    "EXTENSIONS":{
        'scrapy.extensions.telnet.TelnetConsole': None,
        'ClappScrapers.nieuwbouw.spider.extension.CustomLogExtension': 1,},
    'RETRY_ENABLED': True,
    'RETRY_TIMES': 5,  # Number of times to retry
    'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429, 403, 407], 
}
