# Panduan untuk Backend: memakai bagian Model

Dokumen ini menjelaskan apa yang sudah disediakan bagian Model dan apa yang perlu dikerjakan Backend.
Acuan lain: `PRD.md` (§10 dan §11), `jinja-components.md` (§3 dan §5), `docs/model-README.md`.

## 1. Apa yang sudah disediakan Model

| Hasil | Lokasi | Keterangan |
|---|---|---|
| Kode rekomendasi | `src/recommender.py` | Tiga fungsi: `recommend`, `recommend_for_user`, `popular` |
| Skrip pembangun model | `src/build_model.py` | Mengubah CSV menjadi file model |
| File model (artefak) | `models/recommender.joblib` | **Tidak ada di Git**; dibagikan lewat Google Drive |
| Tes | `tests/` | `python -m pytest -q` |

Backend **tidak perlu** menghitung kemiripan sendiri. Cukup memanggil tiga fungsi di bawah.

## 2. Persiapan

```bash
pip install -r requirements.txt           # samakan versi scikit-learn dengan Model
# taruh file model di models/recommender.joblib  (atau set env MOVIEMATCH_MODEL=/path/ke/file)
```

Muat model **sekali** saat aplikasi start, jangan per permintaan:

```python
from flask import Flask
from src.recommender import load_model

def create_app():
    app = Flask(__name__)
    try:
        load_model()      # muat sekali saat start (±1 dtk untuk 45 ribu film)
    except FileNotFoundError:
        app.logger.warning("File model belum ada; rekomendasi kosong sampai model dibangun.")
    ...
    return app
```

## 3. Tiga fungsi yang dipanggil

```python
from src.recommender import recommend, recommend_for_user, popular

recommend(movie_id, n=10)             # film serupa
recommend_for_user(history_ids, n=10) # rekomendasi personal di Beranda
popular(n=10)                         # film populer (cold start, "Jelajahi Film")
```

| Fungsi | Dipakai di | Catatan |
|---|---|---|
| `recommend(movie_id, n)` | Detail (n=10), Cari Film Serupa langkah 3 (n=12) | Film acuan tidak ikut dikembalikan. Id tidak ada → `KeyError` → tampilkan 404 |
| `recommend_for_user(ids, n)` | Beranda (n=8) | `ids` **diurutkan dari yang terbaru**. Riwayat kosong otomatis jadi `popular(n)` |
| `popular(n)` | Beranda, pilihan film di Cari Film Serupa (n=10) | `similarity` dan `source_movie_id` bernilai `None` |

Contoh route:

```python
from flask import abort, render_template

@bp.route("/film/<int:movie_id>")
def movie_detail(movie_id):
    movie = db_get_movie(movie_id)            # dari tabel movies; None -> 404
    if movie is None:
        abort(404)
    recs = recommend(movie_id, n=10)          # id pasti ada jika ada di tabel movies
    ...
    return render_template("pages/movie_detail.html", movie=movie, recommendations=recs)

@bp.route("/")
def home():
    if current_user:
        ids = [h.movie_id for h in latest_history(current_user.id)]  # terbaru dulu
        personal = recommend_for_user(ids, n=8) if ids else []
    ...
    return render_template("pages/home.html", personal_recs=personal, popular_movies=popular(10))
```

## 4. Bentuk data yang dikembalikan

Tiap film adalah dict berisi tipe Python biasa (aman untuk Jinja dan `json.dumps`):

```
id, title, release_year (int atau None), genres (list), director (teks, "A, B" jika lebih dari satu),
vote_average, vote_count, overview, keywords (list),
similarity (0..1), similarity_percent (int 0..100), keduanya None pada popular(); score, reasons (list teks),
source_movie_id (int atau None), shared_genres (list), shared_keywords (list),
same_director (bool), shared_cast (selalu [])
```

Hal yang perlu diperhatikan saat membuat template/context:
- Tampilkan kemiripan memakai `similarity_percent` (bilangan bulat 0–100) + "% Mirip", jangan `similarity` mentah (0–1). Untuk `popular()` nilainya `None`, jadi jangan tampilkan badge.
- Hasil bisa **kurang dari `n`** (film dengan kemiripan 0 tidak dikembalikan). Tampilkan `empty_state` jika kosong.
- `release_year` bisa `None`. `poster_url` tidak disediakan Model; Backend menambahkannya jika memakai TMDB (opsional).
- Untuk banner "Direkomendasikan berdasarkan" (`?dari=`): panggil `recommend(dari, n=12)` lalu cari item yang `id`-nya sama dengan film yang dibuka. Itu `why`-nya. Rekomendasi personal juga membawa `source_movie_id` sebagai nilai `dari`.

## 5. Yang perlu dikerjakan Backend

1. **Database MySQL**: tabel `users`, `movies`, `search_history` (PRD §11). **Id film harus sama** dengan kolom `id` di CSV, karena Model memakai id itu.
2. **Import CSV** `movies_clean_final.csv` (45.430 film) ke tabel `movies` lewat `scripts/import_csv.py` (CSV ada di `data/processed/`), bersama anggota Data.
   - Kolom `genres_list` dan `keywords_list` dipisah `|`; kolom `director` juga `|` jika lebih dari satu.
   - Pastikan `release_year` dan `vote_count` masuk sebagai bilangan bulat (tahun kosong = `NULL`). CSV terbaru dari Data sudah berformat bilangan bulat, tapi tetap aman memakai `int(float(x))`.
3. **Autentikasi**: session Flask, sandi di-hash, `SECRET_KEY` di `.env`, proteksi CSRF (NF-06).
4. **Pencarian dan Explore**: cari judul, filter genre, pagination (data 45 ribu film). Pencarian memakai MySQL, bukan Model.
5. **Riwayat**: simpan saat pengguna login membuka Detail; ambil dengan urutan terbaru; hapus riwayat; hanya pemilik yang boleh membaca.
6. **Route dan context** sesuai `jinja-components.md` §3 dan §5, dan menyambungkan tiga fungsi Model di atas menggantikan data dummy Frontend.
7. **Build Tailwind** dan perintah menjalankannya.

## 6. Hal yang sering jadi masalah

- **File model tidak ada**: `load_model()` melempar `FileNotFoundError`. Ambil dulu dari Google Drive.
- **Peringatan versi scikit-learn**: artinya versi di komputermu berbeda dari saat model dibangun. Samakan lewat `requirements.txt`, atau minta Model membangun ulang.
- **Versi library berbeda**: samakan versi scikit-learn dengan yang dipakai Model.
- **Id tidak cocok**: jika id di MySQL berbeda dengan CSV, `recommend` melempar `KeyError`.
- **Memuat model berulang**: jangan panggil `load_model()` di dalam route. Cukup sekali saat start; model aman dipakai banyak permintaan sekaligus.
- **Model berubah**: jika CSV atau konfigurasi berubah, Model membangun ulang file model dan membagikan versi baru. Backend cukup mengganti file dan restart aplikasi.

## 7. Kontak koordinasi dengan Model

Yang perlu dikonfirmasi sebelum integrasi: urutan riwayat (terbaru dulu), jumlah `n` di tiap halaman, dan apakah poster diambil dari TMDB.
