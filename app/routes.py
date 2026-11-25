"""Route halaman utama MovieMatch (Beranda, Explore, Detail, Cari Serupa, riwayat)."""

from __future__ import annotations

import logging
import sys
from math import ceil
from pathlib import Path

from flask import (
    Blueprint,
    abort,
    g,
    redirect,
    render_template,
    request,
    url_for,
)
from sqlalchemy import or_

from .auth import login_required
from .genre_styles import ALL_GENRES, HERO_GENRES
from .models import Movie, SearchHistory, db

# Pastikan akar repo bisa mengimpor src.recommender
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)

PER_PAGE = 24
N_POPULER = 10
N_PERSONAL = 8
N_DETAIL = 10
N_SERUPA = 12
N_RIWAYAT_MODEL = 10
N_RIWAYAT_PREVIEW = 5

_model_tidak_tersedia = False


def _poster_url(poster_path):
    """Ubah poster_path menjadi URL, atau None jika kosong."""
    if not poster_path:
        return None
    path = str(poster_path).strip()
    if not path:
        return None
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if path.startswith("/"):
        return f"https://image.tmdb.org/t/p/w500{path}"
    return path


def _film_ke_dict(movie: Movie) -> dict:
    """Bentuk dict film sesuai kebutuhan kartu dan halaman detail."""
    vote = movie.vote_average
    return {
        "id": int(movie.id),
        "title": movie.title,
        "overview": movie.overview or "",
        "genres": movie.genre_list,
        "keywords": movie.keyword_list,
        "director": movie.director or "",
        "release_year": int(movie.release_year) if movie.release_year is not None else None,
        "vote_average": float(vote) if vote is not None else None,
        "vote_count": int(movie.vote_count or 0),
        "poster_url": _poster_url(movie.poster_path),
        "duration": None,
        "cast": [],
    }


def _lengkapi_hasil_model(items: list[dict]) -> list[dict]:
    """Tambah poster_url, duration, dan cast ke hasil recommender."""
    if not items:
        return []
    ids = [int(item["id"]) for item in items]
    by_id = {
        m.id: m
        for m in Movie.query.filter(Movie.id.in_(ids)).all()
    }
    hasil = []
    for item in items:
        data = dict(item)
        movie = by_id.get(int(item["id"]))
        data["poster_url"] = _poster_url(movie.poster_path if movie is not None else None)
        data.setdefault("duration", None)
        data.setdefault("cast", data.get("shared_cast") or [])
        hasil.append(data)
    return hasil


def _get_recommender():
    """Muat model sekali (lazy). Jika artefak tidak ada, kembalikan None."""
    global _model_tidak_tersedia
    if _model_tidak_tersedia:
        return None
    try:
        from src.recommender import get_model

        return get_model()
    except FileNotFoundError as exc:
        logger.warning(
            "Artefak model tidak ditemukan; rekomendasi dikosongkan. %s", exc
        )
        _model_tidak_tersedia = True
        return None


def _populer(n: int = N_POPULER) -> list[dict]:
    model = _get_recommender()
    if model is None:
        return []
    return _lengkapi_hasil_model(model.popular(n))


def _rekomendasi(movie_id: int, n: int) -> list[dict]:
    model = _get_recommender()
    if model is None:
        return []
    try:
        return _lengkapi_hasil_model(model.recommend(int(movie_id), n))
    except KeyError:
        # Film ada di database tetapi tidak ada di model
        return []


def _rekomendasi_personal(history_ids: list[int], n: int = N_PERSONAL) -> list[dict]:
    """Panggil recommend_for_user hanya jika ada id yang dikenal model."""
    if not history_ids:
        return []
    model = _get_recommender()
    if model is None:
        return []
    dikenal = [i for i in history_ids if model.has_movie(i)]
    if not dikenal:
        return []
    return _lengkapi_hasil_model(model.recommend_for_user(dikenal, n))


def _riwayat_pengguna(user_id: int):
    """Ambil riwayat unik, terbaru dulu. Mengembalikan (preview, jumlah, id untuk model)."""
    baris = (
        SearchHistory.query.filter_by(user_id=user_id)
        .order_by(SearchHistory.created_at.desc(), SearchHistory.id.desc())
        .all()
    )
    unik: list[Movie] = []
    sudah = set()
    for item in baris:
        if item.movie_id in sudah:
            continue
        sudah.add(item.movie_id)
        if item.movie is not None:
            unik.append(item.movie)
    ids = [m.id for m in unik]
    preview = [_film_ke_dict(m) for m in unik[:N_RIWAYAT_PREVIEW]]
    return preview, len(unik), ids[:N_RIWAYAT_MODEL]


def _simpan_riwayat(user_id: int, movie_id: int) -> None:
    """Simpan riwayat saat buka detail. Lewati jika film terakhir sama (hindari spam)."""
    terakhir = (
        SearchHistory.query.filter_by(user_id=user_id)
        .order_by(SearchHistory.created_at.desc(), SearchHistory.id.desc())
        .first()
    )
    if terakhir is not None and terakhir.movie_id == movie_id:
        return
    db.session.add(SearchHistory(user_id=user_id, movie_id=movie_id))
    db.session.commit()


def _parse_halaman(nilai, total_halaman: int) -> int:
    try:
        halaman = int(nilai)
    except (TypeError, ValueError):
        halaman = 1
    if total_halaman < 1:
        return 1
    return min(max(halaman, 1), total_halaman)


@main.route("/")
def home():
    history_preview: list[dict] = []
    history_count = 0
    personal_recs: list[dict] = []

    if g.get("user"):
        history_preview, history_count, history_ids = _riwayat_pengguna(g.user.id)
        # Jangan panggil recommend_for_user jika riwayat kosong (model akan fallback ke popular)
        if history_ids:
            personal_recs = _rekomendasi_personal(history_ids, N_PERSONAL)

    return render_template(
        "pages/home.html",
        history_preview=history_preview,
        history_count=history_count,
        personal_recs=personal_recs,
        popular_movies=_populer(N_POPULER),
        hero_genres=HERO_GENRES,
        total_movies=Movie.query.count(),
    )


@main.route("/explore")
def explore():
    query = (request.args.get("q") or "").strip()
    active_genre = (request.args.get("genre") or "").strip() or None

    filt = Movie.query
    if query:
        pola = f"%{query}%"
        filt = filt.filter(
            or_(
                Movie.title.ilike(pola),
                Movie.director.ilike(pola),
                Movie.genres.ilike(pola),
            )
        )
    if active_genre:
        genre = active_genre
        filt = filt.filter(
            or_(
                Movie.genres == genre,
                Movie.genres.like(f"{genre}|%"),
                Movie.genres.like(f"%|{genre}"),
                Movie.genres.like(f"%|{genre}|%"),
            )
        )

    filt = filt.order_by(Movie.vote_count.desc(), Movie.title.asc())
    result_count = filt.count()
    total_pages = max(ceil(result_count / PER_PAGE), 1) if result_count else 1
    page = _parse_halaman(request.args.get("page"), total_pages)
    rows = filt.offset((page - 1) * PER_PAGE).limit(PER_PAGE).all()

    has_searched = bool(query or active_genre)
    history = []
    if g.get("user") and not has_searched:
        history, _, _ = _riwayat_pengguna(g.user.id)

    return render_template(
        "pages/explore.html",
        query=query,
        active_genre=active_genre,
        all_genres=ALL_GENRES,
        result_count=result_count,
        movies=[_film_ke_dict(m) for m in rows],
        total_movies=Movie.query.count(),
        has_searched=has_searched,
        history=history,
        pagination={
            "page": page,
            "per_page": PER_PAGE,
            "total_pages": total_pages,
            "has_prev": page > 1,
            "has_next": page < total_pages and result_count > 0,
        },
        page=page,
        per_page=PER_PAGE,
        total_pages=total_pages,
        has_prev=page > 1,
        has_next=page < total_pages and result_count > 0,
    )


@main.route("/film/<int:movie_id>")
def movie_detail(movie_id):
    movie = db.session.get(Movie, movie_id)
    if movie is None:
        abort(404)

    if g.get("user"):
        _simpan_riwayat(g.user.id, movie.id)

    return render_template(
        "pages/movie_detail.html",
        movie=_film_ke_dict(movie),
        recommendations=_rekomendasi(movie.id, N_DETAIL),
        source_movie=None,
        why=None,
        runtime_str=None,
        cast=[],
    )


@main.route("/cari-serupa")
def find_similar():
    selected_raw = request.args.get("selected")
    show_results = request.args.get("hasil") == "1"
    query = (request.args.get("q") or "").strip()

    selected_movie = None
    if selected_raw not in (None, ""):
        try:
            selected_id = int(selected_raw)
        except (TypeError, ValueError):
            abort(404)
        terpilih = db.session.get(Movie, selected_id)
        if terpilih is None:
            abort(404)
        selected_movie = _film_ke_dict(terpilih)

    similar_movies: list[dict] = []
    if selected_movie and show_results:
        similar_movies = _rekomendasi(selected_movie["id"], N_SERUPA)

    # Hasil pencarian judul acuan (untuk template setelah form ?q= siap)
    search_results: list[dict] = []
    if query and selected_movie is None:
        rows = (
            Movie.query.filter(Movie.title.ilike(f"%{query}%"))
            .order_by(Movie.vote_count.desc(), Movie.title.asc())
            .limit(N_SERUPA)
            .all()
        )
        search_results = [_film_ke_dict(m) for m in rows]

    return render_template(
        "pages/find_similar.html",
        selected_movie=selected_movie,
        show_results=show_results and selected_movie is not None,
        similar_movies=similar_movies,
        popular_movies=_populer(N_POPULER),
        query=query,
        search_results=search_results,
    )


@main.route("/riwayat/hapus", methods=["POST"])
@login_required
def clear_history():
    SearchHistory.query.filter_by(user_id=g.user.id).delete()
    db.session.commit()
    return redirect(url_for("main.explore"))
