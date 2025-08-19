from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config_db.db import Config_db,Config_db_hml,Config_db_prd
from config import  Config

db = SQLAlchemy()

def create_app(config_class=Config_db_prd,):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from src.route import init_route
    init_route(app)
    return app