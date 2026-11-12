"""LC-0201 - Bitwise AND of Numbers Range

Level 1 · 02 XOR 不变量与二进制算术 —— **Range AND = 两端点的公共二进制高位前缀**
题目在问：给定非负整数 `left`、`right`，求闭区间 `[left, right]` 内
         **所有整数**的按位与。

### 决定性观察

> **答案 = `left` 和 `right` 的公共二进制高位前缀，低位全部补 0。**

```python
shifts = 0
while left < right:
    left >>= 1
    right >>= 1
    shifts += 1
return left << shifts          # ! 把公共前缀挪回原位
```

---

## 四个必须解释的 why

### ① 为什么不同的低位最终会被 AND 清零？

设 `left` 和 `right` 的二进制在第 `k` 位首次不同（从高位往低看），
那么 `left` 第 `k` 位是 0、`right` 第 `k` 位是 1（因为 `left <= right`）。

更低的那些位（第 `k-1 .. 0` 位）：区间里一定同时存在
「该位为 0」和「该位为 1」的数 —— 因为区间跨过了第 `k` 位的翻转点，
长度至少是 `2^k`，低 `k` 位把 `0 .. 2^k - 1` **全部取遍了**。

AND 的性质是「**有一个 0 就是 0**」⟹ 这些低位全部清零。∎

具体一点：`[4, 7]` = `100, 101, 110, 111`。
第 2 位（值 4）全是 1 ⟹ 保留；第 1、0 位各自都出现过 0 ⟹ 清零。
答案 `100 = 4` ✓

### ② 为什么公共高位是答案的关键？

高于第 `k` 位的部分，`left` 和 `right` **完全相同**。
而区间里的任何数 `x` 满足 `left <= x <= right`
⟹ `x` 的高位也必须等于这个共同前缀（否则 `x` 会跑到区间外）。
所以这些位上**所有数都是 1 的位**在 AND 后仍是 1，是 0 的位仍是 0
—— **整段高位原样保留**。∎

### ③ 为什么可以同时右移两个端点？

右移一位 = 去掉最低位。我们要找的是「最长公共高位前缀」，
而**同时**右移不改变两者高位的对齐关系。
当 `left == right` 时，说明已经把所有「不同的低位」都移掉了,
剩下的就是公共前缀。∎

### ④ 为什么循环条件是 `left < right` 而不是 `left != right`？

两者在本题**等价**（因为题目保证 `left <= right`，右移保持这个序关系）。
用 `<` 更安全：万一输入违反了 `left <= right`，`!=` 可能死循环，
而 `<` 会直接跳过循环。**写 `<` 是防御性的习惯。**

### ⑤ 结果如何恢复到原位？

记录右移了 `shifts` 次，最后 `left << shifts` 把公共前缀挪回高位，
**低位自动补 0** —— 正好就是「低位被清零」的结果。∎

---

## ⚠️ AND ≠ OR：不要把公共前缀的思路套到别的 Range 运算上

| 运算 | `[4, 7]` 的结果 | 规律 |
|---|---|---|
| **Range AND** | `4` (`100`) | **公共高位前缀** |
| Range OR | `7` (`111`) | 公共前缀 + **低位全置 1** |
| Range XOR | `4^5^6^7 = 0` | 要用前缀 XOR 的周期性公式，**完全不同** |

**AND 只会把 1 变成 0，永不把 0 变成 1**（单调递减）；
**OR 只会把 0 变成 1**（单调递增）；
**XOR 两个方向都可能**。

> **三种运算的「区间聚合」规律完全不同，不存在通用公式。**
> 本题学到的是 AND 的规律，不要迁移到 OR / XOR。
> （Range OR 的答案是：公共前缀 + 从第一个不同位往下全是 1。）

---

## 另一种解法：Brian Kernighan 技巧

```python
while left < right:
    right &= right - 1       # ! 清掉 right 的最低位 1
return right
```
**为什么这也对？**
`right & (right - 1)` 把 `right` 最低位的 1 清零，使它**单调减小**。
一直清到 `right <= left` 时，`right` 剩下的就是
「`right` 的某个高位前缀」，而这个前缀必然也是 `left` 的前缀
（因为它 `<= left <= right` 且是 `right` 的前缀）。∎

**哪个更好？** 两者都是 O(32)。
移位版更直观（直接体现「公共前缀」），Kernighan 版更短。
面试写移位版，因为**它的正确性更容易口述**。

---

复杂度：**O(log(max))** = **O(32)** = O(1) 时间、**O(1)** 空间。
       ⚠️ **不是 O(right - left)** —— 绝不能真的去遍历区间
       （`right` 可达 `2^31 - 1`）。

边界：
  - `left == right` → `left` 本身（循环一次都不进）
  - `left = 0` → **0**（0 和任何数 AND 都是 0）
  - `[5, 7]` → `4`（`101 & 110 & 111 = 100`）
  - `[4, 7]` → `4`
  - `[1, 2^31-1]` → **0**（跨越整个值域）
  - `[2^31-1, 2^31-1]` → `2^31-1`
  - 区间跨过 2 的幂 → 一定被清零
"""


##################################################################################################
##### ! Solution 1: 同时右移两端点直到相等，再左移回去（公共高位前缀）
##### ! 时间复杂度: O(32)   空间复杂度: O(1)
##### ! 适用：所有 Range AND 问题。正确性最容易口述，面试首选
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        shifts = 0
        while left < right:          # ! 用 < 而不是 !=，对异常输入更安全
            left >>= 1               # ! 同时右移，不改变高位对齐关系
            right >>= 1
            shifts += 1
        return left << shifts        # ! 公共前缀挪回原位，低位自动补 0


##################################################################################################
##### ! Solution 2: Brian Kernighan —— 反复清掉 right 的最低位 1
##### ! 时间复杂度: O(right 中 1 的个数) <= O(32)   空间复杂度: O(1)
##### ! 适用：代码最短。但「为什么对」不如解法 1 直观
##################################################################################################


class Solution_2:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        while left < right:
            right &= right - 1       # ! 清掉 right 最低位的 1 ⟹ right 单调减小
        return right


##################################################################################################
##### ! Solution 3: 逐位判断（这一位在整个区间内是否恒为 1）
##### ! 时间复杂度: O(32)   空间复杂度: O(1)
##### ! 适用：把「为什么低位会被清零」写成代码；一位一位地验证高位前缀的结论
##################################################################################################


class Solution_3:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        res = 0
        for i in range(31, -1, -1):
            bit = 1 << i
            # ! 该位在 left 和 right 上都是 1，且区间没有跨过这一位的翻转点
            if (left & bit) and (right & bit):
                # ! 翻转点判定：把第 i 位及以下清零后，left 和 right 的高位必须相同
                if (left >> i) == (right >> i):
                    res |= bit
                else:
                    break            # ! 高位首次不同 ⟹ 这一位及以下全部清零
            elif (left & bit) != (right & bit):
                break                # ! 该位不同 ⟹ 区间跨过翻转点 ⟹ 这一位及以下全 0
        return res


##################################################################################################
##### ! Solution 4: 暴力基准（真的遍历整个区间，仅用于小范围对拍）
##### ! 时间复杂度: O(right - left)   空间复杂度: O(1)
##### ! 适用：仅用于对拍。right 可达 2^31-1，提交这个必然 TLE
##################################################################################################


class Solution_4:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        res = left
        for x in range(left + 1, right + 1):
            res &= x
            if res == 0:             # ! 小剪枝：归零后不可能再变回来（AND 单调递减）
                break
        return res


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3, Solution_4):
        s = cls()
        assert s.rangeBitwiseAnd(5, 7) == 4          # ! 101 & 110 & 111 = 100
        assert s.rangeBitwiseAnd(4, 7) == 4
        assert s.rangeBitwiseAnd(0, 0) == 0
        assert s.rangeBitwiseAnd(1, 1) == 1
        assert s.rangeBitwiseAnd(0, 1) == 0          # ! left = 0 ⟹ 必然 0
        assert s.rangeBitwiseAnd(6, 6) == 6          # ! 单点区间
        assert s.rangeBitwiseAnd(12, 15) == 12       # ! 1100..1111

    # ! 大区间只测 O(1) 的三个解法（暴力会跑 21 亿次）
    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert s.rangeBitwiseAnd(1, 2147483647) == 0
        assert s.rangeBitwiseAnd(2147483647, 2147483647) == 2147483647
        assert s.rangeBitwiseAnd(2147483646, 2147483647) == 2147483646

    print("rangeBitwiseAnd(5, 7)  =", Solution_1().rangeBitwiseAnd(5, 7), "(101 & 110 & 111 = 100)")
    print("rangeBitwiseAnd(1, 2147483647) =", Solution_1().rangeBitwiseAnd(1, 2147483647))

    # ! 顺带验证「AND 和 OR 的区间规律不同」这个论断
    def range_or(lo, hi):
        r = lo
        for x in range(lo + 1, hi + 1):
            r |= x
        return r
    assert Solution_1().rangeBitwiseAnd(4, 7) == 4 and range_or(4, 7) == 7
    print("Range AND [4,7] = 4，Range OR [4,7] = 7  ⟹ 两者规律不同，公式不可互换 ✓")

    for _ in range(3000):                            # ! 随机对拍（小区间，含 0 和单点）
        lo = random.randint(0, 200)
        hi = lo + random.randint(0, 200)
        a = Solution_1().rangeBitwiseAnd(lo, hi)
        b = Solution_2().rangeBitwiseAnd(lo, hi)
        c = Solution_3().rangeBitwiseAnd(lo, hi)
        d = Solution_4().rangeBitwiseAnd(lo, hi)
        assert a == b == c == d, (lo, hi, a, b, c, d)
    print("随机对拍 3000 组通过 ✓（右移前缀 == Kernighan == 逐位判断 == 区间暴力）")
