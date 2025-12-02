from flask import Blueprint, request, jsonify, send_file
from models import save_file, get_public_files, get_user_files, get_file_by_id, delete_file
from utils import token_required, allowed_file, check_file_size, generate_filename
import os

# --------------------------
# Upload folder setup
# --------------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --------------------------
# Blueprint
# --------------------------
file_bp = Blueprint("file_bp", __name__)

# --------------------------
# Upload file
# --------------------------
@file_bp.route("/api/upload", methods=["POST"])
@token_required
def upload_file(user_id):
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    privacy = request.form.get("privacy", "private")

    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF and MP4 allowed"}), 400

    if not check_file_size(file):
        return jsonify({"error": "File too large"}), 400

    filename = generate_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    save_file(filename, path, os.path.getsize(path), privacy, user_id)
    return jsonify({"message": "File uploaded successfully"}), 200

# --------------------------
# Public files
# --------------------------
@file_bp.route("/api/public-files", methods=["GET"])
def public_files():
    files = get_public_files()
    for f in files:
        f["_id"] = str(f["_id"])
    return jsonify(files)

# --------------------------
# My files (logged-in user)
# --------------------------
@file_bp.route("/api/my-files", methods=["GET"])
@token_required
def my_files(user_id):
    files = get_user_files(user_id)
    for f in files:
        f["_id"] = str(f["_id"])
    return jsonify(files)

# --------------------------
# Download file
# --------------------------
@file_bp.route("/api/files/<file_id>/download", methods=["GET"])
def download_file(file_id):
    file = get_file_by_id(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404
    return send_file(file["path"], as_attachment=True)

# --------------------------
# Delete file
# --------------------------
@file_bp.route("/api/files/<file_id>", methods=["DELETE"])
@token_required
def delete_user_file(user_id, file_id):
    file = get_file_by_id(file_id)
    if not file:
        return jsonify({"error": "File not found"}), 404
    if file["uploaded_by"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    if os.path.exists(file["path"]):
        os.remove(file["path"])
    delete_file(file_id)
    return jsonify({"message": "File deleted successfully"}), 200
