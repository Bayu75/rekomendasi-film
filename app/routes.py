from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("pages/home.html")


# --- Route SEMENTARA supaya link tidak error. Akan diisi pada langkah berikutnya. ---
@main.route("/explore")
def explore():
    return "Halaman Explore (dikerjakan Backend)"


@main.route("/film/<int:movie_id>")
def movie_detail(movie_id):
    return f"Detail film {movie_id} (dikerjakan Backend)"


@main.route("/cari-serupa")
def find_similar():
    return "Cari Film Serupa (dikerjakan Backend)"