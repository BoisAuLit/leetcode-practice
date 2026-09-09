from typing import List


class Solution:
    def mergeTriplets(self, triplets: List[List[int]], target: List[int]) -> bool:
        found = [False, False, False]  # target 的三个位置分别能否被凑到

        for a, b, c in triplets:
            # 任何一位超过 target 的 triplet 不能用，跳过
            if a > target[0] or b > target[1] or c > target[2]:
                continue
            # 安全 triplet：检查它是否恰好命中 target 的某一位
            if a == target[0]:
                found[0] = True
            if b == target[1]:
                found[1] = True
            if c == target[2]:
                found[2] = True

        return all(found)
