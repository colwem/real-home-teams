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
from closest_team.table_extractor import Table

warn = lambda m: log.msg(m, level=log.WARNING)
info = lambda m: log.msg(m, level=log.INFO)
fmt = "id: {:<12} {}"


class EspnRoster(CrawlSpider):
    name = 'EspnRoster'
    allowed_domains = ['espn.go.com']
    start_urls = ['http://espn.go.com/nfl/teams']
    team_roster_extractor = SgmlLinkExtractor(
        allow=(r'team/roster/_/name/\w+/[^/]+$'))
    team_depth_extractor = SgmlLinkExtractor(
        allow=(r'team/depth/_/name/\w+/[^/]+$'))
    team_depth_formation_extractor = SgmlLinkExtractor(
        allow=(r'team/depth/_/name/[^/]+/formation'))
    rules = (Rule(team_roster_extractor, callback='parse_roster'),
             Rule(team_depth_extractor, callback='parse_depth'),
             Rule(team_depth_formation_extractor, callback='parse_depth'))

    def parse_roster(self, response):
        info("parsing: " + response.url)
        team = re.search(r'/name/(\w+)/', response.url)
        if team:
            team = team.group(1)
        sel = Selector(response)
        table_path = '//table[@class="tablehead"]'
        header_path = './/tr[@class="colhead"][1]'
        header_extractor = './/td/text() | .//td/a/text()'
        row_path = './/tr[not(@class="colhead") and not(@class="stathead")]'
        column_extractor = './/td/text() | .//td/a/text()'

        table = Table(table_path=table_path,
                      header_path=header_path,
                      header_extractor=header_extractor,
                      row_path=row_path,
                      column_extractor=column_extractor,
                      item=RosterItem)

        for i in table.items(sel):
            i['team'] = team
            yield i

    def parse_depth(self, response):
        team = re.search(r'/name/(\w+)/', response.url)
        if team:
            team = team.group(1)
        info("parsing: " + response.url)
        sel = Selector(response)
        table_path = '//table[@class="tablehead"]'
        header_path = './/tr[@class="colhead"][1]'
        header_extractor = './/td/text() | .//td/a/text()'
        row_path = './/tr[not(@class="colhead") and not(@class="stathead")]'
        column_extractor = './/td/text() | .//td//a/text()'
        t = sel.xpath(table_path)
        formation = t.xpath('.//tr[@class="stathead"]/td/text()').extract()[0]
        table = Table(table_path=table_path,
                      header_path=header_path,
                      header_extractor=header_extractor,
                      row_path=row_path,
                      column_extractor=column_extractor,
                      item=DepthItem)

        for i in table.items(sel):
            i['formation'] = formation
            i['team'] = team
            yield i

        for l in self.team_depth_formation_extractor.extract_links(response):
            yield Request(l.url, self.parse_depth)

