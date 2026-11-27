import os

from dotenv import load_dotenv
from flask import Flask, render_template

from .genre_styles import register_template_globals
from .models import db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "ganti-di-env")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    register_template_globals(app)

    from .auth import auth, inject_current_user, load_current_user
    from .routes import main

    app.before_request(load_current_user)
    app.context_processor(inject_current_user)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    @app.errorhandler(404)
    def halaman_tidak_ditemukan(error):
        return render_template("errors/404.html"), 404

    with app.app_context():
        db.create_all()

    return app