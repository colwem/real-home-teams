import peewee
from peewee import *
from models import *
import re
import sys

db = database

# query = PlayersT.select(
    # PlayersT.pfr_high_school,
    # HighSchoolT.pfr_high_school_id
# ).join(
    # HighSchoolT).limit(10)

# for q in query.execute():
    # print q

query = PlayersT.select(
    PlayersT.birthplace,
    PlayersT.player_t).where(
        PlayersT.birthday != '',
        PlayersT.birthday != None,
        PlayersT.birthplace != '',
        PlayersT.birthplace != None)

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



