"""LC-0371 - Sum of Two Integers

Level 1 · 02 XOR 不变量与二进制算术 —— **用 XOR 和 AND 手搓二进制加法**
题目在问：不使用 `+` 和 `-`，返回 `a + b`。

### 两个决定性等式（整道题就这两行）

```python
sum_without_carry = a ^ b          # ! 无进位加法
carry             = (a & b) << 1   # ! 需要进位的位置，左移一位
```
然后把这两者**再相加**，重复直到 `carry == 0`。

**为什么 XOR 对应无进位加法？**
看单个二进制位的加法真值表（忽略进位，只看本位结果）：

| `a` | `b` | 本位和 | `a ^ b` |
|---|---|---|---|
| 0 | 0 | 0 | 0 ✓ |
| 0 | 1 | 1 | 1 ✓ |
| 1 | 0 | 1 | 1 ✓ |
| 1 | 1 | **0**（进位了，本位是 0） | 0 ✓ |

**完全一致** ⟹ `a ^ b` 就是「每一位各自相加、不互相影响」的结果。

**为什么 AND 能找到需要产生进位的位置？**
只有 `1 + 1` 才会进位，而「两位都是 1」正是 `a & b`。

**为什么 Carry 要左移一位？**
进位的含义是「向**更高一位**贡献 1」。二进制里高一位的权重是 2 倍
⟹ 左移一位。

**为什么这个过程一定会结束？**
每一轮 `carry = (a & b) << 1`，**最低的那个 1 至少往左挪一位**。
更严格地说：设 `t(x)` 是 `x` 最低位 1 的位置，则新 carry 的最低 1 位置
`>= t(a & b) + 1 > t(a & b)`。由于固定宽度是 32 位，
最多 32 轮后 carry 的所有 1 都被移出 32 位之外 ⟹ `carry == 0`。∎

---

## ⚠️ Python 的大坑：负数会让这个循环**永不终止**

**为什么？**
Python 的 `int` 是**任意精度**的，负数在概念上是**无限符号扩展**的补码：
```
-1  ==  ...111111111111   （无限多个 1 往左延伸）
```
所以 `(a & b) << 1` 永远还有 1 可以左移 —— **carry 永远不为 0，死循环。**

**验证**（这就是为什么不能直接照搬 C++ 的写法）：
```python
a, b = -1, 1
# a ^ b = -2  = ...1110
# (a & b) << 1 = (1) << 1 = 2
# 下一轮 a, b = -2, 2 → a^b = -4, carry = 4 → -4, 8 → -8, 16 → … 永不收敛
```

### 正确做法：手动限制成 32 位补码

```python
MASK    = 0xFFFFFFFF      # ! 32 个 1，用来把结果截断成 32 位
MAX_INT = 0x7FFFFFFF      # ! 2^31 - 1，32 位有符号的最大值

while b != 0:
    carry = ((a & b) << 1) & MASK    # ! 每轮都 & MASK ⟹ 高位不会无限生长
    a = (a ^ b) & MASK
    b = carry
# ! 此时 a 是 32 位无符号表示，要还原成 Python 的有符号整数
return a if a <= MAX_INT else ~(a ^ MASK)
```

**最后那一行在做什么？**
循环结束后 `a` 是一个 `0 .. 0xFFFFFFFF` 的**无符号**数。
若 `a > MAX_INT`，说明它的第 31 位（符号位）是 1 ⟹ 代表一个**负数**。
按补码规则还原：
- `a ^ MASK` = 把 32 位全部取反（得到 `|a|-1` 的 32 位表示）
- 再 `~` 取反并加一（Python 的 `~x == -x-1`）⟹ 得到正确的负值

**举例**：`a = 0xFFFFFFFE`（32 位补码的 -2）
- `a ^ MASK = 0x00000001 = 1`
- `~1 = -2` ✓

> **一句话**：C++ 的 `int` 天然就是 32 位，所以不需要 mask；
> Python 的 `int` 是无限位的，所以**必须手动模拟 32 位的"溢出截断"**。
> 这不是优化，是**正确性的必要条件** —— 不加 mask 的代码在负数输入上会挂死。

---

## 和本层其他题的关系

| 题 | 用的恒等式 | 问的是什么 |
|---|---|---|
| [LC-0136 Single Number](<../../01 - XOR 抵消与缺失元素/01 - LC-0136 - Single Number>) | `x ^ x == 0`、`x ^ 0 == x` | XOR 的**抵消性** |
| [LC-0268 Missing Number](<../../01 - XOR 抵消与缺失元素/02 - LC-0268 - Missing Number>) | 同上 | 同上 |
| **LC-0371** 本题 | `a^b` = 无进位和、`a&b` = 进位 | XOR 的**算术含义** |
| [LC-0201 Range AND](<../../03 - Range AND 与共同高位前缀/01 - LC-0201 - Bitwise AND of Numbers Range>) | AND 只会**清零**，不会置一 | AND 的**单调性** |

> **LC-0136/0268 把 XOR 当「配对消除器」，LC-0371 把 XOR 当「半加器」。**
> 同一个运算符，两种完全不同的用法 —— 这是本 Level 1 想教的核心。

复杂度：**O(1)** 时间（固定宽度 ⟹ 最多 32 轮）、**O(1)** 空间。

边界（指令点名必测）：
  - `(1, 2)` → 3
  - `(2, 3)` → 5
  - `(-1, 1)` → **0**（最容易死循环的输入）
  - `(-2, 3)` → 1
  - `(-5, -7)` → -12（**两个都是负数**）
  - `(0, 0)` → 0
  - `(-1, 0)` → -1
  - `(2147483647, 0)` / `(-2147483648, 0)` → 32 位边界
  - `(2147483647, -2147483648)` → -1（两端相加）
"""

MASK = 0xFFFFFFFF           # ! 32 个 1
MAX_INT = 0x7FFFFFFF        # ! 2^31 - 1


##################################################################################################
##### ! Solution 1: 迭代半加器 + 32 位 MASK 截断（负数安全）
##### ! 时间复杂度: O(1)（最多 32 轮）   空间复杂度: O(1)
##### ! 适用：所有「不用 + - 做加法」的题；MASK 是 Python 下的正确性必需品
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def getSum(self, a: int, b: int) -> int:
        a &= MASK                                 # ! 先把输入也规整成 32 位无符号表示
        b &= MASK
        while b != 0:
            carry = ((a & b) << 1) & MASK         # ! & MASK 防止高位无限生长（关键！）
            a = (a ^ b) & MASK                    # ! 无进位和
            b = carry                             # ! 把进位当成新的加数，再加一轮
        # ! 还原成 Python 的有符号整数
        return a if a <= MAX_INT else ~(a ^ MASK)


##################################################################################################
##### ! Solution 2: 递归版（同一个恒等式，写成递归更能看出「再加一次」的结构）
##### ! 时间复杂度: O(1)（递归深度 <= 32）   空间复杂度: O(1)（递归栈，固定深度）
##### ! 适用：想强调 a+b == (a^b) + ((a&b)<<1) 这个递归式时
##################################################################################################


class Solution_2:
    def getSum(self, a: int, b: int) -> int:
        def helper(x: int, y: int) -> int:
            if y == 0:
                return x
            # ! a + b 恒等于 (无进位和) + (进位)，所以可以递归
            return helper((x ^ y) & MASK, ((x & y) << 1) & MASK)

        res = helper(a & MASK, b & MASK)
        return res if res <= MAX_INT else ~(res ^ MASK)


##################################################################################################
##### ! Solution 3: 逐位处理 + 显式 carry（最接近硬件全加器，便于讲解）
##### ! 时间复杂度: O(32)   空间复杂度: O(1)
##### ! 适用：讲「全加器真值表」时。一位一位算，和手算竖式一模一样
##################################################################################################


class Solution_3:
    def getSum(self, a: int, b: int) -> int:
        a &= MASK
        b &= MASK
        res = 0
        carry = 0
        for i in range(32):
            bit_a = (a >> i) & 1
            bit_b = (b >> i) & 1
            # ! 全加器：本位 = 三个输入的 XOR；进位 = 至少两个输入为 1
            total = bit_a + bit_b + carry
            res |= (total & 1) << i
            carry = 1 if total >= 2 else 0
        # ! 第 32 位的进位直接丢弃（32 位溢出的定义）
        return res if res <= MAX_INT else ~(res ^ MASK)


##################################################################################################
##### ! Solution 4: 会死循环的错误写法（保留下来，作为「为什么必须 MASK」的反面教材）
##### ! 时间复杂度: 负数输入下 **永不终止**   空间复杂度: O(1)
##### ! 适用：仅用于演示。下面的测试给它加了轮数上限来证明它确实不收敛
##################################################################################################


class Solution_4_BROKEN:
    def getSum(self, a: int, b: int, _max_rounds: int = 200) -> int:
        """没有 MASK 的版本 —— 在 C++ 里对，在 Python 里负数会挂死。"""
        rounds = 0
        while b != 0:
            rounds += 1
            if rounds > _max_rounds:
                raise RuntimeError("不收敛：Python 的负数是无限位补码，carry 永远有 1 可以左移")
            a, b = a ^ b, (a & b) << 1
        return a


if __name__ == "__main__":
    import random

    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        # ! 指令点名要测的六组
        assert s.getSum(1, 2) == 3
        assert s.getSum(2, 3) == 5
        assert s.getSum(-1, 1) == 0
        assert s.getSum(-2, 3) == 1
        assert s.getSum(-5, -7) == -12
        assert s.getSum(0, 0) == 0
        # ! 32 位边界
        assert s.getSum(-1, 0) == -1
        assert s.getSum(2147483647, 0) == 2147483647
        assert s.getSum(-2147483648, 0) == -2147483648
        assert s.getSum(2147483647, -2147483648) == -1
        assert s.getSum(-2147483648, 2147483647) == -1
        assert s.getSum(1000, -1000) == 0

    print("getSum(1, 2)   =", Solution_1().getSum(1, 2))
    print("getSum(-1, 1)  =", Solution_1().getSum(-1, 1))
    print("getSum(-5, -7) =", Solution_1().getSum(-5, -7))

    # ! 证明「不加 MASK 真的会死循环」—— 这不是理论担忧
    try:
        Solution_4_BROKEN().getSum(-1, 1)
        raise AssertionError("预期它不收敛，但它居然返回了")
    except RuntimeError as e:
        print("✓ 无 MASK 版本在 (-1, 1) 上确实不收敛：", e)
    # ! 但它对两个非负数是对的（所以在 C++ 里看起来"没问题"）
    assert Solution_4_BROKEN().getSum(1, 2) == 3

    for _ in range(20000):                        # ! 随机对拍，覆盖正/负/零与边界附近
        a = random.choice([
            random.randint(-50, 50),
            random.randint(-1000, 1000),
            random.randint(-2**31, 2**31 - 1),
            random.choice([0, -1, 1, 2**31 - 1, -2**31]),
        ])
        b = random.choice([
            random.randint(-50, 50),
            random.randint(-2**31, 2**31 - 1),
            random.choice([0, -1, 1, 2**31 - 1, -2**31]),
        ])
        want = a + b
        if not (-2**31 <= want <= 2**31 - 1):     # ! 题目保证和在 32 位内
            continue
        r1 = Solution_1().getSum(a, b)
        r2 = Solution_2().getSum(a, b)
        r3 = Solution_3().getSum(a, b)
        assert r1 == r2 == r3 == want, (a, b, want, r1, r2, r3)
    print("随机对拍 20000 组通过 ✓（迭代半加器 == 递归 == 逐位全加器 == 真实的 a+b）")
