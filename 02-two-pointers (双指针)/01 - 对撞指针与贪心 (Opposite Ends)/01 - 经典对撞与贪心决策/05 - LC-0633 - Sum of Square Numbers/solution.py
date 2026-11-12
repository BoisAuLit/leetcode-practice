"""LC-0633 - Sum of Square Numbers

Level 1 · 01 对撞指针与贪心 —— 对撞指针作用在「虚拟有序序列」上
题目在问：给定非负整数 c，是否存在非负整数 a、b 使 a² + b² = c

决定性观察：双指针**不需要真的有一个数组**。
  这里的"数组"是 `0, 1, 4, 9, ..., ⌊√c⌋²`，它天然有序且可以 O(1) 按下标算出来，
  所以可以直接在 `a = 0`、`b = ⌊√c⌋` 之间对撞。

循环不变量：`a <= b`，且所有「a' < a 的可能解」和「b' > b 的可能解」都已被排除。
  - `a² + b² < c` → 当前 a 配最大的 b 都不够大，a 再小更不够 → a += 1
  - `a² + b² > c` → 当前 b 配最小的 a 都太大，b 再大更超 → b -= 1
  这正是 LC-0167 的两句话，只是"数组元素"换成了平方。

坑：
  - `b` 的初值用 `math.isqrt(c)`，不要用 `int(c ** 0.5)`：大数开方有浮点误差
  - 条件是 `a <= b` 而不是 `a < b`：a == b 的情况（如 c = 2 = 1+1、c = 8 = 4+4）合法
  - c 可以是 0（0² + 0² = 0），也可以让 a 为 0
  - 数学解法：Fermat 两平方和定理 —— c 能写成两平方和 ⟺ 它的质因数分解里
    所有形如 4k+3 的质因子的指数都是偶数。O(√c) 试除，面试里当加分项提一句就够
"""

from math import isqrt


##################################################################################################
##### ! Solution 1: 对撞指针（a 从 0 往上，b 从 ⌊√c⌋ 往下）
##### ! 时间复杂度: O(√c)   空间复杂度: O(1)
##### ! 适用：说明双指针的本质是「在一个有序的候选空间里排除」，候选空间不必是真实数组
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def judgeSquareSum(self, c: int) -> bool:
        a, b = 0, isqrt(c)   # ! isqrt 精确，不要用 ** 0.5
        while a <= b:        # ! <= ：允许 a == b
            s = a * a + b * b
            if s == c:
                return True
            if s < c:
                a += 1       # ! 不够大，只能让小的那头变大
            else:
                b -= 1       # ! 太大了，只能让大的那头变小
        return False


##################################################################################################
##### ! Solution 2: 枚举 a，用 isqrt 验证剩下的是不是完全平方数
##### ! 时间复杂度: O(√c)   空间复杂度: O(1)
##### ! 适用：最直接的写法，复杂度和解法 1 同阶；用来对照「双指针省掉的其实是开方运算」
##################################################################################################


class Solution_2:
    def judgeSquareSum(self, c: int) -> bool:
        a = 0
        while a * a <= c:
            rest = c - a * a
            r = isqrt(rest)
            if r * r == rest:
                return True
            a += 1
        return False


if __name__ == "__main__":
    cases = [(5, True), (3, False), (4, True), (0, True), (1, True), (2, True),
             (8, True), (7, False), (2147482647, False)]
    sols = [Solution_1(), Solution_2()]
    for sol in sols:
        for c, want in cases:
            got = sol.judgeSquareSum(c)
            assert got == want, f"{type(sol).__name__} c={c}: got {got}, want {want}"
    # ! 穷举对拍：0..2000 全部和「暴力枚举 a、b」比较
    brute = {a * a + b * b for a in range(50) for b in range(50)}
    for c in range(2001):
        want = c in brute
        for sol in sols:
            assert sol.judgeSquareSum(c) == want, (type(sol).__name__, c, want)
    print("2 个解法全过（含 c = 0..2000 穷举对拍）")
