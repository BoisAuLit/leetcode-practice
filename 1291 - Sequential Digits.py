from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        sample = "123456789"
        n = 10
        nums = []

        for length in range(len(str(low)), len(str(high)) + 1):
            for start in range(n - length):
                num = int(sample[start: start + length])
                if num >= low and num <= high:
                    nums.append(num)
        
        return nums


s = Solution()
# low = 1000
# high = 13000
low = 10
high = 1000000000
result = s.sequentialDigits(low, high)
print(result)
