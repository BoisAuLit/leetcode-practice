from typing import List


class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False
        self.linkCount = 0  # number of children

    def addChild(self, char: str):
        if char not in self.children:
            self.children[char] = TrieNode()
            self.linkCount += 1


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.addChild(ch)
            node = node.children[ch]
        node.isEnd = True


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        trie = Trie()
        
        for word in strs:
            trie.insert(word)
        
        
        node = trie.root
        prefix_chars = []

        while node.linkCount == 1 and not node.isEnd:
            # get the single child (char, child_node)
            (ch, child_node), = node.children.items()
            prefix_chars.append(ch)
            node = child_node

        return "".join(prefix_chars)
