from src.Domain.product_sell import SaleDomain
from src.Infrastructure.models.product_sell import Venda
from src import db

class SaleException(Exception):
    def __init__(self, msg):
        super().__init__(msg)
        self.msg = msg

class SaleService:
    
    @staticmethod
    def test():
        pass
