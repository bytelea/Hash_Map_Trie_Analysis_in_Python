""" implements the Trie (Prefix Tree) data structure for efficient prefix-based search and autocomplete on movie titles
contains two classes TrieNode (fundamental building block of the Trie) and Trie (manages all insert, search and
autocomplete operations) adapted for the MovieLens dataset movie titles are stored in lowercase to make all searches case insensitive
time complexities
insert O(k) where k is the length of the movie title
search O(k) where k is the length of the query string
starts_with O(k) where k is the length of the prefix
autocomplete O(k + m) where m is the number of results collected"""

# TrieNode
class TrieNode:
    """ single node within the Trie (Prefix Tree)
    each node represents one character in a movie title path, nodes are connected to form paths from the root, where
    each complete path from root to an end of word node spells out full movie titles
    attributes
    children: dict[str, TrieNode] (mapping of character,child TrieNode for all possible continuations) allows each node
    to branch into multiple next characters
    is_end_of_word: bool (true if the path from the root to this node forms a complete title
    distinguishes a valid complete title from a prefix only path
    movie: Movie or None (movie object stored at the end of a title path, none for intermediate nodes that are not the end of any complete title"""

    def __init__(self):
        """ initialise a TrieNode with an empty children dict and no end marker"""
        # dictionary: character - TrieNode allows each node to branch to multiple next characters
        self.children = {}

        # flag to distinguish a complete title from a prefix only node
        self.is_end_of_word = False

        # stores the movie object once a complete title path is formed
        self.movie = None

# trie
class Trie:
    """ prefix Tree supporting insertion, exact search, prefix search and autocomplete on movie titles
    all titles are stored and searched in lowercase to ensure case insensitive behaviour"""
    def __init__(self):
        """initialise the Trie with an empty root node, the root node does not represent any character its just
        the entry point to all possible title paths"""
        self.root = TrieNode()

    # insert
    def insert(self, title: str, movie) -> None:
        """insert a movie title into the Trie, storing the Movie object at the terminal node
        characters are inserted one by one from the root, if a node for a character does not yet exist, a new TrieNode
        is created, when all characters have been inserted, the final node is marked as is_end_of_word and the Movie object is attached
        time complexity O(k) where k = len(title)
        parameters
        title: str (movie title to insert)
        movie: Movie (Movie object to store at the end of the title path)"""
        # normalise to lowercase for case insensitive prefix matching
        title = title.lower()
        current = self.root

        for char in title:
            # create a new node if this character has no child yet
            if char not in current.children:
                current.children[char] = TrieNode()

            # move down to the next node along the character path
            current = current.children[char]

        # mark the final node as the end of a complete movie title
        current.is_end_of_word = True
        current.movie = movie  # attach the movie object

    # internal helpers
    def _traverse(self, string: str):
        """ follow the path defined by 'string' through the Trie from the root, used internally by search() and
        starts_with() to navigate to the node corresponding to the end of a given word or prefix
        Returns None if any character in the string is not found, meaning the string or prefix does not exist in the Trie
        time complexity O(k) where k = len(string)
        parameters
        string: str (string to traverse)
        returns TrieNode or None (node at the end of the path, or None if not found) """
        current = self.root

        for char in string:
            if char not in current.children:
                return None  # path breaks, string not in Trie
            current = current.children[char]

        return current  # successfully reached the end of the path

    def _dfs(self, node, path: str, results: list) -> None:
        """perform a depth first search from 'node', collecting all complete movie titles reachable
        from this point recursive helper used by autocomplete() appends each complete movie object to
        the results list when it reaches an end node
        parameters
        node: TrieNode (the node to start the dfs from)
        path: str (the string built so far along the path from the prefix node)
        results: list (accumulator complete movie objects are appended here) """
        #if this node marks the end of a valid title, record the movie
        if node.is_end_of_word and node.movie is not None:
            results.append(node.movie)

        # recursively explores all child nodes
        for char, child_node in node.children.items():
            # extend the current path with this character and recurse
            self._dfs(child_node, path + char, results)

    # search
    def search(self, title: str):
        """ check if exact movie title exists in the Trie uses _traverse() to reach the node at
        the end of the title path,then checks whether that node is marked as is_end_of_word
        returns the Movie object if found, or None if not, time complexity O(k) where k = len(title)
        parameters
        title: str (the exact movie title to search for) returns Movie or None """
        node = self._traverse(title.lower())

        # path must exist and the node must mark a complete title
        if node is not None and node.is_end_of_word:
            return node.movie
        return None

    # prefix/starts_with
    def starts_with(self, prefix: str):
        """ check whether any movie title in the Trie begins with 'prefix', returns the node at the end
        of the prefix path if it exists, or None if the prefix is not present. Used as the starting point
        for autocomplete(), time complexity O(k) where k = len(prefix)
        parameters
        prefix: str (prefix string to check, returns TrieNode or None """
        return self._traverse(prefix.lower())

    # autocomplete
    def autocomplete(self, prefix: str, limit: int = 10) -> list:
        """return all movie titles in the Trie that begin with 'prefix' locates the prefix node using starts_with(),
        then performs a dfs to collect all reachable complete titles and results are capped at 'limit' to avoid returning
        big lists, time complexity O(k + m) where k = len(prefix) m = results found
        parameters
        prefix: str (prefix to search case-insensitive)
        limit: int (maximum number of results to return default is 10)
        returns list[Movie] (movie objects whose titles start with the prefix, up to 'limit' + an empty list if the prefix is not found """
        prefix_node = self.starts_with(prefix)

        if prefix_node is None:
            return []  # prefix not found in the Trie

        results = []
        self._dfs(prefix_node, prefix.lower(), results)

        return results[:limit]

    # aliases for benchmark compatibility
    def exact_search(self, title: str):
        """alias for search() used by the benchmark module"""
        return self.search(title)

    def search_prefix(self, prefix: str) -> list:
        """alias for autocomplete() used by the benchmark module"""
        return self.autocomplete(prefix)