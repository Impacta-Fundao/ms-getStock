import os
from flask import Blueprint, jsonify, request
from twilio.rest import Client
from src.Application.Service.seller_service import SellerService
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
service_sid = os.environ["VERIFY_SERVICE_SID"]

client = Client(account_sid, auth_token)

send_sms_bp = Blueprint('send_sms', __name__)

@send_sms_bp.route('/enviar_codigo', methods=['POST'])
def enviar_codigo():
    celular = request.json.get("celular", None)

    verificar_num = SellerService.verificar_numero(celular)

    if verificar_num:
        try:
            verification = client.verify.v2.services(service_sid
            ).verifications.create(
                    to=f"+55{celular}",
                    channel="sms"
            )
            return jsonify({"mensagem": "Código enviado com sucesso.", "status": verification.status}), 200
        except Exception as e:
            return jsonify({"erro": e.args}), 400
    elif verificar_num is False:
        return jsonify({"erro": "O usuário já se encontra ativado"}), 400
    else:
        return jsonify({"erro": "O número informado não existe no banco de dados"}), 400


@send_sms_bp.route('/verificar_codigo', methods=['POST'])
def verificar_codigo():
    celular = request.json.get("celular", None)
    codigo = request.json.get("codigo", None)

    verificar_num = SellerService.verificar_numero(celular)

    if verificar_num:
        try:
            verification_check = client.verify.v2.services(service_sid
            ).verification_checks.create(
                to=f"+55{celular}",
                code=codigo
            )

            if verification_check.status == "approved":
                ativar_usuario = SellerService.ativar_usuario(celular)
                return jsonify({"mensagem": "Verificação concluída. Usuário ativo com sucesso", "status": ativar_usuario}), 200
            else:
                return jsonify({"mensagem": "Código inválido ou expirado"}), 401
        except:
            return jsonify({"mensagem": "Nenhum código foi solicitado ou você ja verificou o número"}), 400
    elif verificar_num is False:
        return jsonify({"erro": "O usuário já se encontra ativado"}), 400
    else:
        return jsonify({"erro": "O número informado não existe no banco de dados"}), 400
