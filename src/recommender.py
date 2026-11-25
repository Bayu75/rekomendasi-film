"""Kontrak MODEL -> BACKEND (PRD §10). Dipakai Flask lewat::

    from src.recommender import recommend, recommend_for_user, popular

* ``recommend(movie_id, n=10)``            -> film serupa (Detail, Cari Film Serupa)
* ``recommend_for_user(history_ids, n=10)`` -> rekomendasi personal (Beranda)
* ``popular(n=10)``                         -> cold start / "Jelajahi Film"

Artefak dimuat SEKALI (lazy, saat pemanggilan pertama) lalu dipakai ulang (NF-01).
Lokasi artefak: env ``MOVIEMATCH_MODEL`` atau ``models/recommender.joblib`` di akar repo.
``movie_id`` yang tidak ada di data -> ``KeyError`` (backend menampilkan 404).

Setiap item hasil adalah dict berisi tipe Python biasa (aman untuk Jinja dan ``json.dumps``)::

    id, title, release_year (int|None), genres (list), director, vote_average, vote_count,
    overview, keywords (list), similarity (0..1, None pada popular()), score,
    reasons (list[str]), source_movie_id (int|None),
    shared_genres (list), shared_keywords (list), same_director (bool), shared_cast ([])
"""
from __future__ import annotations

import os
import threading
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from .preprocessing import split_list

DEFAULT_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "recommender.joblib"


class Recommender:
    """Pembungkus artefak model. Hanya-baca setelah dibuat, jadi aman dipakai antar thread."""

    def __init__(self, bundle: dict):
        self.config: dict = bundle["config"]
        self.matrix = bundle["matrix"]  # csr, baris L2-normalized
        self.movies = bundle["movies"].reset_index(drop=True)

        self._ids = self.movies["id"].to_numpy()
        self._id_to_idx = {int(i): k for k, i in enumerate(self._ids)}
        self._rating = self.movies["rating_score"].to_numpy(dtype=np.float64)
        self._genres = self.movies["genres"].tolist()
        self._keywords = self.movies["keywords"].tolist()
        # "director" di CSV bisa berisi beberapa nama dipisah "|"
        self._directors = [list(dict.fromkeys(split_list(d))) for d in self.movies["director"]]

        # popular(): urut weighted rating menurun; seri -> vote_count terbanyak, lalu id
        order = np.lexsort((self._ids, -self.movies["vote_count"].to_numpy(), -self._rating))
        self._popular_order = order

    # ------------------------------------------------------------------ util
    def __len__(self) -> int:
        return len(self.movies)

    def has_movie(self, movie_id: int) -> bool:
        return int(movie_id) in self._id_to_idx

    def _idx(self, movie_id: int) -> int:
        try:
            return self._id_to_idx[int(movie_id)]
        except (KeyError, TypeError, ValueError):
            raise KeyError(f"movie_id {movie_id!r} tidak ada di data") from None

    def _similarity(self, idx: int) -> np.ndarray:
        """Cosine similarity satu film ke semua film (vektor panjang N, dihitung saat diminta)."""
        sims = (self.matrix @ self.matrix[idx].T).toarray().ravel().astype(np.float64)
        return np.clip(sims, 0.0, 1.0)

    def _rank(self, sims: np.ndarray, exclude: set[int], n: int, alpha: float, pool: int):
        """Ambil ``pool`` kandidat teratas menurut similarity, lalu ranking ulang dengan rating.

        score = (1 - alpha) * (sim / sim_maks_pool) + alpha * rating_minmax_pool
        Mengembalikan (indeks film, score) terurut dari score tertinggi, sebanyak <= n.
        """
        sims = sims.copy()
        if exclude:
            sims[list(exclude)] = -1.0
        pool = max(n, pool)
        if pool < len(sims):
            cand = np.argpartition(-sims, pool - 1)[:pool]
        else:
            cand = np.arange(len(sims))
        cand = cand[sims[cand] > 0.0]  # buang yang sama sekali tidak mirip
        if cand.size == 0:
            return cand, np.array([])

        s = sims[cand]
        s_norm = s / s.max()
        r = self._rating[cand]
        span = r.max() - r.min()
        r_norm = (r - r.min()) / span if span > 0 else np.zeros_like(r)
        score = (1.0 - alpha) * s_norm + alpha * r_norm

        # urut: score desc, lalu similarity desc, lalu id asc (hasil deterministik)
        order = np.lexsort((self._ids[cand], -s, -score))[:n]
        return cand[order], score[order]

    def _explain(self, src_idx: int, cand_idx: int):
        """Alasan kemiripan kandidat terhadap film sumber (F-18)."""
        src_genres = set(self._genres[src_idx])
        shared_genres = [g for g in self._genres[cand_idx] if g in src_genres]

        src_kw = set(self._keywords[src_idx])
        shared_keywords, seen = [], set()
        for k in self._keywords[cand_idx]:
            if k in src_kw and k not in seen:
                shared_keywords.append(k)
                seen.add(k)

        src_dir = set(self._directors[src_idx])
        shared_dir = [d for d in self._directors[cand_idx] if d in src_dir]
        same_director = bool(shared_dir)

        reasons: list[str] = []
        if same_director:
            reasons.append("Sutradara sama: " + ", ".join(shared_dir))
        if shared_genres:
            reasons.append("Genre: " + ", ".join(shared_genres[:3]))
        if shared_keywords:
            reasons.append("Kata kunci: " + ", ".join(shared_keywords[:3]))
        if not reasons:
            reasons.append("Sinopsis dan tema mirip")
        return shared_genres, shared_keywords, same_director, reasons

    def _item(self, idx: int, similarity, score: float, src_idx: int | None) -> dict:
        row = self.movies.iloc[idx]
        year = row["release_year"]
        if src_idx is not None:
            sg, sk, sd, reasons = self._explain(src_idx, idx)
        else:
            sg, sk, sd, reasons = [], [], False, ["Rating tinggi dari banyak penonton"]
        return {
            "id": int(row["id"]),
            "title": str(row["title"]),
            "release_year": None if pd.isna(year) else int(year),
            "genres": list(self._genres[idx]),
            "director": ", ".join(self._directors[idx]),
            "vote_average": float(row["vote_average"]),
            "vote_count": int(row["vote_count"]),
            "overview": str(row["overview"]),
            "keywords": list(self._keywords[idx]),
            "similarity": None if similarity is None else round(float(similarity), 4),
            "score": round(float(score), 4),
            "reasons": reasons,
            "source_movie_id": None if src_idx is None else int(self._ids[src_idx]),
            "shared_genres": sg,
            "shared_keywords": sk,
            "same_director": sd,
            "shared_cast": [],  # CSV tidak punya cast (isu #2 PRD)
        }

    # ------------------------------------------------------------- API publik
    def recommend(self, movie_id: int, n: int = 10, *, alpha: float | None = None,
                  pool: int | None = None) -> list[dict]:
        """Film serupa untuk satu film acuan. Film acuan tidak ikut dikembalikan."""
        idx = self._idx(movie_id)
        if n <= 0:
            return []
        alpha = self.config["alpha"] if alpha is None else alpha
        pool = self.config["pool"] if pool is None else pool
        sims = self._similarity(idx)
        cand, scores = self._rank(sims, {idx}, n, alpha, pool)
        return [self._item(int(c), sims[c], sc, idx) for c, sc in zip(cand, scores)]

    def recommend_for_user(self, history_ids: list[int], n: int = 10, *,
                           alpha: float | None = None, pool: int | None = None,
                           max_history: int | None = None, agg: str | None = None) -> list[dict]:
        """Rekomendasi personal dari riwayat.

        ``history_ids`` diurutkan dari yang TERBARU. Hanya ``max_history`` film terbaru
        (default 10) yang dipakai. Id ganda dan id yang tidak ada di data dilewati. Kandidat
        dari tiap film riwayat digabung, duplikat dibuang, film riwayat dikecualikan (F-14, F-15).
        ``similarity`` = kemiripan tertinggi ke salah satu film riwayat, dan ``source_movie_id``
        = film riwayat asalnya. Riwayat kosong -> ``popular(n)`` (cold start, NF-03).
        """
        if n <= 0:
            return []
        alpha = self.config["alpha"] if alpha is None else alpha
        pool = self.config["pool"] if pool is None else pool
        max_history = self.config["max_history"] if max_history is None else max_history
        agg = self.config["agg"] if agg is None else agg
        if agg not in ("max", "mean"):
            raise ValueError("agg harus 'max' atau 'mean'")

        idxs: list[int] = []
        for h in history_ids or []:
            k = self._id_to_idx.get(int(h)) if h is not None else None
            if k is not None and k not in idxs:
                idxs.append(k)
        if not idxs:
            return self.popular(n)
        idxs = idxs[:max_history]

        S = np.vstack([self._similarity(k) for k in idxs])  # (h, N)
        combined = S.max(axis=0) if agg == "max" else S.mean(axis=0)
        cand, scores = self._rank(combined, set(idxs), n, alpha, pool)

        out = []
        for c, sc in zip(cand, scores):
            best = int(np.argmax(S[:, c]))
            out.append(self._item(int(c), S[best, c], sc, idxs[best]))
        return out

    def popular(self, n: int = 10) -> list[dict]:
        """Film populer berdasarkan weighted rating (vote_average + vote_count). ``similarity`` = None."""
        if n <= 0:
            return []
        return [self._item(int(i), None, self._rating[i], None) for i in self._popular_order[:n]]


# ---------------------------------------------------------------- singleton
_lock = threading.RLock()
_model: Recommender | None = None


def load_model(path: str | os.PathLike | None = None) -> Recommender:
    """Muat artefak dari disk dan jadikan model global."""
    global _model
    path = Path(path or os.environ.get("MOVIEMATCH_MODEL") or DEFAULT_MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(
            f"Artefak model tidak ditemukan: {path}. Bangun dulu dengan "
            "`python -m src.build_model --csv data/movies_clean_final.csv`."
        )
    with _lock:
        _model = Recommender(joblib.load(path))
    return _model


def get_model() -> Recommender:
    if _model is None:
        with _lock:
            if _model is None:
                load_model()
    return _model  # type: ignore[return-value]


def recommend(movie_id: int, n: int = 10) -> list[dict]:
    return get_model().recommend(movie_id, n)


def recommend_for_user(history_ids: list[int], n: int = 10) -> list[dict]:
    return get_model().recommend_for_user(history_ids, n)


def popular(n: int = 10) -> list[dict]:
    return get_model().popular(n)
