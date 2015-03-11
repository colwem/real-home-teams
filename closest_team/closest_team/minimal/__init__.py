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
    p, hs = m.PlayersT, m.HighSchoolT
    p = p.select(
        p.name,
        m.HighSchoolT.latitude,
        m.HighSchoolT.longitude).join(
        m.HighSchoolT).where(
            m.HighSchoolT.latitude != None,
            m.HighSchoolT.longitude != None).naive().limit(10)
    s = m.Stadium.select()
    t = render_template('players.html', players=p, stadiums=s)
    return t


@app.route('/players.json')
def players():
    p, hs = m.PlayersT, m.HighSchoolT
    q = (p.select(p.name, p.weighted_av, hs.latitude, hs.longitude)
         .join(hs)
         .where(hs.latitude != None, hs.longitude != None, p.weighted_av > 0.1)
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
             "coordinates": [s.longitude, s.latitude],
             "av": randint(80,120)})
    stadiums.sort(key=lambda a: a['abbr'])
    # import pdb; pdb.set_trace()
    json = {"stadiums": stadiums}
    return jsonify(json)
# @app.route('/player-map')
# def player_map():
    # PlayerT.select(PlayerT.name, PlayerT.high_school


if __name__ == '__main__':
    app.debug = True
    app.run()
