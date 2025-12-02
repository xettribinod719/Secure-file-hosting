from pymongo import MongoClient
import os

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Make sure MongoDB is running locally
db = client["secure_file_hosting"]

# Collections
users_collection = db["users"]
files_collection = db["files"]
