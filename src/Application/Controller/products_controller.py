from flask import request, jsonify, make_response
from src.Application.Service.products_service import ProductService, ProductException

class ProductController:
    @staticmethod
    def post_product():
        try:
            data = request.get_json()
            produto = ProductService.cadastrar_produto(data)
            return make_response(jsonify({"data": produto, "message": "Produto cadastrado com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao cadastrar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def get_products():
        try:
            data = ProductService.listar_produtos()
            return make_response(jsonify({"data": data}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao listar produtos: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def get_product_id(produto_id):
        try:
            data = ProductService.listar_produto_id(produto_id)
            return make_response(jsonify({"data": data}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao buscar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def delete_product(produto_id):
        try:
            ProductService.deletar_produto(produto_id)
            return make_response(jsonify({"data": "Produto removido com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao deletar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def put_product(produto_id):
        try:
            data = request.get_json()
            update_product = ProductService.atualizar_produto(produto_id, data)
            return make_response(jsonify({"data": update_product, "message": "Produto atualizado com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao atualizar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def patch_product(produto_id):
        try:
            data = request.get_json()
            update_patch_product = ProductService.atualizar_patch_produto(produto_id, data)
            return make_response(jsonify({"data": update_patch_product, "message": "Produto atualizado com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao atualizar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def activate_product(produto_id):
        try:
            ProductService.ativar_produto(produto_id)
            return make_response(jsonify({"data": "Produto ativado com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao ativar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def inactivate_product(produto_id):
        try:
            ProductService.inativar_produto(produto_id)
            return make_response(jsonify({"data": "Produto inativado com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao inativar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
