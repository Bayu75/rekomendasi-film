"""Data dummy untuk pratinjau komponen (BUKAN hasil model).

Format mengikuti kontrak model PRD §10 + poster_url dari backend.
id, judul, tahun, genre, sutradara, vote_average, vote_count diambil dari The Movies Dataset
(TMDB, data 2017); similarity hanya contoh. poster_url sengaja dicampur:
- URL placeholder (picsum) -> gambar tampil
- None                     -> fallback inisial langsung dari Jinja
- URL rusak                -> fallback lewat poster.js
"""

BROKEN = "https://image.invalid/poster-tidak-ada.jpg"


def _p(seed):
    return f"https://picsum.photos/seed/{seed}/300/450"


MOVIES = [
    {"id": 27205, "title": "Inception", "release_year": 2010,
     "genres": ["Action", "Thriller", "Science Fiction", "Mystery", "Adventure"],
     "director": "Christopher Nolan", "vote_average": 8.1, "vote_count": 14075,
     "overview": "Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets...",
     "poster_url": _p("inception"), "similarity": 0.53},
    {"id": 155, "title": "The Dark Knight", "release_year": 2008,
     "genres": ["Drama", "Action", "Crime", "Thriller"],
     "director": "Christopher Nolan", "vote_average": 8.2, "vote_count": 12269,
     "overview": "Batman raises the stakes in his war on crime...",
     "poster_url": _p("darkknight"), "similarity": 0.85},
    {"id": 157336, "title": "Interstellar", "release_year": 2014,
     "genres": ["Adventure", "Drama", "Science Fiction"],
     "director": "Christopher Nolan", "vote_average": 8.1, "vote_count": 11187,
     "overview": "Interstellar chronicles the adventures of a group of explorers...",
     "poster_url": None, "similarity": 0.64},
    {"id": 129, "title": "Spirited Away", "release_year": 2001,
     "genres": ["Fantasy", "Adventure", "Animation", "Family"],
     "director": "Hayao Miyazaki", "vote_average": 8.3, "vote_count": 3968,
     "overview": "A young girl, Chihiro, becomes trapped in a strange new world of spirits...",
     "poster_url": _p("spirited"), "similarity": 0.31},
    {"id": 680, "title": "Pulp Fiction", "release_year": 1994,
     "genres": ["Thriller", "Crime"],
     "director": "Quentin Tarantino", "vote_average": 8.3, "vote_count": 8670,
     "overview": "A burger-loving hit man, his philosophical partner...",
     "poster_url": BROKEN, "similarity": 0.12},
    {"id": 238, "title": "The Godfather", "release_year": 1972,
     "genres": ["Drama", "Crime"],
     "director": "Francis Ford Coppola", "vote_average": 8.5, "vote_count": 6024,
     "overview": "Spanning the years 1945 to 1955, a chronicle of the fictional Italian-American Corleone crime family...",
     "poster_url": _p("godfather"), "similarity": 0.27},
    {"id": 862, "title": "Toy Story", "release_year": 1995,
     "genres": ["Animation", "Comedy", "Family"],
     "director": "John Lasseter", "vote_average": 7.7, "vote_count": 5415,
     "overview": "Led by Woody, Andy's toys live happily in his room...",
     "poster_url": _p("toystory"), "similarity": 0.09},
    {"id": 278, "title": "The Shawshank Redemption", "release_year": 1994,
     "genres": ["Drama", "Crime"],
     "director": "Frank Darabont", "vote_average": 8.5, "vote_count": 8358,
     "overview": "Framed in the 1940s for the double murder of his wife and her lover...",
     "poster_url": None, "similarity": 0.18},
    {"id": 99999, "title": "Film Tanpa Sutradara dan Tahun (uji data kosong)", "release_year": None,
     "genres": [], "director": "", "vote_average": None, "vote_count": 0,
     "overview": "", "poster_url": None},
    {"id": 11, "title": "Star Wars", "release_year": 1977,
     "genres": ["Adventure", "Action", "Science Fiction"],
     "director": "George Lucas", "vote_average": 8.1, "vote_count": 6778,
     "overview": "Princess Leia is captured and held hostage by the evil Imperial forces...",
     "poster_url": _p("starwars"), "similarity": 0.72},
]

DEV_USER = {"name": "Kadek Bayu Dwi Pradnya", "email": "bayu@contoh.com"}


MORE_MOVIES = [
    {"id": 550, "title": "Fight Club", "release_year": 1999, "genres": ["Drama"],
     "director": "David Fincher", "vote_average": 8.3, "vote_count": 9678, "poster_url": _p("fightclub")},
    {"id": 13, "title": "Forrest Gump", "release_year": 1994, "genres": ["Comedy", "Drama", "Romance"],
     "director": "Robert Zemeckis", "vote_average": 8.2, "vote_count": 8147, "poster_url": _p("forrest")},
    {"id": 603, "title": "The Matrix", "release_year": 1999, "genres": ["Action", "Science Fiction"],
     "director": "Lana Wachowski", "vote_average": 7.9, "vote_count": 9079, "poster_url": _p("matrix")},
    {"id": 807, "title": "Se7en", "release_year": 1995, "genres": ["Crime", "Mystery", "Thriller"],
     "director": "David Fincher", "vote_average": 8.1, "vote_count": 5915, "poster_url": _p("seven")},
    {"id": 1124, "title": "The Prestige", "release_year": 2006, "genres": ["Drama", "Mystery", "Thriller"],
     "director": "Christopher Nolan", "vote_average": 8.0, "vote_count": 4391, "poster_url": _p("prestige")},
    {"id": 244786, "title": "Whiplash", "release_year": 2014, "genres": ["Drama", "Music"],
     "director": "Damien Chazelle", "vote_average": 8.3, "vote_count": 4376, "poster_url": _p("whiplash")},
    {"id": 120, "title": "The Lord of the Rings: The Fellowship of the Ring", "release_year": 2001,
     "genres": ["Adventure", "Fantasy", "Action"], "director": "Peter Jackson",
     "vote_average": 8.0, "vote_count": 8892, "poster_url": _p("lotr")},
]

ALL_MOVIES = [m for m in MOVIES if m["id"] != 99999] + MORE_MOVIES
_BY_ID = {m["id"]: m for m in ALL_MOVIES}

# popular(n=10): urut vote_average lalu vote_count (rumus final: isu #4, Bayu)
POPULAR = sorted(ALL_MOVIES, key=lambda m: (m["vote_average"], m["vote_count"]), reverse=True)[:10]

# Riwayat dummy (terbaru dulu) – 7 film supaya "+2 lainnya" terlihat
HISTORY_IDS = [27205, 155, 157336, 680, 129, 603, 862]
HISTORY = [_BY_ID[i] for i in HISTORY_IDS]

# recommend_for_user(history_ids, n=8): contoh saja, similarity bukan hasil model
_PERSONAL = [(1124, 0.82), (807, 0.67), (11, 0.61), (550, 0.58), (120, 0.44), (238, 0.39), (244786, 0.33), (278, 0.27)]
PERSONAL_RECS = [dict(_BY_ID[i], similarity=s) for i, s in _PERSONAL]

TOTAL_MOVIES = 45430  # jumlah baris movies_clean_final.csv (PRD §10)
