from flask import Blueprint, request, jsonify, send_file, session
from models import save_file, get_public_files, get_user_files, get_file_by_id, delete_file
from utils import token_required, allowed_file, check_file_size, generate_filename
import os
from database import db  # Import the database instance

# --------------------------
# Upload folder setup
# --------------------------
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --------------------------
# Blueprint
# --------------------------
file_bp = Blueprint("file_bp", __name__, url_prefix="/api")


# --------------------------
# Upload file
# --------------------------
@file_bp.route("/upload", methods=["POST"])
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
        return jsonify({"error": "File too large (max 20MB)"}), 400

    filename = generate_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    save_file(filename, path, os.path.getsize(path), privacy, user_id)
    return jsonify({"message": "File uploaded successfully", "filename": filename}), 200


# --------------------------
# Public files
# --------------------------
@file_bp.route("/public-files", methods=["GET"])
def public_files():
    try:
        files = get_public_files()
        # Ensure _id is string for JSON serialization
        for f in files:
            f["_id"] = str(f.get("_id", ""))
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
# My files (logged-in user)
# --------------------------
@file_bp.route("/my-files", methods=["GET"])
@token_required
def my_files(user_id):
    try:
        files = get_user_files(user_id)
        # Ensure _id is string for JSON serialization
        for f in files:
            f["_id"] = str(f.get("_id", ""))
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
# Download file
# --------------------------
@file_bp.route("/files/<file_id>/download", methods=["GET"])
def download_file(file_id):
    try:
        file = get_file_by_id(file_id)
        if not file:
            return jsonify({"error": "File not found"}), 404

        # Check access: either public, or user owns it, or has share token
        is_public = file.get('privacy') == 'public'

        # Check if user is logged in and owns the file
        user_id = session.get('user_id')
        is_owner = user_id and file.get('uploaded_by') == user_id

        # Check for share token in query parameter
        share_token = request.args.get('token')
        has_valid_token = share_token and db.find_file_by_share_token(share_token)

        if not (is_public or is_owner or has_valid_token):
            return jsonify({"error": "Access denied"}), 403

        # Check if file exists
        if not os.path.exists(file["path"]):
            return jsonify({"error": "File not found on server"}), 404

        return send_file(file["path"], as_attachment=True, download_name=file["filename"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
# Generate shareable link for private file
# --------------------------
@file_bp.route("/files/<file_id>/share", methods=["POST"])
@token_required
def generate_share_link(user_id, file_id):
    try:
        file = get_file_by_id(file_id)
        if not file:
            return jsonify({"error": "File not found"}), 404

        # Check if user owns the file
        if file.get('uploaded_by') != user_id:
            return jsonify({"error": "Not authorized"}), 403

        # Check if file is private (only private files need share links)
        if file.get('privacy') != 'private':
            return jsonify({"error": "Only private files can have share links"}), 400

        # Generate share token
        share_token = db.generate_share_token(file_id)

        # Save token to file
        db.update_file_share_token(file_id, share_token)

        # Create the shareable URL
        base_url = request.host_url.rstrip('/')
        share_url = f"{base_url}/shared/{share_token}"

        return jsonify({
            'share_url': share_url,
            'message': 'Share link created successfully'
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
# Access shared file via token
# --------------------------
@file_bp.route("/shared/<share_token>", methods=["GET"])
def shared_file_download(share_token):
    try:
        # Find file by share token
        file = db.find_file_by_share_token(share_token)
        if not file:
            return "File not found or link expired", 404

        # Check if file exists
        if not os.path.exists(file["path"]):
            return "File not found on server", 404

        # Serve the file
        return send_file(file["path"], as_attachment=True, download_name=file["filename"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --------------------------
# Delete file
# --------------------------
@file_bp.route("/files/<file_id>", methods=["DELETE"])
@token_required
def delete_user_file(user_id, file_id):
    try:
        file = get_file_by_id(file_id)
        if not file:
            return jsonify({"error": "File not found"}), 404

        if file["uploaded_by"] != user_id:
            return jsonify({"error": "Unauthorized"}), 403

        if os.path.exists(file["path"]):
            os.remove(file["path"])

        delete_file(file_id)
        return jsonify({"message": "File deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
