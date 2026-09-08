"""
📌 信号→模式: 分成 k 张连续的顺子 → 计数 + 从最小牌批量扣除 k 张连续
📅 首次: 2026-09-04 | 卡点: （待补） | 守卫: （待补）
🔁 复习: 未排期
"""
from typing import List
from collections import Counter


class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False
        counter = Counter(hand)
        for num in sorted(counter):  # 只对去重后的值排序
            count = counter[num]
            if count == 0:
                continue

            """
            倘若一开始的最小值的 count 是 > 1 的, 那么对于所有其后的值都必须批量删除
            """
            for currNum in range(num, num + groupSize):
                if counter[currNum] < count:
                    return False
                counter[currNum] -= count
        return True


s = Solution()
hand = [1, 2, 4, 2, 3, 5, 3, 4]
groupSize = 4
result = s.isNStraightHand(hand, groupSize)
print(result)
