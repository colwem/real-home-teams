from models import *
import numpy as np
import logging
import sys

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('peewee.log', mode='w'))

pmf = lambda p, k: p * (1 - p) ** k


def scaler(p, year):
    return lambda av, y: av * pmf(p, year - y)

ps = PlayerSeasons
pl = PlayersT
cur_y = ps.select(fn.Max(ps.year).alias('max')).first().max


q = (pl.select(pl, ps)
     .join(ps)
     .where((ps.av != None) & (ps.year != None))
     .order_by(pl.birthday_date.desc)
     .aggregate_rows())

# q = pl.select()
# q = q.limit(10000)

p = 0.4
scale = scaler(p, cur_y)
with database.transaction() as t:
    p_count = 0
    for player in q:
        p_count += 1
        t = 0
        for s in player.seasons:
            # import pdb; pdb.set_trace()
            if not s.year or not s.av:
                continue
            t += scale(s.av, s.year)
        sys.stdout.write('.')
        if not p_count % 1000:
            sys.stdout.write(str(p_count))
        # sys.stdout.write(' ' + str(t) + ' ')
        player.weighted_av = t
        player.save()



