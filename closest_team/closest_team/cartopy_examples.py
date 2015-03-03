import siteconfig
import peewee
from peewee import *
from models import *
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import models
from cartopy.io.img_tiles import MapQuestOpenAerial
import cartopy.io.shapereader as shpreader
import random

siteconfig.update_config(cartopy.config)

gd = ccrs.Geodetic()
# tiler = MapQuestOpenAerial()
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()
extents = (-65, -125, 20, 55 )
ax.set_extent(extents, gd)
# ax.add_image(tiler, 1)
shpfilename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='50m',
                                     category='cultural',
                                     name=shpfilename)

colors = ['green', 'blue', 'red', 'yellow', 'orange', 'cyan', 'tan', 'grey']
for shape in shpreader.Reader(states_shp).geometries():
    facecolor = random.choice(colors)
    print facecolor
    edgecolor = 'black'
    ax.add_geometries([shape],ccrs.PlateCarree(), facecolor=facecolor, edgecolor=edgecolor)

q = Stadium.select()
for s in q:
    plt.plot(float(s.longitude), float(s.latitude), marker='o', color='blue',
             transform=gd)
    plt.text(float(s.longitude) - 2, float(s.latitude) - 0.2, s.name,
             transform=gd, stretch=1, weight=1000)

plt.show()
