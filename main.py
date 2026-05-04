""" entry point for the project provides a simple command line interface allowing the user to search for a movie by
exact title (HashMap O(1) average), search by prefix/autocomplete (Trie O(k)), run the full benchmark
MovieLens dataset in folder called 'dataset/':
dataset/movies.csv
dataset/ratings.csv
dataset- https://grouplens.org/datasets/movielens/ """

import sys
import os
import time
from movie import Movie
from loader import load_movies
from hashmap import HashMap
from trie import Trie
from benchmark import run_benchmarks

# paths for dataset/folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MOVIES_PATH  = os.path.join(BASE_DIR, "dataset", "movies.csv")
RATINGS_PATH = os.path.join(BASE_DIR, "dataset", "ratings.csv")

# build both structures from the dataset
def load_and_build(movies_path: str, ratings_path: str):
    """ load the dataset and build both the HashMap and Trie
    parameters
    movies_path: str (path to movies.csv)
    ratings_path: str (path to ratings.csv used only if the file exists)
    returns
    tuple(list[Movie], HashMap, Trie) """

    ratings = ratings_path if os.path.isfile(ratings_path) else None

    print("\nLoading dataset...")
    movies = load_movies(movies_path, ratings)
    print(f"  Loaded {len(movies):,} movies.")

    print("Building HashMap...")
    start = time.perf_counter()
    hm = HashMap()
    for movie in movies:
        hm.insert(movie.title, movie) # lookup by title
        hm.insert(str(movie.movie_id), movie) # lookup by id
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  HashMap built in {elapsed:.2f} ms  "
          f"(load factor: {hm.load_factor():.3f})")

    print("Building Trie...")
    start = time.perf_counter()
    trie = Trie()
    for movie in movies:
        trie.insert(movie.title, movie)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"  Trie built in {elapsed:.2f} ms")

    return movies, hm, trie

# display helpers
def display_movie(movie: Movie) -> None:
    """ print a formatted summary of a single movie """
    genres = ", ".join(movie.genres) if movie.genres else "N/A"
    rating = f"{movie.rating:.2f}" if movie.rating else "N/A"
    print(f"\n  ID      : {movie.movie_id}")
    print(f"  Title   : {movie.title}")
    print(f"  Genres  : {genres}")
    print(f"  Rating  : {rating}")

def search_exact(hm: HashMap, query: str) -> None:
    """ perform an exact movie lookup using the HashMap, accepts either a full
    movie title or a numeric movie id, displays the result and the time taken in microseconds """
    start = time.perf_counter()
    result = hm.search(query)

    # fall back to numeric id lookup if title search found nothing
    if result is None and query.isdigit():
        result = hm.search(query)

    elapsed = (time.perf_counter() - start) * 1_000_000

    if result:
        print(f"\n  Found (HashMap, {elapsed:.2f} µs):")
        display_movie(result)
    else:
        print(f"\n  No exact match found for '{query}' ({elapsed:.2f} µs)")

def search_prefix(trie: Trie, prefix: str, limit: int = 10) -> None:
    """ perform a prefix search using the Trie (autocomplete) returns up to 'limit'
    movies whose titles begin with the given prefix displays each result and the total
    time taken in microseconds """
    start = time.perf_counter()
    results = trie.autocomplete(prefix, limit=limit)
    elapsed = (time.perf_counter() - start) * 1_000_000

    if results:
        print(f"\n  Found {len(results)} result(s) for '{prefix}' ({elapsed:.2f} µs):")
        for i, movie in enumerate(results, 1):
            genres = ", ".join(movie.genres) if movie.genres else "N/A"
            print(f"  [{i}] {movie.title}  |  {genres}  |  * {movie.rating:.2f}")
    else:
        print(f"\n  No titles found starting with '{prefix}' ({elapsed:.2f} µs)")

# main menu loop
def main():
    """ run the interactive cli for movie search presents a menu for exact search, prefix search and benchmark """
    print("=" * 55)
    print("  Movie Search HashMap & Trie")
    print("  Algorithms and Data Structures CA2")
    print("=" * 55)

    if not os.path.isfile(MOVIES_PATH):
        print(f"\n[Error] movies.csv not found at: {MOVIES_PATH}")
        print("  Download the MovieLens dataset from:")
        print("  https://grouplens.org/datasets/movielens/")
        print("  and place movies.csv in the dataset/folder.")
        sys.exit(1)
    movies, hm, trie = load_and_build(MOVIES_PATH, RATINGS_PATH)

    while True:
        print("\n" + "-" * 40)
        print("  [1] Exact search  (HashMap)")
        print("  [2] Prefix search (Trie autocomplete)")
        print("  [3] Run benchmarks")
        print("  [q] Quit")
        print("-" * 40)

        choice = input("  Enter choice: ").strip().lower()

        if choice == "1":
            query = input("  Enter exact title or movie ID: ").strip()
            if query:
                search_exact(hm, query)

        elif choice == "2":
            prefix = input("  Enter prefix for autocomplete: ").strip()
            if prefix:
                search_prefix(trie, prefix)

        elif choice == "3":
            print("\n  Running benchmarks (this might take a while)...")
            run_benchmarks(MOVIES_PATH)

        elif choice == "q":
            print("\n  Goodbye.")
            break

        else:
            print("  Invalid choice - enter 1, 2, 3 or q")

if __name__ == "__main__":
    main()