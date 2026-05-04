""" data model representing a single movie record from the MovieLens dataset acts as a simple
container for all relevant fields parsed from the csv file and its used across the HashMap and
Trie so that both structures store and return the same object type """

class Movie:
    """ represents a single movie record
    attributes
    movie_id: int (nique numeric identifier from the MovieLens dataset)
    title: str (full movie title including release year
    genres: list[str] (one or more genre labels associated with the movie)
    rating: float (avg user rating derived from the ratings cvs) """

    def __init__(self, movie_id: int, title: str, genres: list, rating: float = 0.0):
        """ initialises a Movie object
        parameters
        movie_id: int (unique identifier for the movie)
        title: str (full title string including release year)
        genres: list[str] (list of genre labels)
        rating: float (avg rating across all user ratings defaults to 0.0) """
        self.movie_id = movie_id
        self.title = title
        self.genres = genres
        self.rating = rating

    def __repr__(self) -> str:
        """return a readable string representation of the movie"""
        genres_str = "|".join(self.genres)
        return (
            f"Movie(id={self.movie_id}, title='{self.title}', "
            f"genres='{genres_str}', rating={self.rating:.2f})"
        )

    def __eq__(self, other) -> bool:
        """2 movies are equal if they share the same movie_id"""
        if not isinstance(other, Movie):
            return False
        return self.movie_id == other.movie_id