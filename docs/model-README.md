# Bagian Model — panduan singkat

Pemilik: Model (anggota 2). Semua nama fungsi mengikuti kontrak di `PRD.md` §10.

## Menjalankan

```bash
pip install -r requirements.txt
# taruh CSV asli di data/processed/movies_clean_final.csv (tidak di-commit)
python -m src.build_model --csv data/processed/movies_clean_final.csv --out models/recommender.joblib
python -m pytest -q                      # 26 tes
jupyter nbconvert --to notebook --execute --inplace notebooks/model_rekomendasi.ipynb
```

`data/movies_standin.csv` hanya data uji (TMDB 5000, 4.803 film) agar kode bisa dicoba tanpa CSV asli.
**Jangan memakai angkanya untuk laporan.**

## Untuk Backend

```python
from src.recommender import recommend, recommend_for_user, popular

recommend(movie_id, n=10)            # KeyError jika id tidak ada -> tampilkan 404
recommend_for_user(history_ids, n=10) # history_ids: TERBARU dulu; kosong -> popular(n)
popular(n=10)                        # similarity = None, source_movie_id = None
```

- Artefak dimuat sekali. Lokasi: `models/recommender.joblib` atau env `MOVIEMATCH_MODEL`.
  Sebaiknya panggil `load_model()` sekali di `create_app` (dalam `try/except FileNotFoundError`), supaya pengunjung
  pertama tidak menunggu. `model_info()` mengembalikan jumlah film, versi scikit-learn, dan konfigurasi.
  Jika versi scikit-learn saat memuat berbeda dari saat membangun, muncul `RuntimeWarning`; samakan versinya.
- Tiap item = dict tipe Python biasa (aman untuk Jinja dan `json.dumps`). Field = kontrak PRD §10
  ditambah `overview` dan `keywords` (dipakai `jinja-components.md`). `shared_cast` selalu `[]` (CSV tidak punya cast, isu #2).
- `release_year` bisa `None`. `similarity` 0–1; untuk ditampilkan pakai `similarity_percent` (bilangan bulat 0–100,
  `None` pada `popular()`), jangan menampilkan `similarity` mentah.
- Film dengan similarity 0 tidak dikembalikan, jadi hasil bisa kurang dari `n` (tampilkan `empty_state` jika kosong).
- Id di `recommend_for_user` yang tidak ada di data dilewati; hanya 10 film riwayat terbaru dipakai (`max_history`).

## Cara kerja

1. `tags` = overview + genre + keyword + sutradara; genre dan sutradara dijadikan satu token.
2. `TfidfVectorizer` (stopword Inggris, `sublinear_tf`, `min_df=2`, `max_df=0.8`); matriks sparse L2-normalized.
3. Cosine similarity satu film ke semua film dihitung saat diminta (±5 ms pada 4.803 film).
4. Ranking: kandidat 200 teratas menurut similarity → `score = (1−α)·sim_norm + α·rating_norm`, α = 0,2.
   Rating = weighted rating gaya IMDb (film dengan sedikit vote ditarik ke rata-rata).
5. Personalisasi: similarity ke tiap film riwayat digabung (`max`), film riwayat dibuang, duplikat otomatis hilang.
6. `popular()` = urut weighted rating.

## Keputusan yang masih terbuka (usulan Model, perlu disepakati)

| Isu PRD          | Usulan di kode                                                       | Catatan                                                                                                     |
| ---------------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| #4 bobot rating  | α = 0,2; `popular()` = weighted rating, m = kuantil 80% `vote_count` | Ubah di `DEFAULT_CONFIG`; hitung ulang di CSV asli                                                          |
| Definisi relevan | Jaccard genre ≥ 0,5                                                  | Sebagian sirkular (genre ada di `tags`); lengkapi dengan SUS/penilaian manual                               |
| Riwayat          | `max_history` = 10, gabungan `max`                                   | `mean` memberi Precision lebih tinggi pada pengguna simulasi satu selera, tetapi simulasinya bias ke `mean` |
| #14 ambang badge | lihat §7 notebook (persentil sebaran similarity)                     | Jalankan ulang di CSV asli                                                                                  |
| #5 nilai N       | `n` per pemanggilan; evaluasi K = 5, 10                              | UI Cari Film Serupa memanggil `n=12`                                                                        |
