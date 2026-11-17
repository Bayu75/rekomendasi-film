# MovieMatch – Sistem Rekomendasi Film

Sistem rekomendasi film content-based (TF-IDF + cosine similarity) dengan Flask, Jinja, Tailwind, dan MySQL. Dataset: Kaggle The Movies Dataset.

## Menjalankan
1. `python -m venv .venv` lalu aktifkan (`.venv\Scripts\activate` di Windows)
2. `pip install -r requirements.txt`
3. Salin `.env.example` menjadi `.env` lalu isi nilainya
4. `python run.py` lalu buka http://127.0.0.1:5000

## Struktur
- `app/` aplikasi Flask (routes, templates Jinja, static)
- `src/` model rekomendasi
- `notebooks/` notebook data dan model
- `data/`, `models/` file besar (tidak di-push, bagikan lewat Drive)
- `docs/` PRD, design system, user stories, pemetaan komponen Jinja

## Branch
`main` (stabil), `data`, `model`, `backend`, `frontend-a`, `frontend-b`. Gabung ke `main` lewat Pull Request.
