from flask_jwt_extended import get_jwt_identity
from datetime import datetime
from src.Infrastructure.models.product_sell import Venda
from src.Infrastructure.models.product import Produto
from src.utils.return_service import ReturnSale
from src import db

class SaleException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class SaleService:
    @staticmethod
    def realizar_venda(data):
        mercado_id = get_jwt_identity()
        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not data: raise SaleException("Nenhum dado fornecido")
        if not data.get("produtoId"): raise SaleException(f"Passe um valor para o campo produtoId")
        if not data.get("quantidade"): raise SaleException(f"Passe um valor para o campo quantidade")

        produto_id = data["produtoId"]
        quantidade_venda = int(data["quantidade"])

        produto = Produto.query.filter_by(id=produto_id, seller_id=mercado_id).first()

        if not produto: raise SaleException("Não existe nenhum produto com este ID para seu mercado")
        if not produto.status: raise SaleException("Este produto não pode ser vendido porque está inativado")

        preco_venda = produto.preco
        quantidade_produto = produto.quantidade

        if not (0 < quantidade_venda <= quantidade_produto): raise SaleException("Quantidade inválida para o produto")

        venda_produto = Venda(
            seller_id=mercado_id,
            produto_id=produto_id,
            quantidade=quantidade_venda,
            preco_venda=preco_venda,
            total_venda=float(preco_venda * quantidade_venda),
            data_venda=data_venda
        )

        produto.quantidade -= quantidade_venda
        produto.status = False if produto.quantidade == 0 else produto.status

        db.session.add(venda_produto)
        db.session.commit()

        venda_realizada = Venda.query.order_by(Venda.id.desc()).first()
        
        return ReturnSale.sales(venda_realizada)

    @staticmethod
    def listar_vendas():
        mercado_id = get_jwt_identity()
        vendas = Venda.query.filter_by(seller_id=mercado_id).all()
        
        if not vendas: raise SaleException("Não foram encontradas vendas realizadas para este mercado")
        
        return [ReturnSale.sales(venda) for venda in vendas]
    
    @staticmethod
    def listar_venda_id(venda_id):
        mercado_id = get_jwt_identity()
        venda = Venda.query.filter_by(id=venda_id, seller_id=mercado_id).first()

        if not venda: raise SaleException("Venda não encontrada ou não pertence a este mercado")

        return ReturnSale.sales(venda)
