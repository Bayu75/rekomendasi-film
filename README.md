# MovieMatch – Sistem Rekomendasi Film

Sistem rekomendasi film content-based (TF-IDF + cosine similarity) dengan Flask, Jinja, Tailwind, dan MySQL. Dataset: Kaggle The Movies Dataset.

## Persiapan

1. `python -m venv .venv` lalu aktifkan (`.venv\Scripts\activate` di Windows, `source .venv/bin/activate` di Linux atau macOS)
2. `pip install -r requirements.txt`
3. Salin `.env.example` menjadi `.env`, lalu isi nilainya:
   - `SECRET_KEY` harus berupa string acak yang panjang. Jangan biarkan kosong atau memakai nilai contoh.
   - `DATABASE_URL` menunjuk ke MySQL. Contoh XAMPP tanpa kata sandi: `mysql+pymysql://root:@localhost:3306/moviematch`. Jika ada kata sandi, sisipkan setelah `root:`.

Aplikasi menolak untuk start jika `SECRET_KEY` atau `DATABASE_URL` belum diisi, atau jika `SECRET_KEY` masih memakai nilai bawaan yang tidak aman.

## Urutan menjalankan

Jalankan perintah berikut dari folder utama proyek, berurutan:

1. Siapkan dataset lewat notebook Data `notebooks/01_data_preprocessing.ipynb`. Hasilnya disimpan di `data/processed/movies_clean_final.csv`.
2. Buat database MySQL (misalnya `moviematch`), lalu impor CSV: `python scripts/import_csv.py`
3. Bangun model: `python -m src.build_model --csv data/processed/movies_clean_final.csv --out models/recommender.joblib`
4. Jalankan aplikasi: `python run.py` lalu buka http://127.0.0.1:5000

## Struktur

- `app/` aplikasi Flask (routes, templates Jinja, static)
- `src/` model rekomendasi
- `notebooks/` notebook data dan model
- `scripts/import_csv.py` impor CSV bersih ke MySQL
- `data/`, `models/` file besar (tidak di-push, bagikan lewat Drive)
- `docs/` PRD, design system, user stories, pemetaan komponen Jinja

## Branch

`main` (stabil). Pekerjaan anggota lewat branch lalu digabung ke `main` lewat Pull Request.
