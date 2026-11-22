# MovieMatch – Sistem Rekomendasi Film

Sistem rekomendasi film content-based (TF-IDF + cosine similarity) dengan Flask, Jinja, Tailwind, dan MySQL. Dataset: Kaggle The Movies Dataset.

## Menjalankan
1. `python -m venv .venv` lalu aktifkan (`.venv\Scripts\activate` di Windows, `source .venv/bin/activate` di Linux/macOS)
2. `pip install -r requirements.txt`
3. Salin `.env.example` menjadi `.env` lalu isi nilainya
4. (Opsional, kalau template atau `input.css` berubah) `./build_css.sh` — `app/static/css/app.css` sudah di-commit, jadi langkah ini tidak wajib untuk menjalankan aplikasi
5. `python run.py` lalu buka http://127.0.0.1:5000

Halaman yang sudah ada: `/` (Beranda), `/masuk`, `/daftar`. Explore, detail film, dan Cari Film Serupa masih stub. Akun demo di halaman Masuk hanya muncul jika `MOVIEMATCH_DEMO_HINT=1`.

Catatan Frontend A (cara build CSS, context tiap halaman, deviasi, pertanyaan terbuka): [`docs/frontend-a.md`](docs/frontend-a.md).

## Struktur
- `app/` aplikasi Flask (routes, templates Jinja, static)
- `src/` model rekomendasi
- `notebooks/` notebook data dan model
- `data/`, `models/` file besar (tidak di-push, bagikan lewat Drive)
- `docs/` PRD, design system, user stories, pemetaan komponen Jinja

## Branch
`main` (stabil), `data`, `model`, `backend`, `frontend-a`, `frontend-b`. Gabung ke `main` lewat Pull Request.
