from geoalchemy2 import Geometry

from app import db

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(64), index=True)
    location = db.Column(Geometry(geometry_type="Point", management=True, use_st_prefix=False))

