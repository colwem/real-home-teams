from minimal.models import *
import sys
from urllib2 import urlopen, Request
from urllib import urlencode
import json
import logging
import concurrent.futures

logging.basicConfig(filename='hsli.log', level=logging.DEBUG)
logging.debug('starting')

sql = '''select *, concat(name, " high school, ", city, " ", state) as `search`
         from high_schools
         where full_address is null
         order by state'''
logging.debug("sql: " + sql)
query = HighSchool.raw(sql)


def run(hs):
    key = 'AIzaSyCLYTjFEy3-5hneCyMHBP44CYyXG-6N0gw'
    url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    logging.debug("key: " + key)
    data = {'query': hs.search,
            'key': key}
    values = urlencode(data)
    response = urlopen(url + '?' + values)
    text = response.read()
    place_data = json.loads(text)
    if place_data['status'] != 'ZERO_RESULTS' and (place_data.has_key('results') and len(place_data['results'])):
        sys.stdout.write('.')
        place = place_data['results'][0]
        loc = place['geometry']['location']
        hs.latitude2 = loc['lat']
        hs.longitude2 = loc['lng']
        hs.full_address = place['formatted_address']
        hs.save()
        fmt = "{:<15}: {}"
        logging.info(fmt.format('search', hs.search))
        logging.info(fmt.format('full_address', hs.full_address))
        logging.info(fmt.format('lat', hs.latitude2))
        logging.info(fmt.format('lng', hs.longitude2))
    else:
        sys.stdout.write('x')
        hs.full_address = ''
        hs.save
        logging.warning("no results for: " + hs.search)

executor = concurrent.futures.ThreadPoolExecutor(100)
futures = [executor.submit(run, hs) for hs in query]
concurrent.futures.wait(futures)


