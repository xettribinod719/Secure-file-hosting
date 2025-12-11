from database import users_collection, files_collection
from datetime import datetime
import time


def create_user(username, email, hashed_password):
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow().isoformat()
    }
    return users_collection.insert_one(user_data)


def get_user_by_email(email):
    return users_collection.find_one({"email": email})


def save_file(filename, path, size, privacy, uploaded_by):
    file_data = {
        "filename": filename,
        "path": path,
        "size": size,
        "privacy": privacy,
        "uploaded_by": uploaded_by,
        "uploaded_at": datetime.utcnow().isoformat()
    }
    return files_collection.insert_one(file_data)


def get_public_files():
    files = files_collection.find({"privacy": "public"})
    # Convert cursor to list if needed
    if hasattr(files, '__iter__') and not isinstance(files, list):
        files = list(files)

    # Ensure _id is string
    for file in files:
        if "_id" in file and not isinstance(file["_id"], str):
            file["_id"] = str(file["_id"])
    return files


def get_user_files(user_id):
    files = files_collection.find({"uploaded_by": user_id})
    # Convert cursor to list if needed
    if hasattr(files, '__iter__') and not isinstance(files, list):
        files = list(files)

    # Ensure _id is string
    for file in files:
        if "_id" in file and not isinstance(file["_id"], str):
            file["_id"] = str(file["_id"])
    return files


def get_file_by_id(file_id):
    # Our JSON database needs string IDs
    file_id = str(file_id)
    files = files_collection.find()
    for file in files:
        if str(file.get("_id")) == file_id:
            return file
    return None


def delete_file(file_id):
    # Our JSON database needs string IDs
    file_id = str(file_id)
    result = files_collection.delete_one({"_id": file_id})
    return result.deleted_count > 0
