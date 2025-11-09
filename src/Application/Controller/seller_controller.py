from flask import request, jsonify, make_response
from src.Application.Service.seller_service import SellerService, MercadoException

class SellerController:
    @staticmethod
    def post_seller():
        try:
            data = request.get_json()
            seller = SellerService.create_seller(data)           
            return make_response(jsonify({"data": seller, "message": "Mercado criado com sucesso", "verification": "Código para ativação enviado por SMS"}), 200)
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
            return make_response(jsonify({"data": data}), 200)
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao buscar mercado: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
    
    @staticmethod
    def delete_seller(mercado_id):
        try:
            SellerService.deletar_mercado(mercado_id)
            return make_response(jsonify({"message": "Mercado inativado com sucesso"}), 200)
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao deletar mercado: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
        
    @staticmethod
    def put_seller(mercado_id):
        try:
            data = request.get_json()
            update_seller = SellerService.atualizar_mercado(mercado_id, data)
            return make_response(jsonify({"data": update_seller, "message": "Mercado atualizado com sucesso"}), 200)
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao atualizar mercado: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
    
    @staticmethod
    def patch_seller(mercado_id):
        try:
            data = request.get_json()
            update_patch_seller = SellerService.atualizar_patch_mercado(mercado_id, data)
            return make_response(jsonify({"data": update_patch_seller, "message": "Mercado atualizado com sucesso"}), 200)
        except MercadoException as e:
            return make_response(jsonify({"message": f"Erro ao atualizar mercado: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
