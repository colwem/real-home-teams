from minimal.models import *
from pprint import pprint as pp
import logging
import sys
import json

logging.basicConfig(filename="aptp.log", level=logging.INFO)
info = logging.info
warn = logging.warning

db = database
pt = Players

with db.transaction() as t:
    with open('playerpos.json', 'r') as fh:
        for l in fh.readlines():
            js = json.loads(l)
            try:
                player = pt.get(pt.pfr_player_id == js['id'])
            except Exception, e:
                print e.message
                warn(e.message + str(js))
                continue

            player.pos = js['pos']
            try:
                sys.stdout.write('.')
                player.save()
                info(js)
            except:
                sys.stdout.write('x')
                warn(js)



# map
# te te te
# p p p
# ss s db
# k k k
# slb olb lb
# wr wr
# fs s db
# rcb cb db
# c c ol
# rt t ol
# rg g ol
# lg g ol
# lt t ol
# jlb ilb lb
# wlb olb lb
# lde de dl
# rde de dl
# rg/rt null ol
# qb qb qb
# s s db
# ilb
# fb
# wr/r
# cb
# dl
# lb
# nt
# te/wr
# llb
# lg/lt
# db
# lb/mlb
# lcb
# lolb
# mlb
# will
# olb
# rdt
# lb/rcb
# rolb
# de/dt/nt
# rb
# dt
# de
# s/slb/ss
# sam
# rolb/ss
# lde/rde
# ds/rcb
# fs/ss
# cb/lcb/rcb
# c/rg/te
# de/nt
# lb/olb
# ldt
# rt/te
# nb/s
# lg/rg/rt
# lg/rg
# db,cb
# lg/rt
# dt/nt
# db/lcb
# lt/rt
# olb,lb
# lilb
# s/ss
# mlb/slb/wlb
# lg/lg/lt/rg/rt
# ls
# cb/db/lcb
# cb/db
# slb/wlb
# ot/rt/t
# h-b
# te/l
# fs/s
# fb/te
# fs/s/ss
# lcb/nb/rcb
# cb/lcb/ss
# rde/rdt
# jlb/mlb
# jack
# fs/lcb
# ldt/rdt
# cb/lcb
# t
# cb/nb
# lde,dl
# lb/slb
