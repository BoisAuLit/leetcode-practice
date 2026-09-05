from typing import List


class Solution:
    def maxFreeTime(
        self, eventTime: int, startTime: List[int], endTime: List[int]
    ) -> int:
        n = len(startTime)

        max_l = [0] * n
        max_l[0] = startTime[0]
        for i in range(1, n):
            max_l[i] = max(max_l[i - 1], startTime[i] - endTime[i - 1])

        max_r = [0] * n
        max_r[-1] = eventTime - endTime[-1]
        for i in range(n - 2, -1, -1):
            max_r[i] = max(max_r[i + 1], startTime[i + 1] - endTime[i])

        max_ = 0
        for i in range(n):
            slot_l = max_l[i - 1] if i >= 1 else 0
            slot_r = max_r[i + 1] if i <= n - 2 else 0
            duration = endTime[i] - startTime[i]
            next_s = startTime[i + 1] if i <= n - 2 else eventTime
            prev_e = endTime[i - 1] if i >= 1 else 0
            if slot_l >= duration or slot_r >= duration:
                max_ = max(max_, next_s - prev_e)
            else:
                max_ = max(max_, next_s - prev_e - duration)
        return max_


# # Test case 1: Expecting 7
# s = Solution()
# eventTime = 10
# startTime = [0, 7, 9]
# endTime = [1, 8, 10]
# result = s.maxFreeTime(eventTime, startTime, endTime)
# print(result)

# Test case 2: Expecting 6
s = Solution()
eventTime = 10
startTime = [0, 3, 7, 9]
endTime = [1, 4, 8, 10]
result = s.maxFreeTime(eventTime, startTime, endTime)
print(result)
