from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.config_db.db import Config_db, Config_db_hml, Config_db_prd
from flask_jwt_extended import JWTManager
from src.Infrastructure.auth.seller_jwt import jwt_service
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class=Config_db):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.config["JWT_SECRET_KEY"] = config_class.JWT_SECRET_KEY
    db.init_app(app)
    jwt_service.init_app(app)
    CORS(app)

    from src.routes.auth.seller_jwt import seller_jwt_bp
    from src.routes.auth.check_sms import sms_bp
    from src.routes.products.route import products_bp
    from src.routes.sales.route import sales_bp
    from src.routes.sellers.route import init_route
    app.register_blueprint(seller_jwt_bp)
    app.register_blueprint(sms_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(sales_bp)
    
    init_route(app)
    
    return app
