from typing import List

"""
Difficulty: Medium

Given an array of non-negative integers arr,
you are initially positioned at start index of the array.

When you are at index i,
you can jump to i + arr[i] or i - arr[i],
check if you can reach any index with value 0.

Notice that you can not jump outside of the array at any time.

Example 1:

Input: arr = [4,2,3,0,3,1,2], start = 5
Output: true
Explanation:
All possible ways to reach at index 3 with value 0 are:
index 5 -> index 4 -> index 1 -> index 3
index 5 -> index 6 -> index 4 -> index 1 -> index 3

------------------------------------------------------------------

Example 2:

Input: arr = [4,2,3,0,3,1,2], start = 0
Output: true
Explanation:
One possible way to reach at index 3 with value 0 is:
index 0 -> index 4 -> index 1 -> index 3

------------------------------------------------------------------

Example 3:

Input: arr = [3,0,2,1,2], start = 2
Output: false
Explanation: There is no way to reach at index 1 with value 0.

------------------------------------------------------------------

Constraints:

1 <= arr.length <= 5 * 104
0 <= arr[i] < arr.length
0 <= start < arr.length
"""


class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        visited = set()
        length = len(arr)

        def dfs(index: int) -> bool:
            if index < 0 or index >= length:
                return False
            if arr[index] == 0:
                return True
            if index in visited:
                return False
            visited.add(index)

            return dfs(index - arr[index]) or dfs(index + arr[index])

        return dfs(start)


s = Solution()

# Test case 1: Expecting True
# input_ = [4,2,3,0,3,1,2]
# start_ = 5

# Test case 2: Expecting True
# input_=  [4,2,3,0,3,1,2]
# start_ = 0

# Test case 3: Expecting False
input_ = [3, 0, 2, 1, 2]
start_ = 2

result = s.canReach(input_, start_)
print(result)
