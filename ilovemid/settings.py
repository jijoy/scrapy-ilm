# -*- coding: utf-8 -*-

# Scrapy settings for ilovemid project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ilovemid'

SPIDER_MODULES = ['ilovemid.spiders']
NEWSPIDER_MODULE = 'ilovemid.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ilovemid (+http://www.yourdomain.com)'
DOWNLOAD_TIMEOUT = 180
# DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS = 1
CONCURRENT_REQUESTS_PER_IP = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
RETRY_TIMES = 50
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]

USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36"\
             " (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 8,
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 20,
    'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 30,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,
}

ITEM_PIPELINES = {
    'ilovemid.pipelines.MyImagesPipeline' : 2,
    'ilovemid.pipelines.XmlExportPipeline': 1

}
IMAGES_STORE= 'D:/work/images'
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'