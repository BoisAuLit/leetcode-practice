class PrefixTree:

    def __init__(self):
        self.trie = {}

    def insert(self, word: str) -> None:
        node = self.trie
        for ch in word:
            node = node.setdefault(ch, {})
        node['#'] = word

    def search(self, word: str) -> bool:
        node = self.trie
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return '#' in node

    def startsWith(self, prefix: str) -> bool:
        node = self.trie
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return bool(node)
        