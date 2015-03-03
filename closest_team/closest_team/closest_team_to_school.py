from geopy.distance import vincenty
from models import *
import sys

stadiums = list(Stadium.select())
schools = HighSchoolT.select().where(HighSchoolT.latitude != None,
                                     HighSchoolT.longitude != None)
for school in schools:
    min_d = 999999999
    min_stadium = None
    school_loc = (school.latitude, school.longitude)
    for stadium in stadiums:
        sys.stdout.write('.')
        stadium_loc = (stadium.latitude, stadium.longitude)
        distance = vincenty(school_loc, stadium_loc).miles
        if distance < min_d:
            sys.stdout.write('+')
            min_d = distance
            min_stadium = stadium
    if min_stadium:
        sys.stdout.write('!=!')
        school.closest_stadium = min_stadium
        school.save()

