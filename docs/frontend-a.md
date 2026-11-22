# Frontend A – layout, komponen bersama, Beranda, Masuk, Daftar

Pemilik: **Frontend A (Bayu)**. Acuan visual: desain Figma Make (struktur HTML, kelas Tailwind, teks UI). Stack: Flask + Jinja + Tailwind v4, JS vanilla.

Nama route, endpoint, macro, dan context variable masih **[Usulan]** sesuai `jinja-components.md`.

Integrasi ke skeleton repo:

- Template, CSS, JS, `app/genre_styles.py`, dan data dummy menggantikan stub Frontend A.
- `app/__init__.py` tetap memuat `load_dotenv()`, `SECRET_KEY`, dan `SQLALCHEMY_DATABASE_URI`. Ditambah Jinja global genre, context `current_user` / `active_page`, dan CSRF jika Flask-WTF terpasang.
- Endpoint publik tetap di `app/routes.py` (`from .routes import main` tidak berubah). Isi fungsinya masih memanggil `app/dev.py` (data dummy + akun di memori). Blueprint `dev` (`/dev/komponen`) terpisah supaya Backend bisa mengganti `routes.py` tanpa ikut menghapus galeri komponen.
- `src/recommender.py` tidak diubah. `run.py` tetap pintu masuk; `HOST` dan `PORT` bisa dioverride lewat environment.
- `app/static/css/app.css` (hasil build Tailwind) ikut di-commit supaya clone langsung tampil. Jangan edit `app.css` manual.

## Cara build CSS

`input.css` memakai `@import 'tailwindcss' source(none)` lalu `@source` manual ke `templates/`, `static/js/`, dan `genre_styles.py`. Kelas yang dirangkai dinamis harus tertulis utuh di file yang dipindai. Utility `.skeleton`, `.fade-in`, dan `.fade-in-up` didefinisikan dengan `@utility`.

```bash
./build_css.sh            # sekali, minified -> app/static/css/app.css
./build_css.sh --watch    # ulang saat template berubah
```

`build_css.sh` memakai `tools/tailwindcss` (atau `tools/tailwindcss.exe`) jika file itu ada dan executable. Kalau tidak, skrip memasang `tailwindcss` dan `@tailwindcss/cli` ke `node_modules` lalu menjalankan CLI dari sana. `npx @tailwindcss/cli` saja tidak cukup: `@import "tailwindcss"` di-resolve dari `node_modules` proyek, dan paket itu tidak ikut terunduh. Biner CLI dan `node_modules/` tidak di-commit (lihat `.gitignore`).

Unduh CLI standalone (tanpa Node), sekali:

```bash
# Linux x64
curl -sSL -o tools/tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tools/tailwindcss
# macOS Apple Silicon: tailwindcss-macos-arm64
# Windows: tailwindcss-windows-x64.exe lalu tools\tailwindcss.exe -i app/static/css/input.css -o app/static/css/app.css --watch
```

## Menjalankan

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Kotak akun demo di halaman Masuk:

```bash
MOVIEMATCH_DEMO_HINT=1 python run.py
```

Akun demo (hanya di server dev, di memori): `demo@moviematch.com` / `demo123`, atau nilai `MOVIEMATCH_DEMO_EMAIL` / `MOVIEMATCH_DEMO_PASSWORD`. Akun yang dibuat lewat `/daftar` hilang saat server di-restart.

| URL | Isi |
|---|---|
| http://127.0.0.1:5000/ | Beranda (data dummy) |
| `/?login=1&riwayat=1` | Login + riwayat (pill "Berdasarkan:" + grid rekomendasi) |
| `/?login=1&riwayat=0` | Login tanpa riwayat |
| `/?login=0` | Tamu |
| `/masuk`, `/daftar` | Masuk & Daftar |
| `/dev/komponen` | Demo komponen |
| `/explore`, `/film/<id>`, `/cari-serupa` | Stub "belum dibuat" (Frontend B) |

## Context yang diharapkan tiap halaman

`current_user` (`{name, email}` atau `None`) dan `active_page` (`request.endpoint`, misalnya `main.home`) disuntik lewat context processor. Navbar membandingkan `active_page` dengan nama endpoint, bukan string pendek `"home"` dari stub lama.

`GENRE_STYLES`, `GENRE_DEFAULT_STYLE`, `ALL_GENRES`, dan `GENRE_LABELS` didaftarkan sebagai **Jinja global** (`register_template_globals`), bukan context processor, karena macro yang di-import dengan `{% from ... import ... %}` tidak melihat variabel context.

**`pages/home.html` (`main.home`)**

| Variabel | Isi |
|---|---|
| `history_preview` | list film riwayat terakhir (maks. 5 dipakai) untuk pill "Berdasarkan:" |
| `history_count` | int, total riwayat (`+N lainnya`) |
| `personal_recs` | `recommend_for_user(..., n=8)`; tiap item punya `similarity` (0–1). Kosong jika belum ada riwayat |
| `popular_movies` | `popular(n=10)`, bagian "Jelajahi Film" |
| `hero_genres` | list nama genre CSV; default `HERO_GENRES` di `genre_styles.py` |
| `total_movies` | int jumlah film (mis. 45430). `None` menyembunyikan item statistik itu |

Tiga keadaan "Rekomendasi Untukmu": tamu / login tanpa rekomendasi / login + rekomendasi.

**`pages/login.html` (`auth.login`)**

`error`, `email`, `show_demo_hint`, `demo_email`, `demo_password`. Flash kategori `success` / `error` tampil di atas form. Field POST: `email`, `password`.

**`pages/register.html` (`auth.register`)**

`error`, `name`, `email` (sandi tidak pernah dikirim balik). Field POST: `name`, `email`, `password`, `confirm_password`.

Pesan error yang dipakai server dev (sama dengan source): "Email dan kata sandi harus diisi.", "Email atau kata sandi salah.", "Semua field harus diisi.", "Format email tidak valid.", "Kata sandi minimal 6 karakter.", "Konfirmasi kata sandi tidak cocok.", "Email sudah terdaftar."

Contoh validasi ada di `app/dev.py` (hash `werkzeug.security`). Sukses daftar: redirect ke `/masuk` dengan flash "Akun berhasil dibuat. Silakan masuk."

**CSRF:** jika Flask-WTF terpasang, `create_app()` memanggil `CSRFProtect(app)`. Form POST (Masuk, Daftar, Keluar) menyertakan `csrf_token` lewat macro `csrf_field()` di `partials/auth.html`. Tanpa Flask-WTF, field itu tidak dirender.

## Komponen

```jinja
{% from 'partials/cards.html' import movie_card %}
{% from 'partials/badges.html' import genre_badge, rating_badge, similarity_badge %}
{% from 'partials/search_bar.html' import search_bar %}
```

- `movie_card(movie, similarity=None, href=None, action_label=None, action_url=None, index=None)`
  - `movie`: `id, title, release_year, genres, director, vote_average, vote_count, poster_url` (boleh `None`).
  - `similarity` 0–1 harus dikirim eksplisit; tidak diambil otomatis dari `movie.similarity`.
  - `href` default `url_for('main.movie_detail', movie_id=movie.id)`.
- `genre_badge(genre, size='sm'|'md')`
- `rating_badge(rating, size='sm'|'md'|'lg', show_label=False)` — `show_label=True` menambah teks "Rating TMDB".
- `similarity_badge(similarity, size='sm'|'lg')` — **stub milik Frontend B**.
- `search_bar(action, value='', placeholder='Cari judul film...', size='md'|'lg', autofocus=False, extra_params={}, name='q')`

`recommendation_card` (Frontend B) belum ada; tempatnya di bawah `partials/cards.html`.

## Deviasi dari desain

| Bagian | Source React | Di sini | Alasan |
|---|---|---|---|
| Strip statistik | "20+ Film tersedia" | `total_movies` dari context ("45.430") | Isu #16 PRD |
| Strip statistik (mobile) | `gap-8` | `gap-x-6 gap-y-4 sm:gap-16` | "45.430" lebih lebar; `gap-8` memecah strip di 390px |
| Chip hero | 6 chip, `?query=Sci-Fi` | 6 chip sama, link `?genre=<nama CSV>` (label "Sci-Fi" → nilai "Science Fiction") | Isu #13 |
| Setelah Daftar | langsung login → Beranda | redirect ke `/masuk` + flash sukses | Laporan (isu #15, usulan) |
| Kotak demo Masuk | selalu tampil | hanya jika `SHOW_DEMO_HINT` | Hanya untuk development |
| Validasi | hanya JS + localStorage | server (utama) + cek awal JS, pesan sama | Tanpa localStorage |
| Animasi hero | state React 700ms | `.fade-in-up` CSS 400ms | Tanpa JS |
| Tombol × search bar | kosongkan + jalankan pencarian kosong | hanya kosongkan + fokus | SSR: pencarian saat "Cari" |
| Login tapi model kosong | grid kosong | empty state "Belum Ada Rekomendasi Untukmu" | Hindari area kosong |
| Kartu Cara Kerja 01 | `onNavigate("home")` | link `/#rekomendasi` | Gulir di halaman yang sama |

## Pertanyaan terbuka untuk tim

1. **Konfirmasi kontrak [Usulan].** Apakah endpoint dan context di atas (dan di `jinja-components.md` §3–§5) sudah final? Navbar, footer, dan kartu sudah memanggil `main.home`, `main.explore`, `main.movie_detail`, `main.find_similar`, `auth.login`, `auth.register`, `auth.logout`.
2. **Isu #13 (genre).** Chip hero memakai nama CSV (`Science Fiction`) dengan label "Sci-Fi". `GENRE_STYLES` menyimpan alias "Sci-Fi" dan "Biography" (tidak ada di CSV). Documentary, Family, Foreign, TV Movie memakai warna default. Apakah daftar chip Explore nanti juga 20 genre CSV?
3. **Isu #14 (ambang kemiripan).** Stub `similarity_badge` memakai ambang desain ≥80 kuning / ≥60 hijau / selainnya abu, dengan `round(similarity × 100)`. Cosine similarity model biasanya jauh di bawah itu. Frontend B yang memiliki macro final; Model yang menentukan ambang setelah melihat distribusi skor.
4. **Isu #15 (setelah daftar).** Server dev mengarahkan ke `/masuk` + flash sukses (laporan), bukan langsung login seperti source React. Apakah alur ini yang dipakai?
5. **Isu #16 (Beranda).** Angka strip dari `total_movies`, bukan "20+". Cold start ditampilkan lewat "Jelajahi Film" (`popular()`), sedangkan "Rekomendasi Untukmu" tanpa riwayat tetap empty state. Apakah strip statistik dipertahankan?
6. **Isu #2 (rating & poster).** Badge memakai label "Rating TMDB". Kartu tidak menampilkan `runtime` atau `cast`. Poster kosong memakai inisial; URL rusak dijatuhkan `poster.js`. Siapa yang mengisi `poster_url` (TMDB atau placeholder)?
7. **CSRF.** `Flask-WTF` ditambahkan ke `requirements.txt` dan `CSRFProtect` aktif bila paket itu terpasang. Apakah Backend ingin CSRF wajib di semua POST, termasuk `/keluar`?
8. **Sesi pengguna.** Context processor masih membaca `session["dev_user"]`. Backend perlu menggantinya dengan user dari tabel `users` tanpa mengubah bentuk dict `{name, email}` yang dibaca navbar.
9. **Frontend B.** `similarity_badge` masih stub di `partials/badges.html`. `recommendation_card`, `empty_state`, dan halaman Explore / Detail / Cari Film Serupa belum ada. Setelah Explore ada, chip `?genre=` dan pencarian navbar `?q=` perlu dicek benar-benar memfilter.
10. **Isu #11 (cara build Tailwind).** `build_css.sh` mendukung CLI standalone dan npx. Apakah tim menstandarkan salah satu, dan apakah `app.css` tetap di-commit?
