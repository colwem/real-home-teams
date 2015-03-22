import peewee
from peewee import *
from models import *
import re
import sys

db = database

# query = Player.select(
    # Player.pfr_high_school,
    # HighSchool.pfr_high_school_id
# ).join(
    # HighSchool).limit(10)

# for q in query.execute():
    # print q

query = Player.select(
    Player.birthplace,
    Player.player).where(
        Player.birthday != '',
        Player.birthday != None,
        Player.birthplace != '',
        Player.birthplace != None)

print query.sql()
pat = re.compile(r'\s*,\s*')

for player in query:
    try:
        city, state = pat.split(player.birthplace)
        sys.stdout.write('.')
        player.birth_city =  city
        player.birth_state =  state
        player.save()
    except ValueError as e:
        print 'error: {}\n player_t: {}\n birthplace: {}\n'.format(
            e,
            player.player_t,
            player.birthplace)



