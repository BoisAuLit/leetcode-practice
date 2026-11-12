"""LC-0901 - Online Stock Span

Level 1 · 01 最近更大元素与跨度 —— Previous Greater（左侧最近更大）的在线（Online）版本
题目在问：每来一个 price，返回「从今天往左连续回溯，有多少天的价格 <= 今天」（含今天）。

和 LC-0739 的关系（必须分清）：
  - Daily Temperatures：**未来的元素出现时，去解决过去元素的答案**（答案延迟产出）。
  - Online Stock Span：**当前元素出现时，立刻汇总过去的跨度**（答案当场产出）。
  两者用的是同一个单调栈骨架，但「谁解决谁」的方向相反。

决定性观察：
  1. span 的边界就是**左侧第一个严格大于今天的价格**那一天。
     span = 今天下标 - 那一天的下标；没有这样的一天就是 今天下标 + 1。
  2. 关键的压缩（Compression）：那些已经被今天“吃掉”的历史日子，
     以后**永远不可能单独作为谁的边界** —— 因为今天比它们都高，今天会先挡住。
     所以可以把它们合并进今天的 span，直接从栈里删掉。
  3. 于是栈里存 `(price, span)`：span 表示「这个价格代表了它自己 + 被它吞掉的那一段」。

Pop 条件：`stack[-1].price <= price` —— **用 <=，不是 <**。
      题目要的是「价格 <= 今天」都算进跨度，所以等值的历史日子必须被吞掉。
      （对比 LC-0739 要的是「严格更高的温度」，那里用的是严格不等号。）

为什么可以不逐个重新比较历史：被吞掉的那些天已经把自己的 span 交给了今天，
      信息没有丢失，只是换了持有者。这就是把一段连续区间压成一个栈元素。

复杂度（这里很容易说错）：
      单次 next() 最坏 O(n)（一口气弹空整个栈）。
      但每个 (price, span) 只会入栈一次、出栈一次，
      所以 n 次调用总共 O(n)，**摊还（Amortized）O(1)**。
      不能不加说明地声称「每次调用都是 O(1)」。
      空间 O(n)（严格递减的输入会让栈一直涨）。

边界：
  - 价格严格递减 [80,70,60] → span 全是 1（栈一直涨到 n）
  - 价格严格递增 [10,20,30] → span 1,2,3（每次把栈弹空）
  - 全部相等   [5,5,5]      → span 1,2,3（<= 所以等值被吞）
"""

from typing import List, Tuple


##################################################################################################
##### ! Solution 1: 单调递减栈，存 (price, span) 聚合状态
##### ! 时间复杂度: 单次最坏 O(n)，n 次调用总计 O(n) → 摊还 O(1)   空间复杂度: O(n)
##### ! 适用：流式（Online）求「左侧连续满足条件的长度」；Previous Greater 的标准写法
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class StockSpanner_1:
    def __init__(self) -> None:
        self.stack: List[Tuple[int, int]] = []   # ! (price, span)，price 从栈底到栈顶严格递减

    def next(self, price: int) -> int:
        span = 1                                  # ! 今天自己算 1 天
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]           # ! 把被吞掉那段的 span 接管过来（<= 所以等值也吞）
        self.stack.append((price, span))
        return span


##################################################################################################
##### ! Solution 2: 单调递减「索引栈」+ 单独保存所有价格（和 LC-0739 的模板完全同形）
##### ! 时间复杂度: 摊还 O(1)   空间复杂度: O(n)
##### ! 适用：想把 496/739/901 统一成一个「存下标」的模板来记时用这版
##################################################################################################


class StockSpanner_2:
    def __init__(self) -> None:
        self.prices: List[int] = []
        self.stack: List[int] = []     # ! 存下标，对应价格严格递减

    def next(self, price: int) -> int:
        self.prices.append(price)
        i = len(self.prices) - 1
        while self.stack and self.prices[self.stack[-1]] <= price:
            self.stack.pop()
        # ! 栈顶（若存在）就是左侧第一个严格大于 price 的那天
        span = i - self.stack[-1] if self.stack else i + 1
        self.stack.append(i)
        return span


##################################################################################################
##### ! Solution 3: 暴力 —— 每次往左一天天数（基准答案，用来对拍）
##### ! 时间复杂度: 单次 O(n)，总计 O(n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照
##################################################################################################


class StockSpanner_3:
    def __init__(self) -> None:
        self.prices: List[int] = []

    def next(self, price: int) -> int:
        self.prices.append(price)
        span = 0
        for p in reversed(self.prices):
            if p > price:
                break
            span += 1
        return span


if __name__ == "__main__":
    import random

    cases = [
        [100, 80, 60, 70, 60, 75, 85],   # LeetCode 官方样例 → 1,1,1,2,1,4,6
        [80, 70, 60],
        [10, 20, 30],
        [5, 5, 5],
        [31, 41, 48, 59, 79],
    ]
    for prices in cases:
        a, b, c = StockSpanner_1(), StockSpanner_2(), StockSpanner_3()
        out = [a.next(p) for p in prices]
        assert out == [b.next(p) for p in prices] == [c.next(p) for p in prices]
        print(f"{prices} -> {out}")

    for _ in range(300):                 # ! 随机对拍，重点覆盖重复价格
        prices = [random.randint(1, 6) for _ in range(random.randint(1, 20))]
        a, b, c = StockSpanner_1(), StockSpanner_2(), StockSpanner_3()
        assert [a.next(p) for p in prices] == [b.next(p) for p in prices] == [c.next(p) for p in prices]
    print("随机对拍 300 组通过 ✓")
