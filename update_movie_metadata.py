
import pandas as pd
from sqlalchemy import text

from app import create_app
from app.models import db


CSV_PATH = "data/processed/movies_clean_final (2).csv"


def main():
    app = create_app()

    with app.app_context():
        print("Membaca dataset...")

        df = pd.read_csv(CSV_PATH)

        # Pastikan kolom yang diperlukan tersedia
        kolom_wajib = {"id", "runtime", "cast_list"}
        if not kolom_wajib.issubset(df.columns):
            raise ValueError("Kolom id, runtime, atau cast_list tidak ditemukan.")

        # Siapkan data yang akan diperbarui
        df = df[["id", "runtime", "cast_list"]].copy()
        df = df.dropna(subset=["id"])
        df = df.drop_duplicates(subset=["id"], keep="last")

        data = []

        for row in df.itertuples(index=False):
            data.append({
                "id": int(row.id),
                "runtime": (
                    float(row.runtime)
                    if pd.notna(row.runtime)
                    else None
                ),
                "cast_list": (
                    str(row.cast_list)
                    if pd.notna(row.cast_list)
                    else None
                ),
            })

        print(f"Jumlah data CSV: {len(data)}")
        print("Memperbarui database...")

        query = text("""
            UPDATE movies
            SET runtime = :runtime,
                cast_list = :cast_list
            WHERE id = :id
        """)

        with db.engine.begin() as connection:
            connection.execute(query, data)

        print("Selesai memperbarui data film!")


if __name__ == "__main__":
    main()
