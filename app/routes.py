"""Endpoint publik MovieMatch.

Nama mengikuti docs/jinja-components.md §3:
  main.home, main.explore, main.movie_detail, main.find_similar,
  auth.login, auth.register, auth.logout

Badan fungsi di bawah ini masih DEV (data dummy + akun di memori, lihat app/dev.py)
supaya template Frontend A bisa dirender. Backend mengganti isi fungsi ini dengan
MySQL + src.recommender tanpa mengubah nama endpoint atau blueprint.
"""
from flask import Blueprint

from . import dev

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)


@main.get("/")
def home():
    return dev.render_home()


@main.get("/explore")
def explore():
    return dev.render_explore()


@main.get("/film/<int:movie_id>")
def movie_detail(movie_id):
    return dev.render_movie_detail(movie_id)


@main.get("/cari-serupa")
def find_similar():
    return dev.render_find_similar()


@auth.route("/masuk", methods=["GET", "POST"])
def login():
    return dev.login()


@auth.route("/daftar", methods=["GET", "POST"])
def register():
    return dev.register()


@auth.post("/keluar")
def logout():
    return dev.logout()
