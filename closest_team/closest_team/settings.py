# Scrapy settings for closest_team project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
import scrapy
import user_agent_list

BOT_NAME = 'closest_team'

SPIDER_MODULES = ['closest_team.spiders']
NEWSPIDER_MODULE = 'closest_team.spiders'

ENV = 'development'

EXTENSIONS = {}
if ENV == 'development':
    HTTPCACHE_ENABLED = True
    HTTPCACHE_POLICY = 'scrapy.contrib.httpcache.DummyPolicy'
    # EXTENSIONS['scrapy.contrib.closespider.CloseSpider'] = 500
    # CLOSESPIDER_PAGECOUNT = 100

DOWNLOAD_DELAY = 1
COOKIES_ENABLED = False

USER_AGENT_LIST = user_agent_list.USER_AGENT_LIST

DOWNLOADER_MIDDLEWARES = {
    'closest_team.middlewares.RandomUserAgentMiddleware': 400,
    'closest_team.middlewares.ProxyMiddleware': 410,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None
    # Disable compression middleware, so the actual HTML pages are cached
}


LOG_LEVEL = 'INFO'

# ITEM_PIPELINES = {
    # 'closest_team.pipelines.MultiCSVItemPipeline': 100
# }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'closest_team (+http://www.yourdomain.com)'

