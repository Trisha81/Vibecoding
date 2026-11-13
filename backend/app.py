"""Application factory. Serves the JSON API and the static frontend."""
from pathlib import Path

from flask import Flask, send_from_directory

from .api.routes import api

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)
    app.register_blueprint(api)

    @app.get("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.get("/<path:filename>")
    def assets(filename):
        return send_from_directory(FRONTEND_DIR, filename)

    return app
