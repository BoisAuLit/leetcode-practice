"""
📌 信号→模式: 按"内容等价"分组 → 规范化成哈希键（排序串 / 26 位计数元组）当字典 key
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 下次: 2026-09-05
"""
from typing import List


class Solution:
    def hash(self, word: str) -> str:
        counter = [0] * 26
        for ch in word:
            counter[ord(ch) - ord('a')] += 1
        return "-".join(str(c) for c in counter)


    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        position = dict()
        result = []
        for str_ in strs:
            hash_ = self.hash(str_)
            if hash_ in position:
                position[hash_].append(str_)
            else:
                result.append([str_])
                position[hash_] = result[-1]
        return result
