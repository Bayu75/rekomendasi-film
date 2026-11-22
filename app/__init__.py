import os

from flask import Flask, request, session
from dotenv import load_dotenv

from .genre_styles import register_template_globals

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "ganti-di-env")
    # Koneksi MySQL (dipakai nanti oleh backend dengan Flask-SQLAlchemy)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "")
    # Kotak akun demo di halaman Masuk: mati kecuali MOVIEMATCH_DEMO_HINT=1.
    app.config["SHOW_DEMO_HINT"] = os.getenv("MOVIEMATCH_DEMO_HINT") == "1"
    app.config["DEMO_EMAIL"] = os.getenv("MOVIEMATCH_DEMO_EMAIL", "demo@moviematch.com")
    app.config["DEMO_PASSWORD"] = os.getenv("MOVIEMATCH_DEMO_PASSWORD", "demo123")

    # CSRF [Usulan]: jika Flask-WTF terpasang, aktifkan CSRFProtect. Template sudah
    # menyisipkan <input name="csrf_token"> otomatis bila fungsi csrf_token() tersedia.
    try:
        from flask_wtf.csrf import CSRFProtect
        CSRFProtect(app)
    except ImportError:
        pass

    register_template_globals(app)

    @app.context_processor
    def inject_globals():
        return {
            # DEV: backend mengganti ini dengan user dari session + tabel users.
            "current_user": session.get("dev_user"),
            # Endpoint Flask (mis. "main.home"), bukan string pendek "home" dari stub lama.
            "active_page": request.endpoint,
        }

    from .dev import dev_bp
    from .routes import auth, main

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(dev_bp)
    return app
