from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config_db.db import Config_db,Config_db_hml,Config_db_prd
from config import  Config
from flask_jwt_extended import JWTManager
from src.Infrastructure.auth.seller_jwt import jwt_service

db = SQLAlchemy()

def create_app(config_class=Config_db,):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["JWT_SECRET_KEY"] = Config_db.JWT_SECRET_KEY
    db.init_app(app)
    jwt_service.init_app(app)

    from src.routes.auth.seller_jwt import seller_jwt_bp
    from src.routes.sellers.route import init_route
    app.register_blueprint(seller_jwt_bp)    
    
    init_route(app)
    return app