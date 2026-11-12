"""LC-0398 - Random Pick Index

Level 1 · 03 Randomized Data Structures → Level 2 · 02 加权随机、蓄水池采样与洗牌

题目在问：数组里可能有重复，`pick(target)` 要在**所有等于 target 的下标**里等概率返回一个。
题目明说「数组很大，尽量不要用额外空间」—— 这就是在点名蓄水池采样。

### 和 LC-0382 是同一个算法，只是「流」变成了「过滤后的流」

扫一遍数组，只把 `nums[i] == target` 的位置当成流里的元素；
看到第 k 个匹配时，以 1/k 的概率把答案换成 i。证明和 LC-0382 一字不差：P(每个匹配留下) = 1/k_total。

### 三种解法对应三种内存假设

| | 预处理 | pick | 空间 | 什么时候选它 |
|---|---|---|---|---|
| 蓄水池 | 0 | O(n) | **O(1)** | 题目要求的 —— 数组大、pick 次数少 |
| 哈希表 value → [下标] | O(n) | O(1) | O(n) | pick 调用极多、内存够 |
| 两遍扫描（先数后挑） | 0 | O(n) | O(1) | 想避开随机数被反复调用；本质上和蓄水池一样是常数空间 |
"""
from collections import Counter, defaultdict
from typing import List
import random


##################################################################################################
##### ! Solution 1: 蓄水池采样（对「等于 target 的下标」这条子流采样）
##### ! 时间复杂度: 初始化 O(1)，每次 pick O(n)   空间复杂度: O(1)
##### ! 适用：题目点名的解法。不存任何索引表，一遍扫描、常数空间
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def pick(self, target: int) -> int:
        ans, k = -1, 0
        for i, x in enumerate(self.nums):
            if x != target:
                continue
            k += 1                                   # ! 这是第 k 个匹配
            if random.randint(1, k) == 1:            # ! 以 1/k 概率替换
                ans = i
        return ans


##################################################################################################
##### ! Solution 2: 哈希表预存每个值的所有下标
##### ! 时间复杂度: 初始化 O(n)，每次 pick O(1)   空间复杂度: O(n)
##### ! 适用：pick 调用次数远大于 n、且内存不是瓶颈。面试里要主动说出它违背了题目的空间提示
##################################################################################################


class Solution_2:
    def __init__(self, nums: List[int]):
        self.pos = defaultdict(list)
        for i, x in enumerate(nums):
            self.pos[x].append(i)

    def pick(self, target: int) -> int:
        return random.choice(self.pos[target])


##################################################################################################
##### ! Solution 3: 两遍扫描 —— 先数有几个匹配，再随机挑第 r 个
##### ! 时间复杂度: 每次 pick O(n)   空间复杂度: O(1)
##### ! 适用：想只调一次随机数（蓄水池每个匹配都要调一次 random）；
#####         代价是扫两遍，而且它不是单遍流式算法
##################################################################################################


class Solution_3:
    def __init__(self, nums: List[int]):
        self.nums = nums

    def pick(self, target: int) -> int:
        total = sum(1 for x in self.nums if x == target)
        r = random.randint(1, total)                 # ! 要第 r 个匹配
        for i, x in enumerate(self.nums):
            if x == target:
                r -= 1
                if r == 0:
                    return i
        return -1


if __name__ == "__main__":
    random.seed(398)
    nums = [1, 2, 3, 3, 3]
    N = 60000
    for cls in (Solution_1, Solution_2, Solution_3):
        obj = cls(nums)
        cnt = Counter(obj.pick(3) for _ in range(N))
        assert set(cnt) == {2, 3, 4}, (cls.__name__, cnt)
        freq = [cnt[i] / N for i in (2, 3, 4)]
        assert all(abs(f - 1 / 3) < 0.01 for f in freq), (cls.__name__, freq)
        assert obj.pick(1) == 0                      # ! 唯一匹配必须被返回
        print(f"{cls.__name__:12s} pick(3) 频率 {[round(f, 3) for f in freq]}")
    print("所有测试通过 ✓")
