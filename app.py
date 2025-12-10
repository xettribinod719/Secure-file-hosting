from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS  # Add this import
import os
from file_routes import file_bp
from auth import auth_bp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Frontend template and static locations (relative to project root)
TEMPLATE_DIR = os.path.join(PROJECT_ROOT, "frontend", "templates")
STATIC_DIR = os.path.join(PROJECT_ROOT, "frontend", "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR,
    static_url_path="/static"
)

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Register blueprints (file routes & auth)
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

# Add these routes to connect HTML templates
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/upload")
def upload_page():
    return render_template("upload.html")

@app.route("/myfiles")
def myfiles_page():
    return render_template("myfiles.html")

@app.route("/downloads")
def downloads_page():
    return render_template("downloads.html")

# Global variable for frontend API URL
@app.context_processor
def inject_api_url():
    return dict(API_URL="http://127.0.0.1:5000")

if __name__ == "__main__":
    # Run in debug for development; when running in PyCharm, this runs the dev server
    app.run(debug=True, host="127.0.0.1", port=5000)
