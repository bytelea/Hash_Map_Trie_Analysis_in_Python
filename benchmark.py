# import libraries and packages needed for the project
import time
import os
import sys
from loader import load_movies
from hashmap import HashMap
from trie import Trie

# configuration
DATASET_PATH = "dataset/movies.csv" # path to MovieLens movies.csv
TRIALS = 10 # repetition per experiment (average)
DATASET_SIZES = [1000, 5000, 10000, 25000, 50000, 87585]

# search terms used for benchmarking
EXACT_QUERIES = ["Toy Story (1995)", "Jumanji (1995)", "Heat (1995)",
                  "Casino (1995)", "Sense and Sensibility (1995)"]
PREFIX_QUERIES = ["Toy", "Star", "The", "Lo", "Bat"]

# timing helpers
def time_insertion_hashmap(movies: list) -> float:
    """ build a HashMap from a list of movies and return the average
    insertion time in milliseconds over TRIALS runs """
    times = []
    for _ in range(TRIALS):
        hm = HashMap()
        start = time.perf_counter()
        for movie in movies:
            hm.insert(movie.title, movie)
            hm.insert(str(movie.movie_id), movie)
        end = time.perf_counter()
        times.append(end - start)
    return (sum(times) / len(times)) * 1000 # convert to ms

def time_insertion_trie(movies: list) -> float:
    """ build a Trie and return average insertion time in ms """
    times = []
    for _ in range(TRIALS):
        trie = Trie()
        start = time.perf_counter()
        for movie in movies:
            trie.insert(movie.title, movie)
        end = time.perf_counter()
        times.append(end - start)
    return (sum(times) / len(times)) * 1000

def time_exact_search_hashmap(hm: HashMap, queries: list[str]) -> float:
    """ time exact lookup on a pre-built HashMap returns average time per query in microseconds """
    times = []
    for _ in range(TRIALS):
        start = time.perf_counter()
        for q in queries:
            hm.search(q)
        end = time.perf_counter()
        times.append((end - start) / len(queries))
    return (sum(times) / len(times)) * 1_000_000 # convert to µs

def time_exact_search_trie(trie: Trie, queries: list[str]) -> float:
    """ time exact lookup on a pre-built Trie returns avg µs per query """
    times = []
    for _ in range(TRIALS):
        start = time.perf_counter()
        for q in queries:
            trie.exact_search(q)
        end = time.perf_counter()
        times.append((end - start) / len(queries))
    return (sum(times) / len(times)) * 1_000_000

def time_exact_search_linear(movies: list, queries: list[str]) -> float:
    """ linear scan baseline - O(n) returns avg µs per query"""
    times = []
    for _ in range(TRIALS):
        start = time.perf_counter()
        for q in queries:
            _ = next((m for m in movies if m.title == q), None)
        end = time.perf_counter()
        times.append((end - start) / len(queries))
    return (sum(times) / len(times)) * 1_000_000

def time_prefix_search_trie(trie: Trie, queries: list[str]) -> float:
    """time prefix search on a pre-built Trie returns avg µs per query"""
    times = []
    for _ in range(TRIALS):
        start = time.perf_counter()
        for q in queries:
            trie.search_prefix(q)
        end = time.perf_counter()
        times.append((end - start) / len(queries))
    return (sum(times) / len(times)) * 1_000_000

def time_prefix_search_linear(movies: list, queries: list[str]) -> float:
    """ linear scan prefix baseline - O(n) returns avg µs per query"""
    times = []
    for _ in range(TRIALS):
        start = time.perf_counter()
        for q in queries:
            _ = [m for m in movies if m.title.lower().startswith(q.lower())]
        end = time.perf_counter()
        times.append((end - start) / len(queries))
    return (sum(times) / len(times)) * 1_000_000

# table printers
def print_header(title: str):
    print("\n" + "=" * 72)
    print(f"  {title}")
    print("=" * 72)

def print_table(headers: list[str], rows: list[list], col_width: int = 16):
    header_row = "".join(str(h).rjust(col_width) for h in headers)
    print(header_row)
    print("-" * (col_width * len(headers)))
    for row in rows:
        print("".join(str(cell).rjust(col_width) for cell in row))

# main benchmark runner
def run_benchmarks(dataset_path: str):
    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset not found at '{dataset_path}'")
        print("Please place your MovieLens movies.csv in the same folder as this script")
        sys.exit(1)

    print(f"\nLoading full dataset from '{dataset_path}'...")
    all_movies = load_movies(dataset_path)
    available = len(all_movies)
    print(f"Loaded {available:,} movies total")

    sizes = [s for s in DATASET_SIZES if s <= available]
    if available not in sizes:
        sizes.append(available)

    # table 1 (insertion time)
    print_header("TABLE 1 - Insertion time (ms) averaged over 10 trials")
    rows = []
    for size in sizes:
        movies = all_movies[:size]
        hm_time   = time_insertion_hashmap(movies)
        trie_time = time_insertion_trie(movies)
        rows.append([f"{size:,}", f"{hm_time:.3f}", f"{trie_time:.3f}"])
    print_table(["Dataset Size", "HashMap (ms)", "Trie (ms)"], rows)

    # table 2 (exact search time
    print_header("TABLE 2 - Exact search time (µs/query) averaged over 10 trials")
    rows = []
    for size in sizes:
        movies = all_movies[:size]

        hm = HashMap()
        for m in movies:
            hm.insert(m.title, m)

        trie = Trie()
        for m in movies:
            trie.insert(m.title, m)

        hm_time     = time_exact_search_hashmap(hm, EXACT_QUERIES)
        trie_time   = time_exact_search_trie(trie, EXACT_QUERIES)
        linear_time = time_exact_search_linear(movies, EXACT_QUERIES)

        rows.append([
            f"{size:,}",
            f"{hm_time:.3f}",
            f"{trie_time:.3f}",
            f"{linear_time:.3f}",
        ])
    print_table(["Dataset Size", "HashMap (µs)", "Trie (µs)", "Linear (µs)"], rows)

    # table 3 (prefix search time)
    print_header("TABLE 3 - Prefix search time (µs/query) averaged over 10 trials")
    rows = []
    for size in sizes:
        movies = all_movies[:size]

        trie = Trie()
        for m in movies:
            trie.insert(m.title, m)

        trie_time   = time_prefix_search_trie(trie, PREFIX_QUERIES)
        linear_time = time_prefix_search_linear(movies, PREFIX_QUERIES)

        rows.append([
            f"{size:,}",
            f"{trie_time:.3f}",
            f"{linear_time:.3f}",
        ])
    print_table(["Dataset Size", "Trie (µs)", "Linear (µs)"], rows)

    # HashMap collision stats at full size
    print_header("HashMap Internals (Full Dataset)")
    hm = HashMap()
    for m in all_movies[:sizes[-1]]:
        hm.insert(m.title, m)
    stats = hm.collision_stats()
    for k, v in stats.items():
        print(f"  {k:<25} {v}")

    print("\nBenchmark complete.\n")

# entry point
if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else DATASET_PATH
    run_benchmarks(path)