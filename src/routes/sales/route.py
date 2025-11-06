from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.Application.Controller.sales_controller import SaleController

sales_bp = Blueprint('sales', __name__) 


@sales_bp.route('/sales', methods=['POST'])
@jwt_required()
def sales():
    return SaleController.make_sale()
