from flask_jwt_extended import JWTManager

class JWTService:
    def __init__(self):
        self.jwt = JWTManager()
        
    def init_app(self,app):
        self.jwt.init_app(app)
        
jwt_service = JWTService()