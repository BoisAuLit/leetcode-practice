from typing import List


class Solution:
    def minTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)
        last_finish = [0] * n  # 第 i 名巫师完成上一瓶药水的时间
        for m in mana:
            # 按题意模拟
            sum_t = 0
            for x, last in zip(skill, last_finish):
                # 每一次的 max 都是在使用木桶原理
                sum_t = max(sum_t, last)  # 手写 max
                sum_t += x * m
            # 倒推：如果酿造药水的过程中没有停顿，那么 last_finish[i] 应该是多少
            last_finish[-1] = sum_t
            for i in range(n - 2, -1, -1):
                last_finish[i] = last_finish[i + 1] - skill[i + 1] * m
        return last_finish[-1]


# # Test case 1: Expecting 110
# s = Solution()
# skill = [1, 5, 2, 4]
# mana = [5, 1, 4, 2]
# result = s.minTime(skill, mana)
# print(result)

# # Test case 2: Expecting 5
# s = Solution()
# skill = [1, 1]
# mana = [1, 2]
# result = s.minTime(skill, mana)
# print(result)

# # # Test case 3: Expecting 33
# s = Solution()
# skill = [1, 10, 1]
# mana = [2, 1]
# result = s.minTime(skill, mana)
# print(result)

# # Test case 4: Expecting
s = Solution()
skill = [1, 2, 1]
mana = [2, 1]
result = s.minTime(skill, mana)
print(result)
