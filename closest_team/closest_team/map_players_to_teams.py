import peewee
from peewee import *
from models import *
import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import models
from cartopy.io.img_tiles import MapQuestOpenAerial
import cartopy.io.shapereader as shpreader
import random
import siteconfig

siteconfig.update_config(cartopy.config)

gd = ccrs.Geodetic()
tiler = MapQuestOpenAerial()
ax = plt.axes(projection=tiler.crs)
ax.stock_img()
extents = (-58, -125, 22, 50 )
ax.set_extent(extents, gd)
ax.add_image(tiler, 5)

shpfilename = 'admin_1_states_provinces_lakes_shp'
states_shp = shpreader.natural_earth(resolution='50m',
                                     category='cultural',
                                     name=shpfilename)

colors = ['green', 'blue', 'red', 'yellow', 'orange', 'cyan', 'tan', 'grey']
for shape in shpreader.Reader(states_shp).geometries():
    facecolor = random.choice(colors)
    edgecolor = 'black'
    ax.add_geometries([shape],ccrs.PlateCarree(), facecolor=facecolor,
                      edgecolor=edgecolor, alpha=0.5)

q = Stadium.select()
pe = [path_effects.withSimplePatchShadow(offset=(0,0), rho=2, alpha=1),
      path_effects.withStroke(linewidth=3, foreground='#222222')]
for s in q:
    plt.plot(float(s.longitude), float(s.latitude), marker='o', color='blue',
             transform=gd)

    plt.text(float(s.longitude), float(s.latitude) - 0.4, s.name,
             fontsize=12, weight=500, va='center', ha='center', color='#EEEEEE',
             transform=gd, path_effects=pe)

plt.show()
