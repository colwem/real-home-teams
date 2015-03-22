from models import *
import numpy as np


pmf = lambda p, k: p * (1 - p) ** k
def scaler(p, year):
    return lambda av, y: av * pmf(p, year - y)

ps = PlayerSeasons
cur_y = ps.select(fn.Max(ps.year).alias('max')).first().max

p = 0.4
scale = scaler(p, cur_y)
for player in Player.select():
    t = 0
    for s in player.seasons():
        t += scale(s.av, s.year)
    import pudb; pudb.set_trace()  # XXX BREAKPOINT
    player.weighted_av = t
    player.save()


get all seasons for each player
get their av

