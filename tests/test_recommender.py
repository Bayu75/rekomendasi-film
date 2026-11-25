import json

import numpy as np
import pandas as pd
import pytest

from src.build_model import build_bundle, save_bundle
from src.evaluation import (GenreRelevance, evaluate_similar, precision_at_k, recall_at_k,
                            sample_queries, simulate_users)
from src.preprocessing import build_tags, clean_text, prepare_movies, split_list, squash
from src.recommender import Recommender, load_model

ITEM_KEYS = {
    "id", "title", "release_year", "genres", "director", "vote_average", "vote_count",
    "overview", "keywords", "similarity", "score", "reasons", "source_movie_id",
    "shared_genres", "shared_keywords", "same_director", "shared_cast",
}


def _rows():
    sci = ["space", "alien", "robot", "future", "planet", "galaxy"]
    crime = ["gang", "heist", "police", "detective", "murder", "mafia"]
    rom = ["love", "wedding", "romance", "couple", "kiss", "marriage"]
    rows, i = [], 1
    for name, words, genre, director in [
        ("Sci", sci, "Science Fiction|Action", "Ann Lee"),
        ("Crime", crime, "Crime|Thriller", "Bob Ray"),
        ("Rom", rom, "Romance|Comedy", "Cy Tan"),
    ]:
        for k in range(5):
            rows.append({
                "id": i * 10, "title": f"{name} {k}",
                "overview": f"A story about {words[k % 6]} and {words[(k + 1) % 6]} and {words[(k + 2) % 6]}.",
                "genres_list": genre, "keywords_list": "|".join(words[k:k + 3]),
                "director": director if k < 3 else "Other Person",
                "release_year": 2000 + k if k != 4 else np.nan,
                "vote_average": 6.0 + k * 0.5, "vote_count": 100 * (k + 1),
            })
            i += 1
    return pd.DataFrame(rows)


@pytest.fixture(scope="module")
def df():
    return _rows()


@pytest.fixture(scope="module")
def model(df):
    return Recommender(build_bundle(df, min_df=1))


# ------------------------------------------------------------- preprocessing
def test_split_and_clean():
    assert split_list("Action|Crime") == ["Action", "Crime"]
    assert split_list(None) == [] and split_list(float("nan")) == [] and split_list("") == []
    assert clean_text("Spider-Man's  Return!") == "spider mans return"
    assert squash("Science Fiction") == "sciencefiction"


def test_build_tags_director_is_one_token():
    t = build_tags("Hello.", ["Science Fiction"], ["space war"], "Christopher Nolan")
    assert "christophernolan" in t.split() and "sciencefiction" in t.split()


def test_prepare_movies_validates_and_dedups(df):
    with pytest.raises(ValueError):
        prepare_movies(df.drop(columns=["director"]))
    dup = pd.concat([df, df.iloc[[0]].assign(title="Duplikat")])
    out = prepare_movies(dup)
    assert len(out) == len(df) and out.loc[0, "title"] == df.loc[0, "title"]  # keep='first'


# ----------------------------------------------------------------- recommend
def test_recommend_contract(model):
    res = model.recommend(10, 5)
    # data mini: hanya 4 film lain yang berbagi kata dengan film 10; yang similarity-nya 0 dibuang
    assert len(res) == 4
    assert all(set(r) == ITEM_KEYS for r in res)
    ids = [r["id"] for r in res]
    assert 10 not in ids and len(set(ids)) == len(ids)  # acuan tidak ikut, tanpa duplikat
    scores = [r["score"] for r in res]
    assert scores == sorted(scores, reverse=True)
    assert all(0 <= r["similarity"] <= 1 for r in res)
    assert all(r["source_movie_id"] == 10 for r in res)
    json.dumps(res)  # semua tipe Python biasa


def test_recommend_finds_same_theme(model, df):
    res = model.recommend(10, 4)  # film Sci: 4 teratas harus film Sci lain
    assert {r["title"].split()[0] for r in res} == {"Sci"}


def test_recommend_reasons(model):
    res = model.recommend(10, 4)
    top = res[0]
    assert top["same_director"] is True
    assert "Science Fiction" in top["shared_genres"]
    assert any(r.startswith("Sutradara sama") for r in top["reasons"])
    assert top["shared_cast"] == []


def test_recommend_unknown_id_raises_keyerror(model):
    for bad in (999999, "abc", None):
        with pytest.raises(KeyError):
            model.recommend(bad)


def test_recommend_n_edge_cases(model):
    assert model.recommend(10, 0) == []
    assert len(model.recommend(10, 1000)) <= len(model) - 1
    assert len(model.recommend(10, 3)) == 3


def test_release_year_na_becomes_none(model):
    by_id = {m["id"]: m for m in model.popular(len(model))}
    assert by_id[50]["release_year"] is None  # baris k == 4 punya tahun NaN
    assert by_id[10]["release_year"] == 2000


# ------------------------------------------------------------------- popular
def test_popular(model):
    res = model.popular(5)
    assert len(res) == 5 and all(set(r) == ITEM_KEYS for r in res)
    assert all(r["similarity"] is None and r["source_movie_id"] is None for r in res)
    scores = [r["score"] for r in res]
    assert scores == sorted(scores, reverse=True)
    assert model.popular(0) == []
    json.dumps(res)


def test_popular_penalises_few_votes():
    df = _rows()
    df.loc[len(df)] = {"id": 999, "title": "Hype", "overview": "x", "genres_list": "Drama",
                       "keywords_list": "a", "director": "Z", "release_year": 2020,
                       "vote_average": 10.0, "vote_count": 1}
    m = Recommender(build_bundle(df, min_df=1))
    assert m.popular(1)[0]["id"] != 999  # 1 vote 10.0 tidak boleh jadi nomor satu


# ------------------------------------------------------- recommend_for_user
def test_for_user_excludes_history_and_dedups(model):
    hist = [10, 20, 30]  # terbaru dulu
    res = model.recommend_for_user(hist, 8)
    ids = [r["id"] for r in res]
    assert not set(ids) & set(hist)
    assert len(set(ids)) == len(ids)
    assert all(r["source_movie_id"] in hist for r in res)
    json.dumps(res)


def test_for_user_empty_or_unknown_falls_back_to_popular(model):
    pop = [r["id"] for r in model.popular(5)]
    assert [r["id"] for r in model.recommend_for_user([], 5)] == pop
    assert [r["id"] for r in model.recommend_for_user([424242], 5)] == pop
    assert [r["id"] for r in model.recommend_for_user(None, 5)] == pop


def test_for_user_ignores_unknown_and_duplicate_ids(model):
    a = model.recommend_for_user([10, 10, 424242], 5)
    b = model.recommend_for_user([10], 5)
    assert [r["id"] for r in a] == [r["id"] for r in b]


def test_for_user_follows_taste(model):
    res = model.recommend_for_user([10, 11], 3)
    assert {r["title"].split()[0] for r in res} == {"Sci"}


def test_for_user_respects_max_history(model):
    hist = [10, 20, 30]
    only_first = model.recommend_for_user(hist, 5, max_history=1)
    assert all(r["source_movie_id"] == 10 for r in only_first)


def test_for_user_bad_agg(model):
    with pytest.raises(ValueError):
        model.recommend_for_user([10], 3, agg="median")


# ------------------------------------------------ artefak & singleton & eval
def test_save_and_load_roundtrip(tmp_path, df, monkeypatch):
    path = save_bundle(build_bundle(df, min_df=1), tmp_path / "m.joblib")
    m = load_model(path)
    assert m.recommend(10, 3)[0]["id"] in {20, 30, 40, 50}
    import src.recommender as rec
    assert rec.recommend(10, 2) and rec.popular(2) and rec.recommend_for_user([10], 2)


def test_load_model_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_model(tmp_path / "tidak_ada.joblib")


def test_metrics():
    assert precision_at_k([1, 2, 3, 4], {1, 3}, 4) == 0.5
    assert precision_at_k([1, 2], {1}, 5) == 0.5  # dibagi jumlah item yang ada
    assert recall_at_k([1, 2, 3], {1, 3, 9, 10}, 3) == 0.5
    assert recall_at_k([1], set(), 5) == 0.0 and precision_at_k([], {1}, 5) == 0.0


def test_genre_relevance(model):
    rel = GenreRelevance(model, 0.5)
    ids = rel.relevant_ids(10)
    assert 10 not in ids and ids == {20, 30, 40, 50}


def test_evaluate_similar_and_users(model):
    q = sample_queries(model, 10, min_votes=0)
    res = evaluate_similar(model, q, ks=(3,), n=3)
    assert res["P@3"] > 0.9  # tema sangat terpisah di data mini
    assert len(simulate_users(model, 3, history_size=2, min_rating=0, seed=1, min_holdout=2)) >= 1
