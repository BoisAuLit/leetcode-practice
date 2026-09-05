from collections import Counter

class Solution:
    def minimumDeletions(self, word: str, k: int) -> int:
        cnt = Counter(word)
        res = len(word)

        for a in cnt.values():
            deleted = 0
            for b in cnt.values():
                if b < a:
                    deleted += b
                elif b > a + k:
                    deleted += b - (a + k)
            res = min(res, deleted)

        return res
