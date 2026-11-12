"""LC-0986 - Interval List Intersections

Level 1 · 05 多序列同步扫描 —— Interval Intersection（两个有序区间表同步推进）
题目在问：两个各自有序、内部互不重叠的区间列表，求它们所有的交集区间

决定性观察（两条就够）：
  1. 两个区间 `[a1,a2]`、`[b1,b2]` 的交集是 `[max(a1,b1), min(a2,b2)]`，
     当且仅当 `max(a1,b1) <= min(a2,b2)` 时非空。**没有别的情况要分类讨论**。
  2. 比较完之后，**结束得更早的那个区间可以彻底丢弃** ——
     它右边界最小，不可能再和对面后面的（起点更大的）区间相交。

循环不变量：`i`、`j` 分别指向两个列表里「还可能产生交集」的最靠前的区间。
  每轮至少丢掉一个区间，所以总共 O(m + n) 轮。

和归并排序的区别：归并是「每轮取走较小的那个」，这里是「每轮算一次交集，
  再丢掉结束更早的那个」。形状一样，决策规则不同。

坑：
  - 判空用 `lo <= hi`，不是 `<`：题目是闭区间，`[5,5]` 是合法交集
  - 推进条件比较的是**右端点**（`a2 < b2`），不是左端点
  - 相等时（`a2 == b2`）推进任意一个都对，但只能推进一个，两个一起推会漏解
"""

from typing import List


##################################################################################################
##### ! Solution 1: 双指针同步推进，交集 = [max(起点), min(终点)]
##### ! 时间复杂度: O(m + n)   空间复杂度: O(1) 额外（不含输出）
##### ! 适用：区间交集的标准解；会议室、日程表（LC-0729 / 0759）都是同一套
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def intervalIntersection(self, firstList: List[List[int]],
                             secondList: List[List[int]]) -> List[List[int]]:
        res = []
        i = j = 0
        while i < len(firstList) and j < len(secondList):
            a1, a2 = firstList[i]
            b1, b2 = secondList[j]
            lo, hi = max(a1, b1), min(a2, b2)
            if lo <= hi:            # ! 闭区间，所以用 <=
                res.append([lo, hi])
            if a2 < b2:             # ! 丢掉结束更早的那个；比的是右端点
                i += 1
            else:
                j += 1
        return res


##################################################################################################
##### ! Solution 2: 暴力两重循环（基线）
##### ! 时间复杂度: O(m * n)   空间复杂度: O(1) 额外
##### ! 适用：对拍参照；它不需要「有序」这个前提，正好反衬出有序才是双指针成立的条件
##################################################################################################


class Solution_2:
    def intervalIntersection(self, firstList: List[List[int]],
                             secondList: List[List[int]]) -> List[List[int]]:
        res = []
        for a1, a2 in firstList:
            for b1, b2 in secondList:
                lo, hi = max(a1, b1), min(a2, b2)
                if lo <= hi:
                    res.append([lo, hi])
        return sorted(res)


if __name__ == "__main__":
    import random
    cases = [
        ([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]],
         [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]),
        ([[1, 3], [5, 9]], [], []),
        ([], [[4, 8], [10, 12]], []),
        ([[1, 7]], [[3, 10]], [[3, 7]]),
    ]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for a, b, want in cases:
            got = sol.intervalIntersection([x[:] for x in a], [x[:] for x in b])
            assert got == want, f"{type(sol).__name__}: got {got}, want {want}"

    def rnd_list(rng):   # ! 生成有序、互不重叠的区间表
        out, t = [], rng.randint(0, 3)
        for _ in range(rng.randint(0, 5)):
            s = t + rng.randint(1, 3)
            e = s + rng.randint(0, 3)
            out.append([s, e]); t = e + rng.randint(1, 2)
        return out
    rng = random.Random(986)
    for _ in range(2000):
        a, b = rnd_list(rng), rnd_list(rng)
        want = Solution_2().intervalIntersection([x[:] for x in a], [x[:] for x in b])
        got = Solution_1().intervalIntersection([x[:] for x in a], [x[:] for x in b])
        assert got == want, (a, b, got, want)
    print("2 个解法全过（含 2000 组随机对拍）")
