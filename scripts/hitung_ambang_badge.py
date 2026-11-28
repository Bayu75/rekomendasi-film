"""Hitung ambang warna badge kemiripan dari data asli.

Skrip berdiri sendiri: tidak mengubah src/ dan tidak menyimpan model.
Jalankan dari folder utama proyek:
    python scripts/hitung_ambang_badge.py
    python scripts/hitung_ambang_badge.py --csv data/processed/movies_clean_final.csv --queries 500
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.build_model import build_bundle  # noqa: E402
from src.evaluation import sample_queries  # noqa: E402
from src.recommender import Recommender  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=str(ROOT / "data/processed/movies_clean_final.csv"))
    ap.add_argument("--queries", type=int, default=500)
    a = ap.parse_args()

    model = Recommender(build_bundle(pd.read_csv(a.csv)))
    q = sample_queries(model, a.queries, 42)

    semua, top1, top6 = [], [], []
    for i in q:
        recs = model.recommend(i, 15)
        p = [r["similarity_percent"] for r in recs if r["similarity_percent"] is not None]
        semua += p
        top1 += p[:1]
        top6 += p[:6]
    semua = np.array(semua)
    print(f"{len(q)} query, {len(semua)} hasil.\n")
    print("Persentil similarity_percent (semua hasil Top-15):")
    for pct in (10, 25, 40, 50, 60, 75, 90):
        print(f"  P{pct:<3d}: {np.percentile(semua, pct):.0f}%")
    print(f"\nRata-rata hasil #1: {np.mean(top1):.0f}% | rata-rata Top-6: {np.mean(top6):.0f}%")
    tinggi, sedang = np.percentile(semua, 75), np.percentile(semua, 40)
    print("\nUsulan ambang badge (bulatkan ke 5 terdekat):")
    print(f"  hijau/utama  (sangat mirip) : >= {round(tinggi / 5) * 5:.0f}%")
    print(f"  hijau muda   (mirip)        : >= {round(sedang / 5) * 5:.0f}%")
    print("  abu-abu      (cukup mirip)  : di bawahnya")


if __name__ == "__main__":
    main()
