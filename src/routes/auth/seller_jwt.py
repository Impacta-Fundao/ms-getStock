from flask import Blueprint, jsonify, request,make_response
from flask_jwt_extended import create_access_token
from src.Application.Service.seller_service import SellerService 

seller_jwt_bp = Blueprint('seller_jwt', __name__)

@seller_jwt_bp.route('/auth/login', methods=['POST'])
def login():    
    try:
        email_cadastrado = request.json.get("email", None)
        senha = request.json.get("senha", None)

        seller = SellerService.authenticate(email_cadastrado, senha)
        
        if seller is False:
            return make_response(jsonify({"message": "Login não autorizado - Mercado inativado"}), 401)
        elif seller:
            access_token = create_access_token(identity=str(seller.id))
            return jsonify({
                "access_token": access_token,
                "message": "Login realizado com sucesso",
                "seller_id": seller.id,
                "nome": seller.nome
                }), 200
        else:
            return make_response(jsonify({"message": "Login não autorizado - Email ou senha incorretos"}), 401)
    except Exception:
        return jsonify({"message": "Falha ao fazer autenticação - Verifique seu email ou senha"}), 400
