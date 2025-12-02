from database import users_collection, files_collection
from datetime import datetime

def create_user(username, email, hashed_password):
    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

def get_user_by_email(email):
    return users_collection.find_one({"email": email})

def save_file(filename, path, size, privacy, uploaded_by):
    files_collection.insert_one({
        "filename": filename,
        "path": path,
        "size": size,
        "privacy": privacy,
        "uploaded_by": uploaded_by,
        "uploaded_at": datetime.utcnow()
    })

def get_public_files():
    return list(files_collection.find({"privacy": "public"}))

def get_user_files(user_id):
    return list(files_collection.find({"uploaded_by": user_id}))

def get_file_by_id(file_id):
    from bson.objectid import ObjectId
    return files_collection.find_one({"_id": ObjectId(file_id)})

def delete_file(file_id):
    from bson.objectid import ObjectId
    files_collection.delete_one({"_id": ObjectId(file_id)})
