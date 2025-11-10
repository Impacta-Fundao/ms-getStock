from flask import Blueprint
from flask_jwt_extended import jwt_required
from src.Application.Controller.products_controller import ProductController

products_bp = Blueprint('product', __name__)

@products_bp.route('/products', methods=['GET'])
@jwt_required()
def list_products():
    return ProductController.get_products()

@products_bp.route('/products/<int:id>', methods=['GET'])
@jwt_required()
def get_id_product(id):
    return ProductController.get_product_id(id)

@products_bp.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    return ProductController.post_product()

@products_bp.route('/products/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_product(id):
    return ProductController.delete_product(id)

@products_bp.route('/products/<int:id>', methods=['PUT'])
@jwt_required()
def update_product(id):
    return ProductController.put_product(id)

@products_bp.route('/products/<int:id>', methods=['PATCH'])
@jwt_required()
def update_patch_product(id):
    return ProductController.patch_product(id)

@products_bp.route('/products/<int:id>/activate', methods=['PATCH'])
@jwt_required()
def activate_product(id):
    return ProductController.activate_product(id)

@products_bp.route('/products/<int:id>/inactivate', methods=['PATCH'])
@jwt_required()
def inactivate_product(id):
    return ProductController.inactivate_product(id)
