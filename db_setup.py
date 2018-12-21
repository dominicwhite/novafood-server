from sqlalchemy import create_engine
from sqlalchemy.event import listen

DB_NAME = 'gis.db'

def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')

import os
if DB_NAME in os.listdir(os.getcwd()):
    os.remove('gis.db')

engine = create_engine('sqlite:///' + DB_NAME, echo=True)
listen(engine, 'connect', load_spatialite)
conn = engine.connect()
from sqlalchemy.sql import select, func
conn.execute(select([func.InitSpatialMetaData(1)]))
conn.close()

from app.models import Restaurant

Restaurant.__table__.create(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# r = Restaurant(restaurant_name="Test McDonalds", location='POINT(1 1)')
# session.add(r)

import json
with open('all_data.json') as f:
    data = json.load(f)
    restaurant_data = data['restaurants']
    data_to_load = []
    # x = 0
    for r in restaurant_data:
        data_to_load.append(
            Restaurant(id=r['id'], restaurant_name=r['name'], location=f'POINT({r["long"]} {r["lat"]})')
        )
        # x += 1
        # if x > 10: break

session.add_all(data_to_load)
session.commit()

from geoalchemy2 import functions

q = session.query(Restaurant, functions.ST_X(Restaurant.location), functions.ST_Y(Restaurant.location)).limit(3)
for r in q:
    print(r)
    print(r[0])
    print(r[0].restaurant_name)