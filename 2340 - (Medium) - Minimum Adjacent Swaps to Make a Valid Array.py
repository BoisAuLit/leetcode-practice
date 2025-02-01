from typing import List


class Solution:
    def minimumSwaps(self, nums: List[int]) -> int:
        small = nums[0]
        p1 = 0

        large = nums[0]
        p2 = 0

        for index, value in enumerate(nums):
            if value >= large:
                large = value
                p2 = index
            if value < small:
                small = value
                p1 = index

        if small == large:
            return 0
        if p1 > p2:
            return len(nums) + p1 - p2 - 2
        else:
            return len(nums) + p1 - p2 - 1


s = Solution()

# Test case 1: Expecting 6
input_ = [3, 4, 5, 5, 3, 1]

# Test case 2: Expecting 4
input_ = [3, 3, 1, 5, 2, 3]

# Test case 3: Expecting 0
input_ = [10, 10, 10, 10, 10]

# Test case 4: Expecting 0
input_ = [10, 10, 10, 10, 20]

# Test case 5: Expecting 4
input_ = [20, 10, 10, 10, 10]

result = s.minimumSwaps(input_)
print(result)
