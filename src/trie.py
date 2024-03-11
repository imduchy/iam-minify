class TrieNode:
    def __init__(self):
        self.children = {}
        self.occurences = 0
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root

        for char in word:
            node.occurences += 1

            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True
