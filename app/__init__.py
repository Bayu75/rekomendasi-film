import os
from flask import Flask
from dotenv import load_dotenv

from .genre_styles import register_template_globals

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "ganti-di-env")
    # Koneksi MySQL (dipakai nanti oleh backend dengan Flask-SQLAlchemy)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "")

    register_template_globals(app)

    from .routes import main, auth
    app.register_blueprint(main)
    app.register_blueprint(auth)
    return app