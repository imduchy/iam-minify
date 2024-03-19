from src.trie import Trie


class TestTrie:

    def test_insert_one_word(self):
        trie = Trie()

        trie.insert("abc")

        assert trie.root.children["a"].children["b"].children["c"]

    def test_insert_two_words(self):
        trie = Trie()

        trie.insert("abc")
        trie.insert("def")

        assert trie.root.children["a"].children["b"].children["c"]
        assert trie.root.children["d"].children["e"].children["f"]

    def test_trie_node_occurence_increases(self):
        trie = Trie()

        trie.insert("ab")
        trie.insert("ac")

        assert trie.root.children["a"].occurences == 2
        assert trie.root.children["a"].children["b"].occurences == 1
        assert trie.root.children["a"].children["c"].occurences == 1

    def test_from_list_constructor(self):
        trie = Trie.from_list(["abc", "def"])

        assert trie.root.children["a"].children["b"].children["c"]
        assert trie.root.children["d"].children["e"].children["f"]
