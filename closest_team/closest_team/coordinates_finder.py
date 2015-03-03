import peewee
from scrapy.selector import Selector
from peewee import *
from models import *
from geopy.geocoders import Nominatim, GeoNames
from geopy.exc import GeocoderTimedOut, GeocoderParseError, GeocoderServiceError
from time import sleep
import re
import sys
import lxml

db = database
gl = GeoNames(username='colwem', timeout=5)

fmt = "{}, {}"

def problem(s):
    print '{}\t{}, {}'.format(s.high_school_t, s.city, s.state)


def loop(q):
    retry = []
    for s in q:
        sleep(0.4)
        try:
            l = gl.geocode(fmt.format(s.city, s.state))
            if l:
                s.latitude, s.longitude = l.latitude, l.longitude
                s.save()
                sys.stdout.write('.')
            else:
                problem(s)
        except GeocoderTimedOut as e:
            retry.append(s)
            problem(s)
            print 'error: ', e
        except GeocoderParseError as e:
            retry.append(s)
            problem(s)
            print 'error: ', e
        except GeocoderServiceError as e:
            retry.append(s)
            problem(s)
            print 'error: ', e
            sleep(60 * 5)
    return retry

query = HighSchoolT.select().where(
    HighSchoolT.state != None,
    HighSchoolT.city != None,
    HighSchoolT.latitude == None,
    HighSchoolT.longitude == None)

print query.sql()

retry = loop(query)
retry = loop(retry)
print retry

# url_fmt = 'http://nominatim.openstreetmap.org/search/{},{}?format=xml&limit=1'

