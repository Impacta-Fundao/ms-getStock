from flask import request, jsonify, make_response
from src.Application.Service.products_service import ProductService, ProductException
from src.Domain.product import ProductDomain

class ProductController:
    
    @staticmethod
    def post_product():
        try:
            data = request.get_json()
            requiredField = []
            
            domain = ProductDomain(
                nome = data['nome'] if data.get('nome') else None,
                preco = data.get('preco') if data.get('preco') else None,
                quantidade = data.get('quantidade') if data.get('quantidade') else None,
                imagem = data.get('imagem') if data.get('imagem') else None
                )
            
            requiredField.append({"nome": domain.nome, "preco": domain.preco, "quantidade": domain.quantidade, "imagem": domain.imagem})
            for field in requiredField:
                for k, v in field.items():
                    if v is None:
                        return make_response(jsonify({"message": f"Passe um valor para o campo {k}"}), 400)

            produto = ProductService.cadastrar_produto(domain)
            
            return make_response(jsonify({ 
                "data": produto.to_dict(),
                "message": "Produto cadastrado com sucesso"
                }), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro na requisição: {str(e)}"}), 400)
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
            data = ProductService.get_id(produto_id)
            if data:
                return make_response(jsonify({"data": data}), 200)
            
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao buscar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def delete_product(produto_id):
        try:
            data = ProductService.deletar_produto(produto_id)
            if data:
                return make_response(jsonify({"data": "Produto removido com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao deletar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def put_product(produto_id):
        try:
            resp = request.get_json()

            if not resp:
                return make_response(jsonify({"error": "Nenhum dado fornecido"}), 400)

            update_product = ProductService.atualizar_patch_produto(produto_id, resp)

            return make_response(jsonify({"data": update_product, "message": "Produto atualizado com sucesso"}), 200)

        except ProductException as e:
            return make_response(jsonify({"message": f"{str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def patch_product(produto_id):
        try:
            resp = request.get_json()

            if not resp:
                return make_response(jsonify({"error": "Nenhum dado fornecido"}), 400)

            update_product = ProductService.atualizar_patch_produto(produto_id, resp)

            return make_response(jsonify({"data": update_product, "message": "Produto atualizado com sucesso"}), 200)

        except ProductException as e:
            return make_response(jsonify({"message": f"{str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)

    @staticmethod
    def inactivate_product(produto_id):
        try:
            data = ProductService.inativar_produto(produto_id)
            if data:
                return make_response(jsonify({"data": "Produto inativado com sucesso"}), 200)
        except ProductException as e:
            return make_response(jsonify({"message": f"Erro ao inativar produto: {str(e)}"}), 400)
        except Exception as e:
            return make_response(jsonify({"message": f"Erro interno do servidor: {str(e)}"}), 500)
