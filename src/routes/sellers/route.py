from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required
from src.Application.Controller.seller_controller import SellerController

mercado_bp = Blueprint('mercado', __name__) 

def init_route(app):
    app.register_blueprint(mercado_bp)
    @app.route('/', methods=["GET"])
    def raiz():
        return jsonify({"message": "API OK"}), 200

@mercado_bp.route('/mercados', methods=['GET'])
@jwt_required()
def list_seller():
    return SellerController.get_sellers()

@mercado_bp.route('/mercados/<int:id>', methods=['GET'])
@jwt_required()
def get_id_seller(id):
    return SellerController.get_seller_id(id)

@mercado_bp.route('/mercados', methods=['POST'])
def create_seller():
    return SellerController.post_seller()

@mercado_bp.route('/mercados/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_seller(id):
    return SellerController.delete_seller(id)

@mercado_bp.route('/mercados/<int:id>', methods=['PUT'])
def update_seller(id):
    return SellerController.put_seller(id)

@mercado_bp.route('/mercados/<int:id>', methods=['PATCH'])
@jwt_required()
def update_patch_seller(id):
    return SellerController.patch_seller(id)
