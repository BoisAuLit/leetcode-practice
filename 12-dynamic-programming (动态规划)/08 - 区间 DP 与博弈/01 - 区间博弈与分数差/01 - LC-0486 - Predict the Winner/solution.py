from typing import List


class Solution_1_Recursive:
    """
    Time complexity: O(2ⁿ)
    Space complexity: O(n)
    """

    def predictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)

        def maxDiff(left, right):
            if left == right:
                return nums[left]
            score_by_left = nums[left] - maxDiff(left + 1, right)
            score_by_right = nums[right] - maxDiff(left, right - 1)
            return max(score_by_left, score_by_right)

        return maxDiff(0, n - 1) >= 0


class Solution_Dymanica_Programming_with_Memoization:
    """
    Dynamic programming top-down appraoche: memoization.
    Break big problems down into small problems until the moment when
    we reach the base case, hence find the final solution.

    Time complexity: O(n²)
    Space complexity: O(n²)
    """

    def predictTheWinner(self, nums: List[int]) -> bool:
        hashmap = {}

        def maxDiff(left, right):
            if left == right:
                return nums[left]
            if (left + 1, right) not in hashmap:
                hashmap[(left + 1, right)] = maxDiff(left + 1, right)
            score_by_left = nums[left] - hashmap[(left + 1, right)]
            if (left, right - 1) not in hashmap:
                hashmap[(left, right - 1)] = maxDiff(left, right - 1)
            score_by_right = nums[right] - maxDiff(left, right - 1)
            return max(score_by_left, score_by_right)

        return maxDiff(0, len(nums) - 1) >= 0


class Solution_Dynamic_Programming_Bottom_Up:
    """
    Time complexity: O(n²)
    Space complexity: O(n²)
    """

    def predictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        dp = [[0] * n for _ in range(n)]
        for i in range(n):
            dp[i][i] = nums[i]

        for diff in range(1, n):
            for left in range(n - diff):
                right = left + diff
                dp[left][right] = max(
                    nums[left] - dp[left + 1][right],
                    nums[right] - dp[left][right - 1],
                )

        return dp[0][n - 1] >= 0


class Solution_Dynamic_Programming_Bottom_Up_Space_Optimized:
    """
    Time complexity: O(n²)
    Space complexity: O(n)
    """

    def predictTheWinner(self, nums: List[int]) -> bool:
        n = len(nums)
        dp = nums[:]

        for diff in range(1, n):
            for left in range(n - diff):
                right = left + diff
                dp[left] = max(
                    nums[left] - dp[left + 1], nums[right] - dp[left]
                )

        return dp[0] >= 0
