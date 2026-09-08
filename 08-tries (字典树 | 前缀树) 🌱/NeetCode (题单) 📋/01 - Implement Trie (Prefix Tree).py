"""
📌 信号→模式: 前缀树 insert/search/startsWith → 节点 children 字典 + end 标记
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
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
        