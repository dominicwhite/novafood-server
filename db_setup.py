from sqlalchemy import create_engine
from sqlalchemy.event import listen
import os

DB_NAME = 'gis.db'

def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension(os.getenv('SPATIALITE_LIBRARY_PATH','/usr/lib/x86_64-linux-gnu/mod_spatialite.so'))

import os
if DB_NAME in os.listdir(os.getcwd()):
    os.remove('gis.db')

engine = create_engine('sqlite:///' + DB_NAME, echo=True)
listen(engine, 'connect', load_spatialite)
conn = engine.connect()
from sqlalchemy.sql import select, func
conn.execute(select([func.InitSpatialMetaData(1)]))
conn.close()

from app.models import Restaurant, Inspection

Restaurant.__table__.create(engine)
Inspection.__table__.create(engine)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

import datetime

def parse_date(ts):
    d = ts[:ts.find(' ')]
    return datetime.datetime.strptime(d, '%m/%d/%Y')

data_dict = {}

import csv
with open('geocoded.csv', 'r') as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        data_dict[row['UNID']] = {
            'id': idx + 1,
            'street': row['fullstreet'],
            'city': row['PCITY'],
            'state': row['PSTATE'],
            'zip': row['PCODE'],
            'lat': row['Latitude'],
            'lon': row['Longitude'],
            'inspections': {}
        }

with open('inspections.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['UNID'] not in data_dict:
            continue
        data_dict[row['UNID']]['status'] = row['STAGE']
        data_dict[row['UNID']]['name'] = row['NAME']
        if row['INSPNO'] in data_dict[row['UNID']]['inspections']:
            inspection_dict = data_dict[row['UNID']]['inspections'][row['INSPNO']]
            inspection_dict['codes'] = inspection_dict['codes'] + '; ' + row['CODE']
            inspection_dict['violation_count'] += 1
        else:
            inspection_dict = {'codes': row['CODE'], 'violation_count': 1}
            inspection_dict['comment'] = row['COMM']
            inspection_dict['date'] = parse_date(row['EDATE'])
        data_dict[row['UNID']]['inspections'][row['INSPNO']] = inspection_dict

restaurants_to_load = []
inspections_to_load = []
for k in data_dict.keys():
    r = data_dict[k]
    if r['status'] != 'Active':
        continue
    restaurants_to_load.append(
        Restaurant(
            id=r['id'],
            restaurant_name=r['name'],
            street=r['street'],
            city=r['city'],
            state=r['state'],
            zip=r['zip'],
            source_id=k,
            location=f'POINT({r["lon"]} {r["lat"]})',

        )
    )
    for i_k in r['inspections'].keys():
        i = r['inspections'][i_k]
        inspections_to_load.append(Inspection(
            restaurant_id=r['id'],
            source_id=i_k,
            year=i['date'].year,
            month=i['date'].month,
            day=i['date'].day,
            codes=i['codes'],
            comment=i['comment']
        ))

session.add_all(restaurants_to_load)
session.add_all(inspections_to_load)
session.commit()

from geoalchemy2 import functions

q = session.query(Restaurant, functions.ST_X(Restaurant.location), functions.ST_Y(Restaurant.location)).limit(3)
for r in q:
    print(r)
    print(r[0])
    print(r[0].restaurant_name)

q2 = session.query(Inspection).limit(3)
for r in q2:
    print(r)
    print(r.restaurant.restaurant_name)
    print(r.source_id)

