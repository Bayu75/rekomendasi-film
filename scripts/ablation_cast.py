"""Ablasi cast: bandingkan model TANPA cast vs DENGAN cast pada data asli.

Skrip ini berdiri sendiri. Tidak mengubah file di src/, tidak menyentuh
models/recommender.joblib, dan tidak menyimpan model apa pun.

Jalankan dari folder utama proyek:
    python scripts/ablation_cast.py
    python scripts/ablation_cast.py --csv data/processed/movies_clean_final.csv --queries 300

Keluaran (folder reports/):
    ablation_cast.csv        metrik tiap varian
    ablation_cast_top10.txt  Top-10 sebelum/sesudah cast untuk beberapa film
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.build_model import build_bundle  # noqa: E402
from src.evaluation import (  # noqa: E402
    GenreRelevance, evaluate_personal, evaluate_similar, sample_queries,
)
from src.preprocessing import build_tags, split_list, squash  # noqa: E402
from src.recommender import Recommender  # noqa: E402

# (nama varian, jumlah pemeran teratas, bobot). N=0 -> tanpa cast (baseline).
VARIAN = [
    ("tanpa_cast", 0, 0),
    ("cast_top3_w1", 3, 1),
    ("cast_top5_w1", 5, 1),
    ("cast_top5_w2", 5, 2),
]
UJI_MANUAL = [155, 862, 597, 27205, 11]  # Dark Knight, Toy Story, Titanic, Inception, Star Wars
K_UKUR = 10


def parse_cast(value) -> list[str]:
    """'Nama::Peran|Nama2::Peran2' -> ['Nama', 'Nama2'] (peran dibuang)."""
    if value is None or (isinstance(value, float) and np.isnan(value)) or not str(value).strip():
        return []
    names = [p.split("::", 1)[0].strip() for p in str(value).split("|")]
    return [n for n in dict.fromkeys(names) if n]


def bangun_model(df: pd.DataFrame, base: dict, cast_by_id: dict, top_n: int, w: int) -> Recommender:
    """Bangun ulang matriks TF-IDF dengan parameter yang sama; hanya tags yang ditambah cast."""
    cfg, movies = base["config"], base["movies"]
    tags = []
    for row in movies.itertuples(index=False):
        t = build_tags(row.overview, row.genres, row.keywords, row.director,
                       genre_weight=cfg["genre_weight"], keyword_weight=cfg["keyword_weight"],
                       director_weight=cfg["director_weight"])
        if top_n and w:
            toks = [squash(n) for n in cast_by_id.get(int(row.id), [])[:top_n]]
            t = (t + " " + " ".join(x for x in toks for _ in range(w) if x)).strip()
        tags.append(t)
    vec = TfidfVectorizer(stop_words="english", min_df=cfg["min_df"], max_df=cfg["max_df"],
                          ngram_range=tuple(cfg["ngram_range"]), sublinear_tf=cfg["sublinear_tf"],
                          dtype=np.float32)
    matrix = vec.fit_transform(tags).tocsr()
    return Recommender({**base, "matrix": matrix, "vectorizer": vec})


def metrik_tambahan(model: Recommender, query_ids, cast5_by_id, k=K_UKUR) -> dict:
    """Ukuran di luar genre: pemeran sama, sutradara sama, rata-rata Jaccard genre."""
    rel = GenreRelevance(model)
    pakai_cast, pakai_dir, jac = [], [], []
    for q in query_ids:
        recs = model.recommend(q, k)
        if not recs:
            continue
        qi = model._idx(q)
        qcast = set(cast5_by_id.get(int(q), []))
        qdir = set(split_list(model.movies.iloc[qi]["director"]))
        jv = rel.jaccard(qi)
        for r in recs:
            pakai_cast.append(bool(qcast & set(cast5_by_id.get(int(r["id"]), []))))
            pakai_dir.append(bool(qdir & set(split_list(model.movies.iloc[model._idx(r['id'])]["director"]))))
            jac.append(jv[model._idx(r["id"])])
    return {
        f"cast_sama@{k}": float(np.mean(pakai_cast)) if pakai_cast else 0.0,
        f"sutradara_sama@{k}": float(np.mean(pakai_dir)) if pakai_dir else 0.0,
        f"jaccard_genre@{k}": float(np.mean(jac)) if jac else 0.0,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", default=str(ROOT / "data/processed/movies_clean_final.csv"))
    ap.add_argument("--queries", type=int, default=300)
    ap.add_argument("--users", type=int, default=100)
    ap.add_argument("--out", default=str(ROOT / "reports"))
    a = ap.parse_args()

    df = pd.read_csv(a.csv)
    if "cast_list" not in df.columns:
        sys.exit("Kolom cast_list tidak ada di CSV. Pakai CSV terbaru (12 kolom).")
    cast_by_id = {int(i): parse_cast(c) for i, c in zip(df["id"], df["cast_list"])}
    cast5_by_id = {i: v[:5] for i, v in cast_by_id.items()}
    print(f"Film: {len(df)} | punya cast: {sum(bool(v) for v in cast_by_id.values())}")

    base = build_bundle(df)  # persis model yang dipakai sekarang
    models = {}
    for nama, n, w in VARIAN:
        print("membangun", nama, "...")
        models[nama] = bangun_model(df, base, cast_by_id, n, w)

    q = sample_queries(models["tanpa_cast"], a.queries, 42)  # query yang SAMA untuk semua varian
    rows, tops = [], {}
    for nama, m in models.items():
        s = evaluate_similar(m, q)
        p = evaluate_personal(m, a.users)
        row = {"varian": nama,
               "P@5": s["P@5"], "R@5": s["R@5"], "P@10": s["P@10"], "R@10": s["R@10"],
               "P@5_personal": p["P@5"], "P@10_personal": p["P@10"]}
        row.update(metrik_tambahan(m, q, cast5_by_id))
        tops[nama] = [[r["id"] for r in m.recommend(i, 10)] if m.has_movie(i) else [] for i in q]
        rows.append(row)

    # seberapa banyak Top-10 berubah dibanding baseline (overlap rata-rata, 1 = identik)
    for row in rows:
        ov = [len(set(x) & set(y)) / 10 for x, y in zip(tops["tanpa_cast"], tops[row["varian"]]) if x]
        row["overlap_top10_vs_baseline"] = float(np.mean(ov))

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    res = pd.DataFrame(rows).set_index("varian")
    res.to_csv(out / "ablation_cast.csv")
    pd.set_option("display.width", 200)
    print("\n", res.round(4).T.to_string())

    base_m = models["tanpa_cast"]
    judul = lambda m, i: m.movies.iloc[m._idx(i)]["title"]
    with open(out / "ablation_cast_top10.txt", "w", encoding="utf-8") as f:
        for fid in UJI_MANUAL:
            if not base_m.has_movie(fid):
                continue
            f.write(f"=== {judul(base_m, fid)} (id {fid}) ===\n")
            for nama in ("tanpa_cast", "cast_top3_w1", "cast_top5_w2"):
                f.write(f"[{nama}]\n")
                for r in models[nama].recommend(fid, 10):
                    f.write(f"  {r['title']} ({r['release_year']})\n")
            f.write("\n")
    print(f"\nTersimpan di {out}/ablation_cast.csv dan ablation_cast_top10.txt")


if __name__ == "__main__":
    main()
