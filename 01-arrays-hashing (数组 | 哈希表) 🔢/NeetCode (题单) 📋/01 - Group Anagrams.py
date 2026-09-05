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
