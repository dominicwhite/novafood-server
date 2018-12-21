from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from geoalchemy2 import Geometry

from app import db

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    restaurant_name = Column(String(64), index=True)
    location = Column(Geometry(geometry_type="POINT", management=True, use_st_prefix=False))


