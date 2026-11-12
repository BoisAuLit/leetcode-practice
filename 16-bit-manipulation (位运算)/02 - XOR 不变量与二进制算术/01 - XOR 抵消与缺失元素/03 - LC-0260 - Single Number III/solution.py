"""LC-0260 - Single Number III     ★ 第二轮审核新增（XOR 抵消 + 最低位 1 分组）

Level 1 · 02 XOR 不变量与二进制算术 —— **用一个「区分位」把数组劈成两半**
题目在问：数组里恰好有**两个**元素只出现一次，其余都出现两次。
         找出这两个数（顺序任意）。要求 **O(n) 时间、O(1) 额外空间**。

### 决定性观察：全体 XOR 得到的是「两个答案的 XOR」

```python
xor_all = 0
for x in nums: xor_all ^= x
# ! 成对的全部抵消 ⟹ xor_all == a ^ b（a、b 是那两个答案）
```

但我们要的是 `a` 和 `b` 各自的值，不是它们的 XOR。**怎么分开？**

### 关键一步：`a ^ b` 中任何一个为 1 的位，都能把数组劈成两半

因为 `a != b`，所以 `a ^ b != 0` ⟹ 它**至少有一个为 1 的位**。
在那一位上，`a` 和 `b` **必然一个是 0、一个是 1**（这就是 XOR 为 1 的含义）。

取**最低位的 1** 作为「区分位」：
```python
diff = xor_all & (-xor_all)      # ! 只保留最低位的 1
```

按这一位把整个数组分成两组：
- **第 1 组**：该位是 1 的所有数 —— 含 `a`（或 `b`），以及若干**完整的成对元素**
- **第 2 组**：该位是 0 的所有数 —— 含另一个答案，以及其余**完整的成对元素**

**为什么成对的元素一定落在同一组？**
两个相等的数，每一位都相同 ⟹ 该区分位上也相同 ⟹ **必然同组**
⟹ 在组内 XOR 时互相抵消。∎

于是**对每组各做一次 XOR**，剩下的就是该组里那个唯一的答案。

```python
a = 0
for x in nums:
    if x & diff: a ^= x          # ! 只 XOR 第 1 组
b = xor_all ^ a                  # ! 另一个直接推出来，不用再扫一遍
```

---

## `x & (-x)` 为什么能取出最低位的 1？

补码的定义：`-x == ~x + 1`。

以 `x = 0b1011000` 为例（最低位 1 在第 3 位）：
```
 x      = 0b0001011000
~x      = 0b1110100111
~x + 1  = 0b1110101000     ← 最低位 1 及其右边与 x 相同，左边全部取反
x & -x  = 0b0000001000     ← 只剩最低位的那个 1 ✓
```

**原理**：`-x` 等于「把 `x` 最低位 1 右边的部分保持不变，
最低位 1 本身保持，更高位全部取反」。
AND 之后高位全灭，只剩最低位的 1。∎

**等价写法**：`x & (x - 1)` 是**清掉**最低位 1（Brian Kernighan），
`x & (-x)` 是**只保留**最低位 1。**两个要分清。**

| 表达式 | 作用 | 用在哪 |
|---|---|---|
| `x & (x - 1)` | **清掉**最低位 1 | Popcount（LC-0191）、判 2 的幂（LC-0231） |
| `x & (-x)` | **只保留**最低位 1 | **本题的区分位**、树状数组的 lowbit |

> ⚠️ **Python 的 `-x` 对任意精度整数依然正确**（因为 `x > 0` 时
> `x & -x` 的结果只取决于低位），所以这里**不需要 32 位 mask**
> —— 和 [LC-0371](<../../02 - XOR 与 AND 形成二进制加法/01 - LC-0371 - Sum of Two Integers>)
> 不同，那里的 `<<` 会让高位无限生长。

---

## 本 Level 2 三道题的递进关系

| 题 | 异常元素 | 核心技巧 | 为什么 XOR 够用 |
|---|---|---|---|
| [LC-0136 Single Number](<../01 - LC-0136 - Single Number>) | **1 个**出现 1 次，其余 2 次 | 全体 XOR | 成对的全抵消，剩下就是答案 |
| [LC-0268 Missing Number](<../02 - LC-0268 - Missing Number>) | 缺 **1 个** | XOR `0..n` 和数组 | 存在的配对抵消，缺的留下 |
| **LC-0260** 本题 | **2 个**出现 1 次 | 全体 XOR **+ 最低位 1 分组** | XOR 只能给出 `a^b`，**必须再分组** |

> **这正是本题值得单独练的理由**：
> 前两题「一次 XOR 就出答案」，本题必须想到**「用一个位把数组分治」**。
> 这个分组思想迁移到：按某一位分治、Trie 的二进制分叉、
> 以及所有「用一个布尔特征把集合劈成两半」的问题。

**LC-0137 Single Number II**（出现 3 次）**不能**用这个技巧 ——
XOR 对 3 个相同元素不抵消（`x^x^x == x`），
要改成「**逐位计数 mod 3**」。本次未收录（见根 README 的 Future Candidates）。

---

复杂度：**O(n)** 时间（两遍扫描）、**O(1)** 额外空间 —— 满足题目的硬性要求。

边界：
  - 最小输入 `[1, 2]` → `{1, 2}`
  - `[1,2,1,3,2,5]` → `{3, 5}`
  - 含 **0**：`[0, 1]` → `{0, 1}`（`xor_all = 1`）
  - 含 **负数**：`[-1, 0]` → `{-1, 0}`
  - 两个答案只差**一个 bit**：`[4, 5, 1, 1]` → `{4, 5}`（`diff = 1`）
  - 两个答案差**最高位**：`[1, 2**30, 7, 7]`
  - 大量成对元素
  - 答案互为相反数：`[3, -3, 9, 9]`
"""

from typing import List


##################################################################################################
##### ! Solution 1: 全体 XOR 得 a^b，取最低位 1 做区分位分两组，各组再 XOR
##### ! 时间复杂度: O(n)   空间复杂度: O(1) 额外
##### ! 适用：所有「两个异常元素」的 XOR 题；分组思想可迁移到按位分治
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def singleNumber(self, nums: List[int]) -> List[int]:
        xor_all = 0
        for x in nums:
            xor_all ^= x                  # ! 成对的全部抵消 ⟹ xor_all == a ^ b
        diff = xor_all & (-xor_all)       # ! 只保留最低位的 1 —— 这就是区分位
        a = 0
        for x in nums:
            if x & diff:                  # ! 只 XOR「该位为 1」那一组
                a ^= x
        return [a, xor_all ^ a]           # ! 另一个直接推出，不用再扫


##################################################################################################
##### ! Solution 2: 同上，但两组各自累加（更对称，便于讲解「劈成两半」）
##### ! 时间复杂度: O(n)   空间复杂度: O(1) 额外
##### ! 适用：想明确看到两个组各自独立 XOR 的过程时
##################################################################################################


class Solution_2:
    def singleNumber(self, nums: List[int]) -> List[int]:
        xor_all = 0
        for x in nums:
            xor_all ^= x
        diff = xor_all & (-xor_all)
        group1 = group2 = 0
        for x in nums:
            if x & diff:
                group1 ^= x               # ! 区分位为 1 的那一半
            else:
                group2 ^= x               # ! 区分位为 0 的那一半
        return [group1, group2]


##################################################################################################
##### ! Solution 3: 哈希计数基准（O(n) 额外空间，不满足题目要求，仅用于对拍）
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：仅用于对拍。题目明确要求 O(1) 空间，所以这个版本不能提交
##################################################################################################


class Solution_3:
    def singleNumber(self, nums: List[int]) -> List[int]:
        from collections import Counter

        return [v for v, c in Counter(nums).items() if c == 1]


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert sorted(s.singleNumber([1, 2, 1, 3, 2, 5])) == [3, 5]
        assert sorted(s.singleNumber([-1, 0])) == [-1, 0]          # ! 含负数
        assert sorted(s.singleNumber([0, 1])) == [0, 1]            # ! 含 0
        assert sorted(s.singleNumber([1, 2])) == [1, 2]            # ! 最小输入
        assert sorted(s.singleNumber([4, 5, 1, 1])) == [4, 5]      # ! 只差一个 bit
        assert sorted(s.singleNumber([1, 2**30, 7, 7])) == [1, 2**30]   # ! 差最高位
        assert sorted(s.singleNumber([3, -3, 9, 9])) == [-3, 3]    # ! 互为相反数

    print("[1,2,1,3,2,5] ->", sorted(Solution_1().singleNumber([1, 2, 1, 3, 2, 5])))
    print("[4,5,1,1]     ->", sorted(Solution_1().singleNumber([4, 5, 1, 1])))

    # ! 演示 x & -x 和 x & (x-1) 的区别（两个最容易记混的恒等式）
    x = 0b1011000
    print(f"x        = {x:#09b}")
    print(f"x & -x   = {x & -x:#09b}   ← 只保留最低位的 1")
    print(f"x & (x-1)= {x & (x - 1):#09b}   ← 清掉最低位的 1")
    assert x & -x == 0b1000 and x & (x - 1) == 0b1010000

    for _ in range(3000):                         # ! 随机对拍
        pairs = [random.randint(-50, 50) for _ in range(random.randint(0, 6))]
        a, b = random.sample(range(-60, 60), 2)
        while a in pairs or b in pairs:           # ! 保证 a、b 真的只出现一次
            pairs = [p for p in pairs if p not in (a, b)]
        arr = pairs * 2 + [a, b]
        random.shuffle(arr)
        r1 = sorted(Solution_1().singleNumber(arr[:]))
        r2 = sorted(Solution_2().singleNumber(arr[:]))
        r3 = sorted(Solution_3().singleNumber(arr[:]))
        assert r1 == r2 == r3 == sorted([a, b]), (arr, a, b, r1, r2, r3)
    print("随机对拍 3000 组通过 ✓（区分位分组 == 对称双组 == 哈希计数基准）")
