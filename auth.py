from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from models import create_user, get_user_by_email
from utils import SECRET_KEY

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.json
    if get_user_by_email(data["email"]):
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = generate_password_hash(data["password"])
    create_user(data["username"], data["email"], hashed_pw)
    return jsonify({"message": "User registered successfully"})


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    user = get_user_by_email(data["email"])
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        "user_id": str(user["_id"]),
        "exp": datetime.utcnow() + timedelta(hours=5)
    }, SECRET_KEY)
    return jsonify({"token": token})
