from typing import List
from collections import defaultdict


class Solution:
    def arithmeticTriplets(self, nums: List[int], diff: int) -> int:
        mapping = defaultdict(lambda: [])
        count = 0
        for num in nums:
            slot = num % diff
            mapping[slot].append(num)
            if len(mapping[slot]) >= 3:
                a, b, c = mapping[slot][-3:]
                if b - a == diff and c - b == diff:
                    count += 1
        return count


s = Solution()

nums = [0, 1, 4, 6, 7, 10]
diff = 3

result = s.arithmeticTriplets(nums, diff)
print(result)

"""

"""

