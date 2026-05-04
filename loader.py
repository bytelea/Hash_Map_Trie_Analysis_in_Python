""" reading the MovieLens CSV files and producing Movie objects
handles two CSV files:
- movies.csv: movieId, title, genres
- ratings.csv: userId, movieId, rating, timestamp
DataLoader pre-computes an average rating per movie from ratings.csv and
attaches it to each movie object made from movies.csv"""

import csv
import os
from movie import Movie

def load_movies(movies_path: str, ratings_path: str = None, limit: int = None) -> list:
    """ parse movies.csv and return a list of Movie objects also optionally reads ratings.csv to
    attach an average rating to each movie but if ratings_path is not provided, rating defaults to 0.0
    parameters
    movies_path: str (path to the MovieLens movies.csv file)
    ratings_path: str (path to the MovieLens ratings.csv file)
    limit: int (maximum number of movies to load, lads all if theres none)
    returns list[Movie] ordered list of movie objects parsed from the csv"""
    if not os.path.isfile(movies_path):
        raise FileNotFoundError(f"[Loader] movies.csv not found at '{movies_path}'")

    # pre load avg ratings
    avg_ratings = _load_average_ratings(ratings_path)
    movies = []
    with open(movies_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            # respect the optional limit on dataset size
            if limit is not None and i >= limit:
                break

            movie_id = int(row["movieId"])
            title = row["title"].strip()

            # genres are pipe separated in MovieLens
            genres_raw = row["genres"].strip()
            genres = genres_raw.split("|") if genres_raw != "(no genres listed)" else []

            rating = avg_ratings.get(movie_id, 0.0)
            movies.append(Movie(movie_id, title, genres, rating))

    return movies

def _load_average_ratings(ratings_path: str) -> dict:
    """ parse ratings.csv and compute the average rating per movie id which reads every row,
    accumulates sum and count per movieId, then computes the mean.
    Parameters - ratings_path (str or None)
        Path to ratings.csv, or None if not available.

    Returns
    -------
    dict[int, float]
        Mapping of movieId to average rating.
    """
    if ratings_path is None or not os.path.isfile(ratings_path):
        return {}

    totals = {} # {movie_id: sum of ratings}
    counts = {} # {movie_id: number of ratings}

    with open(ratings_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            mid = int(row["movieId"])
            rating = float(row["rating"])
            totals[mid] = totals.get(mid, 0.0) + rating
            counts[mid] = counts.get(mid, 0) + 1

    return {mid: round(totals[mid] / counts[mid], 2) for mid in totals}