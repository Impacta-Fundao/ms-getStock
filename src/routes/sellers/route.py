from flask import Blueprint, jsonify, make_response
from src.Application.Controller.seller_controller import SellerController

mercado_bp = Blueprint('mercado', __name__) 

def init_route(app):
    app.register_blueprint(mercado_bp)
    @app.route('/', methods=["GET"])
    def raiz():
        return make_response(jsonify({
            "message": "API - OK"
        }), 200)

@mercado_bp.route('/mercados', methods=['GET'])
def list_seller():
    return SellerController.get_sellers()

@mercado_bp.route('/mercados/<int:id>', methods=['GET'])
def get_id_seller(id):
    return SellerController.get_seller_id(id)

@mercado_bp.route('/mercados', methods=['POST'])
def create_seller():
    return SellerController.post_seller()

@mercado_bp.route('/mercados/<int:id>', methods=['DELETE'])
def delete_seller(id):
    return SellerController.delete_seller(id)

@mercado_bp.route('/mercados/<int:id>', methods=['PUT'])
def update_seller(id):
    return SellerController.put_seller(id)

@mercado_bp.route('/mercados/<int:id>', methods=['PATCH'])
def update_patch_seller(id):
    return SellerController.patch_seller(id)
    
