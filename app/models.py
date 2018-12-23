from geoalchemy2 import Geometry

from app import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(128), index=True)
    street = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zip = db.Column(db.String(5))
    source_id = db.Column(db.String(32), index=True)
    location = db.Column(Geometry(geometry_type="POINT", management=True, use_st_prefix=False))
    inspections = db.relationship('Inspection', backref='restaurant', lazy=True)

class Inspection(db.Model):
    __tablename__ = 'inspections'
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False, index=True)
    source_id = db.Column(db.String(32))
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    codes = db.Column(db.String)
    comment = db.Column(db.String)

