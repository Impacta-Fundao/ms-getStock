from flask_jwt_extended import get_jwt_identity
from src.Domain.product import ProductDomain
from src.Infrastructure.models.product import Produto
from src import db

class ProductException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ProductService:
    
    @staticmethod
    def cadastrar_produto(product_data: ProductDomain):
        mercado_id = get_jwt_identity()
        produto_existente = Produto.query.filter_by(nome=product_data.nome, seller_id=mercado_id).first()

        if produto_existente: raise ProductException("Já existe um produto com esse nome neste mercado")
                                                                                                                                                                                                                         
        new_product = Produto(
            nome=product_data.nome,
            preco=product_data.preco,
            quantidade=product_data.quantidade,
            status=product_data.status,
            imagem=product_data.imagem,
            seller_id=mercado_id
        )

        db.session.add(new_product)
        db.session.commit()

        return new_product
    
    @staticmethod
    def listar_produtos():
        mercado_id = get_jwt_identity()
        produtos = Produto.query.filter_by(seller_id=mercado_id).all()
        
        if not produtos: raise ProductException("Não foram encontrados produtos cadastrados para este mercado")
        
        return [{
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "imagem": produto.imagem,
            "status": produto.status
        } for produto in produtos]
    
    @staticmethod
    def get_id(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise ProductException("Produto não encontrado ou não pertence a este mercado")

        return {
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "imagem": produto.imagem,
            "status": produto.status
        }

    @staticmethod
    def deletar_produto(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()
        
        if not produto: raise ProductException("Produto não encontrado")
        if produto.status: raise ProductException("Só é possível remover produtos inativados")

        db.session.delete(produto)
        db.session.commit()

        return True
    
    @staticmethod
    def atualizar_produto(produto_id, produto_data):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise ProductException("Produto não encontrado")
        
        required_fields = {
            "nome": produto_data.get("nome"),
            "preco": produto_data.get("preco"),
            "quantidade": produto_data.get("quantidade"),
            "imagem": produto_data.get("imagem")
        }

        for field, value in required_fields.items():
            if not value:
                raise ProductException(f"Passe um valor para o campo {field}")
            
        produto.nome = required_fields["nome"]
        produto.preco = required_fields["preco"]
        produto.quantidade = required_fields["quantidade"]
        produto.imagem = required_fields["imagem"]

        db.session.commit()

        return {
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "imagem": produto.imagem,
            "status": produto.status
        }
    
    @staticmethod
    def atualizar_patch_produto(produto_id, produto_data):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto:
            raise ProductException("Produto não encontrado")
        if produto_data.get("nome"):
            produto.nome = produto_data["nome"]
        if produto_data.get("preco"):
            produto.preco = produto_data["preco"]
        if produto_data.get("quantidade"):
            produto.quantidade = produto_data["quantidade"]
        if produto_data.get("imagem"):
            produto.imagem = produto_data["imagem"]

        db.session.commit()
        
        return {
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "imagem": produto.imagem,
            "status": produto.status
        }

    @staticmethod
    def ativar_produto(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise ProductException("Produto não encontrado")
        if produto.status: raise ProductException("O produto já se encontra ativado")

        produto.status = True

        db.session.commit()

        return True

    @staticmethod
    def inativar_produto(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise ProductException("Produto não encontrado") 
        if not produto.status: raise ProductException("O produto já se encontra inativado")

        produto.status = False

        db.session.commit()

        return True
