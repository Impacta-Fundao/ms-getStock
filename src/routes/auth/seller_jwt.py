from flask import Blueprint, jsonify, request,make_response
from flask_jwt_extended import create_access_token
from src.Application.Service.seller_service import SellerService 

seller_jwt_bp = Blueprint('seller_jwt', __name__)

@seller_jwt_bp.route('/login', methods=['POST'])
def login():    
    try:
        username = request.json.get("email", None)
        password = request.json.get("senha", None)

        seller = SellerService.authenticate(username,password)
        
        if seller:
            access_token = create_access_token(identity=str(seller.id))
            return jsonify({
                "access_token":access_token,
                "message":"Login realizado com sucesso",
                "seller_id": seller.id,
                "nome": seller.nome
                }),200
        else:
            return make_response(jsonify({"message": "Usuário não autorizado - Email ou senha incorretos"}), 401)
    except Exception:
        return jsonify({"message": "Falha ao fazer autenticação: verifique seu email ou sua senha"}),400
