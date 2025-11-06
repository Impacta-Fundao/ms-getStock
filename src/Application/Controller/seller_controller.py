import os
from flask import request, jsonify, make_response
from src.Application.Service.seller_service import SellerService, MercadoException
from src.Domain.seller import SellerDomain
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
service_sid = os.environ["VERIFY_SERVICE_SID"]

client = Client(account_sid, auth_token)

class SellerController:
    @staticmethod
    def post_seller():
        try:
            data = request.get_json()
            requiredField = []
            
            domain = SellerDomain(
                nome = data['nome'] if data.get('nome') else None,
                cnpj = data.get('cnpj') if data.get('cnpj') else None,
                email = data.get('email') if data.get('email') else None,
                celular = data.get('celular') if data.get('celular') else None,
                senha = data.get('senha') if data.get('senha') else None,
                )
            
            requiredField.append({"nome": domain.nome, "cnpj": domain.cnpj, "email": domain.email, "celular": domain.celular, "senha": domain.senha})
            for field in requiredField:
                for k, v in field.items():
                    if v is None:
                        return make_response(jsonify({"message": f"Passe um valor para o campo {k}"}), 400)

            seller = SellerService.create_seller(domain)

            client.verify.v2.services(service_sid).verifications.create(to=f"+55{domain.celular}", channel="sms")
            
            return make_response(jsonify({ 
                "data": seller.to_dict(),
                "message": "Mercado criado com sucesso",
                "verification": "Código para ativação enviado por SMS"
                    }), 200)
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro na requisição: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
        
    @staticmethod
    def get_sellers():
        try:
            data = SellerService.listar_mercados()
            return make_response(jsonify({"data": data}), 200)
        
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao listar mercados: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
        
    @staticmethod
    def get_seller_id(mercado_id):
        try:
            data = SellerService.get_id(mercado_id)
            if not data:
                return make_response(jsonify({"message": "Não existe esse mercado cadastrado"}), 400)
            return make_response(jsonify({"data": data}), 200)
            
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao buscar mercado: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
    
    @staticmethod
    def delete_seller(mercado_id):
        try:
            data = SellerService.deletar_mercado(mercado_id)
            if not data:
                return make_response(jsonify({"message": "Não existe esse mercado cadastrado"}), 400)
            return make_response(jsonify({"data": data}), 200)
            
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao deletar mercado: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
        
    @staticmethod
    def put_seller(mercado_id):
        try:
            resp = request.get_json()
            
            if not resp:
                return make_response(jsonify({"error": "Nenhum dado fornecido"}), 400)
            
            update_seller = SellerService.atualizar_patch_mercado(mercado_id,resp)
            
            return make_response(jsonify({"data": update_seller, "message": "Mercado atualizado com sucesso"}), 200)
            
        except MercadoException as e:
            return make_response(jsonify({"message": f"{str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
    
    @staticmethod
    def patch_seller(mercado_id):
        try:
            resp = request.get_json()
            
            if not resp:
                return make_response(jsonify({"error": "Nenhum dado fornecido"}), 400)
            
            update_seller = SellerService.atualizar_patch_mercado(mercado_id, resp)
            
            return make_response(jsonify({"data": update_seller, "message": "Mercado atualizado com sucesso"}), 200)
            
        except MercadoException as e:
            return make_response(jsonify({"message": f"{str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
