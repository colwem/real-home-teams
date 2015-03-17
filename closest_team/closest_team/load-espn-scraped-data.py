#!/usr/bin/env python
from minimal.models import *
from tablemaker import Table
import json


def monkeypatch(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


@monkeypatch(file)
def jsonlines(self):
    for l in self.readlines():
        yield json.loads(l)

roster = Table('espn_roster_players')
depth = Table('espn_depth_positions')

with open('file', 'r') as fh:
    for d in fh.jsonlines():
        table = depth if d.has_key('formation') else roster
        for k, v in d.items():
            if k == 'NO':
                v = '' if v == '--' else v
            if k == 'HT':
                ft, inches = v.split('-')
                v = str(int(ft) * 12 + int(inches))
            if k == 'EXP':
                v = '0' if v == 'R' else v
            col = table.column_for(k.lower())
            col.add_example(v)

roster.add_primary_key()
depth.add_primary_key()

print roster.to_definition()
print depth.to_definition()

with database.transaction() as t:
    for d in load_json():
        table = EspnDepthPosition if d.has_key('formation') else EspnRosterPlayer
        if d.has_key('NO'):
            d['NO'] = '' if d['NO'] == '--' else d['NO']
        if d.has_key('HT'):
            v = d['HT']
            ft, inches = v.split('-')
            d['HT'] = str(int(ft) * 12 + int(inches))
        if d.has_key('EXP'):
            v = d['EXP']
            d['EXP'] = '0' if v == 'R' else v
        if d.has_key('2nd'):
            d['second'] = d['2nd']
            del d['2nd']
        if d.has_key('3rd'):
            d['third'] = d['3rd']
            del d['3rd']
        if d.has_key('4th'):
            d['fourth'] = d['4th']
            del d['4th']
        d = {k.lower(): v for k, v in d.items() if v}
        table.insert(**d).execute()
