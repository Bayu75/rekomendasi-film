# User Stories – MovieMatch (Sistem Rekomendasi Film)

Dokumen pendamping `PRD.md`. Kode F-xx mengacu ke tabel Kebutuhan Fungsional di PRD, dan kode T-xx mengacu ke skenario black-box testing (Tabel 3.6 laporan).

**Ketentuan umum:**
- Prioritas Must/Should/Could masih **[Usulan]**.
- Owner adalah peran (Data, Model, Backend, Frontend A, Frontend B), bukan nama orang. Nama penanggung jawab backend, Frontend A, dan Frontend B belum ditentukan, sedangkan Model dipegang Bayu.
- Angka yang belum disepakati (misalnya nilai N, bobot rating, dan batas waktu respons) ditulis "belum ditentukan".

**Jenis pengguna:**
- **Tamu**: pengunjung yang belum login.
- **Pengguna terdaftar**: sudah login dan punya riwayat pencarian.
- **Pengguna baru**: sudah login, tetapi belum punya riwayat (cold start).

## Ringkasan

| ID | Persona | Judul singkat | Prioritas | F-xx | Owner |
|---|---|---|---|---|---|
| US-01 | Tamu | Mendaftar akun | Must | F-01 | Backend, Frontend A |
| US-02 | Tamu | Masuk (login) | Must | F-02 | Backend, Frontend A |
| US-03 | Pengguna terdaftar | Keluar (logout) | Should | F-02 | Backend, Frontend A |
| US-04 | Tamu / pengguna | Mencari film | Must | F-03, F-04 | Backend, Frontend B |
| US-05 | Tamu / pengguna | Filter genre di Explore | Should | F-17 | Frontend B, Backend |
| US-06 | Tamu / pengguna | Melihat detail film | Must | F-05 | Backend, Frontend B |
| US-07 | Tamu / pengguna | Melihat film serupa di Detail | Must | F-07, F-08, F-11, F-12 | Model, Backend, Frontend B |
| US-08 | Tamu / pengguna | Memahami alasan kemiripan | Should | F-18 | Model, Frontend B |
| US-09 | Tamu / pengguna | Cari Film Serupa secara manual | Must | F-16, F-08, F-12 | Model, Backend, Frontend B |
| US-10 | Pengguna terdaftar | Riwayat tersimpan otomatis | Must | F-06 | Backend |
| US-11 | Pengguna terdaftar | Rekomendasi personal di Beranda | Must | F-09, F-10, F-11, F-12, F-13, F-14, F-15 | Model, Backend, Frontend A |
| US-12 | Pengguna baru | Rekomendasi umum (cold start) | Must | F-11, F-12, F-13 | Model, Backend, Frontend A |
| US-13 | Tamu | Melihat Beranda tanpa login | Should | F-03, F-13 | Frontend A, Backend |
| US-14 | Pengguna terdaftar | Melihat riwayat saya | Could | F-20 | Belum ditentukan |
| US-15 | Tamu / pengguna | Melihat poster film | Could | F-19 | Backend, Frontend A, Frontend B |
| US-16 | Tim (penilai) | Data film bersih & konsisten | Must | F-08 (pendukung) | Data |
| US-17 | Tim (penilai) | Evaluasi kualitas rekomendasi | Must | F-08, F-12 | Model |

---

## A. Tamu (belum login)

### US-01 – Mendaftar akun
**Sebagai** tamu, **saya ingin** membuat akun dengan nama, email, dan kata sandi, **agar** riwayat pencarian saya bisa disimpan dan saya mendapat rekomendasi personal.

- Prioritas: Must · F-01 · Uji: T-01 · Owner: Backend (validasi, simpan ke `users`, hash password), Frontend A (halaman Daftar)

Acceptance criteria:
- **Given** saya di halaman Daftar, **when** saya mengisi nama, email valid yang belum terdaftar, kata sandi minimal 6 karakter, dan konfirmasi yang sama, lalu menekan "Buat Akun", **then** akun tersimpan dengan password ter-hash dan saya diarahkan ke halaman Masuk dengan notifikasi berhasil.
- **Given** email sudah terdaftar, **when** saya mengirim form, **then** muncul pesan kesalahan dan akun tidak dibuat.
- **Given** kata sandi kurang dari 6 karakter atau konfirmasinya berbeda, **when** saya mengirim form, **then** muncul pesan kesalahan di field terkait.
- [ ] Ada link "Masuk di sini" dan "← Kembali ke Beranda", sesuai desain.

### US-02 – Masuk (login)
**Sebagai** tamu yang sudah punya akun, **saya ingin** masuk dengan email dan kata sandi, **agar** saya bisa memakai fitur yang membutuhkan riwayat.

- Prioritas: Must · F-02 · Uji: T-02 · Owner: Backend (autentikasi, sesi), Frontend A (halaman Masuk)

Acceptance criteria:
- **Given** kredensial valid, **when** saya menekan "Masuk", **then** sesi login dibuat dan saya diarahkan ke Beranda.
- **Given** kredensial salah, **when** saya menekan "Masuk", **then** muncul pesan gagal login tanpa menyebut field mana yang salah, dan saya tetap di halaman Masuk.
- [ ] Navbar menampilkan status login, bukan tombol Masuk/Daftar, setelah berhasil masuk. Tampilan pastinya belum ada di desain.
- [ ] Kotak "akun demo" di desain hanya dipakai saat development atau presentasi, dan tidak berisi akun asli.

### US-13 – Melihat Beranda tanpa login
**Sebagai** tamu, **saya ingin** tetap bisa melihat Beranda dan mencari film, **agar** saya bisa mencoba MovieMatch sebelum mendaftar.

- Prioritas: Should · F-03, F-13 · Owner: Frontend A, Backend

Acceptance criteria:
- **Given** saya belum login, **when** saya membuka Beranda, **then** hero, search bar, dan chip genre tampil, dan area rekomendasi menampilkan rekomendasi umum (sama dengan US-12).
- [ ] Riwayat tidak disimpan untuk tamu.
- [ ] Apakah tamu boleh membuka Detail dan Cari Film Serupa tanpa login belum diputuskan. Laporan menggambarkan alur dimulai dari login/registrasi.

---

## B. Semua pengguna (tamu atau login)

### US-04 – Mencari film
**Sebagai** pengguna, **saya ingin** mencari film dengan mengetik kata kunci, **agar** saya cepat menemukan film yang saya maksud.

- Prioritas: Must · F-03, F-04 · Uji: T-03 · Owner: Backend (query ke tabel `movies`), Frontend B (Explore), Frontend A (search bar di navbar dan Beranda)

Acceptance criteria:
- **Given** saya di Explore, **when** saya mengetik "Inception" lalu menekan "Cari" atau Enter, **then** muncul teks "Hasil pencarian untuk: "Inception"", jumlah film ditemukan, dan grid kartu poster.
- **Given** kata kunci tidak cocok dengan film mana pun, **when** saya mencari, **then** muncul pesan bahwa tidak ada film yang ditemukan, bukan halaman kosong.
- **Given** saya mencari dari search bar di Beranda atau navbar, **when** saya menekan "Cari", **then** saya diarahkan ke Explore dengan hasil pencarian tersebut.
- [ ] Tombol "×" mengosongkan kata kunci.
- [ ] Field yang dicari (judul saja, judul + keyword, atau judul + sutradara + genre) belum diputuskan. Lihat isu #6 di PRD.

### US-05 – Filter genre di Explore
**Sebagai** pengguna, **saya ingin** memfilter film berdasarkan genre, **agar** saya bisa menjelajah film tanpa mengetik judul.

- Prioritas: Should · F-17 · Owner: Frontend B, Backend

Acceptance criteria:
- **Given** saya di Explore, **when** saya menekan chip genre (misalnya "Sci-Fi"), **then** chip itu tampil aktif dan grid hanya menampilkan film yang `genres_list`-nya memuat genre tersebut.
- **Given** satu chip aktif, **when** saya menekannya lagi, **then** filter dilepas.
- [ ] Tersedia 16 chip sesuai desain. Nama chip harus dipetakan ke nama genre di dataset (misalnya "Sci-Fi" ke "Science Fiction"). Chip "Biography" tidak punya padanan di dataset, karena genre di CSV tidak memuat Biography. Sebaliknya, Documentary, Family, Foreign, Horror, dan TV Movie ada di data tetapi tidak punya chip. Perlu disepakati.
- [ ] Apakah filter bisa digabung dengan kata kunci atau dengan lebih dari satu genre belum ditentukan.

### US-06 – Melihat detail film
**Sebagai** pengguna, **saya ingin** membuka halaman detail film, **agar** saya tahu sinopsis, genre, sutradara, tahun, dan rating sebelum memutuskan menonton.

- Prioritas: Must · F-05 · Uji: T-04 · Owner: Backend (route `/film/<id>`), Frontend B (halaman Detail)

Acceptance criteria:
- **Given** saya menekan sebuah kartu poster, **when** halaman Detail terbuka, **then** tampil judul, tag genre, tahun rilis, sutradara, rating (`vote_average`) beserta jumlah vote, dan sinopsis.
- **Given** id film tidak ada, **when** URL dibuka, **then** muncul halaman 404 yang ramah.
- **Given** sinopsis film kosong (954 film di CSV), **when** Detail dibuka, **then** muncul teks pengganti seperti "Sinopsis belum tersedia".
- [ ] Durasi, pemeran, poster, dan label "Rating IMDb" ada di desain tetapi datanya belum tersedia di CSV. Lihat isu #2 di PRD. Label rating memakai "Rating TMDB".
- [ ] Tersedia tombol "← Kembali", "Cari Film Serupa" (membuka US-09 dengan film ini sebagai acuan), dan "Cari Film Lainnya".

### US-07 – Melihat film serupa di halaman Detail
**Sebagai** pengguna, **saya ingin** melihat daftar film yang mirip dengan film yang sedang saya buka, **agar** saya menemukan tontonan berikutnya tanpa mencari lagi.

- Prioritas: Must · F-07, F-08, F-11, F-12 · Uji: T-05 · Owner: Model (`recommend(movie_id, n)`), Backend (memanggil model), Frontend B (menampilkan kartu)

Acceptance criteria:
- **Given** saya membuka Detail film X, **when** halaman dimuat, **then** tampil N film serupa yang diurutkan berdasarkan `score` dari yang tertinggi. Nilai N belum ditentukan, dengan default usulan 10.
- [ ] Film X sendiri tidak muncul di daftar.
- [ ] Tidak ada film yang muncul dua kali.
- [ ] Setiap kartu menampilkan badge "NN% Mirip" dari `round(similarity × 100)` dan badge rating.
- [ ] Output model mengikuti format dict/JSON di PRD (id, title, release_year, genres, director, vote_average, vote_count, similarity, score, reasons).
- [ ] Kemiripan dihitung per film dari matriks TF-IDF, tanpa matriks similarity penuh. Batas waktu respons belum ditentukan.

### US-08 – Memahami alasan kemiripan
**Sebagai** pengguna, **saya ingin** tahu kenapa sebuah film direkomendasikan, **agar** saya lebih percaya pada rekomendasinya.

- Prioritas: Should · F-18 · Owner: Model (field `reasons`), Frontend B (banner kemiripan dan chip alasan)

Acceptance criteria:
- **Given** saya membuka Detail dari hasil rekomendasi film acuan A, **when** halaman dimuat, **then** banner menampilkan "NN% Mirip", "Direkomendasikan berdasarkan A", dan chip alasan seperti "Sutradara sama: …" atau "Genre: …".
- [ ] Alasan hanya diambil dari data nyata, yaitu sutradara sama dan irisan genre atau keyword, bukan teks karangan.
- [ ] Jika film dibuka langsung, bukan dari rekomendasi, banner tidak ditampilkan.

### US-09 – Cari Film Serupa secara manual
**Sebagai** pengguna, **saya ingin** sengaja memilih satu film acuan lalu meminta daftar film serupa, **agar** saya mendapat rekomendasi sesuai pilihan saya saat itu.

- Prioritas: Must · F-16, F-08, F-12 · Uji: T-08 · Owner: Model (`recommend`), Backend, Frontend B (alur 3 langkah)

Acceptance criteria:
- **Given** saya di Langkah 1, **when** saya mencari judul atau menekan "Pilih" pada film populer, **then** saya pindah ke Langkah 2 dengan film itu sebagai acuan.
- **Given** saya di Langkah 2 (Konfirmasi), **when** saya menekan "Ganti Film", **then** saya kembali ke Langkah 1. **When** saya menekan "Cari Film Serupa", **then** saya pindah ke Langkah 3.
- **Given** saya di Langkah 3, **then** tampil judul "Film Serupa dengan "<judul>"", jumlah hasil, dan grid film yang diurutkan berdasarkan kemiripan. Desain menampilkan 12 hasil, tetapi nilai N final belum ditentukan (isu #5).
- [ ] Step indicator menunjukkan langkah selesai, aktif, dan belum, sesuai `design-system.md`.
- [ ] Tombol "Ganti Film Acuan" di Langkah 3 kembali ke Langkah 1.
- [ ] Jika pengguna login, film acuan ikut dicatat ke riwayat. Ini masih usulan dan perlu dikonfirmasi.

### US-15 – Melihat poster film
**Sebagai** pengguna, **saya ingin** melihat poster film di kartu dan di Detail, **agar** film lebih mudah dikenali.

- Prioritas: Could · F-19 · Owner: Backend (TMDB API dan `poster_path`), Frontend A (komponen kartu), Frontend B (Detail)

Acceptance criteria:
- **Given** poster tersedia dari TMDB untuk `id` film, **when** kartu dirender, **then** poster tampil dengan rasio sekitar 2:3.
- **Given** poster tidak tersedia atau API gagal, **then** muncul placeholder netral dan halaman tetap berfungsi.
- [ ] API key TMDB disimpan di `.env` dan tidak di-commit.

---

## C. Pengguna terdaftar (sudah punya riwayat)

### US-10 – Riwayat tersimpan otomatis
**Sebagai** pengguna terdaftar, **saya ingin** film yang saya cari atau pilih tersimpan otomatis, **agar** sistem bisa memberi rekomendasi yang sesuai selera saya.

- Prioritas: Must · F-06 · Uji: T-06 · Owner: Backend

Acceptance criteria:
- **Given** saya login, **when** saya membuka Detail sebuah film, **then** satu baris tersimpan di `search_history` (user_id, movie_id, created_at).
- [ ] Untuk tamu, tidak ada data yang disimpan.
- [ ] Riwayat hanya bisa dibaca oleh pemiliknya (NF-06).
- [ ] Apakah kata kunci pencarian tanpa memilih film juga disimpan (kolom `query`) belum diputuskan.

### US-11 – Rekomendasi personal di Beranda
**Sebagai** pengguna terdaftar yang punya riwayat, **saya ingin** melihat rekomendasi personal di Beranda, **agar** saya langsung menemukan film yang cocok tanpa mencari.

- Prioritas: Must · F-09, F-10, F-11, F-12, F-13, F-14, F-15 · Uji: T-07 · Owner: Model (`recommend_for_user(history_ids, n)`), Backend (ambil riwayat), Frontend A (area rekomendasi di Beranda)

Acceptance criteria:
- **Given** saya login dan punya minimal satu film di riwayat, **when** saya membuka Beranda, **then** tampil N rekomendasi personal yang diurutkan berdasarkan `score`.
- [ ] Kandidat dari beberapa film riwayat digabung, dan duplikatnya dihapus (F-14).
- [ ] Film yang sudah ada di riwayat tidak direkomendasikan lagi (F-15).
- [ ] Skor akhir menggabungkan similarity dan rating. Bobotnya belum ditentukan dan dicatat Bayu setelah eksperimen (isu #4).
- [ ] Jumlah film riwayat yang dipakai sebagai acuan (semua atau beberapa terbaru) belum ditentukan.
- [ ] Bagian ini belum terlihat di screenshot desain Beranda, jadi tata letaknya perlu disepakati Frontend A.

### US-03 – Keluar (logout)
**Sebagai** pengguna terdaftar, **saya ingin** keluar dari akun, **agar** akun saya aman di perangkat bersama.

- Prioritas: Should · F-02 · Owner: Backend, Frontend A

Acceptance criteria:
- **Given** saya login, **when** saya menekan "Keluar", **then** sesi dihapus dan navbar kembali menampilkan Masuk/Daftar.
- [ ] Tombol Keluar belum ada di desain. Letaknya diputuskan Frontend A.

### US-14 – Melihat riwayat saya
**Sebagai** pengguna terdaftar, **saya ingin** melihat daftar film yang pernah saya cari, **agar** saya paham dasar rekomendasi personal saya.

- Prioritas: Could · F-20 · Owner: belum ditentukan (usulan: Frontend A + Backend)

Acceptance criteria:
- **Given** saya login, **when** saya membuka halaman atau bagian riwayat, **then** tampil daftar film dari `search_history`, diurutkan dari yang terbaru.
- [ ] Halaman ini belum ada di desain Figma (isu #1). Belum diputuskan apakah dibuat.

---

## D. Pengguna baru (cold start)

### US-12 – Rekomendasi umum untuk pengguna tanpa riwayat
**Sebagai** pengguna baru yang belum pernah mencari film, **saya ingin** tetap melihat rekomendasi di Beranda, **agar** halaman tidak kosong dan saya punya titik awal.

- Prioritas: Must · F-11, F-12, F-13 · Uji: bagian dari T-07 (kondisi tanpa riwayat), NF-03 · Owner: Model (`popular(n)`), Backend, Frontend A

Acceptance criteria:
- **Given** saya login tetapi `search_history` saya kosong, **when** saya membuka Beranda, **then** tampil N film rekomendasi umum berdasarkan rating (`vote_average` dan `vote_count`).
- **Given** saya baru saja membuka Detail film pertama saya, **when** saya kembali ke Beranda, **then** rekomendasi berubah menjadi personal (US-11).
- [ ] Film dengan `vote_count` sangat kecil tidak mendominasi. Rumus dan batas minimum vote belum ditentukan (isu #4).
- [ ] Judul bagian membedakan rekomendasi umum dan personal. Teks persisnya belum ditentukan.

---

## E. Kebutuhan tim (pendukung)

### US-16 – Data film bersih dan konsisten
**Sebagai** anggota tim model dan backend, **saya ingin** CSV film yang bersih dengan format tetap, **agar** model dan database memakai data yang sama.

- Prioritas: Must · pendukung F-08, NF-05 · Owner: Data · Status: selesai, ada perbaikan kecil

Acceptance criteria:
- [x] CSV `movies_clean_final.csv` berisi 45.430 film dan 9 kolom (`id`, `title`, `overview`, `genres_list`, `keywords_list`, `director`, `release_year`, `vote_average`, `vote_count`), dengan list dipisah `|`.
- [ ] Hitungan overview kosong di notebook diperbaiki. Notebook melaporkan 0 karena `isna()` dipakai setelah `fillna('')`, padahal hitung ulang dari CSV menunjukkan 954.
- [ ] EDA rating/vote ditambahkan.
- [ ] Dedup `keep='first'` untuk 13 id yang konflik dijelaskan.
- [ ] Path `'archive (2).zip'` tidak di-hardcode.
- [ ] Notebook diberi dokumentasi markdown per tahap.

### US-17 – Evaluasi kualitas rekomendasi
**Sebagai** tim yang dinilai dosen, **kami ingin** mengukur relevansi rekomendasi, **agar** hasil sistem bisa dilaporkan secara objektif.

- Prioritas: Must · F-08, F-12 · Owner: Model (Bayu); black-box testing dan SUS dikerjakan bersama

Acceptance criteria:
- [ ] Precision@K dan Recall@K dihitung untuk K = 5 dan K = 10 pada tiga fungsi: film serupa, rekomendasi personal, dan cari film serupa manual.
- [ ] Definisi "film relevan" ditulis sebelum pengujian. Isinya belum ditentukan.
- [ ] Skenario black-box T-01 s.d. T-08 dijalankan dan hasilnya dicatat.
- [ ] Kuesioner SUS (10 pernyataan, skala 1–5, skor 0–100) disebar. Jumlah responden dan target skor belum ditentukan.
