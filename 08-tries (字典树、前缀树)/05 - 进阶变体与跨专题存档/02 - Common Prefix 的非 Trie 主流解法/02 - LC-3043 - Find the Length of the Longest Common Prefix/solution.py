
from typing import List


class Solution:
    def longestCommonPrefix(self, arr1: List[int], arr2: List[int]) -> int:
        trie = {}
        for num in arr1:
            node = trie
            for char in str(num):
                node = node.setdefault(char, {})
            node['#'] = str(num)
        res = 0
        for num in arr2:
            level = 0
            node = trie
            for char in str(num):
                if char in node:
                    level += 1
                    node = node[char]
                else:
                    break
            res = max(res, level)
        return res
