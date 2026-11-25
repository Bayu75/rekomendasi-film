"""Impor data film dari CSV bersih ke tabel `movies` di MySQL.

Cara menjalankan (dari folder utama proyek):
    python scripts/import_csv.py
    python scripts/import_csv.py --csv data/processed/movies_clean_final.csv
    python scripts/import_csv.py --replace   # kosongkan tabel movies dulu, lalu impor ulang
"""

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app import create_app  # noqa: E402
from app.models import Movie, SearchHistory, db  # noqa: E402

DEFAULT_CSV = ROOT_DIR / "data" / "processed" / "movies_clean_final.csv"
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
BATCH_SIZE = 1000


def kosong(value):
    return value is None or (isinstance(value, float) and math.isnan(value)) or value is pd.NA


def teks(value, max_len=None):
    if kosong(value):
        return None
    value = str(value).strip()
    if not value:
        return None
    return value[:max_len] if max_len else value


def angka_bulat(value):
    if kosong(value):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def rating(value):
    if kosong(value):
        return None
    try:
        value = round(float(value), 1)
    except (TypeError, ValueError):
        return None
    return min(max(value, 0.0), 10.0)


def baris_ke_dict(row):
    return {
        "id": int(row["id"]),
        "title": teks(row["title"], 255),
        "overview": teks(row["overview"]),
        "genres": teks(row["genres_list"], 255),
        "keywords": teks(row["keywords_list"]),
        "director": teks(row["director"], 255),
        "release_year": angka_bulat(row["release_year"]),
        "vote_average": rating(row["vote_average"]),
        "vote_count": angka_bulat(row["vote_count"]) or 0,
        "poster_path": None,
    }


def main():
    parser = argparse.ArgumentParser(description="Impor CSV film ke tabel movies.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Path file CSV bersih.")
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Hapus semua isi tabel movies (dan riwayat) sebelum impor.",
    )
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        sys.exit(f"File CSV tidak ditemukan: {csv_path}")

    df = pd.read_csv(csv_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        sys.exit(f"Kolom CSV kurang: {missing}")

    df = df.dropna(subset=["id", "title"])
    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df = df.dropna(subset=["id"])
    df["id"] = df["id"].astype("int64")
    df = df.drop_duplicates(subset="id", keep="first")
    print(f"Baris valid di CSV: {len(df)}")

    app = create_app()
    with app.app_context():
        if args.replace:
            SearchHistory.query.delete()
            Movie.query.delete()
            db.session.commit()
            print("Tabel movies dan search_history dikosongkan.")

        sudah_ada = {row[0] for row in db.session.query(Movie.id).all()}
        baru = [baris_ke_dict(r) for r in df.to_dict("records") if int(r["id"]) not in sudah_ada]
        print(f"Sudah ada di database: {len(sudah_ada)}, akan diimpor: {len(baru)}")

        for start in range(0, len(baru), BATCH_SIZE):
            batch = baru[start:start + BATCH_SIZE]
            db.session.execute(db.insert(Movie), batch)
            db.session.commit()
            print(f"  {min(start + BATCH_SIZE, len(baru))}/{len(baru)} film tersimpan")

        total = db.session.query(Movie).count()
        print(f"Selesai. Total film di tabel movies: {total}")


if __name__ == "__main__":
    main()