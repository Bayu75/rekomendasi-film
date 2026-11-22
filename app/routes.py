from flask import Blueprint, render_template, redirect, url_for

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)


@main.route("/")
def home():
    return render_template("pages/home.html")


# --- Route SEMENTARA supaya link tidak error. Diganti Backend / Frontend B. ---
@main.route("/explore")
def explore():
    return "Halaman Explore (dikerjakan Frontend B)"


@main.route("/film/<int:movie_id>")
def movie_detail(movie_id):
    return f"Detail film {movie_id} (dikerjakan Frontend B)"


@main.route("/cari-serupa")
def find_similar():
    return "Cari Film Serupa (dikerjakan Frontend B)"


@auth.route("/masuk", methods=["GET", "POST"])
def login():
    return render_template("pages/login.html")


@auth.route("/daftar", methods=["GET", "POST"])
def register():
    return render_template("pages/register.html")


@auth.route("/keluar", methods=["POST"])
def logout():
    return redirect(url_for("main.home"))