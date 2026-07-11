import bisect
from typing import List


class Solution:
    def maxFrequency(self, nums: List[int], k: int, numOperations: int) -> int:
        nums.sort()
        res = 0
        freqs = {}
        prev_i = 0
        for i in range(len(nums)):
            if nums[i] != nums[prev_i]:
                freq = i - prev_i
                freqs[nums[prev_i]] = freq
                res = max(res, freq)
                prev_i = i

        freq = len(nums) - prev_i
        freqs[nums[prev_i]] = freq
        res = max(res, freq)

        for i in range(nums[0], nums[-1] + 1):
            l = bisect.bisect_left(nums, i - k)
            r = bisect.bisect_right(nums, i + k) - 1

            freq = min(r - l + 1, numOperations + freqs.get(i, 0))
            res = max(res, freq)

        return res
