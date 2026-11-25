"""Bangun artefak model dari CSV (PRD §10, langkah 1-2; NF-04).

Pemakaian::

    python -m src.build_model --csv data/movies_clean_final.csv --out models/recommender.joblib

Artefak berisi: vectorizer TF-IDF, matriks TF-IDF sparse (sudah L2-normalized sehingga
cosine similarity = perkalian titik), tabel film, dan konfigurasi. Matriks similarity
penuh TIDAK disimpan (45.430 x 45.430 float64 ~ 16,5 GB).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from .preprocessing import build_tags, prepare_movies

ARTIFACT_VERSION = 1

# Nilai awal. Bobot akhir (alpha, dst.) diputuskan lewat eksperimen di notebook (isu #4 PRD).
DEFAULT_CONFIG: dict = {
    # --- pembentukan tags
    "genre_weight": 1,
    "keyword_weight": 1,
    "director_weight": 1,
    # --- TF-IDF
    "min_df": 2,
    "max_df": 0.8,
    "ngram_range": (1, 1),
    "sublinear_tf": True,
    # --- rating (Bayesian weighted rating, dipakai ranking dan popular())
    "min_votes_quantile": 0.80,
    # --- ranking: score = (1 - alpha) * similarity_ternormalisasi + alpha * rating_ternormalisasi
    "alpha": 0.2,
    "pool": 200,  # jumlah kandidat teratas menurut similarity yang diranking ulang
    # --- personalisasi
    "max_history": 10,
    "agg": "max",  # "max" | "mean": cara menggabungkan similarity dari banyak film riwayat
}


def weighted_rating(df: pd.DataFrame, min_votes_quantile: float) -> pd.Series:
    """Weighted rating gaya IMDb: WR = v/(v+m)*R + m/(v+m)*C, lalu dibagi 10 -> 0..1.

    R = vote_average, v = vote_count, C = rata-rata vote_average, m = kuantil vote_count.
    Film dengan sedikit vote ditarik ke rata-rata C sehingga tidak mendominasi (US-12).
    """
    rated = df[df["vote_count"] > 0]
    c = float(rated["vote_average"].mean()) if len(rated) else 0.0
    m = float(rated["vote_count"].quantile(min_votes_quantile)) if len(rated) else 0.0
    v = df["vote_count"].astype(float)
    r = df["vote_average"].astype(float)
    denom = (v + m).replace(0, np.nan)
    wr = (v / denom * r + m / denom * c).fillna(c)
    return (wr / 10.0).clip(0.0, 1.0)


def build_bundle(df_raw: pd.DataFrame, **overrides) -> dict:
    """Bangun artefak di memori dari DataFrame CSV mentah."""
    config = {**DEFAULT_CONFIG, **overrides}
    unknown = set(overrides) - set(DEFAULT_CONFIG)
    if unknown:
        raise ValueError(f"Parameter tidak dikenal: {sorted(unknown)}")

    movies = prepare_movies(df_raw)
    tags = [
        build_tags(
            row.overview,
            row.genres,
            row.keywords,
            row.director,
            genre_weight=config["genre_weight"],
            keyword_weight=config["keyword_weight"],
            director_weight=config["director_weight"],
        )
        for row in movies.itertuples(index=False)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        min_df=config["min_df"],
        max_df=config["max_df"],
        ngram_range=tuple(config["ngram_range"]),
        sublinear_tf=config["sublinear_tf"],
        dtype=np.float32,
    )
    matrix = vectorizer.fit_transform(tags).tocsr()  # baris sudah L2-normalized

    movies["rating_score"] = weighted_rating(movies, config["min_votes_quantile"]).to_numpy()
    return {
        "version": ARTIFACT_VERSION,
        "config": config,
        "vectorizer": vectorizer,
        "matrix": matrix,
        "movies": movies,
    }


def save_bundle(bundle: dict, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, path, compress=3)
    return path


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description="Bangun artefak model MovieMatch dari CSV.")
    p.add_argument("--csv", default="data/movies_clean_final.csv")
    p.add_argument("--out", default="models/recommender.joblib")
    p.add_argument("--alpha", type=float, default=None, help="bobot rating pada ranking (0..1)")
    args = p.parse_args(argv)

    overrides = {} if args.alpha is None else {"alpha": args.alpha}
    df = pd.read_csv(args.csv)
    bundle = build_bundle(df, **overrides)
    out = save_bundle(bundle, args.out)
    print(
        f"{len(bundle['movies'])} film | {bundle['matrix'].shape[1]} fitur TF-IDF | "
        f"{bundle['matrix'].nnz} nilai tak-nol -> {out}"
    )


if __name__ == "__main__":
    main()
