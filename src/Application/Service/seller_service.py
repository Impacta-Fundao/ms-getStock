from src.Domain.seller import SellerDomain
from src.Infrastructure.models.seller import Mercado
from src import db

class MercadoException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class SellerService:
    
    @staticmethod
    def create_seller(nome,cnpj,email,celular,senha,status ):
        new_seller = SellerDomain(nome,cnpj,email,celular,senha,status)
        seller = Mercado(nome=new_seller.nome,cnpj=new_seller.cnpj,email=new_seller.email,celular=new_seller.celular,senha=new_seller.senha,status=new_seller.status)
        db.session.add(seller)
        db.session.commit()
        return seller
    
    @staticmethod
    def listar_mercados():
        data = Mercado.query.all()
        mercados_json = [{
            'id': mercado.id,
            'nome': mercado.nome,
            'cnpj': mercado.cnpj,
            'email': mercado.email,
            'celular': mercado.celular,
            'status': mercado.status, 
        } for mercado in data]
        
        return mercados_json