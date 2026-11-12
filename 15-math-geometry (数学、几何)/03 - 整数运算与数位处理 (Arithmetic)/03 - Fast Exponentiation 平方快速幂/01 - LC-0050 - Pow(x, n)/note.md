# Pow(x, n) 笔记（2026-09-10）

信号→模式："指数级重复操作（幂/斐波那契矩阵/重复拼接）→ 折半：f(n) 由 f(n//2) 平方拼出，奇数补零头，O(n) 变 O(log n)。"

和位运算手册还有个暗中呼应：k // 2 和 k % 2 就是 k >> 1 和 k & 1——快速幂本质上是沿着指数的二进制位逐位处理（T4 骨架的又一张面孔），这也是它名字里 Binary 的由来。

守卫：
- `(2, -3) → 0.125`（负指数）
- `(2, 0) → 1`（零指数）
- `(0, 5) → 0`（零底数）
- `(1.0000001, 2147483647) → 应瞬间返回`（专杀 O(n) 版：裸循环在这里超时——这就是你的疤痕）

## 去重记录

2026-09-10 之前题库里有两份 LC-0050：本文件夹（2024-02-25，带 cache 的递归）和 `05-binary-search/general`（2025-10-03，递归 + 迭代两解法）。保留本文件夹，另一份移到了 `$$-垃圾-可忽略/LC-0050 - Pow(x, n) (dup from 05-binary-search-general)`，里面的迭代版（result *= x 当 n 为奇数，x *= x，n //= 2）值得回头看一眼。

### 📝 2026-09-15 - retry 1

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def dp(x: float, k: int) -> float:
            # 只算 x^k,k >= 0,不认识负数——职责单一
            if k == 0:
                return 1.0                # base 罩住 0(2^0 = 1)
            h = dp(x, k // 2)             # 一半只算一次!
            if k % 2 == 1:
                return h * h * x
            return h * h

        res = dp(x, abs(n))
        return res if n >= 0 else 1 / res    # 符号在门外,处理恰好一次
```

### 📝 2026-09-21 - retry 2

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def dfs(x: float, k: int) -> float:
            if k == 0: # ! 这里只需要 k == 0 的 base case 即可, 不需要 k == 1 的情况
                return 1.0
            half = dfs(x, k // 2)
            return half * half * (x if k % 2 else 1)

        res = dfs(x, abs(n)) # ! 别忘记这里一定要是 abs 才行
        # ! 我们不需要将 n 是负数的情况放在 dfs 函数里, 那样就太复杂了, 我们在最外层只对它算一次
        return res if n >= 0 else 1 / res 
```

### 📝 2026-09-30 - retry 3

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def dfs(x: float, n: int) -> float:
            # ! 这里只需要一个 if 判断语句即可
            if n == 0:
                return 1
            half = dfs(x, n // 2)
            return half * half * (x if n % 2 else 1)

        # ! 这里一定要是 abs(n)
        res = dfs(x, abs(n))
        # ! 这里一定要考虑负数的情况
        return res if n >= 0 else 1 / res
```
