from flask import request, jsonify, make_response
from src.Application.Service.sales_service import SaleService, SaleException
from src.Domain.product_sell import SaleDomain

class SaleController:
    
    @staticmethod
    def make_sale():
        pass
