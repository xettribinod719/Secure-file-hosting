from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return jsonify({"message": "File uploaded successfully", "filename": file.filename})


@app.route("/files", methods=["GET"])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({"files": files})


@app.route("/delete/<filename>", methods=["DELETE"])
def delete_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    os.remove(filepath)
    return jsonify({"message": "File deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
