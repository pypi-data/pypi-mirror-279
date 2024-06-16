class Node:
    def __init__(self, word=None):
        self.word = word
        self.next = [None] * 20  # Using None for clearer intent

class BKTree:
    def __init__(self, words=None, tolerance=2):
        self.root = Node()
        self.tree = [Node() for _ in range(100)]
        self.ptr = 0
        self.TOL = tolerance
        if words:
            for word in words:
                self.add_word(word)

    @staticmethod
    def edit_distance(a, b):
        """Calculate the Levenshtein distance between two strings."""
        m, n = len(a), len(b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if a[i - 1] != b[j - 1]:
                    dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + 1)
                else:
                    dp[i][j] = dp[i - 1][j - 1]
        return dp[m][n]

    def add_word(self, word):
        """Add a word to the BKTree."""
        curr = Node(word)
        if not self.root.word:
            self.root = curr
            return
        self._add_node(self.root, curr)

    def _add_node(self, root, curr):
        """Recursively place a new word in the tree based on its edit distance from other words."""
        dist = self.edit_distance(curr.word, root.word)
        if not root.next[dist] or not root.next[dist].word:
            self.ptr += 1
            self.tree[self.ptr] = curr
            root.next[dist] = self.tree[self.ptr]
        else:
            self._add_node(root.next[dist], curr)

    def get_similar_words(self, word):
        """Retrieve words from the BKTree that are within a set tolerance distance."""
        return self._search_similar_words(self.root, word)

    def _search_similar_words(self, root, s):
        """Recursive function to search similar words in the tree."""
        if not root or not root.word:
            return []
        ret = []
        dist = self.edit_distance(root.word, s)
        if dist <= self.TOL:
            ret.append(root.word)

        start = max(dist - self.TOL, 1)
        while start <= dist + self.TOL and start < 20:
            if root.next[start]:
                ret += self._search_similar_words(root.next[start], s)
            start += 1
        return ret

# The module can also contain unit tests or be a part of larger package with additional functionality.
