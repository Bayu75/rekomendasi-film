"""Gaya badge genre MovieMatch (milik Frontend A) [Usulan].

File ini SENGAJA ikut dipindai Tailwind (lihat `@source "../../genre_styles.py"` di
`static/css/input.css`), jadi semua kelas di bawah harus ditulis utuh, jangan dirangkai.

Kelas disalin persis dari `figma-src/components/GenreBadge.tsx`. Kunci memakai nama genre
seperti di CSV (`genres_list`), sesuai isu #13 PRD:
- "Sci-Fi" di desain = "Science Fiction" di CSV (alias "Sci-Fi" tetap disimpan).
- "Biography" tidak ada di CSV, tetapi kelasnya tetap disimpan agar tidak error jika muncul.
- Documentary, Family, Foreign, TV Movie memakai warna default (sesuai design-system.md).
"""

# 20 genre di movies_clean_final.csv (urut abjad), dipakai untuk chip filter / showcase.
ALL_GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "Foreign",
    "History", "Horror", "Music", "Mystery", "Romance",
    "Science Fiction", "TV Movie", "Thriller", "War", "Western",
]

GENRE_DEFAULT_STYLE = "bg-secondary text-secondary-foreground border-border"

GENRE_STYLES = {
    "Science Fiction": "bg-blue-950/60 text-blue-300 border-blue-800/50",
    "Sci-Fi": "bg-blue-950/60 text-blue-300 border-blue-800/50",
    "Action": "bg-red-950/60 text-red-300 border-red-800/50",
    "Drama": "bg-purple-950/60 text-purple-300 border-purple-800/50",
    "Thriller": "bg-orange-950/60 text-orange-300 border-orange-800/50",
    "Crime": "bg-zinc-800/80 text-zinc-300 border-zinc-600/50",
    "Comedy": "bg-yellow-950/60 text-yellow-300 border-yellow-700/50",
    "Mystery": "bg-indigo-950/60 text-indigo-300 border-indigo-800/50",
    "Romance": "bg-pink-950/60 text-pink-300 border-pink-800/50",
    "Adventure": "bg-emerald-950/60 text-emerald-300 border-emerald-800/50",
    "Fantasy": "bg-violet-950/60 text-violet-300 border-violet-800/50",
    "Animation": "bg-teal-950/60 text-teal-300 border-teal-800/50",
    "Horror": "bg-red-950/80 text-red-200 border-red-900/50",
    "Biography": "bg-amber-950/60 text-amber-300 border-amber-800/50",
    "History": "bg-stone-800/80 text-stone-300 border-stone-600/50",
    "Western": "bg-yellow-950/60 text-yellow-400 border-yellow-800/50",
    "Music": "bg-fuchsia-950/60 text-fuchsia-300 border-fuchsia-800/50",
    "War": "bg-gray-800/80 text-gray-300 border-gray-600/50",
    # Documentary, Family, Foreign, TV Movie -> GENRE_DEFAULT_STYLE
}


# [Usulan] Label tampilan singkat untuk chip hero Beranda (desain memakai "Sci-Fi").
# Nilai yang dikirim ke ?genre= tetap nama CSV.
GENRE_LABELS = {
    "Science Fiction": "Sci-Fi",
}

# Chip hero Beranda sesuai desain (Home.tsx), memakai nama genre CSV.
HERO_GENRES = ["Science Fiction", "Thriller", "Crime", "Drama", "Action", "Animation"]


def register_template_globals(app):
    """Daftarkan sebagai Jinja *global* (bukan hanya context_processor), karena macro yang
    di-import dengan `{% from ... import ... %}` tidak melihat variabel context."""
    app.jinja_env.globals.update(
        GENRE_STYLES=GENRE_STYLES,
        GENRE_DEFAULT_STYLE=GENRE_DEFAULT_STYLE,
        ALL_GENRES=ALL_GENRES,
        GENRE_LABELS=GENRE_LABELS,
    )
