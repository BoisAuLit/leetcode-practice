# Counting Bits 笔记（2026-09-09）

就是一句话 `dp[i] = dp[i >> 1] + (i & 1)`，很无脑；凭自己想的话自己一辈子都推导不出来，就是死记硬背的傻逼玩意儿。

### 💬 2026-09-15 - finish 🔴

毫无技术可言, 就是 dp[i] = dp[i >> 1] + (i & 1) 死记硬背, 只有这个方法可以记住, 多写十遍就终身难忘了

### 📝 2026-09-26 - retry 1

```python
class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)
        for i in range(n + 1):
            # ! 这里的 (i & 1) 必须要加括号!
            dp[i] = dp[i >> 1] + (i & 1)
        return dp
```
