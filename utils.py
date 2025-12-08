import jwt
from functools import wraps
from flask import request, jsonify
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os
import time

# Secret key - in production use environment variable or .env; kept here for local dev
SECRET_KEY = os.environ.get('SFL_SECRET') or "supersecret"
JWT_ALGORITHM = "HS256"

# Token decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization") or request.args.get('token')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        try:
            # If token is prefixed with "Bearer ", remove the prefix
            if token.startswith("Bearer "):
                token = token.split(" ", 1)[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            user_id = data.get("user_id")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except Exception as e:
            return jsonify({"error": "Token is invalid - %s" % str(e)}), 401
        # Call the protected function, providing user_id as first param
        return f(user_id, *args, **kwargs)
    return decorated

# File helpers
ALLOWED_EXTENSIONS = {'pdf', 'mp4'}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_file_size(file):
    # file is a FileStorage object
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size <= MAX_FILE_SIZE

def generate_filename(filename):
    # secure basename + timestamp to reduce collisions
    base = secure_filename(filename)
    name, ext = os.path.splitext(base)
    ts = int(time.time())
    return f"{name}-{ts}{ext}"
