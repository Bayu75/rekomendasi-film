from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    history = db.relationship(
        "SearchHistory", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(255), nullable=False)
    overview = db.Column(db.Text)
    genres = db.Column(db.String(255))
    keywords = db.Column(db.Text)
    director = db.Column(db.String(255))
    release_year = db.Column(db.SmallInteger, nullable=True)
    vote_average = db.Column(db.Numeric(3, 1))
    vote_count = db.Column(db.Integer)
    poster_path = db.Column(db.String(255), nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    cast_list = db.Column(db.Text, nullable=True)


    @property
    def genre_list(self):
        return [g for g in (self.genres or "").split("|") if g]

    @property
    def keyword_list(self):
        return [k for k in (self.keywords or "").split("|") if k]

    @property
    def cast(self):
        """Ubah cast_list menjadi daftar aktor dan karakter."""
        hasil = []

        for item in (self.cast_list or "").split("|"):
            if not item.strip():
                continue

            bagian = item.split("::", 1)
            nama = bagian[0].strip()
            karakter = bagian[1].strip() if len(bagian) > 1 else ""

            if nama:
                hasil.append({
                    "name": nama,
                    "character": karakter
                })

        return hasil

class SearchHistory(db.Model):
    __tablename__ = "search_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    search_query = db.Column("query", db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)

    movie = db.relationship("Movie", lazy=True)
