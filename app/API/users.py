from . import api
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.database import db
from .model import SalonUser  # replace with correct import if needed

@api.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    conn = db.db_conn()
    users = SalonUser.get_users(conn)
    return jsonify([u.to_dict() for u in users]), 200

@api.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    conn = db.db_conn()
    user = SalonUser.get_user_by_id(conn, user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.to_dict()), 200

# @api.route('/users', methods=['POST'])
# def create_user():
#     conn = db.db_conn()
#     data = request.get_json()
#     new_user = SalonUser.create_user(conn, data)
#     if new_user:
#         return jsonify({"msg": "User created", "user": new_user.to_dict()}), 201
#     return jsonify({"msg": "Failed to create user"}), 400

@api.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    conn = db.db_conn()
    data = request.get_json()
    updated = SalonUser.update_user(conn, user_id, data)
    if updated:
        return jsonify({"msg": "User updated"}), 200
    return jsonify({"msg": "Failed to update user"}), 400

@api.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    conn = db.db_conn()
    deleted = SalonUser.delete_user(conn, user_id)
    if deleted:
        return jsonify({"msg": "User deleted"}), 200
    return jsonify({"msg": "Failed to delete user"}), 400