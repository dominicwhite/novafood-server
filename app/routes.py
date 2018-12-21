import random
from flask import json
from geoalchemy2 import functions, WKTElement
from sqlalchemy.sql import func
from geoalchemy2 import Geometry


from app import app
from app.models import Restaurant

@app.route("/<path:path>")
def home(path):
    geometry_type = Geometry(management=True, use_st_prefix=False)
    restaurants = Restaurant.query.filter(
        func.PtDistWithin(
            Restaurant.location,
            WKTElement('POINT(-77.088477, 38.864428)', srid=4326),
            100000000,
            type_=geometry_type)
    ).all()
    # restaurants = Restaurant.query.filter(Restaurant.location.Distance(WKTElement('POINT(-77.088477, 38.864428)')) < 100000).limit(10)

    restaurant_json = [{
        'name': r.restaurant_name,
        'coords': r.location.data
    } for r in restaurants]
    return json.jsonify(restaurant_json)
