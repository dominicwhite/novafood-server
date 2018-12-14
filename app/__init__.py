import random
import sqlite3

from flask import Flask, g, json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from sqlalchemy.sql import select, func
#from flask_migrate import Migrate

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

@listens_for(db.engine, "connect")
def load_spacialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension('/usr/lib/x86_64-linux-gnu/mod_spatialite.so')
db.engine.execute(select([func.InitSpatialMetaData(1)]))
#migrate = Migrate(app, db)

from app import routes, models

@app.before_first_request
def init_request():
    db.create_all()
