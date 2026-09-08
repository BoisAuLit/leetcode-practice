"""
📌 信号→模式: 字母不跨段的最多分段 → 记每字母最后出现位置，扫到当前段最远边界即切
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
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
