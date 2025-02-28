from typing import List


class Solution:
    def minimumHealth(self, damage: List[int], armor: int) -> int:
        max_ = max(damage)
        sum_ = sum(damage)
        return sum_ - min(armor, max_) + 1


s = Solution()

# Test case 1: Expecting 13
damage = [2, 7, 4, 3]
armor = 4

# Test case 2: Expecting 10
damage = [2,5,3,4]
armor = 7

result = s.minimumHealth(damage, armor)
print(result)
