from typing import List


class Solution:
    def goodDaysToRobBank(self, security: List[int], time: int) -> List[int]:
        streaks = [[0, 0] for i in range(len(security))]

        left_streak = 0
        right_streak = 0
        for i in range(1, len(security)):
            if security[i] <= security[i - 1]:
                left_streak += 1
                streaks[i][0] = left_streak
            else:
                left_streak = 0

            r = len(security) - 1 - i
            if security[r] <= security[r + 1]:
                right_streak += 1
                streaks[r][1] = right_streak
            else:
                right_streak = 0

        result = []
        for i in range(time, len(security) - time):
            left, right = streaks[i]
            if left >= time and right >= time:
                result.append(i)
        return result


s = Solution()

# Test case 1: Expecting [2, 3]
security = [5, 3, 3, 3, 5, 6, 2]
time = 2


result = s.goodDaysToRobBank(security, time)
print(result)
