import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.event import listens_for
from sqlalchemy.sql import select, func

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app)
db = SQLAlchemy(app)

@listens_for(db.engine, "connect")
def load_spacialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension(os.getenv('SPATIALITE_LIBRARY_PATH','/usr/lib/x86_64-linux-gnu/mod_spatialite.so'))
    print(db.app)
db.engine.execute(select([func.InitSpatialMetaData(1)]))

from app import routes, models
