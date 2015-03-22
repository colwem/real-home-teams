from minimal.models import *
import logging
import sys

logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('peewee.log', mode='w'))

pt = Player
hs = HighSchool
s = Stadium


sql = '''
select p.*
from players p
    join high_schools hs on hs.high_school_id = p.high_school_id
    join stadiums s on s.stadium_id = hs.closest_stadium_id
where p.pos like '%{position}%'
    and s.stadium_id = '{stadium_id}'
order by p.weighted_av desc;
'''

for stadium in Stadium.select():
    with database.transaction() as t:
        for pos in Position.select():
            q = (pt
                 .select()
                 .join(hs)
                 .join(s, on=hs.closest_stadium)
                 .where((pt.pos % '%{}%'.format(pos.name)) & (s.stadium == stadium))
                 .order_by(pt.weighted_av.desc()))

            for i, player in zip(range(3), q.iterator()):
                try:
                    StadiumPlayerPosition.create(
                        player_t=player,
                        stadium=stadium,
                        position=pos,
                        order=i)
                    sys.stdout.write('.')
                except Exception, e:
                    sys.stdout.write('x')
                    raise e

