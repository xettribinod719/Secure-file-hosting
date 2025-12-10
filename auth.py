from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from models import create_user, get_user_by_email
from utils import SECRET_KEY, JWT_ALGORITHM

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if get_user_by_email(email):
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = generate_password_hash(password)
    create_user(username, email, hashed_pw)
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing credentials"}), 400

    user = get_user_by_email(email)
    if not user or not check_password_hash(user.get("password", ""), password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create token with 7-day expiration and include username
    payload = {
        "user_id": str(user["_id"]),
        "username": user.get("username", "User"),
        "exp": datetime.utcnow() + timedelta(days=7)  # 7 days expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

    # PyJWT may return bytes in older versions; ensure string
    if isinstance(token, bytes):
        token = token.decode('utf-8')

    return jsonify({
        "token": token,
        "username": user.get("username", "User")
    }), 200
