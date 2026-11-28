import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

from .genre_styles import register_template_globals
from .models import db

load_dotenv()

csrf = CSRFProtect()
migrate = Migrate()

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Nilai contoh / bawaan yang tidak aman dipakai sebagai SECRET_KEY.
_SECRET_TIDAK_AMAN = {
    "ganti-di-env",
    "dev",
    "secret",
    "ganti-dengan-string-acak-panjang",
    "isi-dengan-string-acak",
    "changeme",
}


def _rahasia_tidak_aman(nilai):
    if nilai is None:
        return True
    teks = str(nilai).strip()
    return not teks or teks.lower() in _SECRET_TIDAK_AMAN


def create_app(config_override=None, testing_config=None):
    """Buat aplikasi Flask. Untuk tes, kirim SECRET_KEY dan DATABASE_URL
    (atau SQLALCHEMY_DATABASE_URI) lewat config_override atau testing_config.
    """
    app = Flask(__name__)

    overrides = {}
    if testing_config:
        overrides.update(testing_config)
    if config_override:
        overrides.update(config_override)

    secret = overrides.get("SECRET_KEY", os.getenv("SECRET_KEY"))
    database_url = overrides.get(
        "SQLALCHEMY_DATABASE_URI",
        overrides.get("DATABASE_URL", os.getenv("DATABASE_URL")),
    )

    if _rahasia_tidak_aman(secret):
        raise RuntimeError(
            "SECRET_KEY belum diisi atau masih memakai nilai bawaan yang tidak aman. "
            "Salin .env.example menjadi .env, lalu isi SECRET_KEY dengan string acak yang panjang."
        )
    if not database_url or not str(database_url).strip():
        raise RuntimeError(
            "DATABASE_URL belum diisi. Salin .env.example menjadi .env, lalu isi "
            "DATABASE_URL (contoh: mysql+pymysql://root:@localhost:3306/moviematch)."
        )

    app.config["SECRET_KEY"] = str(secret).strip()
    app.config["SQLALCHEMY_DATABASE_URI"] = str(database_url).strip()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    for key, value in overrides.items():
        if key == "DATABASE_URL":
            continue
        app.config[key] = value

    # Otomatis memuat ulang template HTML/Jinja saat ada perubahan
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

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
        try:
            from src.recommender import load_model

            load_model()
        except Exception as exc:
            app.logger.warning(
                "Model rekomendasi gagal dimuat saat aplikasi start; "
                "rekomendasi akan dikosongkan sampai file model tersedia. %s",
                exc,
            )

    return app
