import jwt
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os

SECRET_KEY = "supersecret"

# Token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user_id = data["user_id"]
        except:
            return jsonify({"error": "Token is invalid"}), 401
        return f(user_id, *args, **kwargs)
    return decorated

# File helpers
ALLOWED_EXTENSIONS = {'pdf', 'mp4'}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_file_size(file):
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE

def generate_filename(filename):
    return secure_filename(filename)
