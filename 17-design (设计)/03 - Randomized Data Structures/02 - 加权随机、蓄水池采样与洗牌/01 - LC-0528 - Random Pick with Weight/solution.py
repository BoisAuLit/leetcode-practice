"""LC-0528 - Random Pick with Weight

Level 1 · 03 Randomized Data Structures → Level 2 · 02 加权随机、蓄水池采样与洗牌

题目在问：给 `w[i]`，设计 `pickIndex()`，使下标 `i` 被选中的概率 = `w[i] / sum(w)`。
Meta / Google 常年高频，面试里的追问几乎固定：**「调用次数远多于初始化次数，怎么优化？」**

### 核心变换：把「按权重抽」变成「在数轴上扔一个点」

把权重首尾相接铺在数轴上：`w = [1, 3, 2]` → 区间 `[0,1) [1,4) [4,6)`，总长 6。
在 `[0, 6)` 里均匀地扔一个点，它落进哪段，就选哪个下标 —— 落进第 i 段的概率正好是 `w[i]/6`。

    前缀和 prefix = [1, 4, 6]
    随机整数 t ∈ [1, 6]   →  找第一个 prefix[j] >= t 的 j   （bisect_left）
    t=1 → 0   t=2,3,4 → 1   t=5,6 → 2       各下标命中次数 1 : 3 : 2 ✓

### 两个容易写错的地方

1. **随机数的范围和二分的开闭必须配套**。用 `randint(1, total)`（闭区间）就配 `bisect_left`；
   用 `random() * total`（`[0, total)` 浮点）就配 `bisect_right`。混用会让 `w[i] = 0` 的下标被选到，
   或者让最后一个下标永远选不到。
2. 前缀和在 `__init__` 里算一次就够了，`pickIndex` 只做一次二分 —— 这就是追问要的答案。
"""
from bisect import bisect_left, bisect_right
from collections import Counter
from itertools import accumulate
from typing import List
import random


##################################################################################################
##### ! Solution 1: 前缀和 + 二分（面试标准答案）
##### ! 时间复杂度: 初始化 O(n)，每次 pickIndex O(log n)   空间复杂度: O(n)
##### ! 适用：pickIndex 调用次数 ≫ n 的场景（题目的限制就是这样设的，10^4 次调用）
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self, w: List[int]):
        self.prefix = list(accumulate(w))      # ! prefix[i] = w[0] + ... + w[i]，严格递增（w[i] >= 1）
        self.total = self.prefix[-1]

    def pickIndex(self) -> int:
        t = random.randint(1, self.total)      # ! 闭区间 [1, total]，配 bisect_left
        return bisect_left(self.prefix, t)     # ! 第一个 prefix >= t 的位置


##################################################################################################
##### ! Solution 2: 浮点随机数 + bisect_right（同一个思路的另一种开闭配对）
##### ! 时间复杂度: 初始化 O(n)，每次 O(log n)   空间复杂度: O(n)
##### ! 适用：权重是浮点数（概率而不是整数权重）时只能这么写；整数权重时和 Solution_1 等价。
#####         random() ∈ [0, 1) → t ∈ [0, total)，落在 [prefix[j-1], prefix[j]) 就选 j，所以用 bisect_right
##################################################################################################


class Solution_2:
    def __init__(self, w: List[int]):
        self.prefix = list(accumulate(w))
        self.total = self.prefix[-1]

    def pickIndex(self) -> int:
        t = random.random() * self.total       # ! 半开区间 [0, total)
        return bisect_right(self.prefix, t)    # ! 第一个 prefix > t 的位置


##################################################################################################
##### ! Solution 3: 线性扫描（不预处理的写法，面试里只配做「第一版」）
##### ! 时间复杂度: 初始化 O(1)，每次 pickIndex O(n)   空间复杂度: O(1)（不算输入）
##### ! 适用：n 很小或者只 pick 一两次。面试官追问「调用 10^4 次」时就该升级到 Solution_1
##################################################################################################


class Solution_3:
    def __init__(self, w: List[int]):
        self.w = w
        self.total = sum(w)

    def pickIndex(self) -> int:
        t = random.randint(1, self.total)
        for i, x in enumerate(self.w):         # ! 一边减一边走，减到 <= 0 就是落点
            t -= x
            if t <= 0:
                return i
        return len(self.w) - 1                 # ! 理论上到不了这里（t <= total）


##################################################################################################
##### ! Solution 4: 展开成「每个下标重复 w[i] 次」的数组再均匀抽（反面教材）
##### ! 时间复杂度: 初始化 O(Σw)，每次 O(1)   空间复杂度: O(Σw)
##### ! 适用：只用来说明为什么不能这样 —— w[i] 最大 10^5、n 最大 10^4，数组会到 10^9
##################################################################################################


class Solution_4:
    def __init__(self, w: List[int]):
        self.bag = [i for i, x in enumerate(w) for _ in range(x)]

    def pickIndex(self) -> int:
        return random.choice(self.bag)


if __name__ == "__main__":
    random.seed(528)
    w = [1, 3, 2]
    N = 60000
    for cls in (Solution_1, Solution_2, Solution_3, Solution_4):
        obj = cls(w)
        cnt = Counter(obj.pickIndex() for _ in range(N))
        freq = [cnt[i] / N for i in range(len(w))]
        expect = [x / sum(w) for x in w]
        # ! 60000 次抽样，每个频率和理论值的偏差应该在 1% 以内（标准差 ≈ sqrt(p(1-p)/N) < 0.003）
        assert all(abs(a - b) < 0.01 for a, b in zip(freq, expect)), (cls.__name__, freq, expect)
        print(f"{cls.__name__:12s} 频率 {[round(f, 3) for f in freq]}  理论 {[round(e, 3) for e in expect]}")

    # ! 边界：只有一个元素时永远返回 0；权重全相同时就是均匀分布
    assert all(Solution_1([7]).pickIndex() == 0 for _ in range(100))
    assert set(Solution_1([2, 2, 2]).pickIndex() for _ in range(2000)) == {0, 1, 2}

    # ! 开闭配对的确定性检查：把随机数钉住，验证 bisect_left 的落点
    s = Solution_1(w)
    for t, want in [(1, 0), (2, 1), (3, 1), (4, 1), (5, 2), (6, 2)]:
        assert bisect_left(s.prefix, t) == want, (t, want)
    print("所有测试通过 ✓")
