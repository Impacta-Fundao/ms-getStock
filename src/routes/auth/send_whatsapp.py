import os
from flask import Blueprint, jsonify, request
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
service_sid = os.environ["VERIFY_SERVICE_SID"]

client = Client(account_sid, auth_token)

send_whatsapp_bp = Blueprint('send_whatsapp', __name__)

@send_whatsapp_bp.route('/enviar_codigo', methods=['POST'])
def enviar_codigo():
    celular = request.json.get("celular", None)

    try:
        verification = client.verify.v2.services(service_sid
        ).verifications.create(
                to=f"+55{celular}",
                channel="sms"
        )
        return jsonify({"mensagem": "Código enviado com sucesso.", "status": verification.status}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@send_whatsapp_bp.route('/verificar_codigo', methods=['POST'])
def verificar_codigo():
    celular = request.json.get("celular", None)
    codigo = request.json.get("codigo", None)

    try:
        verification_check = client.verify.v2.services(service_sid
        ).verification_checks.create(
            to=f"+55{celular}",
            code=codigo
        )

        if verification_check.status == "approved":
            return jsonify({"mensagem": "Verificação concluída com sucesso"}), 200
        else:
            return jsonify({"mensagem": "Código inválido ou expirado"}), 401
    except:
        return jsonify({"mensagem": "Nenhum código foi solicitado ou você ja verificou"}), 400
