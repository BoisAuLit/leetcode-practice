"""LC-0930 - Binary Subarrays With Sum

Level 1 · 04 计数窗口 / 02 Exactly K 与 At Most K
题目在问：01 数组里，和**恰好**等于 goal 的子数组有多少个

决定性观察（本节最重要的恒等式）：
      **exactly(K) = atMost(K) - atMost(K-1)**
      「恰好」这个条件不满足单调性（窗口变长，和会越过 K 再也回不来），
      没法直接用一个窗口数出来；但「至多 K」是单调的，可以用标准计数窗口 O(n) 求出。
      两个「至多」相减，中间那一层就正好是「恰好」。

atMost(K) 的实现就是 LC-0713 的骨架：维护 `sum <= K` 的窗口，
      每个 right 贡献 `right - left + 1` 个合法子数组。

坑：
  - `atMost(-1)` 必须返回 0（goal 可以是 0，此时要算 `atMost(0) - atMost(-1)`）
  - 0/1 数组的和单调不减，所以窗口法成立；一般整数数组请用前缀和 + 哈希表
  - 前缀和解法（解法 2）更通用：它不要求元素非负，而且能推广到任意 target
"""

from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: atMost(goal) - atMost(goal - 1)
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：「恰好 K」类计数题的通解；992 换个 atMost 的定义就能照抄
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def numSubarraysWithSum(self, nums: List[int], goal: int) -> int:
        def at_most(k: int) -> int:
            if k < 0:
                return 0                 # ! goal = 0 时会用到，必须有
            left = 0
            cur = 0
            res = 0
            for right, x in enumerate(nums):
                cur += x
                while cur > k:
                    cur -= nums[left]
                    left += 1
                res += right - left + 1  # ! 以 right 结尾、和 <= k 的子数组个数
            return res
        return at_most(goal) - at_most(goal - 1)


##################################################################################################
##### ! Solution 2: 前缀和 + 哈希表（计数版的 LC-0560）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：★ 更通用 —— 不要求元素非负、不要求 0/1，任意整数数组和任意 target 都能用
##################################################################################################


class Solution_2:
    def numSubarraysWithSum(self, nums: List[int], goal: int) -> int:
        cnt = defaultdict(int)
        cnt[0] = 1                       # ! 空前缀哨兵
        pre = 0
        ans = 0
        for x in nums:
            pre += x
            ans += cnt[pre - goal]       # ! 前面每个 pre - goal 都和当前位置夹出一个解
            cnt[pre] += 1
        return ans


if __name__ == "__main__":
    import random
    cases = [([1, 0, 1, 0, 1], 2, 4), ([0, 0, 0, 0, 0], 0, 15), ([1], 1, 1),
             ([0], 0, 1), ([1, 1, 1], 0, 0)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for nums, g, want in cases:
            got = sol.numSubarraysWithSum(nums[:], g)
            assert got == want, f"{type(sol).__name__} {nums} goal={g}: got {got}, want {want}"
    rng = random.Random(930)
    for _ in range(3000):
        nums = [rng.randint(0, 1) for _ in range(rng.randint(0, 11))]
        g = rng.randint(0, 5)
        want = sum(1 for i in range(len(nums)) for j in range(i, len(nums))
                   if sum(nums[i:j + 1]) == g)
        for sol in sols:
            assert sol.numSubarraysWithSum(nums[:], g) == want, (type(sol).__name__, nums, g, want)
    print("2 个解法全过（含 3000 组随机对拍）")
