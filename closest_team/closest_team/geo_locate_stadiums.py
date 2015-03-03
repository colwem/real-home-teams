
import peewee
from peewee import *
from models import *
from geopy.geocoders import Nominatim, GeoNames
from geopy.exc import GeocoderTimedOut, GeocoderParseError, GeocoderServiceError
from time import sleep
import re
import sys


db = database
gl = GeoNames(username='colwem', timeout=5)
gl = Nominatim()


def problem(s):
    print '{}\t{}\t{}\t{}'.format(s.stadium, s.name, s.team, s.location)


def loop(q):
    retry = []
    fmt = '{}, {}'
    for s in q:
        sleep(0.4)
        try:
            l = gl.geocode(fmt.format(s.name, 'stadium'))
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

query = Stadium.select()

print query.sql()

retry = loop(query)

# url_fmt = 'http://nominatim.openstreetmap.org/search/{},{}?format=xml&limit=1'

