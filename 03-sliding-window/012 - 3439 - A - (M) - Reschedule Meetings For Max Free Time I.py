from typing import List


class Solution:
    def maxFreeTime(
        self, eventTime: int, k: int, startTime: List[int], endTime: List[int]
    ) -> int:
        n = len(startTime)
        left = 0
        right = eventTime if k == n else startTime[k]
        duration = sum(endTime[i] - startTime[i] for i in range(k))
        max_ = right - left - duration
        for i in range(k, n):
            duration += endTime[i] - startTime[i]
            duration -= endTime[i - k] - startTime[i - k]
            right = eventTime if i == n - 1 else startTime[i + 1]
            left = endTime[i - k]
            running_sum = right - left - duration
            max_ = max(max_, running_sum)
        return max_
