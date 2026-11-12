"""LC-0229 - Majority Element II

Level 1 · 02 Frequency Counting 与 Top K —— Boyer-Moore 投票法的推广
题目在问：找出所有出现次数 > ⌊n/3⌋ 的元素。要求 O(n) 时间、O(1) 额外空间

核心观察：出现次数 > n/3 的元素**最多只有 2 个**（3 个就超过 n 了）。
      169（> n/2，最多 1 个）用 1 组「候选 + 计数」；这题就用 2 组。
      推广规律：要找出现次数 > n/k 的元素，维护 k-1 组候选即可。

不变量（这是 Boyer-Moore 的灵魂，必须能讲）：
      把「一个候选 1 和两个不同的数」看成一次**三消**，三消不改变
      「某个数出现次数 > n/3」这个事实（真正的多数元素消不光）。
      所以扫完一遍留下的候选是**仅有的可能答案**，但不保证真的达标 ——
      **必须第二遍扫描数数验证**。这一步不能省，169 可以省是因为题目保证答案存在。

坑：
  - 三个 if 的顺序不能乱：**先判「等于已有候选」，再判「有空位」，最后才一起减**
    顺序写反时，第二个候选会把第一个挤掉
  - 两个候选初始值不能都设成同一个数（比如都是 0），否则同一个数会占两个位置
  - 必须有第二遍验证；`[1,2]` 这种答案不足 2 个的情况全靠它过滤
"""

from collections import Counter
from typing import List


##################################################################################################
##### ! Solution 1: Boyer-Moore 投票法，两组候选 + 第二遍验证
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：> n/k 的众数问题通解（k-1 组候选）；O(1) 空间是它存在的唯一理由
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def majorityElement(self, nums: List[int]) -> List[int]:
        cand1 = cand2 = None
        cnt1 = cnt2 = 0
        for x in nums:
            # ! 顺序：先认领已有候选 → 再占空位 → 都不是才三消
            if cand1 is not None and x == cand1:
                cnt1 += 1
            elif cand2 is not None and x == cand2:
                cnt2 += 1
            elif cnt1 == 0:
                cand1, cnt1 = x, 1
            elif cnt2 == 0:
                cand2, cnt2 = x, 1
            else:
                cnt1 -= 1  # ! 三消：x 和两个候选各抵消一次
                cnt2 -= 1
                if cnt1 == 0:
                    cand1 = None
                if cnt2 == 0:
                    cand2 = None
        # ! 第二遍验证：投票只保证「答案一定在候选里」，不保证候选一定是答案
        need = len(nums) // 3
        return [c for c in (cand1, cand2)
                if c is not None and sum(1 for x in nums if x == c) > need]


##################################################################################################
##### ! Solution 2: Counter 直接数
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：★ 工程里就写这个，三行可读性最好；面试只有在要求 O(1) 空间时才必须换解法 1
##################################################################################################


class Solution_2:
    def majorityElement(self, nums: List[int]) -> List[int]:
        need = len(nums) // 3
        return [v for v, c in Counter(nums).items() if c > need]


if __name__ == "__main__":
    import random
    cases = [([3, 2, 3], [3]), ([1], [1]), ([1, 2], [1, 2]),
             ([2, 2], [2]), ([1, 1, 1, 3, 3, 2, 2, 2], [1, 2]), ([], [])]
    for sol in (Solution_1(), Solution_2()):
        for nums, want in cases:
            got = sorted(sol.majorityElement(nums[:]))
            assert got == sorted(want), f"{type(sol).__name__} {nums}: got {got}, want {want}"
    rng = random.Random(229)
    for _ in range(5000):  # ! 随机对拍，专打「候选顺序」和「验证」两个坑
        nums = [rng.randint(0, 4) for _ in range(rng.randint(0, 12))]
        want = sorted(Solution_2().majorityElement(nums[:]))
        assert sorted(Solution_1().majorityElement(nums[:])) == want, nums
    print("2 个解法全过（含 5000 组随机对拍）")
