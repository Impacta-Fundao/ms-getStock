from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.Application.Controller.sales_controller import SaleController

sales_bp = Blueprint('sales', __name__) 

@sales_bp.route('/sales/history', methods=['GET'])
@jwt_required()
def list_sales():
    return SaleController.get_sales()

@sales_bp.route('/sales/history/<int:id>', methods=['GET'])
@jwt_required()
def get_id_sale(id):
    return SaleController.get_sale_id(id)

@sales_bp.route('/sales', methods=['POST'])
@jwt_required()
def create_sale():
    return SaleController.post_sale()
