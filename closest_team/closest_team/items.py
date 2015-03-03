# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from collections import defaultdict


class PlayerItem(Item):
    # define the fields for your item here like:
    # name = Field()
    name = Field()
    player_id = Field()
    high_school = Field()
    high_school_id = Field()
    birthday = Field()
    birthplace = Field()
    college = Field()
    url = Field()


class SchoolItem(Item):
    # define the fields for your item here like:
    # name = Field()
    school_id = Field()
    name = Field()
    city = Field()
    state = Field()


class PlayerSeasonItem(Item):

    def __setitem__(self, key, value):
        self._values[key] = value
        self.fields[key] = {}
