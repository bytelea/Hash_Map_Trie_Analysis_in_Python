# Hash Map and Trie Analysis in Python
This project was completed as part of the **Algorithms and Data Structures (TU850)** module at TU Dublin.
The aim of the project is to implement and compare two data structures for efficient movie search and analyse how their performance changes as the dataset size increases.

## Project Overview
Data structures are essential in computer science as they determine how efficiently data can be stored and retrieved. In real-world search systems, choosing the right structure is critical — an inefficient approach can make search feel slow even on modern hardware.

In this project, a Hash Map and a Prefix Tree (Trie) were implemented from scratch and tested on a real-world dataset of movies.

The goal was to:
- Measure execution time for insertion, exact search, and prefix search
- Compare empirical results with theoretical time complexity
- Analyse scalability and efficiency across increasing dataset sizes
- Demonstrate autocomplete functionality using the Trie

## Data Structures Implemented
- **Hash Map - O(1) average exact lookup**
- **Trie (Prefix Tree) - O(k) prefix search and autocomplete**
- **Linear Scan - O(n) baseline for comparison**

## Dataset
The dataset used is the **MovieLens dataset** provided by GroupLens Research at the University of Minnesota.

Source: https://grouplens.org/datasets/movielens/

Each record includes:
- Movie ID
- Title (including release year)
- Genres (pipe-separated)
- Average Rating (derived from ratings.csv)

### Preprocessing
Before inserting into data structures:
- Genres were split from pipe-separated strings into lists
- Average ratings were computed per movie from ratings.csv
- All titles were lowercased for case-insensitive search

## How to Run
1. Download the MovieLens dataset from https://grouplens.org/datasets/movielens/
2. Place 'movies.csv' (and optionally 'ratings.csv') in a folder called 'dataset/'
3. Run the application:
4. Choose from the menu:
   - '[1]' Exact search by title or movie ID (HashMap)
   - '[2]' Prefix search / autocomplete (Trie)
   - '[3]' Run full benchmark suite

## Experiments
Three operations were benchmarked across six dataset sizes:

**1,000 -> 5,000 -> 10,000 -> 25,000 -> 50,000 -> 87,585 movies**

Each experiment was:
- Run 10 times
- Averaged for accuracy
- Tested on the same dataset slice

### Operations Measured
- **Insertion time** - time to build each structure from scratch
- **Exact search time** - average time per query (HashMap vs Trie vs Linear)
- **Prefix search time** - average time per query (Trie vs Linear)

## Performance Insights

### Key Findings

- **HashMap (Exact Search)**
  - Near-constant lookup time regardless of dataset size
  - Around 11–13µs per query across all sizes
  - Confirms O(1) average-case behaviour
  - Load factor: 0.333, average chain length: 1.18 at full dataset

- **Trie (Prefix Search)**
  - Consistently faster than linear scan at every dataset size
  - ~7x faster than linear scan at 1,000 movies
  - ~1.6x faster at 87,585 movies
  - Confirms O(k) complexity — traversal depth depends on prefix length, not dataset size

- **Linear Scan**
  - Surprisingly fast for exact search at small sizes due to CPU cache effects
  - Falls behind significantly for prefix search at all dataset sizes
  - Confirms O(n) scaling — time grows linearly with dataset size

### Insertion Time Comparison (full dataset)
| Structure | Time (ms) |
|-----------|-----------|
| HashMap   | 3,479.889 |
| Trie      | 6,438.610 |

The Trie takes approximately twice as long to build because it creates a new node for every character of every title.

## Conclusion
The results show how data structure choice directly impacts search performance.

- The **HashMap** is the best choice for exact lookup — O(1) average case means search time stays constant no matter how large the dataset grows
- The **Trie** is the best choice for prefix search and autocomplete — O(k) means traversal depth depends only on the prefix length, not the number of movies stored
- The **linear scan** is competitive at small sizes due to cache effects, but becomes increasingly inefficient as the dataset grows
- Neither structure alone is sufficient — a real search system needs both working together

This project highlights how theoretical complexity analysis guides data structure selection, and how hardware behaviour creates real-world nuances that Big-O notation alone does not capture.
