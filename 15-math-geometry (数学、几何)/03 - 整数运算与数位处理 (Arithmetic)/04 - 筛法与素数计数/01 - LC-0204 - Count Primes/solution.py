"""LC-0204 - Count Primes     ★ 第二轮审核新增（唯一一道「预处理筛表」算法）

Level 1 · 03 整数运算与数位处理 —— **Sieve of Eratosthenes（埃氏筛）**
题目在问：返回**严格小于 `n`** 的素数个数。

### 决定性观察：不要逐个判素数，要「反过来划掉所有合数」

朴素做法是对每个 `i` 做试除判素（`O(n√n)`），`n = 5×10^6` 会 TLE。
**筛法把问题反过来**：

> 不去问「`i` 是不是素数」，而是**从每个素数出发，把它的倍数全部划掉**。
> 划完之后没被划掉的就是素数。

```python
is_prime = [True] * n
is_prime[0] = is_prime[1] = False
for i in range(2, int(n**0.5) + 1):
    if is_prime[i]:
        for j in range(i * i, n, i):      # ! 从 i*i 开始，步长 i
            is_prime[j] = False
return sum(is_prime)
```

### 两个关键优化，各有一句话的理由

**① 外层只到 `√n` 就够**
若 `n` 有一个大于 `√n` 的因子 `a`，则配对因子 `b = n/a < √n`
⟹ 这个合数早就被 `b`（或 `b` 的某个素因子）划掉了。
所以**每个合数都至少有一个 ≤ √n 的素因子** ⟹ 外层超过 `√n` 后不会再划掉新东西。∎

**② 内层从 `i*i` 开始，不是从 `2*i`**
`i` 的倍数中小于 `i*i` 的那些 —— `2i, 3i, …, (i-1)i` ——
都含有一个**比 `i` 小的因子**（`2, 3, …, i-1`）
⟹ 它们在处理那个更小的因子时**已经被划掉了**。从 `i*i` 开始纯属省功。∎

> 这两条都是「避免重复工作」，不是正确性要求 ——
> 去掉它们答案仍对，只是更慢。**但面试一定会问为什么。**

### 复杂度为什么是 O(n log log n)

总操作数 = `Σ_{p 是素数, p<n} n/p` = `n · Σ 1/p`。
由 Mertens 定理，`Σ_{p<n} 1/p ≈ ln ln n + M`
⟹ 总共 **O(n log log n)**，几乎是线性的。

对 `n = 5×10^6`：`log log n ≈ 2.8` ⟹ 实际只比一次线性扫描慢几倍。
空间 **O(n)**（一个布尔数组）。

| 做法 | 时间 | `n = 5×10^6` 能过吗 |
|---|---|---|
| 逐个试除到 `√i` | O(n√n) | ❌ TLE |
| **埃氏筛** | **O(n log log n)** | ✅ |
| 线性筛（欧拉筛） | **O(n)** | ✅（但代码更长，收益有限） |

### ⚠️ 边界：`n <= 2` 必须返回 0

题目要的是**严格小于 `n`** 的素数个数：
- `n = 0` → 0
- `n = 1` → 0
- `n = 2` → **0**（2 不小于 2！）
- `n = 3` → 1（只有 2）

`is_prime = [True] * n` 在 `n = 0` 或 `1` 时长度不足，
`is_prime[0] = is_prime[1] = False` 会越界 ⟹ **必须先 `if n < 3: return 0`**。
这是本题最常见的提交失败原因。

### 为什么这道题值得单独收录（第二轮审核的理由）

本专题刻意**不扩充数论**（不收 FFT、不收高级数论定理、不收复杂组合数学）。
但埃氏筛是例外：

- **A 填补缺口**：这是本专题唯一一道「**预处理出一张表，之后 O(1) 查询**」的算法，
  和其他题的「单次计算」是完全不同的思维方式。
- **B 面试代表性**：筛法是最经典的面试算法之一。
- **C 可迁移性**：同一张表直接支持**最小质因子分解**、
  LC-0279 Perfect Squares、LC-1175 Prime Arrangements、LC-2521 等一大批题。
- **E 记忆成本**：核心就 5 行，两个优化各一句话。

> **它不是「一个需要背的数论定理」，而是「一个可复用的预处理模板」** ——
> 这正是本专题想要的那类知识。

复杂度：解法 1 **O(n log log n)** / O(n)；解法 2（线性筛）**O(n)** / O(n)；
       解法 3（试除）**O(n√n)** / O(1)。

边界：
  - `n = 0` / `n = 1` / `n = 2` → **0**
  - `n = 3` → 1
  - `n = 10` → 4（2, 3, 5, 7）
  - `n = 4` → 2（2, 3）
  - 完全平方数边界 `n = 25` → 9（`i*i` 优化的试金石）
"""

from typing import List


##################################################################################################
##### ! Solution 1: Sieve of Eratosthenes（外层到 √n，内层从 i*i 起，切片批量赋值）
##### ! 时间复杂度: O(n log log n)   空间复杂度: O(n)
##### ! 适用：所有「n 以内所有素数 / 需要素数表」的问题；本题的标准答案
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def countPrimes(self, n: int) -> int:
        if n < 3:
            return 0                            # ! n=0,1,2 都是 0（2 不小于 2）
        is_prime = [True] * n
        is_prime[0] = is_prime[1] = False
        i = 2
        while i * i < n:                        # ! 外层只到 √n
            if is_prime[i]:
                # ! 从 i*i 开始；Python 切片赋值比 for 循环快一个常数量级
                start = i * i
                count = (n - start + i - 1) // i
                is_prime[start::i] = [False] * count
            i += 1
        return sum(is_prime)


##################################################################################################
##### ! Solution 2: 线性筛（欧拉筛）—— 每个合数只被它的最小质因子划掉一次
##### ! 时间复杂度: O(n)   空间复杂度: O(n)
##### ! 适用：需要顺便拿到「每个数的最小质因子」做分解时；纯计数场合收益有限
##################################################################################################


class Solution_2:
    def countPrimes(self, n: int) -> int:
        if n < 3:
            return 0
        smallest_factor = [0] * n               # ! smallest_factor[x] = x 的最小质因子
        primes: List[int] = []
        for i in range(2, n):
            if smallest_factor[i] == 0:
                smallest_factor[i] = i
                primes.append(i)                # ! 没被标记过 ⟹ i 是素数
            for p in primes:
                if p > smallest_factor[i] or i * p >= n:
                    break                       # ! 关键：p 超过 i 的最小质因子就停
                smallest_factor[i * p] = p      # ! 保证 i*p 只被最小质因子 p 划掉一次
        return len(primes)


##################################################################################################
##### ! Solution 3: 逐个试除判素（基准答案，n 大时会 TLE）
##### ! 时间复杂度: O(n√n)   空间复杂度: O(1)
##### ! 适用：仅用于对拍。对比之下能看清筛法省掉的到底是什么
##################################################################################################


class Solution_3:
    def countPrimes(self, n: int) -> int:
        def is_prime(x: int) -> bool:
            if x < 2:
                return False
            d = 2
            while d * d <= x:                   # ! 只试除到 √x，同样的配对因子论证
                if x % d == 0:
                    return False
                d += 1
            return True

        return sum(1 for x in range(2, n) if is_prime(x))


if __name__ == "__main__":
    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert s.countPrimes(10) == 4           # ! 2, 3, 5, 7
        assert s.countPrimes(0) == 0
        assert s.countPrimes(1) == 0
        assert s.countPrimes(2) == 0            # ! 严格小于 2 ⟹ 没有素数
        assert s.countPrimes(3) == 1
        assert s.countPrimes(4) == 2
        assert s.countPrimes(25) == 9           # ! 完全平方数边界
        assert s.countPrimes(100) == 25
        assert s.countPrimes(1000) == 168

    print("countPrimes(10) =", Solution_1().countPrimes(10), "(2,3,5,7)")
    print("countPrimes(2)  =", Solution_1().countPrimes(2), "(严格小于 2 ⟹ 0)")
    print("countPrimes(1000) =", Solution_1().countPrimes(1000))

    for n in range(0, 600):                     # ! 穷举对拍 0..599，三种实现必须一致
        a = Solution_1().countPrimes(n)
        b = Solution_2().countPrimes(n)
        c = Solution_3().countPrimes(n)
        assert a == b == c, (n, a, b, c)
    print("穷举对拍 n = 0..599 通过 ✓（埃氏筛 == 线性筛 == 试除暴力）")

    # ! 顺带验证一下筛表能直接复用做质因数分解（可迁移性的具体体现）
    N = 100
    sf = [0] * N
    for i in range(2, N):
        if sf[i] == 0:
            for j in range(i, N, i):
                if sf[j] == 0:
                    sf[j] = i                   # ! sf[j] = j 的最小质因子
    def factorize(x: int):
        out = []
        while x > 1:
            p = sf[x]
            out.append(p)
            x //= p
        return out
    assert factorize(84) == [2, 2, 3, 7]
    assert factorize(97) == [97]
    print("同一张筛表做质因数分解：84 ->", factorize(84), " 97 ->", factorize(97))
