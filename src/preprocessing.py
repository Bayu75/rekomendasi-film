"""Preprocessing data film dan pembentukan kolom ``tags`` (PRD §10, langkah 1).

Input : ``data/processed/movies_clean_final.csv`` dengan 9 kolom
        id, title, overview, genres_list, keywords_list, director,
        release_year, vote_average, vote_count
Output: DataFrame bersih (``prepare_movies``) dan teks ``tags`` per film (``build_tags``).

Penghapusan stopword bahasa Inggris dilakukan oleh ``TfidfVectorizer(stop_words="english")``
di ``build_model.py``, jadi tidak diulang di sini.
"""
from __future__ import annotations

import re

import pandas as pd

LIST_SEP = "|"

REQUIRED_COLUMNS = [
    "id",
    "title",
    "overview",
    "genres_list",
    "keywords_list",
    "director",
    "release_year",
    "vote_average",
    "vote_count",
]

_APOSTROPHE = re.compile(r"['’`]")
_NON_ALNUM = re.compile(r"[^a-z0-9\s]")
_SPACES = re.compile(r"\s+")


def is_missing(value) -> bool:
    """True untuk None / NaN / pd.NA."""
    if value is None:
        return True
    try:
        return bool(pd.isna(value))
    except (TypeError, ValueError):
        return False


def split_list(value) -> list[str]:
    """``"Action|Crime"`` -> ``["Action", "Crime"]``. Nilai kosong -> ``[]``."""
    if is_missing(value):
        return []
    return [p.strip() for p in str(value).split(LIST_SEP) if p.strip()]


def clean_text(text) -> str:
    """Case folding + hapus tanda baca. Apostrof dibuang ("one's" -> "ones"),
    tanda baca lain diganti spasi ("spider-man" -> "spider man")."""
    if is_missing(text):
        return ""
    s = str(text).lower()
    s = _APOSTROPHE.sub("", s)
    s = _NON_ALNUM.sub(" ", s)
    return _SPACES.sub(" ", s).strip()


def squash(text) -> str:
    """Bersihkan lalu hapus spasi: "Science Fiction" -> "sciencefiction",
    "Christopher Nolan" -> "christophernolan". Dipakai untuk genre dan sutradara
    supaya satu nama = satu token (tidak bercampur dengan kata lain di sinopsis)."""
    return clean_text(text).replace(" ", "")


def build_tags(
    overview,
    genres: list[str],
    keywords: list[str],
    director,
    genre_weight: int = 1,
    keyword_weight: int = 1,
    director_weight: int = 1,
) -> str:
    """Gabungkan overview + genre + keyword + sutradara menjadi satu teks.

    ``*_weight`` adalah berapa kali bagian itu diulang. Ini cara sederhana
    menaikkan bobot TF (``TfidfVectorizer`` memakai ``sublinear_tf``).
    """
    parts: list[str] = [clean_text(overview)]
    parts += [squash(g) for g in genres] * genre_weight
    parts += [clean_text(k) for k in keywords] * keyword_weight
    # sutradara bisa lebih dari satu ("A|B"): tiap orang jadi satu token sendiri
    for d in dict.fromkeys(squash(x) for x in split_list(director)):
        if d:
            parts += [d] * director_weight
    return _SPACES.sub(" ", " ".join(p for p in parts if p)).strip()


def prepare_movies(df: pd.DataFrame) -> pd.DataFrame:
    """Validasi dan rapikan CSV mentah menjadi tabel yang dipakai model.

    - kolom wajib harus ada;
    - id duplikat dibuang (``keep='first'``, sama seperti bagian data);
    - kolom list dipecah menjadi list Python: ``genres`` dan ``keywords``;
    - teks kosong -> ``""``, vote kosong -> 0;
    - ``release_year`` kosong tetap ``<NA>`` (nanti jadi ``None``).
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ada di CSV: {missing}")

    out = df[REQUIRED_COLUMNS].copy()
    out = out.dropna(subset=["id", "title"])
    out["id"] = out["id"].astype("int64")
    out = out.drop_duplicates(subset="id", keep="first").reset_index(drop=True)

    out["title"] = out["title"].astype(str)
    out["overview"] = out["overview"].fillna("").astype(str)
    out["director"] = out["director"].fillna("").astype(str)
    out["genres"] = out["genres_list"].map(split_list)
    out["keywords"] = out["keywords_list"].map(split_list)
    out["vote_average"] = pd.to_numeric(out["vote_average"], errors="coerce").fillna(0.0)
    out["vote_count"] = pd.to_numeric(out["vote_count"], errors="coerce").fillna(0).astype("int64")
    out["release_year"] = pd.to_numeric(out["release_year"], errors="coerce").astype("Int64")
    return out.drop(columns=["genres_list", "keywords_list"])
