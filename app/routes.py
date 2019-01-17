from flask import json, request
from geoalchemy2 import WKTElement
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

from app import app, db
from app.models import Restaurant, Inspection

def get_data_from_db(filter_by, lat, lon, count, radius):
    # TODO: filter by best & worst as well. Requires some measure of "goodness" and its calculation either during the
    #  query or during the ETL process
    geometry_type = Geometry(management=True, use_st_prefix=False)
    if filter_by == "recent":
        restaurants = db.session.query(Restaurant, func.ST_X(Restaurant.location), func.ST_Y(Restaurant.location), Inspection).filter(
            func.PtDistWithin(
                Restaurant.location,
                WKTElement(f'POINT({lon} {lat})', srid=4326),
                radius,
                type_=geometry_type
            )
        ).filter(
            Restaurant.id == Inspection.restaurant_id
        ).order_by(
            -Inspection.year, -Inspection.month, -Inspection.day
        ).limit(count)
        return restaurants
    restaurants = db.session.query(Restaurant, func.ST_X(Restaurant.location), func.ST_Y(Restaurant.location)).filter(
        func.PtDistWithin(
            Restaurant.location,
            WKTElement(f'POINT({lon} {lat})', srid=4326),
            radius,
            type_=geometry_type
        )
    ).order_by(
        func.ST_Distance(
            Restaurant.location,
            WKTElement(f'POINT({lon} {lat})', srid=4326)
        )
    ).limit(count)
    return restaurants


@app.route("/restaurants/")
def restaurants_view():
    lat = request.args.get('lat', default=38.864428, type=float)
    lon = request.args.get('lon', default=-77.088477, type=float)
    count = request.args.get('count', default=10, type=int)
    radius = request.args.get('radius', default=100, type=int)
    filter_by = request.args.get('filter_by', default='distance', type=str)
    restaurants = get_data_from_db(filter_by, lat, lon, count, radius)
    restaurant_json = [{
        'id': r[0].id,
        'name': r[0].restaurant_name,
        'long': r[1],
        'lat': r[2]
    } for r in restaurants]
    return json.jsonify({'restaurants': restaurant_json})

@app.route('/restaurants/<int:id>/inspections/')
def inspections_view(id):
    inspection_data = []
    inspections = Inspection.query.filter_by(restaurant_id=id).order_by(
        -Inspection.year, -Inspection.month, -Inspection.day
    ).all()
    for i in inspections:
        inspection_data.append({
            'year': i.year,
            'month': i.month,
            'day': i.day,
            'codes': i.codes,
            'comment': i.comment
        })
    return json.jsonify(inspection_data)