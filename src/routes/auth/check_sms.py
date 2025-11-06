from flask import Blueprint, jsonify, request
from src.Application.Service.seller_service import SellerService
from src.Application.Controller.seller_controller import client, service_sid

sms_bp = Blueprint('sms', __name__)

@sms_bp.route('/mercados/verificar_codigo', methods=['POST'])
def verificar_codigo():
    celular = request.json.get("celular", None)
    codigo = request.json.get("codigo", None)

    status_mercado = SellerService.verificar_status_mercado(celular)

    if status_mercado is True:
        return jsonify({"erro": "O mercado já se encontra ativado"}), 400
    elif status_mercado is False:
        try:
            verification_check = client.verify.v2.services(service_sid).verification_checks.create(
                to=f"+55{celular}",
                code=codigo)

            if verification_check.status == "approved":
                mercado = SellerService.ativar_mercado(celular)
                return jsonify({"mensagem": "Verificação concluída. Mercado ativado com sucesso!", "status": mercado}), 200
            else:
                return jsonify({"mensagem": "Código inválido ou expirado"}), 401
        except:
            return jsonify({"mensagem": "Nenhum código foi solicitado ou você ja verificou este número"}), 400        
    else:
        return jsonify({"erro": "O número informado não existe cadastrado em nenhum mercado"}), 400
