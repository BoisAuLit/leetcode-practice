"""LC-0384 - Shuffle an Array

Level 1 · 03 Randomized Data Structures → Level 2 · 02 加权随机、蓄水池采样与洗牌

题目在问：实现 `shuffle()`，使 n! 种排列**等概率**出现；`reset()` 回到原数组。

### Fisher–Yates（Knuth shuffle）：为什么它是均匀的

    for i in range(n - 1, 0, -1):
        j = randint(0, i)          # ! j 可以等于 i（元素留在原地也是一种选择）
        swap(a[i], a[j])

第 n−1 位从 n 个候选里选，第 n−2 位从剩下 n−1 个里选，…… 总共 n·(n−1)·…·1 = n! 条等概率路径，
每条路径对应**恰好一种**排列 ⟹ 每种排列的概率都是 1/n!。

### 面试里最常见的两个错误写法（都不均匀）

1. `j = randint(0, n - 1)`（每次都在**全范围**随机，而不是 `[0, i]`）：
   总路径 nⁿ 条，但 nⁿ 不能被 n! 整除，所以排列不可能等概率。n=3 时 27 条路径分给 6 种排列，有的拿 4 条有的拿 5 条。
2. `sorted(a, key=lambda _: random())` 之类的「随机 key 排序」：
   正确但 O(n log n)，而且比较排序 + 随机 key 在面试里说不清概率。

本文件的 `Solution_3` 把错误写法 1 实现出来并用统计检验**证明它偏了** —— 这是说服面试官的最直接方式。
"""
from collections import Counter
from typing import List
import random


##################################################################################################
##### ! Solution 1: Fisher–Yates / Knuth shuffle（原地、从后往前）
##### ! 时间复杂度: shuffle O(n)，reset O(n)（拷贝一份）   空间复杂度: O(n)（必须保存原数组给 reset）
##### ! 适用：面试标准答案。随机范围是 [0, i] 而不是 [0, n-1]，这是均匀性的全部所在
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self, nums: List[int]):
        self.original = nums[:]                      # ! reset 要用，必须拷一份
        self.arr = nums[:]

    def reset(self) -> List[int]:
        self.arr = self.original[:]
        return self.arr

    def shuffle(self) -> List[int]:
        a = self.arr
        for i in range(len(a) - 1, 0, -1):
            j = random.randint(0, i)                 # ! 闭区间 [0, i]，含 i 本身
            a[i], a[j] = a[j], a[i]
        return a


##################################################################################################
##### ! Solution 2: 「从袋子里不放回地抽」—— Fisher–Yates 的直觉版（非原地）
##### ! 时间复杂度: O(n²)（list.pop(k) 是 O(n)）   空间复杂度: O(n)
##### ! 适用：讲清楚「为什么是 n! 条等概率路径」时最好懂的版本；写代码时应升级成 Solution_1
##################################################################################################


class Solution_2:
    def __init__(self, nums: List[int]):
        self.original = nums[:]
        self.arr = nums[:]

    def reset(self) -> List[int]:
        self.arr = self.original[:]
        return self.arr

    def shuffle(self) -> List[int]:
        bag, out = self.arr[:], []
        while bag:
            out.append(bag.pop(random.randrange(len(bag))))   # ! 每次从剩余元素里等概率拿一个
        self.arr = out
        return out


##################################################################################################
##### ! Solution 3: ❌ 错误写法 —— 每次都在全范围 [0, n-1] 里随机交换（反面教材）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：只用于演示它**不均匀**。n=3 时 27 条路径分给 6 种排列，分不平；
#####         下面的测试用卡方统计量把这个偏差量化出来
##################################################################################################


class Solution_3:
    def __init__(self, nums: List[int]):
        self.original = nums[:]
        self.arr = nums[:]

    def reset(self) -> List[int]:
        self.arr = self.original[:]
        return self.arr

    def shuffle(self) -> List[int]:
        a, n = self.arr, len(self.arr)
        for i in range(n):
            j = random.randint(0, n - 1)             # ! 错在这里：范围没有随 i 收缩
            a[i], a[j] = a[j], a[i]
        return a


def chi_square(counts: Counter, trials: int, k: int) -> float:
    """k 种结果等概率时的卡方统计量；自由度 k-1。"""
    e = trials / k
    return sum((c - e) ** 2 / e for c in counts.values()) + (k - len(counts)) * e


if __name__ == "__main__":
    random.seed(384)
    nums, N = [1, 2, 3], 60000                       # ! 3! = 6 种排列
    for cls in (Solution_1, Solution_2):
        obj = cls(nums)
        cnt = Counter(tuple((obj.reset(), obj.shuffle())[1]) for _ in range(N))   # ! 每次都从原数组出发洗一次
        obj.reset()
        assert len(cnt) == 6 and obj.arr == nums
        chi = chi_square(cnt, N, 6)
        assert chi < 20, (cls.__name__, chi)          # ! 自由度 5 的卡方 99.9% 分位点是 20.5；均匀的话几乎不会超过
        print(f"{cls.__name__:12s} 6 种排列的频率 {sorted(round(c / N, 3) for c in cnt.values())}  χ² = {chi:.1f}（均匀）")

    bad = Solution_3(nums)
    # ! 必须每次 reset 再 shuffle：对一个已经打乱的数组反复乱交换，偏差会被「洗」掉，看不出错误
    cnt = Counter(tuple((bad.reset(), bad.shuffle())[1]) for _ in range(N))
    chi = chi_square(cnt, N, 6)
    assert chi > 100, chi                             # ! 理论上 4/27 vs 5/27 的差距在 60000 次里会给出几百的 χ²
    print(f"{'Solution_3':12s} 6 种排列的频率 {sorted(round(c / N, 3) for c in cnt.values())}  χ² = {chi:.1f}（❌ 明显不均匀：理论 4/27≈0.148 与 5/27≈0.185 两档）")

    # ! reset 必须返回原顺序，而且不受之前 shuffle 的影响
    s = Solution_1([5, 6, 7, 8])
    s.shuffle(); s.shuffle()
    assert s.reset() == [5, 6, 7, 8]
    assert sorted(s.shuffle()) == [5, 6, 7, 8]       # ! shuffle 是排列：元素集合不变
    print("所有测试通过 ✓")
