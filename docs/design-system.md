---
version: alpha
name: MovieMatch
description: >-
  Design system MovieMatch (Sistem Rekomendasi Film, Kelompok 2 Kelas E).
  Tema gelap dengan satu aksen kuning. Nilai diambil dari source React hasil
  ekspor Figma Make (index.css @theme dan kelas Tailwind di components/*.tsx,
  pages/*.tsx). Ukuran Tailwind dikonversi memakai skala default Tailwind v4
  (dicek terhadap tailwindcss 4.3.5). Source React hanya acuan visual;
  implementasinya Flask + Jinja + Tailwind.
colors:
  primary: "#F5C518"
  on-primary: "#09090C"
  accent: "#F5C518"
  ring: "#F5C518"
  background: "#09090C"
  foreground: "#F0F0F5"
  card: "#111116"
  card-foreground: "#E0E0E8"
  secondary: "#1C1C24"
  secondary-foreground: "#A8A8B8"
  muted: "#18181F"
  muted-foreground: "#6E6E80"
  border: "#252530"
  hero-gradient-start: "#0E0E14"
  skeleton-highlight: "#23232E"
  scrollbar-thumb: "#2A2A38"
  scrollbar-thumb-hover: "#3A3A50"
  primary-soft: "#F5C5181A"
  primary-tint: "#F5C5180D"
  primary-outline: "#F5C5184D"
  error-surface: "oklch(25.8% 0.092 26.042 / 0.4)"
  error-border: "oklch(44.4% 0.177 26.899 / 0.4)"
  error-text: "oklch(80.8% 0.114 19.571)"
  success: "oklch(69.6% 0.17 162.48)"
  similarity-mid-text: "oklch(76.5% 0.177 163.223)"
  similarity-low-text: "oklch(70.5% 0.015 286.067)"
  genre-scifi-text: "oklch(80.9% 0.105 251.813)"
  genre-scifi-bg: "oklch(28.2% 0.091 267.935 / 0.6)"
  genre-action-text: "oklch(80.8% 0.114 19.571)"
  genre-action-bg: "oklch(25.8% 0.092 26.042 / 0.6)"
  genre-drama-text: "oklch(82.7% 0.119 306.383)"
  genre-drama-bg: "oklch(29.1% 0.149 302.717 / 0.6)"
  genre-thriller-text: "oklch(83.7% 0.128 66.29)"
  genre-thriller-bg: "oklch(26.6% 0.079 36.259 / 0.6)"
  genre-crime-text: "oklch(87.1% 0.006 286.286)"
  genre-crime-bg: "oklch(27.4% 0.006 286.033 / 0.8)"
typography:
  display:
    fontFamily: Manrope
    fontSize: 72px
    fontWeight: 900
    lineHeight: 1.25
  headline-xl:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: 900
    lineHeight: 1.25
  headline-lg:
    fontFamily: Manrope
    fontSize: 36px
    fontWeight: 900
    lineHeight: 1.111
  headline-md:
    fontFamily: Manrope
    fontSize: 30px
    fontWeight: 900
    lineHeight: 1.2
  headline-sm:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: 900
    lineHeight: 1.333
  title-lg:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: 900
    lineHeight: 1.375
  title-md:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: 700
    lineHeight: 1.556
  title-sm:
    fontFamily: Manrope
    fontSize: 16px
    fontWeight: 700
    lineHeight: 1.5
  card-title:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: 700
    lineHeight: 1.375
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: 400
    lineHeight: 1.625
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.625
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.333
  label-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: 600
    lineHeight: 1.429
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.333
  badge:
    fontFamily: Manrope
    fontSize: 11px
    fontWeight: 500
    lineHeight: 1.25
  eyebrow:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: 600
    lineHeight: 1.333
    letterSpacing: 0.1em
  eyebrow-xs:
    fontFamily: Manrope
    fontSize: 10px
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: 0.1em
  logo:
    fontFamily: Manrope
    fontSize: 18px
    fontWeight: 900
    lineHeight: 1.556
    letterSpacing: -0.025em
rounded:
  sm: 4px
  md: 6px
  lg: 8px
  xl: 12px
  2xl: 16px
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
  2xl: 32px
  3xl: 40px
  section: 64px
  page-top: 96px
  page-top-detail: 112px
  page-bottom: 80px
  navbar-height: 64px
  gutter-mobile: 16px
  gutter: 24px
  grid-gap: 16px
  container-7xl: 1280px
  container-6xl: 1152px
  container-4xl: 896px
  container-2xl: 672px
  container-xl: 576px
  container-lg: 512px
  container-md: 448px
  breakpoint-sm: 640px
  breakpoint-md: 768px
  breakpoint-lg: 1024px
  breakpoint-xl: 1280px
components:
  navbar:
    backgroundColor: "{colors.background}"
    textColor: "{colors.secondary-foreground}"
    height: 64px
  navbar-link:
    textColor: "{colors.secondary-foreground}"
    typography: "{typography.label-md}"
    rounded: "{rounded.lg}"
    padding: 6px 16px
  navbar-link-active:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
  navbar-cta-similar:
    backgroundColor: "{colors.background}"
    textColor: "{colors.primary}"
    rounded: "{rounded.lg}"
  navbar-cta-similar-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  user-avatar:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    size: 32px
  user-menu:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
    width: 224px
  footer:
    backgroundColor: "{colors.card}"
    textColor: "{colors.muted-foreground}"
    padding: 40px 24px
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-md}"
    rounded: "{rounded.lg}"
    padding: 10px 20px
  button-primary-lg:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.title-sm}"
    rounded: "{rounded.xl}"
    padding: 12px 24px
  button-secondary:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.secondary-foreground}"
    rounded: "{rounded.xl}"
    padding: 12px 24px
  button-outline:
    backgroundColor: "{colors.background}"
    textColor: "{colors.secondary-foreground}"
    rounded: "{rounded.lg}"
    padding: 10px 20px
  button-soft:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    rounded: "{rounded.xl}"
    padding: 12px
  search-bar:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
    padding: 12px 16px
  search-bar-lg:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
    padding: 16px 20px
  search-submit:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.lg}"
    padding: 10px 20px
  genre-chip:
    backgroundColor: "{colors.card}"
    textColor: "{colors.secondary-foreground}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  genre-chip-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
  genre-badge-scifi:
    backgroundColor: "{colors.genre-scifi-bg}"
    textColor: "{colors.genre-scifi-text}"
    typography: "{typography.badge}"
    rounded: "{rounded.full}"
    padding: 2px 10px
  genre-badge-action:
    backgroundColor: "{colors.genre-action-bg}"
    textColor: "{colors.genre-action-text}"
    rounded: "{rounded.full}"
  genre-badge-drama:
    backgroundColor: "{colors.genre-drama-bg}"
    textColor: "{colors.genre-drama-text}"
    rounded: "{rounded.full}"
  genre-badge-thriller:
    backgroundColor: "{colors.genre-thriller-bg}"
    textColor: "{colors.genre-thriller-text}"
    rounded: "{rounded.full}"
  genre-badge-crime:
    backgroundColor: "{colors.genre-crime-bg}"
    textColor: "{colors.genre-crime-text}"
    rounded: "{rounded.full}"
  genre-badge-default:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.secondary-foreground}"
    rounded: "{rounded.full}"
  movie-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
    padding: 12px
  recommendation-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
    padding: 12px
  rating-badge:
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.md}"
    padding: 2px 6px
  similarity-badge-high:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 2px 8px
  similarity-badge-mid:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.similarity-mid-text}"
    rounded: "{rounded.full}"
  similarity-badge-low:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.similarity-low-text}"
    rounded: "{rounded.full}"
  pill-badge:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 4px 12px
  section-tag:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.secondary-foreground}"
    typography: "{typography.eyebrow-xs}"
    rounded: "{rounded.full}"
    padding: 4px 10px
  form-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.2xl}"
    padding: 32px
    width: 448px
  input-field:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.xl}"
    padding: 12px 16px
  input-label:
    textColor: "{colors.secondary-foreground}"
    typography: "{typography.label-sm}"
  form-error:
    backgroundColor: "{colors.error-surface}"
    textColor: "{colors.error-text}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.xl}"
    padding: 12px
  demo-hint:
    backgroundColor: "{colors.primary-tint}"
    textColor: "{colors.secondary-foreground}"
    rounded: "{rounded.xl}"
    padding: 12px
  step-indicator-active:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    rounded: "{rounded.full}"
    size: 28px
  step-indicator-done:
    backgroundColor: "{colors.primary-soft}"
    textColor: "{colors.primary}"
    rounded: "{rounded.full}"
    size: 28px
  step-indicator-todo:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.muted-foreground}"
    rounded: "{rounded.full}"
    size: 28px
  similarity-banner:
    backgroundColor: "{colors.primary-tint}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
    padding: 16px
  info-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.xl}"
    padding: 20px
  reference-card:
    backgroundColor: "{colors.card}"
    textColor: "{colors.foreground}"
    rounded: "{rounded.2xl}"
    padding: 24px
  empty-state:
    backgroundColor: "{colors.muted}"
    textColor: "{colors.muted-foreground}"
    rounded: "{rounded.2xl}"
    padding: 20px
  skeleton:
    backgroundColor: "{colors.muted}"
    rounded: "{rounded.md}"
---

# MovieMatch – Design System

> **Sumber dan status nilai.** Nilai di dokumen ini diambil dari source React hasil ekspor Figma Make
> (`/workspace/figma-src`), yaitu blok `@theme` di `index.css` dan kelas Tailwind di `components/*.tsx`
> dan `pages/*.tsx`. Kelas Tailwind dikonversi ke px/hex/oklch dengan skala default **Tailwind v4**
> (`@import 'tailwindcss'` + `@theme` menandakan v4). Nilai skala dicek terhadap `tailwindcss@4.3.5`.
> Source tidak menyertakan `package.json`, jadi versi persis Tailwind yang dipakai Figma Make tidak diketahui.
> - Nilai berlabel **(estimasi)** belum bisa diturunkan dari source.
> - Warna genre memakai palet bawaan Tailwind v4 (oklch). Opasitas seperti `/60` ditulis sebagai kanal alpha (`oklch(… / 0.6)` atau hex 8 digit, misalnya `#F5C5181A` = `primary/10`). Hasilnya setara dengan `color-mix(in oklab, …, transparent)` yang dipakai Tailwind v4.
> - Stack **[Diputuskan 17 Nov 2026]**: Flask + Jinja + Tailwind. Source React hanya acuan visual.
>   Pemetaan komponen ke template Jinja ada di `jinja-components.md`.
> - Desain: https://www.figma.com/make/8Jp3dCRiIeWQV62hZGxB05/Sistem-Rekomendasi-Film

## Overview

MovieMatch adalah web rekomendasi film berbasis kemiripan konten. Nuansanya sinematik dan tenang:
latar hampir hitam (#09090C), teks putih keabu-abuan, dan **satu warna aksen kuning (#F5C518)**
untuk aksi utama, rating, state aktif, dan kata kunci penting di judul. Poster film menjadi fokus visual,
sedangkan UI di sekitarnya datar dengan border tipis agar tidak bersaing dengan poster.

Kepribadian: modern, ramah, dan jelas. Seluruh teks UI berbahasa Indonesia ("Masuk", "Daftar",
"Cari Film Serupa", "53% Mirip", "Gulir ke bawah"). Tata letaknya lega, dengan kartu besar, section
berjarak 64px, dan konten rata tengah pada halaman fokus (hero Beranda, Login, Daftar, empty state).

## Colors

Semua warna inti diambil persis dari `@theme` di `index.css`:

- **Primary / Accent / Ring – Kuning MovieMatch (#F5C518):** tombol utama, logo, baris kedua judul hero,
  bintang dan angka rating, chip genre aktif, langkah aktif, garis progres, link aksi ("Lihat Semua", "Lihat Detail →").
- **Primary foreground (#09090C):** teks di atas tombol kuning.
- **Background (#09090C):** latar halaman. Hero Beranda memakai `bg-gradient-to-br from-[#0E0E14] via-background to-[#09090C]`,
  ditambah dua radial glow kuning (`rgba(245,197,24,0.07)` dan `0.04`) serta pola titik putih 1px dengan grid 32px dan opasitas 0.025.
  Login dan Daftar memakai glow kuning `0.06` dan pola titik dengan opasitas 0.02.
- **Foreground (#F0F0F5):** judul dan teks utama. **Card foreground (#E0E0E8)** didefinisikan di tema tetapi jarang dipakai.
- **Card (#111116):** kartu film, search bar, chip genre (tidak aktif), dropdown pengguna, kartu form, kartu info.
- **Secondary (#1C1C24) / Secondary foreground (#A8A8B8):** input form, tombol sekunder, chip alasan; teks sekunder untuk sinopsis, subjudul, dan label form.
- **Muted (#18181F) / Muted foreground (#6E6E80):** latar skeleton, langkah yang belum aktif, kotak empty state; teks metadata ("2010 · Christopher Nolan"), placeholder, dan jumlah hasil.
- **Border (#252530):** semua border 1px.
- **Turunan primary:** `primary/10` (pill aktif dan badge status), `primary/5` (banner alasan, kotak demo),
  `primary/20–40` (border hover, border kartu konfirmasi `border-2 border-primary/40`).
- **Status error:** `bg-red-950/40 border-red-800/40 text-red-300` (kotak error form), `border-red-700/60` (konfirmasi sandi tidak cocok),
  `text-red-400 hover:bg-red-950/30` (Keluar di menu mobile).
- **Status sukses:** `border-emerald-700/60` dan ikon `text-emerald-500` (konfirmasi sandi cocok).
- **Indikator kekuatan sandi:** 3 bar `h-1` berwarna `bg-red-500` (Terlalu pendek), `bg-orange-500` (Lemah), `bg-yellow-500` (Sedang), `bg-emerald-500` (Kuat). Bar kosong memakai `bg-border`.
- **Scrollbar:** lebar 5px, thumb #2A2A38 (hover #3A3A50), radius 3px.

**Warna badge genre** (persis dari `GenreBadge.tsx`; latar/teks/border):

| Genre | Kelas Tailwind |
|---|---|
| Sci-Fi | `bg-blue-950/60 text-blue-300 border-blue-800/50` |
| Action | `bg-red-950/60 text-red-300 border-red-800/50` |
| Drama | `bg-purple-950/60 text-purple-300 border-purple-800/50` |
| Thriller | `bg-orange-950/60 text-orange-300 border-orange-800/50` |
| Crime | `bg-zinc-800/80 text-zinc-300 border-zinc-600/50` |
| Comedy | `bg-yellow-950/60 text-yellow-300 border-yellow-700/50` |
| Mystery | `bg-indigo-950/60 text-indigo-300 border-indigo-800/50` |
| Romance | `bg-pink-950/60 text-pink-300 border-pink-800/50` |
| Adventure | `bg-emerald-950/60 text-emerald-300 border-emerald-800/50` |
| Fantasy | `bg-violet-950/60 text-violet-300 border-violet-800/50` |
| Animation | `bg-teal-950/60 text-teal-300 border-teal-800/50` |
| Horror | `bg-red-950/80 text-red-200 border-red-900/50` |
| Biography | `bg-amber-950/60 text-amber-300 border-amber-800/50` |
| History | `bg-stone-800/80 text-stone-300 border-stone-600/50` |
| Western | `bg-yellow-950/60 text-yellow-400 border-yellow-800/50` |
| Music | `bg-fuchsia-950/60 text-fuchsia-300 border-fuchsia-800/50` |
| War | `bg-gray-800/80 text-gray-300 border-gray-600/50` |
| Lainnya (default) | `bg-secondary text-secondary-foreground border-border` |

> Nama genre di CSV berbeda dengan kunci di tabel ini. Contohnya, "Science Fiction" di CSV adalah "Sci-Fi" di tabel. Documentary, Family, Foreign, dan TV Movie tidak punya warna, sehingga memakai default. Pemetaan nama ini perlu dibuat di Jinja (lihat isu #13 di PRD).

**Warna badge kemiripan** (dari `SimilarityBadge.tsx`, skor 0–100):
- ≥ 80: `bg-primary/15 text-primary border-primary/30`
- ≥ 60: `bg-emerald-500/10 text-emerald-400 border-emerald-500/25`
- < 60: `bg-zinc-700/30 text-zinc-400 border-zinc-600/40`

Di demo, skor berupa angka dummy 30–99. Ambang warna untuk cosine similarity asli belum ditentukan (isu #14 di PRD).

## Typography

Dua keluarga font dari Google Fonts (`index.css`): **Manrope** (400–900) untuk judul, label, tombol, dan badge
(`font-display`, juga dipasang otomatis ke semua `h1`–`h6`), serta **Inter** (400, 500, 600) untuk teks isi (`font-sans`, default `body`).
Fallback untuk keduanya adalah `ui-sans-serif, system-ui, sans-serif`. Teks dirender dengan `antialiased`.

| Peran | Kelas di source | Nilai |
|---|---|---|
| Display (judul hero) | `text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black leading-tight` | 36 → 48 → 60 → 72px, 900, lh 1.25 |
| Judul film (Detail) | `text-3xl sm:text-4xl lg:text-5xl font-black leading-tight` | 30 → 36 → 48px |
| Judul halaman (Explore, Cari Film Serupa) | `text-3xl sm:text-4xl font-black` | 30 → 36px |
| Judul section (Rekomendasi Untukmu, Jelajahi Film, Film Serupa, hasil) | `text-2xl sm:text-3xl font-black` | 24 → 30px |
| Judul kartu form (Masuk, Buat Akun) | `text-2xl font-black` | 24px |
| Judul film acuan (konfirmasi) | `text-xl font-black leading-snug` | 20px |
| Judul blok (Sinopsis, Langkah 1: …) | `text-lg font-bold` (+ garis `w-1 h-5 bg-primary rounded-full` di Detail) | 18px |
| Judul kecil (hasil Explore, empty state, kartu Cara Kerja) | `text-base font-bold` / `text-lg font-bold` (empty state) | 16 / 18px |
| Judul kartu film | `text-sm font-bold leading-snug line-clamp-2` | 14px, 700, lh 1.375 |
| Subjudul hero | `text-base sm:text-lg leading-relaxed text-secondary-foreground` | 16 → 18px, lh 1.625 |
| Teks isi (sinopsis, deskripsi) | `text-sm leading-relaxed` | 14px, lh 1.625 |
| Metadata | `text-xs text-muted-foreground` | 12px |
| Label form | `text-xs font-semibold font-display text-secondary-foreground` | 12px, 600 |
| Badge genre sm / md | `text-[11px] font-medium` / `text-xs` | 11 / 12px |
| Badge kemiripan, rating sm | `text-xs font-bold` / `text-xs font-semibold` | 12px |
| Eyebrow (JELAJAHI, FILM POPULER, CARA KERJA) | `text-xs font-semibold uppercase tracking-widest text-primary` | 12px, 0.1em |
| Tag section kecil (FILM SERUPA · OTOMATIS) | `text-[10px] font-bold uppercase tracking-widest` | 10px, 0.1em |
| Logo | `text-lg font-black tracking-tight` (navbar), `text-2xl` (auth), `font-black` (footer) | 18 / 24 / 16px |
| Angka statistik | `text-2xl font-black text-primary` | 24px |
| Nomor langkah dekoratif (01, 02, 03) | `text-5xl font-black text-border/40` | 48px |

## Layout

- **Navbar** `fixed top-0 z-50 h-16`, sehingga halaman memberi jarak atas `pt-24` (96px; Detail `pt-28`, 112px; hero `pt-32`).
- **Kontainer:** `max-w-7xl mx-auto px-4 sm:px-6` (1280px, padding 16 → 24px) untuk navbar, footer, Beranda, dan Explore.
  `max-w-6xl` (1152px) untuk Detail dan Cari Film Serupa. `max-w-4xl` (896px) untuk konten hero dan Cara Kerja.
  `max-w-xl` (576px) untuk search bar hero. `max-w-2xl` (672px) untuk search bar langkah 1. `max-w-md` (448px) untuk Login/Daftar.
  `max-w-lg` (512px) untuk kartu konfirmasi.
- **Ritme vertikal:** section `py-16` (64px); jarak judul ke grid `mb-8`; footer `mt-20 py-10`; halaman `pb-20`.
- **Grid:** `gap-4` (16px) untuk semua grid kartu. Skala spasi Tailwind v4 berbasis 4px (`--spacing: 0.25rem`).
- **Breakpoint (default Tailwind v4):** sm 640px, md 768px, lg 1024px, xl 1280px.

| Grid | Kelas |
|---|---|
| Explore, Jelajahi Film, hasil langkah 1, skeleton | `grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5` |
| Rekomendasi Untukmu (Beranda) | `grid-cols-2 sm:grid-cols-3 md:grid-cols-4` (8 film) |
| Hasil Cari Film Serupa | `grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6` (12 film) |
| Film Serupa di Detail (kartu horizontal) | `grid-cols-1 sm:grid-cols-2` (10 film) |
| Detail: konten + sidebar | `grid-cols-1 lg:grid-cols-3` (konten `lg:col-span-2`, sidebar `sticky top-24`) |
| Detail: poster + meta | `flex-col md:flex-row gap-8`, poster `w-full md:w-60 lg:w-72` |
| Cara Kerja | `grid-cols-1 sm:grid-cols-3 gap-6` |

- **Responsif navbar:** menu desktop, kotak cari kecil, dan tombol Masuk/Daftar/avatar tampil mulai `sm`. Di bawah `sm`,
  navbar menampilkan ikon cari (menuju Explore) dan tombol hamburger yang membuka menu vertikal.

### Page layouts

- **Beranda** (`Home.tsx`):
  1. Hero `min-h-screen` dengan badge "Sistem Rekomendasi Film" (titik `animate-pulse`), judul display dua baris (baris 2 kuning), subjudul, search bar `lg`, enam chip genre (Sci-Fi, Thriller, Crime, Drama, Action, Animation) yang menuju Explore, hiasan strip "film" vertikal di kanan (opasitas 10%), dan indikator "Gulir ke bawah" (`animate-bounce`).
  2. Strip statistik `border-y bg-card/40`. Isinya angka dummy: "20+ Film tersedia", "Top-N Rekomendasi personal", "100% Berbasis konten".
  3. **Rekomendasi Untukmu**: tag "Untuk Kamu · Rekomendasi Personal", judul, subjudul, dan link "Lihat Semua". Ada tiga keadaan:
     - (a) **tamu**: kotak `border-dashed rounded-2xl` berjudul "Masuk untuk Mendapatkan Rekomendasi Personal" dengan tombol Masuk dan "Buat Akun Gratis".
     - (b) **login tanpa riwayat**: kotak serupa berjudul "Belum Ada Rekomendasi Untukmu" dengan tombol "Mulai Jelajahi Film".
     - (c) **login dengan riwayat**: baris pill "Berdasarkan:" (maksimal 5 film riwayat, lalu "+N lainnya") dan grid 8 kartu film dengan badge kemiripan.
  4. **Jelajahi Film**: eyebrow "Film Populer", grid 10 film populer, dan tombol "Lihat Semua Film" (hanya mobile).
  5. **Cara Kerja – Tiga Fungsi Rekomendasi**: 3 kartu bernomor 01–03 (Rekomendasi Untukmu, Film Serupa Otomatis, Cari Film Serupa).
- **Explore** (`Explore.tsx`): eyebrow "Jelajahi", judul "Cari Film", search bar `lg` dengan placeholder "Masukkan judul film, sutradara, atau genre...".
  Jika pengguna login dan belum mencari, tampil panel **Riwayat Pencarian** (`rounded-2xl bg-card`) berisi jumlah film, tombol "Hapus Riwayat", daftar baris thumbnail, dan link "Lihat Rekomendasi →".
  Di bawahnya ada 16 chip genre dan judul hasil ("Hasil pencarian untuk: "…"" atau "Film genre: …" dengan jumlah, plus "Tampilkan semua"; tanpa pencarian: "Semua Film (N)").
  Lalu grid, skeleton saat memuat, atau empty state "Film Tidak Ditemukan".
- **Detail film** (`MovieDetail.tsx`): latar atas poster yang di-blur (`opacity-10 blur-2xl`, tinggi 384px), link "Kembali",
  dan banner alasan (hanya jika dibuka dari rekomendasi). Banner berisi badge kemiripan `lg` (cincin progres), "Direkomendasikan berdasarkan <film>", dan chip
  "Sutradara sama: …", "Genre: …" (maks. 3), "Pemeran: …" (maks. 2), "#keyword" (maks. 3).
  Bagian header berisi poster `rounded-2xl` dan meta: badge genre md, judul, "tahun · durasi · rating", grid Sutradara/Durasi/Rating, tombol "Cari Film Serupa" (scroll ke bagian rekomendasi) dan "Cari Film Lainnya".
  Kolom kiri berisi Sinopsis, Pemeran Utama (avatar 64px, scroll horizontal), dan Tema & Kata Kunci. Sidebar berisi kartu "Informasi Film" dan tombol "Lihat Rekomendasi".
  Paling bawah adalah section **Film Serupa** (tag "Film Serupa · Otomatis", tombol "Cari Film Serupa Manual") dengan grid kartu rekomendasi atau empty state.
- **Cari Film Serupa** (`FindSimilar.tsx`): pill "Pencarian Manual", judul, deskripsi, dan step indicator. Isinya bergantung pada langkah:
  - **Langkah 1:** search bar. Hasilnya berupa grid kartu dengan tombol "Pilih sebagai Acuan". Tanpa kata kunci, tampil "Atau pilih dari film populer:" (10 film) dengan tombol "Pilih".
  - **Langkah 2:** kartu konfirmasi berisi poster `w-28`, badge "Film Acuan Dipilih", teks "Sistem akan mencari film lain yang memiliki genre, tema, pemeran, dan sutradara serupa.", tombol "Ganti Film" dan "Cari Film Serupa" (rasio lebar 1:2), serta link "Pilih film lain".
  - **Langkah 3:** tag "Cari Film Serupa · Manual", judul "Film Serupa dengan" diikuti judul film kuning, mini-card film acuan, tombol "Ganti Film Acuan", teks "N film serupa ditemukan · Diurutkan berdasarkan kemiripan tertinggi", lalu grid 12 film, skeleton, atau empty state.
- **Login / Daftar** (`Login.tsx`, `Register.tsx`): layar penuh rata tengah dengan glow dan pola titik. Isinya logo besar, kartu form, dan link "← Kembali ke Beranda".
  Navbar hanya menampilkan logo dan Masuk/Daftar dengan latar solid. **Footer disembunyikan** di kedua halaman ini.

## Elevation & Depth

Hierarki dibangun dari lapisan tonal (background → card → secondary/muted) dan border 1px `border-border`.
Bayangan dipakai terbatas dan selalu berwarna hitam transparan (nilai dasar shadow Tailwind v4, warnanya diganti):
- Navbar setelah scroll lebih dari 16px (juga selalu di Login/Daftar): `bg-background/90 backdrop-blur-md border-b shadow-lg shadow-black/20`.
- Hover kartu film: `hover:-translate-y-1 hover:shadow-lg hover:shadow-black/40 hover:border-primary/40`. Shadow-lg = `0 10px 15px -3px, 0 4px 6px -4px`.
- Hover kartu rekomendasi: `hover:shadow-md hover:shadow-black/30`.
- Dropdown pengguna: `shadow-xl shadow-black/40`. Kartu form: `shadow-2xl shadow-black/40`. Poster Detail: `shadow-2xl shadow-black/60 ring-1 ring-border`.
- Kartu konfirmasi film acuan: `border-2 border-primary/40 shadow-xl shadow-primary/5` (glow kuning tipis).
- Overlay hover poster: `bg-gradient-to-t from-black/80 via-black/20 to-transparent` dengan tombol kuning "Lihat Detail".

**Animasi** (`index.css`):
- `fadeInUp`: opacity 0 → 1, translateY 16px → 0. Kelas `.fade-in-up` 0.4s ease-out. Kartu diberi `animationDelay` bertingkat 40–60ms per item.
- `fadeIn`: opacity 0 → 1, `.fade-in` 0.3s ease-out (langkah, empty state, dropdown, error).
- `shimmer` untuk `.skeleton`: `linear-gradient(90deg, #18181F 25%, #23232E 50%, #18181F 75%)`, `background-size: 200% 100%`,
  background-position dari -200% ke 200%, 1.5s ease-in-out infinite.
- Lainnya: hero masuk `transition-all duration-700` (dari `opacity-0 translate-y-6`), zoom poster `group-hover:scale-105 duration-500`,
  tombol `active:scale-95`, `animate-pulse` (titik badge hero), `animate-bounce` ("Gulir ke bawah"), dan `scroll-behavior: smooth`.

## Shapes

- `rounded-md` 6px: badge rating di poster, thumbnail riwayat, skeleton teks.
- `rounded-lg` 8px: tombol navbar, tombol Cari kecil, tombol kecil, logo navbar, tombol empty state.
- `rounded-xl` 12px: kartu film, kartu rekomendasi, search bar, input form, tombol besar, banner, kartu info, kotak error.
- `rounded-2xl` 16px: kartu form, kartu konfirmasi, poster Detail, kotak empty/ajakan login, panel riwayat, kartu Cara Kerja.
- `rounded-full`: chip genre, badge, avatar, step indicator, bar kekuatan sandi.
- Poster selalu berasio `aspect-[2/3]`.

## Components

- **Navbar** (`Navbar.tsx`): logo (kotak kuning 32px `rounded-lg` + "Movie**Match**"), link Home/Explore
  (`px-4 py-1.5 rounded-lg text-sm font-medium`; aktif `text-primary bg-primary/10`), dan tombol "Cari Film Serupa" (outline `border-primary/30`; aktif kuning penuh).
  Kotak cari kecil berupa tombol "Cari film..." yang berubah menjadi input `w-40` dengan tombol tutup, lalu submit ke Explore.
  - **Tamu:** tombol "Masuk" (outline) dan "Daftar" (kuning).
  - **Login:** avatar inisial kuning 32px + nama depan + panah, membuka dropdown `w-56` (nama, email, tombol "Keluar" merah saat hover).
  - **Mobile:** menu vertikal dengan link yang sama dan tombol auth berdampingan.
- **Footer** (`Footer.tsx`): `border-t bg-card/50 mt-20`, kontainer `max-w-7xl py-10`, `flex-col sm:flex-row justify-between`.
  Isinya logo kecil (28px), link Home, Explore, dan Cari Film Serupa (`text-sm text-muted-foreground hover:text-foreground`),
  serta tagline "Sistem rekomendasi film berbasis kemiripan konten." (`text-xs`). Footer tidak tampil di Login/Daftar.
- **Kartu film** (`MovieCard.tsx`): `bg-card border rounded-xl overflow-hidden`. Isinya poster 2:3 (`loading="lazy"`), badge rating
  kanan atas (`bg-black/70 backdrop-blur-sm rounded-md px-1.5 py-0.5`), dan badge kemiripan kiri atas (opsional).
  Body `p-3` berisi judul (2 baris), "tahun · sutradara pertama", dan maksimal 2 badge genre.
  Jika gambar gagal dimuat, tampil fallback berupa lingkaran inisial kuning di atas gradasi muted → secondary.
- **Kartu rekomendasi** (`RecommendationCard.tsx`): kartu horizontal `flex gap-4 p-3 rounded-xl` dengan poster `w-16`. Isinya judul + badge kemiripan,
  metadata, rating + 2 genre, teks alasan `text-[11px]` ("Sutradara sama · Genre: …"), dan link "Lihat Detail →".
- **Badge genre** (`GenreBadge.tsx`): pill `border rounded-full font-medium font-display leading-tight`. Ukuran sm `px-2.5 py-0.5 text-[11px]`,
  md `px-3 py-1 text-xs`. Warna mengikuti tabel di Colors.
- **Chip genre (filter)**: `px-3 py-1 rounded-full border text-xs font-semibold`. Tidak aktif:
  `bg-card border-border text-secondary-foreground hover:border-primary/40`. **Aktif:** `bg-primary text-primary-foreground border-primary`.
  Menekan chip aktif sekali lagi akan melepas filter. Chip di hero Beranda memakai `bg-muted/60` dan hover `text-primary`.
- **Badge rating** (`RatingBadge.tsx`): bintang `text-primary fill-primary` + angka 1 desimal, `font-display font-semibold`.
  Ukuran: sm (bintang 12px, `text-xs`), md (14px, `text-sm`), lg (16px, `text-base`).
- **Badge kemiripan (% Mirip)** (`SimilarityBadge.tsx`): sm berupa pill `px-2 py-0.5 rounded-full border text-xs font-bold` dengan titik 6px dan teks "NN% Mirip".
  lg berupa pill `px-4 py-2` dengan cincin SVG 32px (r=13, stroke 2.5, keliling 81.7), teks "NN% Mirip", dan "Kemiripan konten" (`text-[11px]`). Warna mengikuti ambang di Colors.
- **Search bar** (`SearchBar.tsx`): `bg-card border rounded-xl`, saat fokus `focus-within:border-primary/50 ring-1 ring-primary/20`.
  Ukuran md `px-4 py-3` (input `text-sm`, tombol `px-4 py-1.5 text-xs`), lg `px-5 py-4` (input `text-base`, tombol `px-5 py-2.5 text-sm`).
  Ada ikon kaca pembesar, tombol "×" (hanya jika ada isi), dan tombol "Cari" kuning. Kata kunci di-trim sebelum dikirim.
- **Tombol:**
  - *primary*: `bg-primary text-primary-foreground font-bold font-display hover:bg-primary/90 active:scale-95`. Ukuran kecil `px-5 py-2.5 rounded-lg text-sm`, besar `px-6 py-3 rounded-xl`.
  - *secondary*: `bg-secondary border border-border hover:border-primary/30`.
  - *outline*: `border border-border text-secondary-foreground hover:border-primary/40 hover:text-foreground`.
  - *soft*: `bg-primary/10 border border-primary/25 text-primary hover:bg-primary/20` ("Lihat Rekomendasi", "Pilih sebagai Acuan").
  - *link*: `text-primary font-semibold` dengan panah →.
  - *disabled*: `disabled:opacity-60 disabled:cursor-not-allowed` dengan spinner dan teks "Memverifikasi..." / "Membuat akun...".
- **Form** (Login/Daftar): kartu `bg-card border rounded-2xl p-8`. Label `text-xs font-semibold mb-1.5`.
  Field `bg-secondary border rounded-xl px-4 py-3` dengan ikon kiri 16px, fokus `border-primary/50 ring-1 ring-primary/20`, dan tombol mata untuk tampil/sembunyi sandi.
  Placeholder: "Nama kamu", "email@contoh.com", "Min. 6 karakter", "Ulangi kata sandi", "Kata sandi kamu". Tombol submit `w-full py-3 rounded-xl`.
  - **State error:** kotak `p-3 rounded-xl bg-red-950/40 border border-red-800/40` dengan ikon dan teks `text-xs text-red-300` (`.fade-in`).
    Pesan di source: "Email dan kata sandi harus diisi.", "Email atau kata sandi salah.", "Semua field harus diisi.",
    "Format email tidak valid.", "Kata sandi minimal 6 karakter.", "Konfirmasi kata sandi tidak cocok.", "Email sudah terdaftar.".
  - **Konfirmasi sandi:** border `red-700/60` dengan ikon silang jika tidak cocok, `emerald-700/60` dengan ikon centang jika cocok.
  - **Indikator kekuatan:** 3 bar + teks "Kekuatan kata sandi: …" (`text-[11px]`). Aturan: kurang dari 6 karakter = Terlalu pendek, kurang dari 8 = Lemah, ada huruf besar dan angka = Kuat, selain itu Sedang.
  - **Kotak demo** (Login): `bg-primary/5 border-primary/15 rounded-xl` dengan tombol "Isi Otomatis". Hanya untuk development (lihat PRD).
- **Step indicator** (`FindSimilar.tsx`): lingkaran 28px `text-xs font-bold`.
  - *aktif*: `bg-primary text-primary-foreground`.
  - *selesai*: `bg-primary/20 text-primary border-primary/40` dengan ikon centang.
  - *belum*: `bg-muted border-border text-muted-foreground`.
  - Garis penghubung `w-8 sm:w-16 h-px`, kuning jika sudah dilewati.
  - Label `text-xs font-semibold` hanya tampil mulai `sm`.
- **Empty state** (`EmptyState.tsx`): rata tengah `py-20` dengan ikon 48px di kotak `p-5 rounded-2xl bg-muted/50 border`, judul `text-lg font-bold`,
  deskripsi `text-sm max-w-xs`, dan tombol primary opsional. Ada empat tipe:
  - "Cari Film"
  - "Film Tidak Ditemukan", dengan deskripsi berisi kata kunci
  - "Belum Ada Rekomendasi"
  - "Pilih Sebuah Film"
- **Loading skeleton** (`LoadingSkeleton.tsx`): `MovieCardSkeleton` berisi poster 2:3, dua baris teks, dua pill, dan baris tombol. `MovieGridSkeleton`
  memakai grid yang sama dengan Explore (default 10 item). `DetailSkeleton` berisi poster `md:w-64` dan blok judul/teks/tombol. Semuanya memakai kelas `.skeleton`.
- **Banner alasan & chip alasan** (Detail): `p-4 rounded-xl bg-primary/5 border-primary/20`. Chip `px-2.5 py-1 rounded-full bg-secondary border text-xs`
  (keyword memakai `bg-muted text-muted-foreground` dengan awalan "#").
- **Kartu Informasi Film** (Detail): `rounded-xl bg-card border p-5`, berisi baris label (muted, kiri) dan nilai (kanan, `text-xs font-medium`).
  Label "Rating IMDb" di source harus diganti menjadi "Rating TMDB" (isu #2 di PRD).

## Do's and Don'ts

- Do: pakai token `@theme` (`bg-card`, `text-muted-foreground`, `border-border`, …), bukan hex mentah, di template Jinja.
- Do: pakai `font-display` (Manrope) untuk judul, tombol, label, dan badge; Inter untuk teks isi.
- Do: pakai kuning `primary` hanya untuk satu aksi utama per area, rating, dan state aktif.
- Do: pakai satu partial kartu film yang sama di Beranda, Explore, dan Cari Film Serupa (lihat `jinja-components.md`).
- Do: tampilkan "% Mirip" sebagai `round(similarity × 100)` dari model, bukan angka dummy demo.
- Do: sediakan fallback inisial jika poster tidak ada, seperti di source.
- Don't: menambah warna aksen baru di luar kuning, warna status (merah/hijau), dan palet genre.
- Don't: memakai bayangan berwarna selain hitam transparan, kecuali glow `primary/5` pada kartu konfirmasi.
- Don't: menyalin logika React (state, `localStorage`, `data/movies.ts`) ke JS. Data selalu dari Flask.
- Don't: menampilkan label "Rating IMDb" atau angka statistik dummy ("20+ Film tersedia").

## Tailwind Mapping

Status: **[Diputuskan 17 Nov 2026]** memakai Tailwind. Versi Tailwind dan cara build-nya **[Usulan]**: Tailwind v4,
karena `index.css` source memakai `@import 'tailwindcss'` dan `@theme`.

Salin isi berikut apa adanya ke `app/static/css/input.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800;900&family=Inter:wght@400;500;600&display=swap');
@import 'tailwindcss';
@source "../../templates";   /* usulan: agar kelas di template Jinja ikut dipindai */

@theme {
  --color-background: #09090C;
  --color-foreground: #F0F0F5;
  --color-card: #111116;
  --color-card-foreground: #E0E0E8;
  --color-primary: #F5C518;
  --color-primary-foreground: #09090C;
  --color-secondary: #1C1C24;
  --color-secondary-foreground: #A8A8B8;
  --color-muted: #18181F;
  --color-muted-foreground: #6E6E80;
  --color-accent: #F5C518;
  --color-accent-foreground: #09090C;
  --color-border: #252530;
  --color-ring: #F5C518;
  --font-sans: 'Inter', ui-sans-serif, system-ui, sans-serif;
  --font-display: 'Manrope', ui-sans-serif, system-ui, sans-serif;
}
/* lalu salin juga: html/body/h1–h6, scrollbar, @keyframes shimmer/fadeInUp/fadeIn,
   .skeleton, .fade-in-up, .fade-in, .line-clamp-2/3/4 dari index.css */
```

| Token DESIGN.md | Kelas Tailwind |
|---|---|
| colors.primary / on-primary | `bg-primary`, `text-primary`, `text-primary-foreground` |
| colors.background / foreground | `bg-background`, `text-foreground` |
| colors.card | `bg-card` (`bg-card/50` footer, `bg-card/40` strip statistik) |
| colors.secondary / secondary-foreground | `bg-secondary`, `text-secondary-foreground` |
| colors.muted / muted-foreground | `bg-muted`, `text-muted-foreground` |
| colors.border | `border-border` |
| colors.primary-soft / primary-tint / primary-outline | `bg-primary/10`, `bg-primary/5`, `border-primary/30` |
| colors.error-* | `bg-red-950/40`, `border-red-800/40`, `text-red-300` |
| typography.display | `text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-black font-display leading-tight` |
| typography.headline-lg | `text-3xl sm:text-4xl font-black font-display` |
| typography.headline-md | `text-2xl sm:text-3xl font-black font-display` |
| typography.title-md | `text-lg font-bold font-display` |
| typography.card-title | `text-sm font-bold font-display leading-snug line-clamp-2` |
| typography.body-md | `text-sm leading-relaxed` |
| typography.eyebrow | `text-xs font-semibold font-display uppercase tracking-widest text-primary` |
| typography.badge | `text-[11px] font-medium font-display leading-tight` |
| rounded.md / lg / xl / 2xl / full | `rounded-md` / `rounded-lg` / `rounded-xl` / `rounded-2xl` / `rounded-full` |
| spacing.container-7xl | `max-w-7xl mx-auto px-4 sm:px-6` |
| spacing.container-6xl | `max-w-6xl mx-auto px-4 sm:px-6` |
| spacing.container-md | `max-w-md` |
| spacing.page-top | `pt-24` (Detail `pt-28`) |
| spacing.section | `py-16` |
| spacing.grid-gap | `gap-4` |
