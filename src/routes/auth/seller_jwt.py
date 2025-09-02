from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token

seller_jwt_bp = Blueprint('seller_jwt', __name__)

@seller_jwt_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username == 'murillo' and not password == 'admin1234':
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)