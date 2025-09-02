from flask_jwt_extended import JWTManager

class JWTService:
    def __init__(self):
        self.jwt = JWTManager()
        
    def init_app(self,app):
        self.jwt.init_app(app)
        self._regiser_callbacks()
        
    def _register_callbacks(self):
        @self.jwt.user_identity_loader
        def identidade_do_usuario(user):
            return user.id
        
        @self.jwt.user_lookup_loader
        def usuario_por_identidade(_jwt_header, jwt_data):
            from src.Infrastructure.models.seller import Mercado
            identity = jwt_data["sub"]
            return Mercado.query.get(identity)
jwt_service = JWTService()