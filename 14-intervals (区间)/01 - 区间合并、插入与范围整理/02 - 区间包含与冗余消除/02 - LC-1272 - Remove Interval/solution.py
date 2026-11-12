"""LC-1272 - Remove Interval     ★ 第二轮审核新增（填补「区间差集 / Subtraction」缺口）

Level 1 · 01 区间合并、插入与范围整理 —— **区间减法：本专题唯一的「减」**
题目在问：`intervals` 是**已排序、互不相交**的半开区间列表 `[a, b)`，
         `toBeRemoved = [c, d)`。返回**集合差** `intervals \\ toBeRemoved`
         （仍然排序、互不相交，去掉空区间）。

### 本章四道题凑成一套完整的区间代数

| 题 | 运算 | 一句话 |
|---|---|---|
| [LC-0056](<../../01 - 标准区间合并与插入/01 - LC-0056 - Merge Intervals>) | **并集（自身）** | 把相交的合起来 |
| [LC-0057](<../../01 - 标准区间合并与插入/02 - LC-0057 - Insert Interval>) | **并集（加一个）** | 插入并合并 |
| [LC-1288](<../01 - LC-1288 - Remove Covered Intervals>) | **包含关系** | 删掉被覆盖的 |
| **LC-1272** 本题 | **差集（减一个）** | 从每段里挖掉 `[c,d)` |

> 57 是加法，**1272 是减法**；合起来才算把「区间作为集合」这件事学完。

### 对单个区间 `[a, b)` 减去 `[c, d)` 的四种形态（整道题就这张表）

```
情况              图示                       输出
① 不相交         [a,b) ... [c,d)            [a,b)          原样保留
② 被完全吃掉     c <= a 且 b <= d           （无）          整段消失
③ 挖中间         a < c 且 d < b             [a,c) 和 [d,b)  **裂成两段**
④ 切掉一边       只重叠左半 / 右半           [d,b) / [a,c)   留一段
```

统一成两行代码，**不用分四种情况写 if**：
```python
if a < c:  res.append([a, min(b, c)])     # ! 左边剩下的那块
if d < b:  res.append([max(a, d), b])     # ! 右边剩下的那块
```
- 情况① 会自然落到其中一行并输出完整区间（因为 `min(b,c)==b` 或 `max(a,d)==a`）
- 情况② 两个条件都不成立 ⟹ 什么都不输出
- 情况③ 两行都成立 ⟹ **一个区间变两个**，这是本题唯一需要留神的地方
- 情况④ 恰好一行成立

**为什么不等号都是严格 `<`？**
半开区间 `[a, b)` 的长度是 `b - a`；`a < c` 保证 `[a, min(b,c))` 非空。
写成 `<=` 会吐出 `[x, x)` 这样的空区间。
**半开区间里「端点相接」永远不算重叠**：`[1,2)` 减 `[2,3)` 结果仍是 `[1,2)`。

**为什么输出天然有序、天然不相交？**
输入已排序不相交，而每段的输出都落在该段原范围内，
段内先 `[a, min(b,c))` 再 `[max(a,d), b)` 也是左→右 ⟹ 顺序和不相交性都被继承。∎

**为什么不需要排序/合并？** 差集只会让区间变小或变碎，不会产生新的相交。
这和 LC-0057（插入会引发合并）正好相反。

**能不能提前退出？** 可以：`intervals` 有序，一旦 `a >= d` 之后的区间都不受影响，
可以直接把剩余部分 `extend` 进结果（解法 2 用了这个优化）。

复杂度：**O(n)** 时间、O(n) 输出空间（最坏裂成 n+1 段）。
       输入已排序，所以**不需要 O(n log n)**。

边界：
  - 挖中间裂成两段：`[[0,5]]` 减 `[2,3]` → `[[0,2],[3,5]]`
  - 整段被吃：`[[1,2]]` 减 `[0,5]` → `[]`
  - 完全不相交：`[[0,1]]` 减 `[5,6]` → `[[0,1]]`
  - 端点相接：`[[1,2]]` 减 `[2,3]` → `[[1,2]]`（半开，不重叠）
  - 刚好等于：`[[1,2]]` 减 `[1,2]` → `[]`
  - 空输入 → `[]`
"""

from typing import List


##################################################################################################
##### ! Solution 1: 逐段做区间减法，左右两块各判一次（两行覆盖全部四种形态）
##### ! 时间复杂度: O(n)   空间复杂度: O(n) 输出
##### ! 适用：所有「区间差集」问题的标准写法；记住 a < c / d < b 这两行就够
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def removeInterval(
        self, intervals: List[List[int]], toBeRemoved: List[int]
    ) -> List[List[int]]:
        c, d = toBeRemoved
        res: List[List[int]] = []
        for a, b in intervals:
            if a < c:
                res.append([a, min(b, c)])        # ! 左残块：从 a 到「被挖起点」或自己的终点
            if d < b:
                res.append([max(a, d), b])        # ! 右残块：从「被挖终点」或自己的起点 到 b
        return res


##################################################################################################
##### ! Solution 2: 三段式 + 提前退出（利用输入有序，整段不相交的直接搬）
##### ! 时间复杂度: O(n)（命中段数少时常数更小）   空间复杂度: O(n) 输出
##### ! 适用：n 很大而 toBeRemoved 只压到少数几段时；也更贴近「扫过去」的直觉
##################################################################################################


class Solution_2:
    def removeInterval(
        self, intervals: List[List[int]], toBeRemoved: List[int]
    ) -> List[List[int]]:
        c, d = toBeRemoved
        res: List[List[int]] = []
        i, n = 0, len(intervals)
        # ! 第一段：整段在 [c,d) 左边（b <= c），原样搬
        while i < n and intervals[i][1] <= c:
            res.append(intervals[i][:])
            i += 1
        # ! 第二段：和 [c,d) 有交集的那些，做减法
        while i < n and intervals[i][0] < d:
            a, b = intervals[i]
            if a < c:
                res.append([a, c])
            if d < b:
                res.append([d, b])
            i += 1
        # ! 第三段：整段在 [c,d) 右边（a >= d），后面全都不受影响 ⟹ 一次搬完
        res.extend(x[:] for x in intervals[i:])
        return res


##################################################################################################
##### ! Solution 3: 暴力基准（在单位段上做集合差，用于对拍）
##### ! 时间复杂度: O(V)   空间复杂度: O(V)
##### ! 适用：仅用于对拍。直接把「集合差」这个定义写成代码
##################################################################################################


class Solution_3:
    def removeInterval(
        self, intervals: List[List[int]], toBeRemoved: List[int]
    ) -> List[List[int]]:
        if not intervals:
            return []
        c, d = toBeRemoved
        lo = min(a for a, _ in intervals)
        hi = max(b for _, b in intervals)
        keep = set()
        for a, b in intervals:
            for t in range(a, b):                 # ! 半开 ⟹ 单位段 [t, t+1)
                keep.add(t)
        for t in range(c, d):
            keep.discard(t)
        res: List[List[int]] = []
        t = lo
        while t < hi:
            if t in keep:
                j = t
                while j < hi and j in keep:
                    j += 1
                res.append([t, j])
                t = j
            else:
                t += 1
        return res


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert s.removeInterval([[0, 2], [3, 4], [5, 7]], [1, 6]) == [[0, 1], [6, 7]]
        assert s.removeInterval([[0, 5]], [2, 3]) == [[0, 2], [3, 5]]   # ! 裂成两段
        assert s.removeInterval([[-5, -4], [-3, -2], [1, 2], [3, 5], [8, 9]], [-1, 4]) == [
            [-5, -4], [-3, -2], [4, 5], [8, 9],
        ]
        assert s.removeInterval([[1, 2]], [0, 5]) == []                 # ! 整段被吃
        assert s.removeInterval([[0, 1]], [5, 6]) == [[0, 1]]           # ! 不相交
        assert s.removeInterval([[1, 2]], [2, 3]) == [[1, 2]]           # ! 半开，端点相接不重叠
        assert s.removeInterval([[1, 2]], [1, 2]) == []                 # ! 刚好等于
        assert s.removeInterval([], [1, 2]) == []

    print([[0, 5]], "减", [2, 3], "->", Solution_1().removeInterval([[0, 5]], [2, 3]))
    print([[0, 2], [3, 4], [5, 7]], "减", [1, 6], "->",
          Solution_1().removeInterval([[0, 2], [3, 4], [5, 7]], [1, 6]))

    # ! 相邻区间「首尾相接」的情形单位段暴力表示不了（[4,6],[6,7] 会被它并成 [4,7]），
    #   所以这类用例单独验，随机对拍里让区间之间至少留 1 的空隙。
    assert Solution_1().removeInterval([[4, 6], [6, 7]], [12, 14]) == [[4, 6], [6, 7]]
    assert Solution_2().removeInterval([[4, 6], [6, 7]], [12, 14]) == [[4, 6], [6, 7]]
    assert Solution_1().removeInterval([[4, 6], [6, 7]], [5, 7]) == [[4, 5]]
    assert Solution_2().removeInterval([[4, 6], [6, 7]], [5, 7]) == [[4, 5]]

    for _ in range(800):                          # ! 随机对拍（输入有序、互不相交且不相接）
        t = random.randint(0, 3)
        iv = []
        for _ in range(random.randint(0, 5)):
            a = t + random.randint(1, 2)          # ! >= 1 的空隙，保证暴力基准可表示
            b = a + random.randint(1, 3)
            iv.append([a, b])
            t = b
        c = random.randint(0, 14)
        d = c + random.randint(0, 5)
        if c == d:
            d = c + 1
        o1 = Solution_1().removeInterval([x[:] for x in iv], [c, d])
        o2 = Solution_2().removeInterval([x[:] for x in iv], [c, d])
        o3 = Solution_3().removeInterval([x[:] for x in iv], [c, d])
        assert o1 == o2 == o3, (iv, [c, d], o1, o2, o3)
    print("随机对拍 800 组通过 ✓（两行减法 == 三段式提前退出 == 单位段集合差）")
