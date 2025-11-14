from flask_jwt_extended import get_jwt_identity
from src.Domain.product import ProductDomain
from src.Infrastructure.models.product import Produto
from src.utils.return_service import ReturnProduct
from src import db

class ProductException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class ProductService:
    @staticmethod
    def cadastrar_produto(produto_data):
        mercado_id = get_jwt_identity()

        if not produto_data: raise ProductException("Nenhum dado fornecido")

        domain = ProductDomain(
            nome = produto_data.get('nome') if produto_data.get('nome') else False,
            preco = produto_data.get('preco') if produto_data.get('preco') and produto_data.get('preco') > 0 else False,
            quantidade = produto_data.get('quantidade') if produto_data.get('quantidade') and produto_data.get('quantidade') > 0 else False,
            imagem = produto_data.get('imagem') if produto_data.get('imagem') else False,
            )
        
        data_itens = {"nome": domain.nome, 
                      "preco": domain.preco, 
                      "quantidade": domain.quantidade, 
                      "imagem": domain.imagem
                      }

        for k, v in data_itens.items():
            if not v: raise ProductException(f"Passe um valor para o campo {k}")
            
        produto_existente = Produto.query.filter_by(nome=domain.nome, seller_id=mercado_id).first()

        if produto_existente: raise ProductException("Já existe um produto com esse nome neste mercado")
                                                                                                                                                                                                                         
        new_product = Produto(
            nome=domain.nome,
            preco=domain.preco,
            quantidade=domain.quantidade,
            status=domain.status,
            imagem=domain.imagem,
            seller_id=mercado_id
        )

        db.session.add(new_product)
        db.session.commit()

        produto_cadastrado = Produto.query.filter_by(nome=domain.nome, seller_id=mercado_id).first()

        return ReturnProduct.products(produto_cadastrado)
    
    @staticmethod
    def listar_produtos():
        mercado_id = get_jwt_identity()
        produtos = Produto.query.filter_by(seller_id=mercado_id).all()
        
        if not produtos: raise ProductException("Não foram encontrados produtos cadastrados para este mercado")
        
        return [ReturnProduct.products(produto) for produto in produtos]
    
    @staticmethod
    def listar_produto_id(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise ProductException("Produto não encontrado ou não pertence a este mercado")

        return ReturnProduct.products(produto)

    @staticmethod
    def deletar_produto(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()
        
        if not produto: raise ProductException("Produto não encontrado")
        if produto.status: raise ProductException("Só é possível remover produtos inativados")

        db.session.delete(produto)
        db.session.commit()
    
    @staticmethod
    def atualizar_produto(produto_id, produto_data):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto_data: raise ProductException("Nenhum dado fornecido")
        if not produto: raise ProductException("Produto não encontrado")
        
        data_itens = {
            "nome": produto_data.get("nome"),
            "preco": produto_data.get("preco"),
            "quantidade": produto_data.get("quantidade"),
            "imagem": produto_data.get("imagem")
        }

        for k, v in data_itens.items():
            if not v:
                raise ProductException(f"Passe um valor para o campo {k}")
            
        produto.nome = str(data_itens["nome"])
        if data_itens["preco"] <= 0: raise ProductException("Passe um valor positivo para o campo preco")
        produto.preco = data_itens["preco"]
        if data_itens["quantidade"] <= 0: raise ProductException("Passe um valor positivo para o campo quantidade")
        produto.quantidade = data_itens["quantidade"]
        produto.imagem = str(data_itens["imagem"])

        db.session.commit()

        return ReturnProduct.products(produto)
    
    @staticmethod
    def atualizar_patch_produto(produto_id, produto_data):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()
        
        if not produto_data: raise ProductException("Nenhum dado fornecido")
        if not produto: raise ProductException("Produto não encontrado")
        
        if produto_data.get("nome"): produto.nome = str(produto_data["nome"])
        
        if produto_data.get("preco"): 
            if produto_data["preco"] > 0: produto.preco = produto_data["preco"]
            else: raise ProductException("Passe um valor positivo para o campo preco")
        
        if produto_data.get("quantidade"):
            if produto_data["quantidade"] > 0: produto.quantidade = produto_data["quantidade"]
            else: raise ProductException("Passe um valor positivo para o campo quantidade")
        
        if produto_data.get("imagem"): produto.imagem = str(produto_data["imagem"])

        db.session.commit()
        
        return ReturnProduct.products(produto)

    @staticmethod
    def ativar_produto(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise ProductException("Produto não encontrado")
        if produto.status: raise ProductException("O produto já se encontra ativado")
        if produto.quantidade == 0: raise ProductException("A quantidade do produto precisa ser superior a 0 para ativa-lo")

        produto.status = True

        db.session.commit()

    @staticmethod
    def inativar_produto(produto_id):
        mercado_id = get_jwt_identity()
        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise ProductException("Produto não encontrado") 
        if not produto.status: raise ProductException("O produto já se encontra inativado")

        produto.status = False

        db.session.commit()
