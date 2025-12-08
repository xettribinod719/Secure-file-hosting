from flask import Flask, render_template
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

# Register blueprints (file routes & auth)
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    # Render the frontend index.html from templates folder
    return render_template("index.html")

if __name__ == "__main__":
    # Run in debug for development; when running in PyCharm, this runs the dev server
    app.run(debug=True, host="127.0.0.1", port=5000)
