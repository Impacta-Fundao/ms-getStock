from flask import Blueprint, request, jsonify, make_response
from src.Application.Service.seller_service import SellerService, SmsException

sms_bp = Blueprint('sms', __name__)

@sms_bp.route('/mercados/verificar_codigo', methods=['POST'])
def verificar_codigo():
    try:
        data = request.get_json()
        SellerService.verificar_sms(data)
        return jsonify({"message": "Verificação concluída. Mercado ativado com sucesso!"}), 200
    except SmsException as e:
        return make_response(jsonify({"message": f"Erro ao ativar mercado: {str(e)}"}), 400)
    except Exception as e:
        return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
