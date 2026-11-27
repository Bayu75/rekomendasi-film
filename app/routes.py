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
N_DETAIL = 6
N_SERUPA = 12
N_KANDIDAT_SERUPA = 60
N_RIWAYAT_MODEL = 10
N_RIWAYAT_PREVIEW = 5

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


def _format_sutradara(nilai):
    """Ubah 'A|B' dari database menjadi 'A, B' agar sama dengan keluaran model."""
    if not nilai:
        return ""
    bagian = [p.strip() for p in str(nilai).split("|") if p.strip()]
    return ", ".join(bagian)


def _format_durasi(menit):
    """Ubah menit menjadi teks seperti '2 j 32 m'. None atau <= 0 menjadi None."""
    if menit is None:
        return None
    try:
        total = int(menit)
    except (TypeError, ValueError):
        return None
    if total <= 0:
        return None
    jam, sisa = divmod(total, 60)
    if jam and sisa:
        return f"{jam} j {sisa} m"
    if jam:
        return f"{jam} j"
    return f"{sisa} m"


def _parse_cast(cast_list):
    """Ubah 'Nama::Peran|Nama2::Peran2' menjadi daftar {name, character}."""
    if not cast_list:
        return []
    hasil = []
    for item in str(cast_list).split("|"):
        item = item.strip()
        if not item:
            continue
        bagian = item.split("::", 1)
        nama = bagian[0].strip()
        peran = bagian[1].strip() if len(bagian) > 1 else ""
        if nama:
            hasil.append({"name": nama, "character": peran})
    return hasil


def _film_ke_dict(movie: Movie) -> dict:
    """Bentuk dict film sesuai kebutuhan kartu dan halaman detail."""
    vote = movie.vote_average
    return {
        "id": int(movie.id),
        "title": movie.title,
        "overview": movie.overview or "",
        "genres": movie.genre_list,
        "keywords": movie.keyword_list,
        "director": _format_sutradara(movie.director),
        "release_year": int(movie.release_year) if movie.release_year is not None else None,
        "vote_average": float(vote) if vote is not None else None,
        "vote_count": int(movie.vote_count or 0),
        "poster_url": _poster_url(movie.poster_path),
        "duration": _format_durasi(movie.runtime),
        "cast": _parse_cast(movie.cast_list),
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
        if movie is not None:
            data["poster_url"] = _poster_url(movie.poster_path)
            data["duration"] = _format_durasi(movie.runtime)
            data["cast"] = _parse_cast(movie.cast_list)
        else:
            data["poster_url"] = _poster_url(None)
            data.setdefault("duration", None)
            data.setdefault("cast", data.get("shared_cast") or [])
        hasil.append(data)
    return hasil


_sudah_peringatan_model = False


def _get_recommender():
    """Ambil model yang sudah dimuat, atau coba muat jika belum ada.

    Tidak mengunci status 'tidak tersedia': jika file model muncul kemudian,
    permintaan berikutnya akan mencoba memuatnya lagi.
    """
    global _sudah_peringatan_model
    try:
        from src.recommender import get_model

        model = get_model()
        _sudah_peringatan_model = False
        return model
    except FileNotFoundError as exc:
        if not _sudah_peringatan_model:
            logger.warning(
                "Artefak model tidak ditemukan; rekomendasi dikosongkan. %s", exc
            )
            _sudah_peringatan_model = True
        return None
    except Exception as exc:
        if not _sudah_peringatan_model:
            logger.warning(
                "Model rekomendasi gagal dimuat; rekomendasi dikosongkan. %s", exc
            )
            _sudah_peringatan_model = True
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


def _cocok_genre(item, genre):
    if not genre:
        return True
    target = str(genre).strip().lower()
    return any(str(g).strip().lower() == target for g in (item.get("genres") or []))


def _cocok_tahun(tahun_film, filter_tahun):
    if filter_tahun in (None, ""):
        return True
    if tahun_film is None:
        return False
    try:
        tahun_film = int(tahun_film)
    except (TypeError, ValueError):
        return False
    teks = str(filter_tahun).strip().lower()
    if teks.endswith("-an") and teks[:-3].isdigit():
        awal = int(teks[:-3])
        return awal <= tahun_film < awal + 10
    if teks.endswith("s") and teks[:-1].lstrip("-").isdigit():
        awal = int(teks[:-1])
        return awal <= tahun_film < awal + 10
    try:
        if teks.startswith(">="):
            return tahun_film >= int(float(teks[2:]))
        if teks.startswith("<="):
            return tahun_film <= int(float(teks[2:]))
        if teks.startswith(">"):
            return tahun_film > int(float(teks[1:]))
        if teks.startswith("<"):
            return tahun_film < int(float(teks[1:]))
        if "-" in teks:
            kiri, kanan = teks.split("-", 1)
            if kiri.strip().lstrip("-").isdigit() and kanan.strip().lstrip("-").isdigit():
                return int(kiri) <= tahun_film <= int(kanan)
        return tahun_film == int(float(teks))
    except (TypeError, ValueError):
        return False


def _cocok_rating(item, filter_rating):
    if filter_rating in (None, ""):
        return True
    nilai = item.get("vote_average")
    if nilai is None:
        return False
    teks = str(filter_rating).strip().replace(",", ".")
    if teks.startswith(">="):
        teks = teks[2:]
    elif teks.startswith(">"):
        teks = teks[1:]
    try:
        ambang = float(teks)
    except (TypeError, ValueError):
        return False
    return float(nilai) >= ambang


def _nilai_kemiripan(item):
    sim = item.get("similarity")
    if sim is None:
        return -1.0
    try:
        return float(sim)
    except (TypeError, ValueError):
        return -1.0


def _urutkan_serupa(items, urut):
    if urut == "rating":
        return sorted(
            items,
            key=lambda item: (
                -(item.get("vote_average") if item.get("vote_average") is not None else -1.0),
                -_nilai_kemiripan(item),
            ),
        )
    if urut == "tahun":
        return sorted(
            items,
            key=lambda item: (
                item.get("release_year") is None,
                -(item.get("release_year") or 0),
                -_nilai_kemiripan(item),
            ),
        )
    return items


def get_similar(movie_id, n, genre=None, tahun=None, rating=None, urut="kemiripan"):
    """Ambil rekomendasi, opsional filter/urut, lalu potong menjadi n item.

    Untuk filter atau pengurutan selain kemiripan, kandidat diambil lebih banyak
    (N_KANDIDAT_SERUPA) agar hasil setelah filter tidak cepat habis.
    Mengembalikan (hasil, jumlah_setelah_filter, jumlah_kandidat).
    """
    urut = (urut or "kemiripan").strip().lower()
    if urut not in {"kemiripan", "rating", "tahun"}:
        urut = "kemiripan"
    genre = (str(genre).strip() or None) if genre not in (None, "") else None
    tahun = (str(tahun).strip() or None) if tahun not in (None, "") else None
    rating = (str(rating).strip() or None) if rating not in (None, "") else None

    ada_filter = bool(genre or tahun or rating)
    butuh_pool = ada_filter or urut != "kemiripan"
    jumlah = max(int(n), N_KANDIDAT_SERUPA) if butuh_pool else int(n)
    kandidat = _rekomendasi(movie_id, jumlah)
    tersaring = [
        item
        for item in kandidat
        if _cocok_genre(item, genre)
        and _cocok_tahun(item.get("release_year"), tahun)
        and _cocok_rating(item, rating)
    ]
    tersaring = _urutkan_serupa(tersaring, urut)
    return tersaring[: int(n)], len(tersaring), len(kandidat)


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
    history_count = 0

    if g.get("user") and not has_searched:
        history, history_count, _ = _riwayat_pengguna(g.user.id)

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
        history_count=history_count,
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

    dari = request.args.get("dari", type=int)
    why = None
    source_movie = None
    if dari:
        sumber = db.session.get(Movie, dari)
        if sumber is not None:
            source_movie = _film_ke_dict(sumber)
        try:
            for item in _rekomendasi(dari, N_SERUPA):
                if int(item["id"]) == int(movie.id):
                    why = dict(item)
                    if source_movie is not None:
                        why["source_title"] = source_movie["title"]
                    break
        except Exception:
            why = None

    film = _film_ke_dict(movie)
    rekomendasi, _, _ = get_similar(movie.id, N_DETAIL)
    return render_template(
        "pages/movie_detail.html",
        movie=film,
        recommendations=rekomendasi,
        source_movie=source_movie,
        why=why,
        runtime_str=film["duration"],
        cast=film["cast"],
    )


@main.route("/cari-serupa")
def find_similar():
    film_raw = request.args.get("film")
    selected_raw = request.args.get("selected")
    query = (request.args.get("q") or "").strip()
    genre = (request.args.get("genre") or "").strip() or None
    tahun = (request.args.get("tahun") or "").strip() or None
    rating = (request.args.get("rating") or "").strip() or None
    urut = (request.args.get("urut") or "kemiripan").strip() or "kemiripan"
    if urut.lower() not in {"kemiripan", "rating", "tahun"}:
        urut = "kemiripan"
    else:
        urut = urut.lower()

    # Parameter baru `film` menampilkan hasil langsung. `selected` + `hasil=1`
    # tetap didukung agar tautan template yang ada tidak rusak.
    id_acuan = None
    if film_raw not in (None, ""):
        try:
            id_acuan = int(film_raw)
        except (TypeError, ValueError):
            abort(404)
    elif selected_raw not in (None, ""):
        try:
            id_acuan = int(selected_raw)
        except (TypeError, ValueError):
            abort(404)

    tampilkan_langsung = film_raw not in (None, "")
    show_results = tampilkan_langsung or request.args.get("hasil") == "1"

    selected_movie = None
    if id_acuan is not None:
        terpilih = db.session.get(Movie, id_acuan)
        if terpilih is None:
            abort(404)
        selected_movie = _film_ke_dict(terpilih)

    similar_movies: list[dict] = []
    filtered_count = 0
    total_candidates = 0
    if selected_movie and show_results:
        similar_movies, filtered_count, total_candidates = get_similar(
            selected_movie["id"],
            N_SERUPA,
            genre=genre,
            tahun=tahun,
            rating=rating,
            urut=urut,
        )

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
        film=id_acuan,
        genre=genre,
        tahun=tahun,
        rating=rating,
        urut=urut,
        filtered_count=filtered_count,
        total_candidates=total_candidates,
        all_genres=ALL_GENRES,
    )


@main.route("/riwayat/hapus", methods=["POST"])
@login_required
def clear_history():
    SearchHistory.query.filter_by(user_id=g.user.id).delete()
    db.session.commit()
    return redirect(url_for("main.explore"))


@main.route("/riwayat/hapus/<int:movie_id>", methods=["POST"])
@login_required
def clear_single_history(movie_id):
    SearchHistory.query.filter_by(
        user_id=g.user.id,
        movie_id=movie_id
    ).delete()

    db.session.commit()
    return redirect(url_for("main.explore"))
