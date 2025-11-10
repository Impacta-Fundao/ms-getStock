from flask import Blueprint, request, jsonify, make_response
from src.Application.Service.seller_service import SellerService, AuthException

seller_jwt_bp = Blueprint('seller_jwt', __name__)

@seller_jwt_bp.route('/auth/login', methods=['POST'])
def login():    
    try:
        data = request.get_json()
        token, id_mercado = SellerService.authenticate(data)
        return make_response(jsonify({"access_token": token, "seller_id": id_mercado, "message": "Login realizado com sucesso"}), 200)
    except AuthException as e:
        return make_response(jsonify({"message": f"Falha ao fazer autenticação: {str(e)}"}), 400)
    except Exception as e:
        return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
