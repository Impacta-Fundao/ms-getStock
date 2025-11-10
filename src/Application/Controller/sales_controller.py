from flask import request, jsonify, make_response
from src.Application.Service.sales_service import SaleService, SaleException

class SaleController:
    @staticmethod
    def post_sale():
        try:
            data = request.get_json()
            sale = SaleService.realizar_venda(data)           
            return make_response(jsonify({"data": sale, "message": "Venda realizada com sucesso"}), 200)
        except SaleException as e:
            return make_response(jsonify({"message": f"Erro ao realizar venda: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def get_sales():
        try:
            data = SaleService.listar_vendas()
            return make_response(jsonify({"data": data}), 200)
        except SaleException as e:
            return make_response(jsonify({"message": f"Erro ao listar vendas: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
        
    @staticmethod
    def get_sale_id(venda_id):
        try:
            data = SaleService.listar_venda_id(venda_id)
            return make_response(jsonify({"data": data}), 200)
        except SaleException as e:
            return make_response(jsonify({"message": f"Erro ao buscar venda: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
