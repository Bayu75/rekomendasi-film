import re
from functools import wraps

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .models import User, db

auth = Blueprint("auth", __name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 6


def load_current_user():
    """Ambil pengguna yang sedang login dari session, dipanggil sebelum tiap request."""
    user_id = session.get("user_id")
    g.user = db.session.get(User, user_id) if user_id else None
    if user_id and g.user is None:
        session.clear()


def inject_current_user():
    """Kirim current_user ke semua template (dipakai navbar)."""
    return {"current_user": g.get("user")}


def login_required(view):
    """Dekorator untuk route yang wajib login."""

    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.get("user") is None:
            flash("Silakan masuk terlebih dahulu.", "error")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def _safe_next(target):
    if target and target.startswith("/") and not target.startswith("//"):
        return target
    return url_for("main.home")


@auth.route("/daftar", methods=["GET", "POST"])
def register():
    if g.get("user"):
        return redirect(url_for("main.home"))

    if request.method == "GET":
        return render_template("pages/register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    error = None
    if not name or not email or not password or not confirm_password:
        error = "Semua kolom wajib diisi."
    elif len(name) > 100:
        error = "Nama maksimal 100 karakter."
    elif not EMAIL_PATTERN.match(email):
        error = "Format email tidak valid."
    elif len(password) < MIN_PASSWORD_LENGTH:
        error = f"Kata sandi minimal {MIN_PASSWORD_LENGTH} karakter."
    elif password != confirm_password:
        error = "Konfirmasi kata sandi tidak cocok."
    elif User.query.filter_by(email=email).first():
        error = "Email sudah terdaftar. Silakan masuk."

    if error:
        return render_template(
            "pages/register.html", error=error, name=name, email=email
        ), 400

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash("Akun berhasil dibuat. Silakan masuk.", "success")
    return redirect(url_for("auth.login"))


@auth.route("/masuk", methods=["GET", "POST"])
def login():
    if g.get("user"):
        return redirect(url_for("main.home"))

    if request.method == "GET":
        return render_template("pages/login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template(
            "pages/login.html", error="Email dan kata sandi wajib diisi.", email=email
        ), 400

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return render_template(
            "pages/login.html", error="Email atau kata sandi salah.", email=email
        ), 401

    session.clear()
    session["user_id"] = user.id
    return redirect(_safe_next(request.args.get("next")))


@auth.route("/keluar", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("main.home"))