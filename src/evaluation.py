"""Evaluasi model: Precision@K dan Recall@K (PRD §14, US-17).

DEFINISI "FILM RELEVAN" [USULAN, perlu disepakati tim sebelum angka dilaporkan]
-------------------------------------------------------------------------------
Film ``j`` relevan terhadap film acuan ``q`` jika kemiripan genre (Jaccard) >= ``min_jaccard``
(default 0,5). Contoh: {Action, Crime, Drama} vs {Action, Crime} -> 2/3 -> relevan.

Catatan jujur untuk laporan:
* Genre ikut dipakai di ``tags``, jadi pengukuran ini tidak sepenuhnya independen dari model.
  Tanpa label penilaian pengguna, ini proxy yang paling umum dipakai. Skor SUS dan penilaian
  manual melengkapinya.
* Himpunan relevan sangat besar (ratusan film), jadi Recall@K otomatis kecil. Itu sifat
  definisinya, bukan tanda model buruk. Bandingkan dengan baseline (acak, populer) yang
  disediakan di sini, bukan dengan angka 1.0.

Tiga fungsi yang diuji (sesuai PRD §14):
1. ``evaluate_similar``   : ``recommend(q, n)``                        (halaman Detail)
2. ``evaluate_personal``  : ``recommend_for_user(riwayat, n)``         (Beranda, pengguna simulasi)
3. ``evaluate_manual``    : ``recommend(q, 12)`` dengan q dari film populer (Cari Film Serupa,
                            karena UI menawarkan film populer sebagai pilihan acuan)
"""
from __future__ import annotations

from typing import Callable, Iterable

import numpy as np
import pandas as pd
from scipy import sparse

from .recommender import Recommender

KS = (5, 10)


# --------------------------------------------------------------------- metrik
def precision_at_k(recommended: list[int], relevant: set[int], k: int) -> float:
    top = recommended[:k]
    if not top:
        return 0.0
    return sum(1 for r in top if r in relevant) / len(top)


def recall_at_k(recommended: list[int], relevant: set[int], k: int) -> float:
    if not relevant:
        return 0.0
    return sum(1 for r in recommended[:k] if r in relevant) / len(relevant)


# ------------------------------------------------------------------ relevansi
class GenreRelevance:
    """Hitung himpunan film relevan lewat Jaccard genre (vektor, tanpa loop per film)."""

    def __init__(self, model: Recommender, min_jaccard: float = 0.5):
        self.model = model
        self.min_jaccard = min_jaccard
        vocab = sorted({g for gs in model._genres for g in gs})
        col = {g: i for i, g in enumerate(vocab)}
        rows, cols = [], []
        for r, gs in enumerate(model._genres):
            for g in gs:
                rows.append(r)
                cols.append(col[g])
        self.G = sparse.csr_matrix(
            (np.ones(len(rows), dtype=np.float32), (rows, cols)), shape=(len(model), len(vocab))
        )
        self.sizes = np.asarray(self.G.sum(axis=1)).ravel()

    def jaccard(self, idx: int) -> np.ndarray:
        inter = (self.G @ self.G[idx].T).toarray().ravel()
        union = self.sizes + self.sizes[idx] - inter
        with np.errstate(divide="ignore", invalid="ignore"):
            j = np.where(union > 0, inter / union, 0.0)
        return j

    def relevant_idx(self, idx: int) -> np.ndarray:
        mask = self.jaccard(idx) >= self.min_jaccard
        mask[idx] = False
        return np.flatnonzero(mask)

    def relevant_ids(self, movie_id: int) -> set[int]:
        idx = self.model._idx(movie_id)
        return {int(self.model._ids[i]) for i in self.relevant_idx(idx)}


# ------------------------------------------------------------------- baseline
def random_baseline(model: Recommender, seed: int = 0) -> Callable[[int, int], list[dict]]:
    rng = np.random.default_rng(seed)

    def fn(movie_id: int, n: int) -> list[dict]:
        idx = model._idx(movie_id)
        picks = rng.choice(len(model), size=min(n + 1, len(model)), replace=False)
        picks = [int(i) for i in picks if i != idx][:n]
        return [{"id": int(model._ids[i])} for i in picks]

    return fn


def popular_baseline(model: Recommender) -> Callable[[int, int], list[dict]]:
    def fn(movie_id: int, n: int) -> list[dict]:
        idx = model._idx(movie_id)
        order = [i for i in model._popular_order[: n + 1] if i != idx][:n]
        return [{"id": int(model._ids[i])} for i in order]

    return fn


# -------------------------------------------------------------------- sampling
def sample_queries(model: Recommender, n_queries: int = 300, seed: int = 42,
                   min_votes: int = 50, from_popular: int | None = None) -> list[int]:
    """Pilih film acuan acak yang punya genre (dan cukup vote). ``from_popular=N`` membatasi
    ke N film teratas ``popular()``, meniru pilihan di halaman Cari Film Serupa."""
    rng = np.random.default_rng(seed)
    movies = model.movies
    ok = movies["vote_count"].to_numpy() >= min_votes
    ok &= np.array([len(g) > 0 for g in model._genres])
    if from_popular is not None:
        top = np.zeros(len(movies), dtype=bool)
        top[model._popular_order[:from_popular]] = True
        ok &= top
    cand = np.flatnonzero(ok)
    if cand.size == 0:
        raise ValueError("Tidak ada film acuan yang memenuhi syarat")
    picks = rng.choice(cand, size=min(n_queries, cand.size), replace=False)
    return [int(model._ids[i]) for i in picks]


# ----------------------------------------------------------------- evaluators
def _summarize(rows: list[dict], ks: Iterable[int]) -> dict:
    df = pd.DataFrame(rows)
    out = {"n_queries": len(df), "avg_relevant": float(df["n_relevant"].mean()) if len(df) else 0.0}
    for k in ks:
        out[f"P@{k}"] = float(df[f"P@{k}"].mean()) if len(df) else 0.0
        out[f"R@{k}"] = float(df[f"R@{k}"].mean()) if len(df) else 0.0
    return out


def evaluate_similar(model: Recommender, query_ids: list[int], ks=KS, n: int | None = None,
                     min_jaccard: float = 0.5, recommend_fn: Callable | None = None,
                     **kwargs) -> dict:
    """Precision/Recall@K untuk film serupa. ``recommend_fn(movie_id, n)`` boleh diganti
    (baseline); ``kwargs`` (mis. ``alpha=0.3``) diteruskan ke ``model.recommend``."""
    rel = GenreRelevance(model, min_jaccard)
    n = n or max(ks)
    fn = recommend_fn or (lambda mid, nn: model.recommend(mid, nn, **kwargs))
    rows, skipped = [], 0
    for q in query_ids:
        relevant = rel.relevant_ids(q)
        if not relevant:
            skipped += 1
            continue
        rec_ids = [r["id"] for r in fn(q, n)]
        row = {"n_relevant": len(relevant)}
        for k in ks:
            row[f"P@{k}"] = precision_at_k(rec_ids, relevant, k)
            row[f"R@{k}"] = recall_at_k(rec_ids, relevant, k)
        rows.append(row)
    res = _summarize(rows, ks)
    res["skipped_no_relevant"] = skipped
    return res


def evaluate_manual(model: Recommender, n_queries: int = 100, seed: int = 42, ks=KS,
                    n: int = 12, popular_pool: int = 200, min_jaccard: float = 0.5,
                    **kwargs) -> dict:
    """Cari Film Serupa manual: acuan dipilih dari film populer, hasil 12 film (PRD isu #5)."""
    q = sample_queries(model, n_queries, seed, from_popular=popular_pool)
    return evaluate_similar(model, q, ks=ks, n=n, min_jaccard=min_jaccard, **kwargs)


def simulate_users(model: Recommender, n_users: int = 100, history_size: int = 3,
                   min_jaccard: float = 0.5, min_rating: float = 6.5, seed: int = 7,
                   min_holdout: int = 5):
    """Pengguna simulasi: satu film acuan q0 menentukan 'selera'. Film yang disukai =
    film berating >= ``min_rating`` yang relevan terhadap q0 (Jaccard genre). Riwayat =
    ``history_size`` film acak dari kumpulan itu (termasuk q0); sisanya jadi himpunan relevan."""
    rng = np.random.default_rng(seed)
    rel = GenreRelevance(model, min_jaccard)
    va = model.movies["vote_average"].to_numpy()
    vc = model.movies["vote_count"].to_numpy()
    seeds = np.flatnonzero((va >= min_rating) & (vc >= 100) & (rel.sizes > 0))
    rng.shuffle(seeds)

    users = []
    for q0 in seeds:
        liked = [i for i in rel.relevant_idx(int(q0)) if va[i] >= min_rating]
        liked = [int(i) for i in liked] + [int(q0)]
        if len(liked) < history_size + min_holdout:
            continue
        hist = [int(q0)] + [int(i) for i in rng.choice([i for i in liked if i != q0],
                                                        size=history_size - 1, replace=False)]
        relevant = {int(model._ids[i]) for i in liked if i not in hist}
        users.append(([int(model._ids[i]) for i in hist], relevant))
        if len(users) >= n_users:
            break
    return users


def evaluate_personal(model: Recommender, n_users: int = 100, history_size: int = 3, ks=KS,
                      min_jaccard: float = 0.5, min_rating: float = 6.5, seed: int = 7,
                      **kwargs) -> dict:
    users = simulate_users(model, n_users, history_size, min_jaccard, min_rating, seed)
    rows = []
    for hist, relevant in users:
        rec_ids = [r["id"] for r in model.recommend_for_user(hist, max(ks), **kwargs)]
        row = {"n_relevant": len(relevant)}
        for k in ks:
            row[f"P@{k}"] = precision_at_k(rec_ids, relevant, k)
            row[f"R@{k}"] = recall_at_k(rec_ids, relevant, k)
        rows.append(row)
    res = _summarize(rows, ks)
    res["skipped_no_relevant"] = 0
    return res


def evaluate_all(model: Recommender, n_queries: int = 300, n_users: int = 100, seed: int = 42,
                 min_jaccard: float = 0.5, ks=KS) -> pd.DataFrame:
    """Tabel ringkas 3 fungsi x (P@5, R@5, P@10, R@10), siap ditempel ke laporan."""
    q = sample_queries(model, n_queries, seed)
    rows = {
        "Film serupa (recommend)": evaluate_similar(model, q, ks=ks, min_jaccard=min_jaccard),
        "Rekomendasi personal (recommend_for_user)": evaluate_personal(
            model, n_users, ks=ks, min_jaccard=min_jaccard),
        "Cari film serupa manual (recommend, n=12)": evaluate_manual(
            model, min(n_queries, 100), seed, ks=ks, min_jaccard=min_jaccard),
    }
    cols = [f"{m}@{k}" for k in ks for m in ("P", "R")]
    df = pd.DataFrame(rows).T[cols + ["avg_relevant", "n_queries"]]
    return df
