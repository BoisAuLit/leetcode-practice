from typing import List


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        n = len(s)
        indices = [-1] * 26
        for i, ch in enumerate(s):
            indices[ord(ch) - ord("a")] = i

        res = []
        i = 0
        while i < n:
            start = i
            last = indices[ord(s[i]) - ord("a")]
            while i <= last:
                last = max(last, indices[ord(s[i]) - ord("a")])
                i += 1
            res.append(last - start + 1)
        return res


s = Solution()
input_ = "xyxxyzbzbbisl"
result = s.partitionLabels(input_)
print()
print(result)
