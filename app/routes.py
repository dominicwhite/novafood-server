import random
from flask import json
from geoalchemy2 import functions, WKBElement, WKTElement
from sqlalchemy.sql import func
from geoalchemy2 import Geometry, shape

from shapely.geometry import Point

from app import app, db
from app.models import Restaurant

@app.route("/<path:path>")
def home(path):
    geometry_type = Geometry(management=True, use_st_prefix=False)
    restaurants = Restaurant.query.filter(
        func.PtDistWithin(
            Restaurant.location,
            WKTElement('POINT(38.864428 -77.088477)', srid=4326),
            10000000000000,
            type_=geometry_type
        )
    ).all()
    restaurant_json = [{
        'name': r.restaurant_name,
        'coords': r.location.data
    } for r in restaurants]
    return json.jsonify(restaurant_json)
