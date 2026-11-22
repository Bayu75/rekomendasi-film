"""Route DEV untuk pratinjau Frontend A. BUKAN route final.

Nama endpoint publik (main.*, auth.*) didaftarkan di app/routes.py dan saat ini
memanggil fungsi di modul ini. Backend mengganti badan fungsi di routes.py
dengan MySQL + src.recommender, tanpa mengubah nama endpoint.

Blueprint `dev` (prefix /dev) hanya untuk galeri komponen.

Simulasi (query string, disimpan di session):
  ?login=1 / ?login=0     -> pengguna login / tamu
  ?riwayat=1 / ?riwayat=0 -> pengguna login punya / tidak punya riwayat
"""
import re

from flask import (Blueprint, current_app, flash, redirect, render_template, request,
                   session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from .dummy_data import DEV_USER, HISTORY, MOVIES, PERSONAL_RECS, POPULAR, TOTAL_MOVIES
from .genre_styles import HERO_GENRES

dev_bp = Blueprint("dev", __name__, url_prefix="/dev")

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

# "Database" pengguna dev di memori (hilang saat server restart). Sandi di-hash.
_DEV_USERS = {}


def _seed_demo_user():
    email = current_app.config["DEMO_EMAIL"]
    if email not in _DEV_USERS:
        _DEV_USERS[email] = {
            "name": "Demo User",
            "email": email,
            "password_hash": generate_password_hash(current_app.config["DEMO_PASSWORD"]),
        }


def _apply_dev_toggles():
    if request.args.get("login") == "1":
        session["dev_user"] = DEV_USER
    elif request.args.get("login") == "0":
        session.pop("dev_user", None)
    if request.args.get("riwayat") in ("0", "1"):
        session["dev_has_history"] = request.args["riwayat"] == "1"


def _stub(name):
    return render_template("dev/stub.html", page_name=name)


def render_home():
    _apply_dev_toggles()
    user = session.get("dev_user")
    has_history = bool(user) and session.get("dev_has_history", True)
    history = HISTORY if has_history else []
    return render_template(
        "pages/home.html",
        history_preview=history[:5],
        history_count=len(history),
        personal_recs=PERSONAL_RECS if has_history else [],
        popular_movies=POPULAR,
        hero_genres=HERO_GENRES,
        total_movies=TOTAL_MOVIES,
    )


def render_explore():
    return _stub("Explore (Frontend B)")


def render_movie_detail(movie_id):
    return _stub(f"Detail film #{movie_id} (Frontend B)")


def render_find_similar():
    return _stub("Cari Film Serupa (Frontend B)")


def _login_context(**extra):
    cfg = current_app.config
    ctx = {"show_demo_hint": cfg["SHOW_DEMO_HINT"]}
    if cfg["SHOW_DEMO_HINT"]:
        ctx.update(demo_email=cfg["DEMO_EMAIL"], demo_password=cfg["DEMO_PASSWORD"])
    ctx.update(extra)
    return ctx


def login():
    _seed_demo_user()
    if request.method == "GET":
        return render_template("pages/login.html", **_login_context())

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    if not email or not password:
        error = "Email dan kata sandi harus diisi."
    else:
        user = _DEV_USERS.get(email)
        error = None if user and check_password_hash(user["password_hash"], password) else "Email atau kata sandi salah."
    if error:
        return render_template("pages/login.html", **_login_context(error=error, email=email)), 400

    session["dev_user"] = {"name": user["name"], "email": user["email"]}
    session["dev_has_history"] = False  # akun baru/demo: belum ada riwayat
    return redirect(url_for("main.home"))


def register():
    _seed_demo_user()
    if request.method == "GET":
        return render_template("pages/register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm:
        error = "Semua field harus diisi."
    elif not EMAIL_RE.match(email):
        error = "Format email tidak valid."
    elif len(password) < 6:
        error = "Kata sandi minimal 6 karakter."
    elif password != confirm:
        error = "Konfirmasi kata sandi tidak cocok."
    elif email in _DEV_USERS:
        error = "Email sudah terdaftar."
    else:
        error = None
    if error:
        return render_template("pages/register.html", error=error, name=name, email=email), 400

    _DEV_USERS[email] = {"name": name, "email": email, "password_hash": generate_password_hash(password)}
    # Sesuai laporan (isu #15 PRD): setelah daftar diarahkan ke halaman Masuk.
    flash("Akun berhasil dibuat. Silakan masuk.", "success")
    return redirect(url_for("auth.login"))


def logout():
    session.pop("dev_user", None)
    return redirect(url_for("main.home"))


@dev_bp.get("/komponen")
def components():
    _apply_dev_toggles()
    return render_template("dev/components.html", movies=MOVIES)
