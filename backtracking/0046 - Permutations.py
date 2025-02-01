from typing import List

"""
Given an array nums of distinct integers, return all the possible 
permutations
. You can return the answer in any order.

--------------------------------------------------------------- 

Example 1:

Input: nums = [1,2,3]
Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

---------------------------------------------------------------

Example 2:

Input: nums = [0,1]
Output: [[0,1],[1,0]]

---------------------------------------------------------------

Example 3:

Input: nums = [1]
Output: [[1]]
 
---------------------------------------------------------------

Constraints:

1 <= nums.length <= 6
-10 <= nums[i] <= 10
All the integers of nums are unique.


"""


class Solution:
    """
    https://www.youtube.com/watch?v=s7AvT7cGdSo
    """

    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []

        if len(nums) == 1:
            return [nums[:]]

        for i in range(len(nums)):
            n = nums.pop(0)
            perms = self.permute(nums)

            result.extend([perm + [n] for perm in perms])
            nums.append(n)
        return result


s = Solution()
input_ = [1, 2, 3, 4, 5, 6]
result = s.permute(input_)
print(result)
