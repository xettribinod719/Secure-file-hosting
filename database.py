import json
import os
from datetime import datetime


# Simple JSON-based database (temporary solution)
class JSONDatabase:
    def __init__(self):
        self.data_dir = "data"
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.users_file = os.path.join(self.data_dir, "users.json")
        self.files_file = os.path.join(self.data_dir, "files.json")

        # Initialize files if they don't exist
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump([], f)

        if not os.path.exists(self.files_file):
            with open(self.files_file, 'w') as f:
                json.dump([], f)

    def _read_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def _write_users(self, data):
        with open(self.users_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _read_files(self):
        try:
            with open(self.files_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def _write_files(self, data):
        with open(self.files_file, 'w') as f:
            json.dump(data, f, indent=2)

    # Users collection
    def insert_user(self, user_data):
        users = self._read_users()
        # Generate a simple ID
        import time
        user_id = str(int(time.time() * 1000))
        user_data["_id"] = user_id
        users.append(user_data)
        self._write_users(users)
        return user_id

    def find_user_by_email(self, email):
        users = self._read_users()
        for user in users:
            if user.get("email") == email:
                return user
        return None

    # Files collection
    def insert_file(self, file_data):
        files = self._read_files()
        # Generate a simple ID
        import time
        file_id = str(int(time.time() * 1000) + len(files))
        file_data["_id"] = file_id
        files.append(file_data)
        self._write_files(files)
        return file_id

    def find_files(self, query=None):
        files = self._read_files()
        if not query:
            return files.copy()  # Return a copy

        result = []
        for file in files:
            match = True
            for key, value in query.items():
                if file.get(key) != value:
                    match = False
                    break
            if match:
                result.append(file.copy())  # Return a copy
        return result

    def find_file_by_id(self, file_id):
        files = self._read_files()
        for file in files:
            if file.get("_id") == file_id:
                return file.copy()  # Return a copy
        return None

    def delete_file(self, file_id):
        files = self._read_files()
        new_files = [f for f in files if f.get("_id") != file_id]
        deleted = len(files) != len(new_files)
        if deleted:
            self._write_files(new_files)
        return deleted


# Create global instance
db = JSONDatabase()


# Mock collections for compatibility with existing code
class MockCollection:
    def __init__(self, db_instance, collection_type):
        self.db = db_instance
        self.type = collection_type

    def insert_one(self, data):
        if self.type == "users":
            _id = self.db.insert_user(data)
            data["_id"] = _id
        else:  # files
            _id = self.db.insert_file(data)
            data["_id"] = _id

        # Create a mock result object
        class MockResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id

        return MockResult(_id)

    def find_one(self, query):
        if self.type == "users":
            if "email" in query:
                return self.db.find_user_by_email(query["email"])
        return None

    def find(self, query=None):
        if self.type == "files":
            return self.db.find_files(query)
        return []

    def delete_one(self, query):
        if self.type == "files" and "_id" in query:
            deleted = self.db.delete_file(query["_id"])

            # Create a mock result object
            class MockResult:
                def __init__(self, deleted_count):
                    self.deleted_count = deleted_count

            return MockResult(1 if deleted else 0)
        return type('obj', (object,), {'deleted_count': 0})()


# Create mock collections
users_collection = MockCollection(db, "users")
files_collection = MockCollection(db, "files")

# Debug print
print("✓ JSON Database initialized (no MongoDB required)")
