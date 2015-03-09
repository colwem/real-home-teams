from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.shell import inspect_response
from closest_team.items import *
from collections import defaultdict
from scrapy import log
import re
import logging

warn = lambda m: log.msg(m, level=log.WARNING)
info = lambda m: log.msg(m, level=log.INFO)
fmt = "id: {:<12} {}"

class PlayerPos(CrawlSpider):
    name = 'PlayerPos'
    allowed_domains = ['pro-football-reference.com']
    start_urls = ['http://www.pro-football-reference.com/players/']
    player_extractor = SgmlLinkExtractor(allow=(r'players/[A-Z]/\w+\.htm'))
    rules = (Rule(player_extractor, callback='parse_player'),
             Rule(SgmlLinkExtractor(allow=(r'players/[A-Z]/$'))))

    def parse_player(self, response):
        sel = Selector(response)
        id_ = None

        id_  = re.search(r'([^/]*)\.htm', response.url)
        if id_:
            id_ = id_.group(1)

        pos = sel.xpath('//div[@id="info_box"]/div[@class="float_left"]/p[2]/text()[1]')
        if pos:
            pos = pos.extract()[0].strip()
            info(fmt.format(id_, pos))
        else:
            warn(fmt.format(id_, pos))

        item = PlayerPosItem()
        item['id'] = id_
        item['pos'] = pos

        yield item

