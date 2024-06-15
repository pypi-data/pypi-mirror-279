#Pruned Trie Space Minimization






# Example usage


if __name__ == '__main__':
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end_of_word = False
    class Trie:
        def __init__(self):
            self.root = TrieNode()
        def insert(self, word):
            current = self.root
            for char in word:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.is_end_of_word = True
        def search(self, word):
            current = self.root
            for char in word:
                if char not in current.children:
                    return False
                current = current.children[char]
            return current.is_end_of_word
        def starts_with(self, prefix):
            current = self.root
            for char in prefix:
                if char not in current.children:
                    return False
                current = current.children[char]
            return True
    trie = Trie()
    words = ["apple", "banana", "cat", "app", "bat"]
    for word in words:
        trie.insert(word)
    print(trie.search("cat"))  # True
    print(trie.search("dog"))  # False
    print(trie.starts_with("ap"))  # True
    print(trie.starts_with("ca"))  # False
