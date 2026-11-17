# Pemetaan Komponen React → Jinja – MovieMatch

Dokumen pendamping `PRD.md` dan `design-system.md`.

**Keputusan kelompok 17 Nov 2026 [Diputuskan]:** MovieMatch dibangun sebagai satu proyek **Flask + Jinja + Tailwind**.
Source React hasil ekspor Figma Make (`/workspace/figma-src`) **hanya acuan visual**. Dari source itu kita menyalin
**struktur HTML, kelas Tailwind, dan teks UI**. State React, `localStorage`, `data/movies.ts`, dan rumus kemiripan dummy **tidak** dipakai.

**Label status:**
- **[Diputuskan]**: sudah disepakati kelompok.
- **[Usulan]**: perlu dikonfirmasi tim. Ini berlaku untuk **semua nama route, endpoint, nama file template, nama macro, dan nama context variable** di dokumen ini.

## 1. Prinsip konversi

| Di React | Di Flask + Jinja | Status |
|---|---|---|
| `App.tsx` mengganti halaman lewat state `nav.page` | Setiap halaman punya URL dan route Flask sendiri; link memakai `url_for(...)` | [Diputuskan] SSR |
| Props komponen | Macro Jinja (`{% macro %}` + `{% from ... import ... %}`) atau `{% include %}` | [Usulan] |
| `useState` untuk hasil pencarian, filter, langkah | Query string (`?q=`, `?genre=`, `?acuan=`) dan render ulang di server | [Usulan] |
| `localStorage` untuk akun dan sandi teks biasa | Session Flask + hash sandi di tabel `users` MySQL | [Diputuskan] mengikuti NF-06 |
| `searchHistory` di state (maks. 10) | Tabel `search_history`, disimpan saat membuka Detail | [Diputuskan] MySQL; batas tampilan: [Usulan] |
| `data/movies.ts` dan `computeSimilarity` | Tabel `movies` + `src/recommender.py` (`recommend`, `recommend_for_user`, `popular`) | [Diputuskan] content-based TF-IDF |
| `setTimeout` palsu untuk efek loading | Skeleton hanya muncul selama request berjalan (JS kecil saat form disubmit) atau dihilangkan | [Usulan] |
| `onError` gambar → fallback inisial | Atribut `onerror` kecil atau `poster.js`; jika `poster_url` kosong, langsung render fallback di Jinja | [Usulan] |
| `style={{ animationDelay: i*40ms }}` | `style="animation-delay: {{ loop.index0 * 40 }}ms"` | [Usulan] |

**Bentuk data film di template [Usulan]:** dict sesuai kontrak model di PRD §10. Field yang dipakai template:
`id`, `title`, `release_year`, `genres` (list), `director`, `vote_average`, `vote_count`, `overview`, `keywords` (list),
`poster_url` (boleh `None`), `similarity` (0–1), `score`, `shared_genres`, `shared_keywords`, `same_director`, `shared_cast`.
`runtime` dan `cast` hanya ada jika isu #2 di PRD diselesaikan; selama belum ada, template harus menyembunyikan bagiannya (`{% if movie.runtime %}`).
Pemetaan dari desain: `rating` → `vote_average`, `poster` → `poster_url`, `similarity` (0–100) → `(movie.similarity * 100) | round | int`.

## 2. Struktur folder template [Usulan]

```
app/
├── templates/
│   ├── base.html                     # A: <html>, font, CSS, navbar, {% block content %}, footer, JS
│   ├── partials/
│   │   ├── navbar.html               # A (include)
│   │   ├── footer.html               # A (include)
│   │   ├── cards.html                # macro movie_card (A), recommendation_card (B)
│   │   ├── badges.html               # macro genre_badge, rating_badge (A); similarity_badge (B)
│   │   ├── search_bar.html           # macro search_bar (A)
│   │   ├── empty_state.html          # macro empty_state (B)
│   │   └── skeleton.html             # macro movie_grid_skeleton, detail_skeleton (B)
│   ├── pages/
│   │   ├── home.html                 # A
│   │   ├── explore.html              # B
│   │   ├── movie_detail.html         # B
│   │   ├── find_similar.html         # B
│   │   ├── login.html                # A
│   │   └── register.html             # A
│   └── errors/404.html               # B (memakai empty_state)
└── static/
    ├── css/input.css → css/app.css   # token @theme dari index.css (lihat design-system.md)
    └── js/
        ├── navbar.js                 # A
        ├── search_bar.js             # A
        ├── auth_form.js              # A
        ├── poster.js                 # A (fallback poster, dipakai semua kartu)
        ├── skeleton.js               # B
        └── find_similar.js           # B (opsional)
```

## 3. Ringkasan route Flask [Usulan]

| Method | URL | Endpoint | Template | Owner backend |
|---|---|---|---|---|
| GET | `/` | `main.home` | `pages/home.html` | Backend |
| GET | `/explore` (`?q=`, `?genre=`, `?page=`) | `main.explore` | `pages/explore.html` | Backend |
| POST | `/riwayat/hapus` | `main.clear_history` | redirect ke `/explore` | Backend |
| GET | `/film/<int:movie_id>` (`?dari=<source_id>`) | `main.movie_detail` | `pages/movie_detail.html` | Backend |
| GET | `/cari-serupa` (`?q=`, `?acuan=<id>`, `?langkah=hasil`) | `main.find_similar` | `pages/find_similar.html` | Backend |
| GET, POST | `/masuk` | `auth.login` | `pages/login.html` | Backend |
| GET, POST | `/daftar` | `auth.register` | `pages/register.html` | Backend |
| POST | `/keluar` | `auth.logout` | redirect ke `/` | Backend |

Context global lewat `@app.context_processor` [Usulan]:
- `current_user`: dict `{name, email}` atau `None`, dibaca dari session.
- `active_page`: diambil dari `request.endpoint`.
- `GENRE_STYLES`: dict nama genre → kelas Tailwind, disalin dari `GenreBadge.tsx`, ditambah alias `"Science Fiction"` → kelas Sci-Fi.

## 4. Komponen bersama (`components/*.tsx`)

| React | Jinja [Usulan] | Cara pakai | Parameter / context | JS vanilla | Owner |
|---|---|---|---|---|---|
| `Navbar.tsx` | `partials/navbar.html` | `{% include %}` di `base.html` | `current_user`, `active_page`, `request.args.q` | `navbar.js`: (1) latar `bg-background/90 backdrop-blur-md border-b shadow-lg` saat `scrollY > 16`; selalu solid di halaman auth (bisa lewat kelas dari server); (2) buka/tutup menu mobile (hamburger ↔ X); (3) dropdown pengguna + tutup saat klik di luar (alternatif tanpa JS: `<details>`); (4) tombol "Cari film..." berubah jadi input kecil, submit `GET /explore?q=`. Tombol Keluar berupa `<form method="post" action="/keluar">`. | **A** |
| `Footer.tsx` | `partials/footer.html` | `{% include %}` di `base.html` dalam `{% block footer %}`; `login.html` dan `register.html` mengosongkan block ini | Tidak ada; link memakai `url_for` | Tidak perlu | **A** |
| `MovieCard.tsx` | macro `movie_card(movie, similarity=None, href=None, action_label=None, action_url=None)` di `partials/cards.html` | `{% from 'partials/cards.html' import movie_card %}` | `movie` (dict film); `similarity` 0–1 (opsional, menampilkan badge kiri atas); `action_*` untuk tombol "Pilih sebagai Acuan" di Cari Film Serupa | Overlay hover cukup CSS (`group-hover`). Fallback poster lewat `poster.js` atau `onerror`. Kartu = `<a href>` | **A** |
| `GenreBadge.tsx` | macro `genre_badge(genre, size='sm')` di `partials/badges.html` | Dipanggil di kartu, Detail, konfirmasi | `genre`, `size` (`sm`/`md`), `GENRE_STYLES` | Tidak perlu | **A** |
| `RatingBadge.tsx` | macro `rating_badge(rating, size='sm')` di `partials/badges.html` | Dipanggil di kartu dan Detail | `rating` = `movie.vote_average`; tampil `"%.1f"\|format(rating)` | Tidak perlu | **A** (bagian dari kartu film) |
| `SearchBar.tsx` | macro `search_bar(action, value='', placeholder='Cari judul film...', size='md', autofocus=False, extra_params={})` di `partials/search_bar.html` | Beranda (hero), Explore, langkah 1 Cari Film Serupa | `action` (URL), `value` (= `query`) | `search_bar.js`: tombol "×" muncul jika ada isi, mengosongkan input lalu fokus. Submit = `<form method="get">` biasa | **A** |
| `RecommendationCard.tsx` | macro `recommendation_card(movie, source_movie_id)` di `partials/cards.html` | Section Film Serupa di Detail | `movie` (dict + `similarity`, `shared_genres`, `same_director`); link ke `url_for('main.movie_detail', movie_id=movie.id, dari=source_movie_id)` | Tidak perlu (fallback poster lewat `poster.js`) | **B** |
| `SimilarityBadge.tsx` | macro `similarity_badge(similarity, size='sm')` di `partials/badges.html` | Kartu film (kiri atas), kartu rekomendasi, banner Detail (`lg`) | `similarity` 0–1 → `score = (similarity*100)\|round\|int`; kelas warna sesuai ambang ≥80 / ≥60 / lainnya (ambang final: isu #14 PRD); `lg`: `stroke-dasharray="{{ score/100*81.7 }} 81.7"` | Tidak perlu | **B** |
| `EmptyState.tsx` | macro `empty_state(type, query=None, action_url=None, action_label=None)` di `partials/empty_state.html` | Explore (tidak ditemukan), Detail (tanpa rekomendasi / 404), Cari Film Serupa | `type` ∈ `search`, `noResults`, `noRecommendations`, `selectMovie`; teks dan ikon SVG disalin dari source | Tidak perlu | **B** |
| `LoadingSkeleton.tsx` | macro `movie_grid_skeleton(count=10)`, `detail_skeleton()` di `partials/skeleton.html` | Disisipkan tersembunyi (`hidden`) di Explore dan Cari Film Serupa | `count` | `skeleton.js`: saat form pencarian/filter disubmit atau link langkah diklik, sembunyikan grid hasil dan tampilkan skeleton sampai halaman baru dimuat. Tanpa JS, skeleton tidak tampil (tidak masalah) | **B** |

> **Ketergantungan:** `movie_card` (A) memanggil `similarity_badge` (B). Usulannya, B menyelesaikan macro `similarity_badge` lebih dulu. Selama belum ada, A boleh memakai stub sederhana dengan nama dan parameter yang sama.

## 5. Halaman (`pages/*.tsx`)

### `App.tsx` + `main.tsx` + `index.css` → `base.html`, route Flask, `static/css/input.css` — Owner: **A** (base) + Backend (route)
- `base.html` memuat link Google Fonts (Inter, Manrope), `css/app.css`, navbar, `<main class="flex-1">{% block content %}`, footer, dan script JS (`defer`).
  Isinya juga `<body class="min-h-screen bg-background flex flex-col">`.
- Fungsi `login`, `register`, `logout`, `addToHistory`, dan `clearHistory` di `App.tsx` dipindah ke route Flask (lihat §3). Logika `localStorage` **dibuang**.
- `vite-env.d.ts` dan `main.tsx` tidak diport. `data/movies.ts` tidak diport; bentuk datanya hanya acuan untuk context dummy.

### `Home.tsx` → `pages/home.html` — Owner: **A**
- Route: `GET /` → `main.home` [Usulan].
- Context [Usulan]:
  - `current_user`: dari context global.
  - `history_preview`: list maks. 5 film riwayat terakhir untuk pill "Berdasarkan:".
  - `history_count`: total riwayat untuk "+N lainnya".
  - `personal_recs`: `recommend_for_user(history_ids, n=8)`, list dict + `similarity`. Kosong jika belum ada riwayat.
  - `popular_movies`: `popular(n=10)`, dipakai bagian "Jelajahi Film" dan cold start.
  - `hero_genres`: `["Sci-Fi","Thriller","Crime","Drama","Action","Animation"]`, link ke `/explore?genre=…`.
  - `stats`: angka strip statistik dari data asli (misalnya jumlah film), atau strip dihapus (isu #16 PRD).
- Logika template: tiga keadaan "Rekomendasi Untukmu" dipilih dengan `{% if not current_user %}` / `{% elif not personal_recs %}` / `{% else %}`.
- JS vanilla: animasi masuk hero (`opacity-0 translate-y-6` → tampil) bisa diganti `.fade-in-up` CSS tanpa JS. Selain itu tidak perlu JS.
- Komponen: `search_bar` (lg), `movie_card`.

### `Explore.tsx` → `pages/explore.html` — Owner: **B**
- Route: `GET /explore` dengan `?q=`, `?genre=`, `?page=` → `main.explore`; `POST /riwayat/hapus` → `main.clear_history` [Usulan].
- Context [Usulan]:
  - `query` (str), `active_genre` (str atau None), `has_searched` (bool).
  - `movies`: hasil pencarian/filter, atau daftar default jika belum mencari.
  - `result_count`, `total_movies`.
  - `pagination`: `page`, `per_page`, `has_next`. **Diperlukan karena data berisi 45.430 film**, padahal demo menampilkan semua 20 film sekaligus.
  - `all_genres`: 16 chip dari source, dengan catatan isu #13.
  - `history`: list film riwayat (hanya jika login dan `not has_searched`).
- JS vanilla:
  - **Filter genre:** usulannya tanpa JS, setiap chip berupa `<a href="?genre=Sci-Fi">`. Chip aktif (`bg-primary text-primary-foreground border-primary`) yang diklik lagi kembali ke `/explore`.
    Jika ingin tanpa reload, `explore.js` boleh memfilter kartu di halaman yang sedang tampil, tetapi hanya untuk hasil yang sudah ada di halaman.
  - **Loading skeleton** saat submit (`skeleton.js`).
  - Tombol "×" search bar (`search_bar.js`).
  - "Hapus Riwayat" berupa `<form method="post">`, bukan JS.
- Komponen: `search_bar` (lg), `movie_card`, `empty_state('noResults', query, url_for('main.explore'), 'Tampilkan Semua Film')`, `movie_grid_skeleton(10)`.

### `MovieDetail.tsx` → `pages/movie_detail.html` — Owner: **B**
- Route: `GET /film/<int:movie_id>` dengan `?dari=<source_movie_id>` opsional → `main.movie_detail` [Usulan]. Jika login, simpan baris ke `search_history`. Jika id tidak ada, tampilkan 404 dengan `empty_state`.
- Context [Usulan]:
  - `movie` (dict lengkap); `runtime_str` (format "2j 28m", hanya jika `runtime` tersedia); `cast` (list, hanya jika tersedia).
  - `recommendations`: `recommend(movie_id, n=10)`.
  - `source_movie`: film dari `?dari=` atau None.
  - `why`: item rekomendasi `source_movie` yang id-nya = film ini. Berisi `similarity`, `shared_genres` (maks. 3), `same_director`, `shared_keywords` (maks. 3), dan `shared_cast` (selalu kosong selama cast tidak ada; isu #2 PRD).
- JS vanilla:
  - Tombol "Cari Film Serupa" dan "Lihat Rekomendasi" cukup `<a href="#film-serupa">`, karena `html { scroll-behavior: smooth }` sudah ada. Tidak perlu JS.
  - Fallback poster dan foto pemeran lewat `poster.js`.
  - Latar blur poster cukup CSS.
- Komponen: `genre_badge` (md), `rating_badge` (md), `similarity_badge` (lg) di banner, `recommendation_card`, `empty_state('noRecommendations')`.
  `detail_skeleton` tidak diperlukan pada SSR biasa.
- Catatan: label "Rating IMDb" diganti "Rating TMDB" (isu #2 PRD).

### `FindSimilar.tsx` → `pages/find_similar.html` — Owner: **B**
- Route: `GET /cari-serupa` → `main.find_similar` [Usulan]. Langkah ditentukan dari query string:
  - **Langkah 1:** tanpa parameter atau dengan `?q=` (cari film acuan).
  - **Langkah 2:** `?acuan=<id>` (konfirmasi).
  - **Langkah 3:** `?acuan=<id>&langkah=hasil` (hasil).
- Context [Usulan]:
  - `step` (`"search"` | `"selected"` | `"results"`), `query`.
  - `search_results`: hasil pencarian judul.
  - `popular_choices`: 10 film pilihan saat belum mencari. Di demo id-nya di-hardcode, jadi diganti dengan `popular(10)`.
  - `reference_movie`.
  - `recommendations`: `recommend(acuan, n=12)`, hanya di langkah 3.
- JS vanilla:
  - **Langkah Cari Film Serupa:** usulannya tanpa JS, karena setiap langkah adalah URL sendiri ("Pilih" → `?acuan=id`, "Cari Film Serupa" → `&langkah=hasil`, "Ganti Film" / "Pilih film lain" → `/cari-serupa`).
    Step indicator dirender server dari `step`.
    `find_similar.js` (opsional) hanya untuk scroll ke atas atau transisi `.fade-in`.
  - **Loading skeleton** saat menekan "Cari Film Serupa" atau submit pencarian (`skeleton.js` + `movie_grid_skeleton(12)` / `(6)`).
- Komponen: `search_bar` (lg, autofocus), `movie_card` (+ tombol "Pilih sebagai Acuan" / "Pilih"), `genre_badge` (md), `rating_badge` (md), `empty_state('noResults' | 'noRecommendations')`, `movie_grid_skeleton`.
- Catatan: kartu hasil langkah 3 menautkan ke `/film/<id>?dari=<acuan>`, sehingga banner "Direkomendasikan berdasarkan" muncul di Detail.

### `Login.tsx` → `pages/login.html` — Owner: **A**
- Route: `GET, POST /masuk` → `auth.login` [Usulan]. Jika sukses, set `session['user_id']` dan redirect ke `/`. Jika gagal, render ulang dengan error.
- Context [Usulan]:
  - `error` (str atau None; pesan disalin dari source, misalnya "Email atau kata sandi salah."). Bisa juga lewat `get_flashed_messages()`.
  - `email` (isian sebelumnya).
  - `show_demo_hint` (bool, `True` hanya jika `app.debug` atau konfigurasi presentasi).
- JS vanilla (`auth_form.js`): toggle tampil/sembunyi kata sandi (ikon mata); tombol "Isi Otomatis" (hanya jika demo aktif); state tombol "Memverifikasi..." + spinner saat submit (`disabled`).
  Validasi tetap dilakukan di server.
- `{% block footer %}{% endblock %}` dikosongkan. Navbar menampilkan versi auth (tanpa menu tengah).

### `Register.tsx` → `pages/register.html` — Owner: **A**
- Route: `GET, POST /daftar` → `auth.register` [Usulan]. Server memvalidasi semua field, format email, sandi minimal 6 karakter, konfirmasi sama, dan email unik, lalu menyimpan `generate_password_hash(password)`.
  Setelah sukses, sesuai laporan diarahkan ke `/masuk` dengan flash "berhasil". Source React justru langsung login lalu ke Beranda (isu #15 PRD).
- Context [Usulan]: `error`, `name`, `email` (isian sebelumnya; sandi tidak pernah dikirim balik).
- JS vanilla (`auth_form.js`):
  - Toggle mata pada kedua field sandi.
  - **Indikator kekuatan sandi** (3 bar, aturan di `design-system.md`).
  - **Cek konfirmasi** live (border merah/hijau + ikon).
  - State tombol "Membuat akun...".
- `{% block footer %}{% endblock %}` dikosongkan.

## 6. Pembagian kerja frontend

| Owner | Template / partial | JS |
|---|---|---|
| **Frontend A** | `base.html`, `partials/navbar.html`, `partials/footer.html`, `movie_card` (`partials/cards.html`), `genre_badge` + `rating_badge` (`partials/badges.html`), `partials/search_bar.html`, `pages/home.html`, `pages/login.html`, `pages/register.html`, `static/css/input.css` | `navbar.js`, `search_bar.js`, `auth_form.js`, `poster.js` |
| **Frontend B** | `pages/explore.html`, `pages/movie_detail.html`, `pages/find_similar.html`, `recommendation_card` (`partials/cards.html`), `similarity_badge` (`partials/badges.html`), `partials/empty_state.html`, `partials/skeleton.html`, `errors/404.html` | `skeleton.js`, `find_similar.js` (opsional), `explore.js` (opsional) |
| **Backend** | Route dan context di §3 dan §5, context processor, auth, riwayat, pagination, build Tailwind | — |
| **Model (Bayu)** | `recommend`, `recommend_for_user`, `popular`, plus `shared_genres` / `shared_keywords` / `same_director` | — |

**Urutan usulan:**
1. A membuat `base.html` + `input.css` + `movie_card`, sedangkan B membuat `similarity_badge` + `empty_state`.
2. Keduanya membangun halaman dengan context dummy (list dict berformat sama dengan kontrak model).
3. Backend mengganti context dummy dengan data MySQL dan model.

## 7. Catatan

- Semua nama route, endpoint, file, macro, dan variabel di atas masih **[Usulan]** dan boleh diganti, asalkan dicatat di sini agar A, B, dan Backend tetap konsisten.
- Kelas Tailwind disalin apa adanya dari source. Agar Tailwind v4 menemukan kelas di template, `input.css` perlu `@source "../../templates"` (atau setara), karena kelas yang dirangkai secara dinamis di Jinja (misalnya dari `GENRE_STYLES`) harus muncul utuh di file yang dipindai.
  Simpan `GENRE_STYLES` di file yang ikut dipindai, atau daftarkan kelasnya dengan `@source inline(...)`.
- Form POST perlu proteksi CSRF (misalnya Flask-WTF) [Usulan].
