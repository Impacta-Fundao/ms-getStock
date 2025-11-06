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
        produto_existente = Produto.query.filter_by(nome=product_data.nome).first()

        if produto_existente: raise ProductException("Nome de produto já cadastrado")
        
        product = Produto(
            nome=product_data.nome,
            preco=product_data.preco,
            quantidade=product_data.quantidade,
            status=product_data.status,
            imagem=product_data.imagem
        )

        db.session.add(product)
        db.session.commit()

        return product
    
    @staticmethod
    def listar_produtos():
        data = Produto.query.all()
        if not data: raise ProductException("Não foram encontrados produtos cadastrados")
        
        produtos_json = [{
            "id": produto.id,
            "nome": produto.nome,
            "preco": produto.preco,
            "quantidade": produto.quantidade,
            "status": produto.status,
            "imagem": produto.imagem
        } for produto in data]

        return produtos_json
    
    @staticmethod
    def get_id(produto_id):
        data = Produto.query.get(produto_id)
        if not data: raise ProductException("Produto não encontrado")
        
        produtos_json = {
            "id": data.id,
            "nome": data.nome,
            "preco": data.preco,
            "quantidade": data.quantidade,
            "status": data.status,
            "imagem": data.imagem
        }

        return produtos_json
    
    @staticmethod
    def deletar_produto(produto_id):
        data = Produto.query.get(produto_id)
        if not data: raise ProductException("Produto não encontrado")
        if data.status: raise ProductException("Só é possível remover produtos inativados")

        db.session.delete(data)
        db.session.commit()

        return True
    
    @staticmethod
    def atualizar_produto(produto_id, produto_data):
        data = Produto.query.get(produto_id)
        if not data: raise ProductException("Produto não encontrado")
        
        required_fields = {
            "nome": produto_data.nome,
            "preco": produto_data.preco,
            "quantidade": produto_data.quantidade,
            "imagem": produto_data.imagem
        }

        for field, value in required_fields.items():
            if not value:
                raise ProductException(f"Passe um valor para o campo {field}")
            
        data.nome = required_fields["nome"]
        data.preco = required_fields["preco"]
        data.quantidade = required_fields["quantidade"]
        if "status" in produto_data:
            data.status = required_fields["status"]
        data.imagem = required_fields["imagem"]

        db.session.commit()

        return {
            "id": data.id,
            "nome": data.nome,
            "preco": data.preco,
            "quantidade": data.quantidade,
            "status": data.status,
            "imagem": data.imagem
        }
    
    @staticmethod
    def atualizar_patch_produto(produto_id, produto_data):
        data = Produto.query.get(produto_id)

        if not data:
            raise ProductException("Produto não encontrado")
        if produto_data.get("nome"):
            data.nome = produto_data["nome"]
        if produto_data.get("preco"):
            data.nome = produto_data["preco"]
        if produto_data.get("quantidade"):
            data.nome = produto_data["quantidade"]
        if produto_data.get("status"):
            data.nome = produto_data["status"]
        if produto_data.get("imagem"):
            data.nome = produto_data["imagem"]

        db.session.commit()
        
        return {
            "id": data.id,
            "nome": data.nome,
            "preco": data.preco,
            "quantidade": data.quantidade,
            "status": data.status,
            "imagem": data.imagem
        }

    @staticmethod
    def inativar_produto(produto_id):
        data = Produto.query.get(produto_id)
        if not data: raise ProductException("Produto não encontrado") 
        if not data.status: raise ProductException("O produto já se encontra inativado")

        data.status = False

        db.session.commit()

        return True
