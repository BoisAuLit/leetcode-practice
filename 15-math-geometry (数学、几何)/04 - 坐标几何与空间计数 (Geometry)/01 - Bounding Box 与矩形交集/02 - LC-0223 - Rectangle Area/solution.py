"""LC-0223 - Rectangle Area

Level 1 · 04 坐标几何与空间计数 —— **Rectangle Intersection（矩形交集）+ 容斥**
题目在问：两个**坐标轴对齐（axis-aligned）**矩形，
         A 由左下 `(ax1, ay1)` 和右上 `(ax2, ay2)` 确定，B 同理。
         求**并集**的总面积。

### 整道题就是一个容斥原理（Inclusion–Exclusion）

```
Area(A ∪ B) = Area(A) + Area(B) − Area(A ∩ B)
```

**为什么要减去重叠面积？**
`Area(A) + Area(B)` 把两个矩形**都**覆盖的那块算了**两次**。
容斥原理说：减一次就回到「每块只算一次」。∎

### 交集的宽高公式（这是唯一需要记的两行）

```python
width  = max(0, min(ax2, bx2) - max(ax1, bx1))
height = max(0, min(ay2, by2) - max(ay1, by1))
intersection = width * height
```

**为什么交集的左边界是 `max(两个左边界)`、右边界是 `min(两个右边界)`？**
一个点 `x` 同时在两个矩形的 x 范围内 ⟺ `ax1 <= x <= ax2` **且** `bx1 <= x <= bx2`
⟺ `max(ax1,bx1) <= x <= min(ax2,bx2)`。这就是区间交集公式
（和 [LC-0986 Interval List Intersections](<../../../14-intervals (区间)/02 - 双指针区间交集与多路合并/01 - 两个有序区间序列求交集/01 - LC-0986 - Interval List Intersections (学习索引 · 实体在 02-two-pointers)>)
的 `max(start) / min(end)` 完全是同一件事）——
**二维矩形交集 = x 方向区间交集 × y 方向区间交集**。

**为什么不重叠时宽度或高度为 0？**
若两矩形在 x 方向分离（比如 A 整个在 B 左边），则 `min(ax2,bx2) = ax2`、
`max(ax1,bx1) = bx1`，而 `ax2 < bx1` ⟹ 差值为**负数**。
负的「宽度」没有几何意义 ⟹ 用 `max(0, ...)` 夹到 0 ⟹ 交集面积 0。
**不加 `max(0, ...)` 会得到负面积，于是「减去」变成「加上」，答案偏大。**

**为什么只在边界相接时交集面积为 0？**
若 `ax2 == bx1`（A 的右边正好贴着 B 的左边），则 `width = ax2 - bx1 = 0`
⟹ 面积 `0 * height = 0`。
几何上两个矩形共享一条**线段**，线段的面积确实是 0 ——
**这不是边界情况的特例，公式自然就给出 0，不需要额外的 if。**

**如何处理负坐标？**
**完全不需要特殊处理。** 公式里只有 `min` / `max` / 减法，
对负数一样成立（题目的坐标范围是 `-10^4 <= x, y <= 10^4`）。
面积 `(ax2-ax1) * (ay2-ay1)` 恒为非负，因为题目保证 `ax1 <= ax2`、`ay1 <= ay2`。

---

## ⚠️ LC-0223 和 LC-3195 的端点语义完全不同（本 Level 2 的核心对照）

| | [LC-3195 Minimum Area to Cover All Ones](<../01 - LC-3195 - Find the Minimum Area to Cover All Ones I>) | **LC-0223** 本题 |
|---|---|---|
| 坐标是什么 | **离散的矩阵格子下标** | **连续平面上的几何坐标** |
| 面积 = | `(maxR - minR + 1) * (maxC - minC + 1)` | `(x2 - x1) * (y2 - y1)` |
| **有没有 `+1`** | **有** | **没有** |
| `[1,1]` 代表 | **1 个格子**（面积 1） | **一个点**（面积 0） |

**为什么 LC-3195 要 `+1`，LC-0223 不要？**
- LC-3195 数的是**格子个数**。从第 2 行到第 5 行一共 `5 - 2 + 1 = 4` 行
  —— 这是**闭区间上的整数个数**，所以要 `+1`。
- LC-0223 算的是**长度**。从 `x = 2` 到 `x = 5` 的长度是 `5 - 2 = 3`
  —— 这是**两点之间的距离**，不加 1。

> **同一个「矩形」，一个在数格子，一个在量长度。**
> 搞混就会差一整圈（LC-3195 漏 `+1` 答案偏小，LC-0223 多 `+1` 答案偏大）。
> 这和 [14-intervals 的闭 / 半开区间](<../../../14-intervals (区间)/_resources/endpoint-semantics-cheat-sheet.md>)
> 是同一个思维陷阱的二维版本。

---

## 判「是否重叠」vs 算「重叠面积」

有时题目只问**有没有**重叠（如 LC-0836 Rectangle Overlap，正面积重叠）：

```python
overlap = ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2   # ! 严格小于
```
注意这里是**严格**小于 —— 只共享边界的两个矩形重叠面积为 0，
按 LC-0836 的定义**不算**重叠。
而本题的面积公式用 `max(0, ...)` 自然处理这种情况，**不需要分支**。

---

复杂度：**O(1)** 时间、**O(1)** 空间 —— 纯公式，没有循环。

边界：
  - 部分重叠：`A=(-3,0,3,4)`, `B=(0,-1,9,2)` → **45**
  - 完全相同：`A=B=(-2,-2,2,2)` → `16`（不是 32）
  - 完全不重叠：`A=(0,0,1,1)`, `B=(5,5,6,6)` → `2`
  - **只在边界相接**：`A=(0,0,1,1)`, `B=(1,0,2,1)` → `2`（交集面积 0）
  - 只在**一个角**相接：`A=(0,0,1,1)`, `B=(1,1,2,2)` → `2`
  - 一个包含另一个：`A=(0,0,10,10)`, `B=(2,2,3,3)` → `100`
  - **零面积矩形**（退化成线段/点）：`A=(0,0,0,0)` → 只算 B 的面积
  - 全负坐标：`A=(-5,-5,-1,-1)`, `B=(-3,-3,-2,-2)` → `16`
"""


##################################################################################################
##### ! Solution 1: 容斥原理 + max(0, ...) 夹住负宽高
##### ! 时间复杂度: O(1)   空间复杂度: O(1)
##### ! 适用：所有「两个轴对齐矩形的并集 / 交集面积」问题；记住这三行就够
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def computeArea(
        self, ax1: int, ay1: int, ax2: int, ay2: int,
        bx1: int, by1: int, bx2: int, by2: int,
    ) -> int:
        area_a = (ax2 - ax1) * (ay2 - ay1)          # ! 注意没有 +1（量长度，不是数格子）
        area_b = (bx2 - bx1) * (by2 - by1)
        # ! 二维交集 = x 方向区间交集 × y 方向区间交集
        w = max(0, min(ax2, bx2) - max(ax1, bx1))   # ! max(0,..) 把负宽度夹成 0
        h = max(0, min(ay2, by2) - max(ay1, by1))
        return area_a + area_b - w * h              # ! 容斥：重复算的那块减掉


##################################################################################################
##### ! Solution 2: 先显式判断是否重叠，再分支计算（更啰嗦，但把语义摆明）
##### ! 时间复杂度: O(1)   空间复杂度: O(1)
##### ! 适用：想把「重叠判定」和「面积计算」分开讲清时；和 LC-0836 共享判定条件
##################################################################################################


class Solution_2:
    def computeArea(
        self, ax1: int, ay1: int, ax2: int, ay2: int,
        bx1: int, by1: int, bx2: int, by2: int,
    ) -> int:
        area_a = (ax2 - ax1) * (ay2 - ay1)
        area_b = (bx2 - bx1) * (by2 - by1)
        # ! 正面积重叠的判定（严格小于 —— 只贴边不算重叠）：这就是 LC-0836 的答案
        overlaps = ax1 < bx2 and bx1 < ax2 and ay1 < by2 and by1 < ay2
        if not overlaps:
            return area_a + area_b                  # ! 交集面积为 0，不用减
        inter = (min(ax2, bx2) - max(ax1, bx1)) * (min(ay2, by2) - max(ay1, by1))
        return area_a + area_b - inter


##################################################################################################
##### ! Solution 3: 暴力基准（在单位格子上数面积，用于对拍）
##### ! 时间复杂度: O(V^2)   空间复杂度: O(V^2)
##### ! 适用：仅用于对拍。把「并集面积」按单位小方格一个个数出来
##################################################################################################


class Solution_3:
    def computeArea(
        self, ax1: int, ay1: int, ax2: int, ay2: int,
        bx1: int, by1: int, bx2: int, by2: int,
    ) -> int:
        cells = set()
        # ! 单位方格 [x, x+1) × [y, y+1)，用左下角坐标代表它
        for x in range(ax1, ax2):
            for y in range(ay1, ay2):
                cells.add((x, y))
        for x in range(bx1, bx2):
            for y in range(by1, by2):
                cells.add((x, y))
        return len(cells)                           # ! 并集 ⟹ set 自动去重


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert s.computeArea(-3, 0, 3, 4, 0, -1, 9, 2) == 45
        assert s.computeArea(-2, -2, 2, 2, -2, -2, 2, 2) == 16      # ! 完全相同，不是 32
        assert s.computeArea(0, 0, 1, 1, 5, 5, 6, 6) == 2           # ! 完全不重叠
        assert s.computeArea(0, 0, 1, 1, 1, 0, 2, 1) == 2           # ! 只贴边 ⟹ 交集 0
        assert s.computeArea(0, 0, 1, 1, 1, 1, 2, 2) == 2           # ! 只碰一个角
        assert s.computeArea(0, 0, 10, 10, 2, 2, 3, 3) == 100       # ! 包含
        assert s.computeArea(0, 0, 0, 0, 1, 1, 3, 3) == 4           # ! 退化成点
        assert s.computeArea(-5, -5, -1, -1, -3, -3, -2, -2) == 16  # ! 全负坐标

    print("A=(-3,0,3,4) B=(0,-1,9,2) ->", Solution_1().computeArea(-3, 0, 3, 4, 0, -1, 9, 2))
    print("只贴边 A=(0,0,1,1) B=(1,0,2,1) ->", Solution_1().computeArea(0, 0, 1, 1, 1, 0, 2, 1))

    for _ in range(3000):                           # ! 随机对拍（含负坐标、退化矩形、贴边）
        def rect():
            x1 = random.randint(-6, 6); x2 = random.randint(x1, 6)
            y1 = random.randint(-6, 6); y2 = random.randint(y1, 6)
            return x1, y1, x2, y2
        a, b = rect(), rect()
        args = (*a, *b)
        r1 = Solution_1().computeArea(*args)
        r2 = Solution_2().computeArea(*args)
        r3 = Solution_3().computeArea(*args)
        assert r1 == r2 == r3, (args, r1, r2, r3)
    print("随机对拍 3000 组通过 ✓（容斥公式 == 显式分支 == 单位格子暴力）")
