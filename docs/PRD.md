# PRD MovieMatch – Sistem Rekomendasi Film

Acuan bersama Kelompok 2 Kelas E: apa yang dibangun, siapa mengerjakan apa, kontrak antarbagian, dan keputusan yang masih terbuka.

**Label status:**
- **[Diputuskan]**: sudah disepakati.
- **[Usulan]**: saran yang masih perlu dikonfirmasi tim.
- **[Belum diputuskan]**: isu terbuka.

## Daftar isi
1. [Info dokumen](#1-info-dokumen)
2. [Ringkasan & tujuan](#2-ringkasan--tujuan)
3. [Latar belakang & masalah](#3-latar-belakang--masalah)
4. [Target pengguna & user stories](#4-target-pengguna--user-stories)
5. [Ruang lingkup](#5-ruang-lingkup)
6. [Kebutuhan fungsional](#6-kebutuhan-fungsional)
7. [Halaman & alur pengguna](#7-halaman--alur-pengguna)
8. [Kebutuhan non-fungsional](#8-kebutuhan-non-fungsional)
9. [Arsitektur & tech stack](#9-arsitektur--tech-stack)
10. [Spesifikasi data & model](#10-spesifikasi-data--model)
11. [Skema database (usulan)](#11-skema-database-usulan)
12. [Pembagian peran](#12-pembagian-peran)
13. [Konvensi Git](#13-konvensi-git)
14. [Metrik & pengujian](#14-metrik--pengujian)
15. [Isu terbuka](#15-isu-terbuka)

---

## 1. Info dokumen

| Properti | Nilai |
|---|---|
| Produk | MovieMatch (nama UI), Sistem Rekomendasi Film berbasis Content-Based Filtering |
| Tim | Kelompok 2 Kelas E, Informatika FMIPA Universitas Udayana |
| Anggota | Gede Widhi Wardhana, Kadek Bayu Dwi Pradnya, Ni Luh Putu Ayu Maytta Wulandhani, Tebuana Agung Ayudia Lory |
| Dosen pengampu | I Made Satria Bimantara, S.Kom., M.Kom. |
| Versi | v2 draf, 17 Nov 2026 (memuat keputusan stack 17 Nov 2026) |
| Tenggat | Belum ditentukan (diskusi awal menyebut pengumpulan sekitar November) |
| Desain | https://www.figma.com/make/8Jp3dCRiIeWQV62hZGxB05/Sistem-Rekomendasi-Film |
| Sumber | Laporan kelompok (Bab I–III), desain Figma Make (screenshot + source React hasil ekspor), CSV bersih bagian data, keputusan diskusi tim |
| Dokumen terkait | `design-system.md` (token visual), `jinja-components.md` (pemetaan React → Jinja), `user-stories.md` |

> **Keputusan kelompok 17 Nov 2026 [Diputuskan]: Opsi 2.** MovieMatch dibangun sebagai **satu proyek Flask + Jinja + Tailwind**.
> Source React hasil ekspor Figma Make (`App.tsx`, `components/*.tsx`, `pages/*.tsx`, `data/movies.ts`, `index.css`) **hanya menjadi acuan visual**. Source ini tidak dijalankan, tidak di-deploy, dan tidak disalin sebagai aplikasi.
> Yang diambil dari source tersebut hanya kelas Tailwind, token warna/font dari `index.css`, teks UI, dan struktur halaman. Logika React (state, `localStorage`, data dummy `movies.ts`, rumus kemiripan dummy) **tidak dipakai**.

## 2. Ringkasan & tujuan

MovieMatch adalah web yang membantu pengguna menemukan film dengan konten mirip film yang mereka sukai. Kemiripan dihitung dari isi film, yaitu sinopsis, genre, keyword, dan sutradara, memakai TF-IDF dan Cosine Similarity. Hasilnya lalu diperingkat dengan bantuan rating.

Tujuan:
- Menampilkan film serupa secara otomatis di halaman detail film.
- Menyediakan pencarian film serupa secara manual: pilih film acuan, konfirmasi, lalu lihat hasil.
- Memberi rekomendasi personal di Beranda dari riwayat pencarian, dan rekomendasi umum untuk pengguna baru.
- Mengukur kualitas rekomendasi (Precision@K, Recall@K) dan kegunaan sistem (black-box testing, SUS).

## 3. Latar belakang & masalah

- Jumlah film sangat banyak sehingga pengguna sulit memilih film yang sesuai selera.
- Collaborative Filtering butuh banyak data rating antarpengguna, sehingga pengguna baru dan film dengan sedikit rating tidak terlayani.
- Content-Based Filtering bisa merekomendasikan dari isi film saja, jadi tetap berjalan tanpa riwayat rating pengguna lain.
- Kualitas rekomendasi bergantung pada kelengkapan fitur teks, jadi data perlu dibersihkan dan digabung dengan benar.

## 4. Target pengguna & user stories

- **Pengguna utama:** penonton umum yang ingin mencari film mirip film favoritnya.
- **Penilai:** dosen dan responden uji SUS.

Rincian lengkap beserta acceptance criteria ada di `user-stories.md`.

| ID | Sebagai | Saya ingin | Agar | Kebutuhan terkait |
|---|---|---|---|---|
| US-01 | Pengunjung baru | mendaftar dan masuk | riwayat pencarian saya tersimpan | F-01, F-02 |
| US-02 | Pengguna | mencari film berdasarkan judul atau keyword | cepat menemukan film yang saya maksud | F-03, F-04 |
| US-03 | Pengguna | melihat detail film | tahu sinopsis, genre, sutradara, dan rating sebelum menonton | F-05 |
| US-04 | Pengguna | melihat film serupa di halaman detail | menemukan tontonan berikutnya tanpa mencari lagi | F-07, F-08 |
| US-05 | Pengguna | sengaja memilih film acuan lalu mencari film serupa | mendapat daftar film mirip sesuai pilihan saya | F-16 |
| US-06 | Pengguna lama | mendapat rekomendasi personal di Beranda | rekomendasi sesuai riwayat saya | F-06, F-09, F-10, F-13 |
| US-07 | Pengguna baru tanpa riwayat | tetap melihat rekomendasi di Beranda | halaman tidak kosong | F-11, F-12 (cold start) |

## 5. Ruang lingkup

**Termasuk:**
- Registrasi, login, dan logout pengguna.
- Pencarian film dan filter genre di Explore.
- Halaman detail film dengan film serupa dan persentase kemiripan.
- Alur Cari Film Serupa 3 langkah.
- Riwayat pencarian di MySQL dan rekomendasi personal di Beranda.
- Rekomendasi umum berbasis rating untuk pengguna baru.
- Evaluasi model dan pengujian perangkat lunak.

**Tidak termasuk:**
- Collaborative Filtering atau model hybrid.
- Streaming, trailer, atau pembelian film.
- Pengguna memberi rating sendiri ke film.
- Panel admin untuk mengedit data film.
- Aplikasi mobile native dan deployment produksi.

## 6. Kebutuhan fungsional

Kode F-01 s.d. F-16 diambil dari Tabel 3.4 laporan, sedangkan F-17 s.d. F-22 diambil dari desain (screenshot dan source React). Prioritas Must/Should/Could masih **[Usulan]**.

| ID | Kebutuhan | Prioritas | Halaman | Pemilik utama |
|---|---|---|---|---|
| F-01 | Registrasi pengguna | Must | Daftar | Backend, Frontend A |
| F-02 | Login pengguna (sesi) | Must | Login | Backend, Frontend A |
| F-03 | Pencarian film berdasarkan judul atau keyword | Must | Explore, Beranda | Backend, Frontend B |
| F-04 | Menampilkan hasil pencarian | Must | Explore | Frontend B |
| F-05 | Menampilkan detail film | Must | Detail | Backend, Frontend B |
| F-06 | Menyimpan riwayat pencarian (film yang dipilih) | Must | Detail | Backend |
| F-07 | Menampilkan film serupa | Must | Detail | Model, Frontend B |
| F-08 | Menghitung kemiripan (TF-IDF + Cosine Similarity) | Must | - | Model |
| F-09 | Mengambil riwayat pencarian | Must | Beranda | Backend |
| F-10 | Rekomendasi personal dari riwayat | Must | Beranda | Model |
| F-11 | Memanfaatkan rating dalam ranking | Must | - | Model |
| F-12 | Ranking kandidat (Top-N) | Must | - | Model |
| F-13 | Menampilkan rekomendasi personal di Beranda | Must | Beranda | Frontend A |
| F-14 | Menghapus duplikasi kandidat | Must | - | Model |
| F-15 | Mengecualikan film yang sudah ada di riwayat | Should | - | Model |
| F-16 | Cari film serupa secara manual | Must | Cari Film Serupa | Model, Frontend B |
| F-17 | Filter genre di Explore (dari desain) | Should | Explore | Frontend B, Backend |
| F-18 | Alasan kemiripan dan % mirip (dari desain) | Should | Detail, Hasil | Model, Frontend B |
| F-19 | Poster film via TMDB API | Could | Semua | Backend |
| F-20 | Melihat riwayat pencarian (panel "Riwayat Pencarian" di Explore dan pill "Berdasarkan:" di Beranda) | Should | Explore, Beranda | Backend, Frontend B (Explore), Frontend A (Beranda) |
| F-21 | Menghapus riwayat pencarian (tombol "Hapus Riwayat" di desain) | Could | Explore | Backend, Frontend B |
| F-22 | Logout lewat menu pengguna di navbar | Should | Semua | Backend, Frontend A |

## 7. Halaman & alur pengguna

| Halaman | Isi utama (dari desain Figma) | Frontend |
|---|---|---|
| Layout umum | Navbar fixed (Home, Explore, Cari Film Serupa, kotak cari kecil, Masuk/Daftar atau avatar + menu Keluar, menu mobile) dan footer (logo, link, tagline; disembunyikan di Login/Daftar); tema gelap dengan aksen kuning | A |
| Beranda | Hero "Temukan Film yang Mirip dengan Film Favoritmu", kotak cari, 6 chip genre; strip statistik; "Rekomendasi Untukmu" (3 keadaan: tamu, login tanpa riwayat, login dengan riwayat); "Jelajahi Film" (film populer); "Cara Kerja – Tiga Fungsi Rekomendasi" | A |
| Login / Daftar | Login: email dan kata sandi, kotak pesan error. Daftar: nama, email, kata sandi min. 6 karakter dengan indikator kekuatan, konfirmasi kata sandi (border merah/hijau) | A |
| Explore | Cari judul/sutradara/genre, panel Riwayat Pencarian (jika login), 16 chip genre (aktif = kuning), grid kartu poster, empty state, skeleton | B |
| Detail film | Banner "Direkomendasikan berdasarkan …" (jika dibuka dari rekomendasi), info film, sinopsis, pemeran, "Tema & Kata Kunci", kartu Informasi Film, bagian "Film Serupa · Otomatis" (kartu rekomendasi 2 kolom) | B |
| Cari Film Serupa | Langkah 1 pilih film acuan, langkah 2 konfirmasi, langkah 3 hasil (12 film, urut kemiripan) | B |

**Alur film serupa (otomatis)**
1. Cari film lewat Explore atau kotak cari.
2. Pilih film dan buka Detail. Film tersebut masuk ke riwayat.
3. Lihat film serupa, yaitu Top-N dari `recommend()`.

**Alur Cari Film Serupa**
1. Pilih film acuan, dengan mencari atau memilih dari film populer.
2. Konfirmasi, lalu pilih Ganti Film atau lanjut.
3. Lihat hasil berupa daftar film yang diurutkan berdasarkan % mirip.

**Alur Beranda**
1. Cek apakah pengguna yang login punya riwayat.
2. Jika ada riwayat, tampilkan `recommend_for_user()`.
3. Jika belum ada, tampilkan `popular()` yang berbasis rating.

> **Catatan dari source desain:** Di source React, bagian "Rekomendasi Untukmu" untuk pengguna tanpa riwayat hanya menampilkan empty state ("Belum Ada Rekomendasi Untukmu"). Film populer muncul di bagian terpisah, "Jelajahi Film", untuk semua pengguna. Dengan begitu, cold start (laporan 3.3.12) terpenuhi lewat bagian "Jelajahi Film" yang diisi `popular()`. Lihat isu #16.

## 8. Kebutuhan non-fungsional

NF-01 s.d. NF-07 diambil dari Tabel 3.5 laporan. Angka targetnya belum ditentukan. Kolom "Cara memenuhi" masih **[Usulan]**.

| ID | Aspek | Kebutuhan | Cara memenuhi (usulan) |
|---|---|---|---|
| NF-01 | Performance | Pencarian dan rekomendasi selesai dalam waktu yang dapat diterima | Artefak model dimuat sekali saat app start; similarity dihitung per film, bukan sebagai matriks penuh |
| NF-02 | Usability | Antarmuka mudah dipahami | Mengikuti desain Figma; diukur dengan SUS |
| NF-03 | Reliability | Tetap memberi hasil saat pengguna belum punya riwayat | Fallback ke `popular()` |
| NF-04 | Scalability | Bisa menampung tambahan film dan pengguna | Model dibangun ulang dari CSV lewat skrip |
| NF-05 | Data Integrity | Data film, pengguna, rating, dan riwayat konsisten | Foreign key di MySQL; id film sama di CSV, model, dan DB |
| NF-06 | Security | Akun dan riwayat terlindungi | Password di-hash di MySQL; session Flask, bukan `localStorage`; route riwayat butuh login; `SECRET_KEY` dan kredensial DB disimpan di `.env`; proteksi CSRF pada form (usulan, misalnya Flask-WTF) |
| NF-07 | Maintainability | Mudah dipelihara | Logika model di `src/`, terpisah dari route dan template |

## 9. Arsitektur & tech stack

Arsitektur: **satu proyek Flask** yang merender halaman di server dengan Jinja (server-side rendering). Tidak ada SPA dan tidak ada build React.

```
Browser  ── HTML hasil render Jinja + CSS Tailwind + JS vanilla kecil (static/js/)
   │ GET/POST (form biasa, query string)
   ▼
Flask (routes, session login, flash message)
   ├──▶ Model: src/recommender.py + artefak joblib  (recommend / recommend_for_user / popular)
   ├──▶ MySQL via Flask-SQLAlchemy + PyMySQL  (users, movies, search_history)
   └┄┄▶ TMDB API untuk poster (opsional)
```

**Frontend = template Jinja + Tailwind + sedikit JavaScript vanilla** [Diputuskan: Jinja + Tailwind; rincian JS: Usulan]:
- Template: `app/templates/base.html`, `partials/*.html` (include/macro), dan satu file per halaman. Pemetaannya ada di `jinja-components.md`.
- Tailwind v4 (sesuai `@import 'tailwindcss'` + `@theme` di `index.css`). Token `@theme` disalin ke `app/static/css/input.css` lalu dibuild menjadi `app/static/css/app.css`. Cara build (Tailwind CLI standalone atau npm) belum ditentukan.
- JS vanilla hanya untuk perilaku di sisi klien:
  - Filter genre di Explore (atau cukup link `?genre=` tanpa JS).
  - Langkah Cari Film Serupa (atau 3 langkah lewat query string tanpa JS).
  - Loading skeleton saat form dikirim.
  - Toggle tampil/sembunyikan kata sandi, indikator kekuatan kata sandi, dan cek konfirmasi kata sandi.
  - Navbar: latar saat scroll, menu mobile, dropdown pengguna, kotak cari kecil.
  - Tombol "×" untuk mengosongkan search bar dan scroll ke bagian Film Serupa.
- Semua logika data (pencarian, rekomendasi, riwayat, autentikasi) tetap di Flask dan model, bukan di JS.

> **Keamanan autentikasi [Diputuskan mengikuti NF-06]:** Source React menyimpan akun **beserta kata sandi teks biasa di `localStorage`** (`mm_users`, `mm_user`) dan memasang akun demo `demo@moviematch.com` / `demo123`. Ini **tidak boleh** ditiru.
> - Autentikasi asli memakai **session Flask** (cookie bertanda tangan dengan `SECRET_KEY` dari `.env`).
> - Kata sandi disimpan sebagai **hash** di tabel `users` MySQL, misalnya dengan `werkzeug.security.generate_password_hash` / `check_password_hash` (usulan).
> - Riwayat disimpan di tabel `search_history`, bukan di state browser.
> - Kotak "akun demo" di halaman Login hanya boleh muncul saat development atau presentasi, dan akunnya dibuat lewat seed data, bukan di-hardcode di template.

| Lapisan | Teknologi | Status |
|---|---|---|
| Bahasa | Python | [Diputuskan] |
| Eksperimen data & model | Google Colab / Jupyter, pandas, scikit-learn (TfidfVectorizer, cosine_similarity), matplotlib/seaborn | [Diputuskan] |
| Database | MySQL (dipilih Bayu, 30 Okt) | [Diputuskan] |
| Web framework | Flask (satu proyek, server-side rendering) | [Diputuskan] – keputusan kelompok 17 Nov 2026 |
| Template & styling | Jinja + Tailwind CSS (v4, token dari `index.css` desain) | [Diputuskan] – keputusan kelompok 17 Nov 2026 |
| Interaksi sisi klien | JavaScript vanilla kecil di `app/static/js/` (tanpa React/framework JS) | [Diputuskan] tanpa React; daftar perilaku: [Usulan] |
| Acuan visual | Source React Figma Make (hanya referensi, tidak dijalankan) | [Diputuskan] |
| Font | Inter (teks isi) dan Manrope (judul), dari Google Fonts sesuai `index.css` | [Diputuskan] mengikuti desain |
| Autentikasi | Session Flask + password ter-hash di MySQL | [Usulan] library hash; prinsipnya wajib (NF-06) |
| Akses database | Flask-SQLAlchemy + PyMySQL | [Usulan] |
| Penyimpanan artefak model | joblib | [Usulan] |
| Poster film | TMDB API (kolom `id` di CSV adalah id TMDB) | [Usulan] |
| Kolaborasi | GitHub, branch per bagian, pull request | [Usulan] |

## 10. Spesifikasi data & model

| Properti | Nilai |
|---|---|
| Dataset | Kaggle The Movies Dataset: movies_metadata, keywords, credits, ratings, links |
| Data bersih | `movies_clean_final.csv`: 45.430 film, 9 kolom |
| Kolom | `id`, `title`, `overview`, `genres_list`, `keywords_list`, `director`, `release_year`, `vote_average`, `vote_count` |
| Format list | `genres_list` dan `keywords_list` dipisah dengan tanda `\|` |
| Overview kosong | 954 film (dihitung ulang dari CSV). Notebook melaporkan 0 karena memakai `isna()` setelah `fillna('')` |
| Status bagian data | Selesai, ada perbaikan kecil (lihat isu #8) |

**Pipeline model:**
1. **Bentuk kolom tags.** Gabungkan overview, genres, keywords, dan director. Lalu lakukan case folding, hapus tanda baca, tokenisasi, dan hapus stopword bahasa Inggris.
2. **TF-IDF.** Terapkan `TfidfVectorizer` pada tags. Simpan vectorizer, matriks TF-IDF, dan indeks id ke baris dengan joblib.
3. **Cosine Similarity.** Hitung kemiripan film acuan ke semua film saat diminta. Film acuan sendiri dikecualikan.
4. **Ranking.** Skor akhir adalah gabungan similarity dan rating. Bobotnya belum ditentukan.
5. **Personalisasi & cold start.** Gabungkan kandidat dari riwayat, lalu buang duplikat dan film yang sudah ada di riwayat. Jika tidak ada riwayat, pakai `popular()`.

> **Catatan ukuran:** Matriks similarity penuh 45.430 × 45.430 bertipe float64 butuh sekitar 16,5 GB, jadi jangan disimpan utuh. Cukup simpan matriks TF-IDF (sparse) lalu hitung per film, atau simpan Top-N per film.

### Kontrak fungsi model → backend [Usulan]

```python
# src/recommender.py  (kontrak antara MODEL dan BACKEND, status: usulan)

def recommend(movie_id: int, n: int = 10) -> list[dict]:
    """Film serupa untuk satu film acuan (halaman Detail & Cari Film Serupa).
    Film acuan sendiri tidak ikut dikembalikan. Urut dari score tertinggi."""

def recommend_for_user(history_ids: list[int], n: int = 10) -> list[dict]:
    """Rekomendasi personal di Beranda dari riwayat pencarian.
    Gabungkan kandidat dari tiap film riwayat, buang duplikat,
    buang film yang sudah ada di riwayat, lalu ranking ulang."""

def popular(n: int = 10) -> list[dict]:
    """Rekomendasi umum untuk pengguna tanpa riwayat (cold start),
    berdasarkan rating (vote_average + vote_count)."""

# movie_id yang tidak ada di data -> raise KeyError (backend menampilkan 404)
```

### Format tiap item hasil (dict / JSON)

```json
{
  "id": 155,
  "title": "The Dark Knight",
  "release_year": 2008,
  "genres": ["Drama", "Action", "Crime", "Thriller"],
  "director": "Christopher Nolan",
  "vote_average": 8.2,
  "vote_count": 12269,
  "similarity": 0.53,
  "score": 0.61,
  "reasons": ["Sutradara sama: Christopher Nolan", "Genre: Action"],
  "source_movie_id": 27205
}
```

| Field | Tipe | Keterangan |
|---|---|---|
| `id` | int | Id film, sama dengan kolom `id` di CSV dan tabel `movies` |
| `title`, `director` | str | Untuk kartu poster |
| `release_year` | int | Tahun rilis |
| `genres` | list[str] | Dari `genres_list`, untuk chip genre |
| `vote_average`, `vote_count` | float, int | Rating TMDB dari dataset |
| `similarity` | float 0–1 | Cosine similarity. Frontend menampilkan `round(similarity × 100)` + "% Mirip" |
| `score` | float | Skor akhir setelah rating; dasar urutan |
| `reasons` | list[str] | Alasan kemiripan, misalnya sutradara sama atau genre sama [Usulan] |
| `source_movie_id` | int / null | Hanya untuk rekomendasi personal: film riwayat asal kandidat |
| `shared_genres` | list[str] | Genre yang sama dengan film acuan; untuk chip "Genre: …" dan teks di kartu rekomendasi [Usulan, diminta desain] |
| `shared_keywords` | list[str] | Keyword yang sama; untuk chip "#keyword" di banner Detail [Usulan, diminta desain] |
| `same_director` | bool | Untuk chip "Sutradara sama: …" [Usulan, diminta desain] |
| `shared_cast` | list[str] | Diminta desain, tetapi **tidak bisa diisi** karena CSV tidak punya cast (isu #2). Untuk sementara kembalikan `[]` |

Contoh di atas hanya ilustrasi format, bukan hasil model. Nilai id, tahun, genre, dan rating sesuai CSV, sedangkan `similarity` dan `score` hanya contoh. Backend boleh menambah `poster_url` sebelum dikirim ke template. Field desain `rating` dipetakan ke `vote_average`, dan `genres` ke `genres_list` yang sudah dipecah.

## 11. Skema database (usulan)

Skema ini mengikuti class diagram laporan (User, Film, RiwayatPencarian). Statusnya masih **[Usulan]** dan belum disepakati.

**users**

| Kolom | Tipe |
|---|---|
| id | INT PK AUTO_INCREMENT |
| name | VARCHAR(100) |
| email | VARCHAR(255) UNIQUE |
| password_hash | VARCHAR(255) |
| created_at | DATETIME |

**movies**

| Kolom | Tipe |
|---|---|
| id | INT PK (id dari CSV) |
| title | VARCHAR(255) |
| overview | TEXT |
| genres | VARCHAR(255), dipisah `\|` |
| keywords | TEXT, dipisah `\|` |
| director | VARCHAR(255) |
| release_year | SMALLINT NULL |
| vote_average | DECIMAL(3,1) |
| vote_count | INT |
| poster_path | VARCHAR(255) NULL |

**search_history**

| Kolom | Tipe |
|---|---|
| id | INT PK AUTO_INCREMENT |
| user_id | INT FK → users.id |
| movie_id | INT FK → movies.id |
| query | VARCHAR(255) NULL |
| created_at | DATETIME |

Rating diambil dari kolom `vote_average` dan `vote_count` di tabel `movies`. Selama pengguna tidak memberi rating sendiri, tabel rating per pengguna tidak diperlukan.

## 12. Pembagian peran

Status per 17 Nov 2026, berdasarkan laporan Bayu di chat.

| Peran | Penanggung jawab | Tanggung jawab | Hasil yang diserahkan | Status |
|---|---|---|---|---|
| Data, preprocessing, EDA | Satu anggota (nama belum dicatat di PRD) | Merge data, cleaning, EDA, ekspor CSV bersih | Notebook + `movies_clean_final.csv` | Selesai, ada perbaikan kecil |
| Model | Bayu [Diputuskan] | Tags, TF-IDF, cosine similarity, ranking dengan rating, personalisasi, cold start, evaluasi Precision@K/Recall@K | `src/recommender.py`, artefak joblib, notebook evaluasi | Belum mulai |
| Backend | Belum ditentukan | Flask app, route dan context variable sesuai `jinja-components.md`, auth (session + hash), MySQL, import CSV ke tabel `movies`, simpan/hapus riwayat, panggil model, setup build Tailwind | Route + model database + perintah build CSS | Belum mulai |
| Frontend A | Belum ditentukan | Template Jinja + Tailwind + JS vanilla: `base.html`, navbar (termasuk menu mobile dan dropdown pengguna), footer, partial kartu film, badge genre, badge rating, search bar; halaman Beranda, Login, Daftar | `base.html`, `partials/` bersama, `home.html`, `login.html`, `register.html`, `static/js/` (navbar, form auth) | Belum mulai |
| Frontend B | Belum ditentukan | Template Jinja + Tailwind + JS vanilla: halaman Explore, Detail film, Cari Film Serupa (3 langkah); partial kartu rekomendasi, badge kemiripan, empty state, loading skeleton; JS filter genre, langkah Cari Film Serupa, skeleton | `explore.html`, `movie_detail.html`, `find_similar.html`, partial terkait, `static/js/` (explore, find-similar, skeleton) | Belum mulai |

Pembagian frontend menjadi dua orang sudah **[Diputuskan]**.

> **Urutan kerja:** Frontend A menyelesaikan `base.html` dan `partials/movie_card.html` lebih dulu karena keduanya dipakai Frontend B. Frontend bisa mulai dengan context dummy, yaitu dict Python dengan field yang sama dengan kontrak model, yang dikirim dari route sementara. Setelah itu baru disambungkan ke model dan MySQL. Nama route dan context variable mengikuti usulan di `jinja-components.md`.

## 13. Konvensi Git

Seluruh bagian ini masih **[Usulan]**. Repo baru akan dibuat sendiri oleh Bayu.

- **Branch:** `main` (stabil), `data`, `model`, `backend`, `frontend`. Dua orang frontend bisa memakai `frontend-a` dan `frontend-b`.
- Semua perubahan masuk ke `main` lewat pull request dan dicek minimal oleh satu anggota lain.
- Commit kecil dan sering dengan pesan yang jelas, misalnya `tambah fungsi recommend()`. Commit tiap anggota akan dicek dosen.
- Jangan commit dataset dan artefak model yang besar. Daftarkan `data/*.csv` dan `models/*.joblib` di `.gitignore`.
- Jangan commit password atau API key. Simpan di `.env`, yang juga didaftarkan di `.gitignore`.
- Library baru ditambahkan ke `requirements.txt` di commit yang sama.

```
sistem-rekomendasi-film/
├── notebooks/        # Colab/Jupyter: EDA, preprocessing, eksperimen model
├── data/             # CSV mentah & bersih (TIDAK di-commit, cukup .gitkeep)
├── models/           # artefak joblib (TIDAK di-commit jika besar)
├── src/              # recommender.py, preprocessing.py, evaluation.py
├── app/
│   ├── templates/    # Jinja: base.html, partials/*.html, home.html, explore.html, ... (lihat jinja-components.md)
│   └── static/       # css/input.css (token @theme) → css/app.css (hasil build), js/*.js (vanilla), img/
├── tests/            # uji fungsi model & route
├── docs/             # PRD, laporan, hasil evaluasi
├── README.md
├── requirements.txt
└── .gitignore
```

## 14. Metrik & pengujian

### Evaluasi model

```
Precision@K = jumlah item relevan di Top-K / jumlah item di Top-K
Recall@K    = jumlah item relevan di Top-K / jumlah seluruh item relevan
```

Diuji pada K = 5 dan K = 10 untuk tiga fungsi: film serupa, rekomendasi personal, dan cari film serupa manual. Definisi film relevan dan target nilainya belum ditentukan.

### Evaluasi kegunaan (SUS)

Responden mencoba fitur utama, lalu mengisi 10 pernyataan SUS dengan skala 1–5. Skor akhirnya 0–100. Jumlah responden dan skor target belum ditentukan.

### Black-box testing (Tabel 3.6 laporan)

| Kode | Fitur | Skenario | Hasil yang diharapkan |
|---|---|---|---|
| T-01 | Registrasi | Mengisi data akun valid | Akun berhasil dibuat |
| T-02 | Login | Memasukkan akun valid | Berhasil masuk |
| T-03 | Pencarian | Memasukkan judul film | Hasil pencarian tampil |
| T-04 | Detail film | Memilih film | Detail film tampil |
| T-05 | Film serupa | Membuka detail film | Rekomendasi film serupa tampil |
| T-06 | Riwayat pencarian | Melakukan pencarian | Film tersimpan di riwayat |
| T-07 | Rekomendasi personal | Pengguna punya riwayat | Rekomendasi tampil di Beranda |
| T-08 | Cari film serupa | Memilih film acuan | Film serupa tampil |

## 15. Isu terbuka

Semua isu di bawah berstatus **[Belum diputuskan]**.

| # | Isu | Dampak | Usulan penyelesaian |
|---|---|---|---|
| 1 | Sebagian terjawab oleh source desain: riwayat ditampilkan sebagai panel "Riwayat Pencarian" di Explore (dengan "Hapus Riwayat") dan pill "Berdasarkan:" di Beranda. Halaman profil tetap tidak ada. | Perlu route hapus riwayat; batas jumlah riwayat yang ditampilkan belum ditentukan (demo React menyimpan maksimal 10) | Pakai panel di Explore (F-20, F-21); halaman profil tidak dibuat kecuali diminta |
| 2 | Model data desain (`data/movies.ts`) memakai field yang **tidak ada di CSV**: `runtime`, `cast` (nama, foto, karakter), `poster`, dan untuk rekomendasi `sharedCast` (juga `sharedKeywords`, `sameDirector`, `sharedGenres` yang harus dihitung model). Desain juga memakai label "Rating IMDb", padahal rating di CSV dari TMDB (`vote_average`). | Detail film (durasi, Pemeran Utama, poster), banner alasan ("Pemeran: …"), dan kartu rekomendasi tidak bisa diisi | Pilih per field: (a) tambah `runtime` dari movies_metadata dan `cast` dari credits ke CSV/tabel `movies`; (b) `poster` lewat TMDB API (F-19) atau placeholder inisial seperti di desain; (c) `sharedCast` hanya bisa jika cast ditambahkan, jika tidak, chip "Pemeran" disembunyikan; (d) ganti label menjadi "Rating TMDB". Sementara itu template menyembunyikan bagian yang datanya kosong. |
| 3 | Laporan menyebut rating rata-rata dari ratings.csv lewat links, sedangkan CSV memakai `vote_average`/`vote_count` | Sumber rating untuk ranking berbeda | Pilih satu sumber dan samakan di laporan |
| 4 | Bobot gabungan similarity dan rating, serta rumus `popular()`, belum ada | Urutan rekomendasi belum pasti | Bayu mengusulkan lewat eksperimen dan mencatatnya |
| 5 | Nilai N berbeda: laporan memberi contoh Top-5/Top-10, sedangkan desain menampilkan 12 hasil | Tampilan dan evaluasi bisa tidak konsisten | Default `n=10` untuk evaluasi; `n` dapat diatur per halaman |
| 6 | Laporan menyebut pencarian berdasarkan judul atau keyword, sedangkan desain Explore menyebut judul, sutradara, atau genre | Lingkup pencarian ambigu | Sepakati field yang dicari |
| 7 | Flowchart 3.3 di laporan menyebut cast sebagai fitur konten, sedangkan tags hanya memakai overview, genre, keyword, dan director | Laporan tidak konsisten | Samakan teks laporan |
| 8 | Notebook data perlu diperbaiki: (a) overview kosong dihitung dengan `isna()` setelah `fillna('')`, sehingga notebook melaporkan 0 padahal hitung ulang dari CSV menunjukkan 954 overview kosong; (b) EDA rating/vote belum ada; (c) dokumentasi markdown minim; (d) dedup `keep='first'` untuk 13 id yang konflik belum dijelaskan; (e) path `'archive (2).zip'` di-hardcode | Kualitas dokumentasi bagian data | Diperbaiki oleh anggota bagian data |
| 9 | Di daftar pustaka, referensi [5] sama dengan [1], dan [6] masih placeholder | Laporan belum rapi | Ganti [5] dan lengkapi [6] dari sumber resminya |
| 10 | Penanggung jawab backend, Frontend A, dan Frontend B belum ditetapkan; ada 5 peran untuk 4 orang | Pekerjaan bisa tumpang tindih | Tetapkan nama per peran di grup |
| 11 | Stack sudah diputuskan (17 Nov 2026). Yang masih terbuka: konvensi Git, cara build Tailwind (CLI standalone atau npm), dan nama route/context variable di `jinja-components.md` | Struktur repo dan alur kerja frontend | Konfirmasi tim sebelum repo dibuat |
| 12 | Tenggat tiap bagian belum ditentukan | Progres sulit dipantau | Sepakati jadwal di grup |
| 13 | Chip genre di desain (dan `GenreBadge.tsx`) memuat "Biography", padahal genre di CSV tidak punya Biography; "Sci-Fi" di data bernama "Science Fiction"; Documentary, Family, Foreign, Horror, dan TV Movie ada di data tetapi tidak punya chip | Filter genre bisa kosong atau tidak lengkap | Samakan daftar chip dengan 20 genre di CSV |
| 14 | Skor kemiripan di desain berupa bilangan bulat 30–99 dari rumus dummy (genre 40%, keyword 30%, sutradara 20%, cast 10%, +20, dibatasi 30–99). Model asli menghasilkan cosine similarity 0–1 dari TF-IDF, yang biasanya jauh lebih rendah. Warna badge di desain: ≥80 kuning, ≥60 hijau, sisanya abu. | Hampir semua badge bisa tampil abu-abu, dan persentase tidak sebanding dengan demo | Tampilkan `round(similarity × 100)` apa adanya; ambang warna badge disesuaikan setelah melihat distribusi skor model (Bayu) |
| 15 | Alur source berbeda dari laporan: Daftar langsung login lalu ke Beranda (laporan: diarahkan ke halaman login); tombol "Cari Film Serupa" di Detail hanya scroll ke bagian Film Serupa (tidak membuka halaman Cari Film Serupa) | User story dan black-box test bisa tidak cocok | Sepakati satu alur; usulan: ikuti laporan untuk registrasi, ikuti desain untuk tombol scroll |
| 16 | "Rekomendasi Untukmu" untuk pengguna tanpa riwayat hanya menampilkan empty state; film populer ada di bagian terpisah. Strip statistik Beranda berisi angka dummy ("20+ Film tersedia") | Cold start dan angka di UI bisa menyesatkan | Isi "Jelajahi Film" dengan `popular()`; ganti angka statistik dengan data asli (45.430 film) atau hapus |
