from . import api
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta
from models.database import db
from .model import SalonUser

@api.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = db.db_conn()
    user = SalonUser.get_user_by_username(conn, username)

    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid username or password"}), 401

    access_token = create_access_token(
        identity=str(user.id),
        expires_delta=timedelta(hours=1)
    )
    return jsonify(msg="Login successful", access_token=access_token), 200