from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.shell import inspect_response
from closest_team.items import *
import re


class NflPlayersHighschool(CrawlSpider):
    name = 'NFLPlayersHighschool'
    allowed_domains = ['pro-football-reference.com']
    start_urls = ['http://www.pro-football-reference.com/players/']
    # start_urls = ['http://www.pro-football-reference.com/players/S/SandDe00.htm']
    school_extractor = SgmlLinkExtractor(allow=(r'schools/high_schools\.cgi\?id'))
    player_extractor = SgmlLinkExtractor(allow=(r'players/[A-Z]/\w+\.htm'))
    rules = (Rule(school_extractor, callback='parse_school'),
             Rule(player_extractor, callback='parse_player'),
             Rule(SgmlLinkExtractor(allow=(r'players/[A-Z]/$'))))

    def parse_school(self, response):
        sel = Selector(response)
        city, state, name = None, None, None

        school_id = self.parse_hs_id(response.url)

        name = sel.xpath('//h1/text()[contains(., "Alumni Pro Stats")]')
        if name:
            name = name[0].extract()
            name = name.replace(' Alumni Pro Stats', '')

        city_state = sel.xpath('//h1[text()[contains(., "Alumni Pro Stats")]]/following-sibling::p/text()')
        if city_state:
            city_state = city_state[0].extract()
            city, state = re.split('\s*,\s*', re.sub('\s*\(\s*', '', city_state))

        school_item = SchoolItem()
        school_item['name'] = name
        school_item['school_id'] = school_id
        school_item['city'] = city
        school_item['state'] = state
        return school_item

    def parse_player(self, response):
        sel = Selector(response)
        id_, name, birthday, birthplace, high_school, high_school_url, high_school_id, college, url = 9 * [None]

        id_  = re.search(r'([^/]*)\.htm', response.url)
        if id_:
            id_ = id_.group(1)
        import ipdb; ipdb.set_trace()
        n = sel.xpath('//h1//text()')
        if n:
            name = n[0].extract()

        bg = sel.xpath('//span[@id = "necro-birth"]//text()')
        if bg:
            t = ''.join(bg.extract()).split(' in ')
            if len(t) > 1:
                birthday, birthplace = t

        hs = sel.xpath('//p/strong[text() = "High School:"]/following-sibling::a/text()')
        if hs:
            high_school = hs[0].extract()

        hsu = sel.xpath('//p/strong[text() = "High School:"]/following-sibling::a/@href')
        if hsu:
            high_school_url = hsu[0].extract()
            high_school_id = self.parse_hs_id(high_school_url)

        c = sel.xpath('//p/strong[text() = "College:"]/following-sibling::a/text()')
        if c:
            college = c[0] .extract()

        for link in self.school_extractor.extract_links(response):
            yield Request(link.url, self.parse_school)

        for link in self.player_extractor.extract_links(response):
            yield Request(link.url, self.parse_player)

        url = response.url

        item                   = PlayerItem()
        item['name']           = name
        item['player_id']      = id_
        item['high_school']    = high_school
        item['high_school_id'] = high_school_id
        item['birthplace']     = birthplace
        item['birthday']       = birthday
        item['college']        = college
        item['url']            = url
        yield item

    def parse_hs_id(self, url):
        match = re.search(r'[^=]*$', url)
        if match:
            return match.group(0)
        return None


# for getting the lat long of every players school
# b = "http://nominatim.openstreetmap.org/search/{},{}?format=xml&limit=1".format('city', 'state')
