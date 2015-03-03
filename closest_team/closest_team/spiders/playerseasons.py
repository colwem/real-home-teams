from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.shell import inspect_response
from closest_team.items import *
from collections import defaultdict
import re


def merged(d1, d2):
    copied = d1.copy()
    copied.update(d2)
    return copied


def get_years(table, cols):
    for tr in table.xpath(".//tbody/tr"):
        vals = {}
        for i, col in enumerate(cols):
            at = tr.xpath(".//td[{}]//a/text()".format(i + 1)).extract()
            if at:
                vals[col] = at[0]
            else:
                t = tr.xpath(".//td[{}]/text()".format(i + 1)).extract()
                if len(t):
                    vals[col] = t[0]
                else:
                    vals[col] = u''

        vals[u'year'] = vals[cols[0]]
        yield vals


def process_table(t, seasons):
    _id = t.xpath("@id").extract()[0]
    cols = t.xpath(".//thead/tr[last()]/th/@data-stat").extract()
    cols = [_id + '_' + str(c) for c in cols]
    for y in get_years(t, cols):
        year = y[u'year']
        seasons[year] = merged(seasons[year], y)
    return seasons


class PlayerSeasons(CrawlSpider):
    name = 'PlayerSeasons'
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

        ok_tables = [u'passing',
                     u'passing_playoffs',
                     u'defense',
                     u'defense_playoffs',
                     u'returns',
                     u'returns_playoffs',
                     u'scoring',
                     u'scoring_playoffs',
                     u'passing_advanced',
                     u'passing_advanced_playoffs',
                     u'receiving_and_rushing',
                     u'receiving_and_rushing_playoffs',
                     u'rushing_and_receiving',
                     u'rushing_and_receiving_playoffs',
                     u'kicking',
                     u'kicking_playoffs']

        seasons = defaultdict(dict)
        tables = sel.xpath("//div[@class='table_container']/table")

        for t in tables:
            _id = t.xpath("@id").extract()[0]
            if _id in ok_tables:
                seasons = process_table(t, seasons=seasons)

        for k, v in seasons.items():
            item = PlayerSeasonItem()
            item['player_id'] = id_
            item['year'] = k
            for k, v in v.items():
                item[k] = v

            yield item


# for getting the lat long of every players school
# b = "http://nominatim.openstreetmap.org/search/{},{}?format=xml&limit=1".format('city', 'state')
