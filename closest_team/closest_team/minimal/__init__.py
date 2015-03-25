import sys
from flask import Flask, render_template, jsonify
import models as m
from os import path
from random import randint

tmpl_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/map')
def player():
    p, hs = m.Player, m.HighSchool
    p = p.select(
        p.name,
        m.HighSchool.latitude,
        m.HighSchool.longitude).join(
        m.HighSchool).where(
            m.HighSchool.latitude != None,
            m.HighSchool.longitude != None).naive().limit(10)
    s = m.Stadium.select()
    t = render_template('players.html', players=p, stadiums=s)
    return t


@app.route('/high_schools.json')
def high_schools():
    P, HS = m.Player, m.HighSchool

    q = (HS.select(HS, P)
         .join(P)
         .where(HS.found == True, P.active == True)
         .order_by(HS.high_school, P.weighted_av.desc())
         .aggregate_rows())

    json = []
    for hs in q:
        players = [{"name": p.name,
                    "weighted_av": p.weighted_av}
                   for p in hs.players]
        if players:
            json.append({"name": hs.name,
                         "coordinates": [hs.longitude, hs.latitude],
                         "av": sum([p["weighted_av"] for p in players]),
                         "players": players})
    return jsonify({"high_schools": json})

@app.route('/players.json')
def players():
    p, hs = m.Player, m.HighSchool
    q = (p.select(p.name, p.weighted_av, hs.latitude, hs.longitude)
         .join(hs)
         .where(hs.latitude != None, hs.longitude != None, p.active == True)
         .order_by(p.weighted_av)
         .naive())
         #.limit(1000))

    json = [{"name": p.name,
             "weighted_av": p.weighted_av,
             "coordinates": [p.longitude, p.latitude]} for p in q]
    json = {"players": json}
    return jsonify(json)


@app.route('/voronoi')
def voronoi():
    stadiums = m.Stadium.select()
    for s in stadiums:
        print s
    t = render_template('voronoi.html', stadiums=stadiums)
    return t


@app.route('/stadiums.json')
def stadiums():
    stadiums = []
    for s in m.Stadium.select():
        stadiums.append(
            {"name": s.name,
             "team": s.teams[0].name,
             "abbr": s.teams[0].abbr,
             "pri_color": s.teams[0].pri_color,
             "sec_color": s.teams[0].sec_color,
             "coordinates": [s.longitude, s.latitude]})
    stadiums.sort(key=lambda a: a['abbr'])
    # import pdb; pdb.set_trace()
    json = {"stadiums": stadiums}
    return jsonify(json)

if __name__ == '__main__':
    app.debug = True
    app.run()
