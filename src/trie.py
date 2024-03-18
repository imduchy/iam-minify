from typing import Self


class TrieNode:
    def __init__(self):
        self.children = {}
        self.occurences = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    @staticmethod
    def from_list(iam_actions: list[str]) -> Self:
        trie = Trie()

        for action in iam_actions:
            trie.insert(action)

        return trie

    def insert(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]
            node.occurences += 1
