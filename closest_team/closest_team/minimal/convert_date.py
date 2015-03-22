from models import *
from datetime import datetime
from playhouse.shortcuts import model_to_dict
import sys

for p in Player.select().iterator():
    try:
        p.birthday_date = datetime.strptime(p.birthday, "%B %d, %Y")
    except ValueError, e:
        sys.stderr.write(str(model_to_dict(p)))
    else:
        # print model_to_dict(p)
        sys.stdout.write('.')
        p.save()

