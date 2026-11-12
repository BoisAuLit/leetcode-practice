"""LC-1797 - Design Authentication Manager     ★ 第二轮审核新增（Expiration Semantics）

Level 1 · 04 时间窗口、计数器与限流 —— **过期语义（Expiration）+ 懒清理**
API：
  - `AuthenticationManager(timeToLive)`：token 的存活时长
  - `generate(tokenId, currentTime)`：生成一个在 `currentTime + ttl` **过期**的 token
  - `renew(tokenId, currentTime)`：若该 token **存在且未过期**，把过期时间重置为
    `currentTime + ttl`；否则**什么都不做**
  - `countUnexpiredTokens(currentTime) -> int`：当前未过期的 token 数

---

## 决定性观察：**只存「过期时刻」，不存「生成时刻」**

```python
self.expiry = {}        # ! tokenId -> 过期时刻
```

**为什么存过期时刻而不是生成时刻？**
判断「是否过期」是最频繁的操作。
- 存过期时刻 ⟹ `expiry[t] > now`，**一次比较**
- 存生成时刻 ⟹ `created[t] + ttl > now`，每次都要**再加一次**

而 `renew` 本来就是「重置过期时刻」⟹ 直接赋值 `expiry[t] = now + ttl`。
**存过期时刻让三个操作都变成最简形式。**

---

## ⚠️ 过期语义：`> now` 还是 `>= now`？

题目说「token 在 `generate` 之后恰好 `timeToLive` 秒**过期**」，
且「**过期发生在那个时刻**」。所以：

```python
unexpired  ⟺  expiry > currentTime        # ! 严格大于
```

**具体验证**（`ttl = 5`，`generate("a", 1)` ⟹ `expiry = 6`）：

| `currentTime` | `expiry > now`？ | 语义 |
|---|---|---|
| 5 | `6 > 5` ✅ | 还活着 |
| **6** | `6 > 6` ❌ | **恰好过期**（这一刻已经无效） |
| 7 | `6 > 7` ❌ | 早就过期 |

写成 `>=` 会让 token 多活一个时刻 ⟹ **`renew` 会复活一个已死的 token**，
`countUnexpiredTokens` 也会多数一个。
**这是本题唯一的坑**，而且官方样例恰好能测出来。

> 和 [LC-0359 Logger Rate Limiter](<../01 - LC-0359 - Logger Rate Limiter>) 的不等号正好相反：
> 359 是「`now - last >= 10` 才允许打印」（**允许**恰好 10 秒），
> 本题是「`expiry > now` 才算活着」（**不允许**恰好到期）。
> **两题的边界语义必须分开记** —— 见下面的对照表。

---

## 两种实现的取舍：懒清理 vs 主动清理

### 解法 1：懒清理（Lazy Cleanup）—— 推荐

```python
def countUnexpiredTokens(self, now):
    return sum(1 for e in self.expiry.values() if e > now)      # ! O(n)
```
**不主动删过期项**，只在计数时过滤。
- `generate` / `renew`：**O(1)**
- `countUnexpiredTokens`：**O(n)**（`n` = 历史 token 总数）
- 空间：**O(n)**，过期的也占着

**本题约束下完全够用**：`generate + renew + count <= 2000` 次 ⟹ 最坏 400 万次比较。

### 解法 2：计数时顺便清理（Amortized Cleanup）

```python
def countUnexpiredTokens(self, now):
    for t in [t for t, e in self.expiry.items() if e <= now]:
        del self.expiry[t]                # ! 过期的永远不会复活 ⟹ 可以安全删
    return len(self.expiry)
```
**为什么可以安全删？**
`currentTime` **单调不减**（题目保证）⟹ 一旦 `expiry <= now`，
对后续更大的 `now'` 必然还有 `expiry <= now'` ⟹ **永久失效，不会复活**。∎

- `countUnexpiredTokens`：**均摊 O(1) + O(本次删除数)**
  （每个 token 一生最多被删一次 ⟹ 总删除代价 O(n)）
- 空间：**O(当前存活数)**，更省

### 解法 3：按过期时刻排序的堆 / 有序结构

把 `(expiry, tokenId)` 放进最小堆，计数时弹掉所有 `expiry <= now` 的。
**问题**：`renew` 会**改变**某个 token 的 expiry，堆里的旧条目变成**陈旧数据**
⟹ 需要**懒删除**（弹出时用 `self.expiry[t] == e` 校验是不是最新条目）。

这和 [LC-1851](<../../../14-intervals (区间)/05 - 离线区间查询与动态预订/01 - 最短覆盖区间的离线查询/01 - LC-1851 - Minimum Interval to Include Each Query>)
的懒删除堆、`09-heap` 的双堆懒删除是**同一套技巧**。
**本题规模不需要它**，但它是「过期 + 可更新」的通用解法。

> **三种解法的分界线**：
> 查询次数少 ⟹ 懒清理（解法 1）；
> 要省空间 ⟹ 计数时清理（解法 2）；
> 要 O(log n) 单次查询 ⟹ 堆 + 懒删除（解法 3）。

---

## 本 Level 1 四道题的「时间语义」对照表（最该记的一张）

| 题 | 存什么 | 判定条件 | 边界含义 |
|---|---|---|---|
| [LC-0933 Recent Calls](<../../01 - Recent Calls 与流式时间窗口/01 - LC-0933 - Number of Recent Calls>) | 请求时刻的队列 | 弹掉 `t < now - 3000` | 窗口是 **`[now-3000, now]` 闭区间** |
| [LC-0362 Hit Counter](<../../01 - Recent Calls 与流式时间窗口/02 - LC-0362 - Design Hit Counter>) | 环形数组 / 队列 | 保留 `t > now - 300` | 窗口是**过去 300 秒** |
| [LC-0359 Logger Rate Limiter](<../01 - LC-0359 - Logger Rate Limiter>) | message -> 上次打印时刻 | `now - last >= 10` **才允许** | **允许**恰好 10 秒 |
| **LC-1797** 本题 | token -> **过期时刻** | `expiry > now` **才算活** | **不允许**恰好到期 |

> **四道题都在做「时间窗口」，但不等号各不相同。**
> 唯一可靠的办法：**拿官方样例的边界时刻手算一遍**，别凭感觉。

---

## 核心不变量

> 任意时刻，`expiry[t]` 恒等于「token `t` 最近一次 `generate`/`renew`
> 所确定的过期时刻」。
> 且 `t` 未过期 ⟺ `expiry[t] > currentTime`。

**`renew` 对已过期 token 必须是 no-op**：
```python
if self.expiry.get(tokenId, -1) > currentTime:      # ! 不存在时 get 返回 -1，恒不 > now
    self.expiry[tokenId] = currentTime + self.ttl
```
一行同时处理了「不存在」和「已过期」两种情况 —— **不需要两个 if**。

---

复杂度：

| 操作 | 解法 1（懒清理） | 解法 2（计数时清理） |
|---|---|---|
| `generate` | **O(1)** | O(1) |
| `renew` | **O(1)** | O(1) |
| `countUnexpiredTokens` | **O(n)** | **均摊 O(当前存活数)** |
| 空间 | O(历史总数) | **O(当前存活数)** |

⚠️ 都是**平均** O(1)（哈希表）。
⚠️ 解法 1 的 `count` **不是 O(1)** —— 不要声称「全部 O(1)」。

边界：
  - `renew` 一个**不存在**的 token → no-op
  - `renew` 一个**恰好过期**的 token（`expiry == now`）→ **no-op**（不能复活）
  - `renew` 一个还活着的 token → 过期时刻重置
  - `countUnexpiredTokens` 在恰好过期的时刻 → **不计入**
  - `generate` 重复的 tokenId → 覆盖（题目保证不会，但实现天然支持）
  - 所有 token 都过期 → 返回 0
  - `ttl = 1` → 下一个时刻就过期
"""

from typing import Dict


##################################################################################################
##### ! Solution 1: 只存过期时刻 + 懒清理（计数时过滤）
##### ! 时间复杂度: generate/renew O(1)，count O(n)   空间复杂度: O(历史 token 总数)
##### ! 适用：本题约束（总操作 <= 2000）下的默认答案；三个方法都最简
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class AuthenticationManager_1:
    def __init__(self, timeToLive: int):
        self.ttl = timeToLive
        self.expiry: Dict[str, int] = {}          # ! tokenId -> 过期时刻（不是生成时刻！）

    def generate(self, tokenId: str, currentTime: int) -> None:
        self.expiry[tokenId] = currentTime + self.ttl

    def renew(self, tokenId: str, currentTime: int) -> None:
        # ! get(.., -1) 让「不存在」和「已过期」走同一个分支；> 是严格大于
        if self.expiry.get(tokenId, -1) > currentTime:
            self.expiry[tokenId] = currentTime + self.ttl

    def countUnexpiredTokens(self, currentTime: int) -> int:
        # ! 懒清理：不删过期项，只在计数时过滤
        return sum(1 for e in self.expiry.values() if e > currentTime)


##################################################################################################
##### ! Solution 2: 计数时顺便清理过期项（均摊 O(1)，空间只占存活数）
##### ! 时间复杂度: generate/renew O(1)，count 均摊 O(存活数)   空间复杂度: O(存活数)
##### ! 适用：token 很多而查询频繁时。正确性依赖 currentTime 单调不减
##################################################################################################


class AuthenticationManager_2:
    def __init__(self, timeToLive: int):
        self.ttl = timeToLive
        self.expiry: Dict[str, int] = {}

    def generate(self, tokenId: str, currentTime: int) -> None:
        self.expiry[tokenId] = currentTime + self.ttl

    def renew(self, tokenId: str, currentTime: int) -> None:
        if self.expiry.get(tokenId, -1) > currentTime:
            self.expiry[tokenId] = currentTime + self.ttl

    def countUnexpiredTokens(self, currentTime: int) -> int:
        # ! currentTime 单调不减 ⟹ 过期的永远不会复活 ⟹ 可以安全删掉
        dead = [t for t, e in self.expiry.items() if e <= currentTime]
        for t in dead:
            del self.expiry[t]
        return len(self.expiry)                   # ! 剩下的全都是活的


##################################################################################################
##### ! Solution 3: 最小堆按过期时刻排序 + 懒删除（陈旧条目用 expiry 表校验）
##### ! 时间复杂度: generate/renew O(log n)，count 均摊 O(log n)   空间复杂度: O(n)
##### ! 适用：需要单次 O(log n) 的大规模场景。renew 会产生陈旧条目 ⟹ 必须懒删除
##################################################################################################


class AuthenticationManager_3:
    def __init__(self, timeToLive: int):
        self.ttl = timeToLive
        self.expiry: Dict[str, int] = {}          # ! 真相表：token -> 最新的过期时刻
        self.heap = []                            # ! (过期时刻, token)，可能含陈旧条目
        self.alive = 0

    def _purge(self, currentTime: int) -> None:
        import heapq

        while self.heap and self.heap[0][0] <= currentTime:
            e, t = heapq.heappop(self.heap)
            # ! 只有当这条确实是该 token 的最新记录时，才真的算它死了
            if self.expiry.get(t) == e:
                del self.expiry[t]
                self.alive -= 1
            # ! 否则它是 renew 留下的陈旧条目 ⟹ 直接丢弃

    def generate(self, tokenId: str, currentTime: int) -> None:
        import heapq

        self._purge(currentTime)
        if tokenId not in self.expiry:
            self.alive += 1
        e = currentTime + self.ttl
        self.expiry[tokenId] = e
        heapq.heappush(self.heap, (e, tokenId))

    def renew(self, tokenId: str, currentTime: int) -> None:
        import heapq

        self._purge(currentTime)
        if self.expiry.get(tokenId, -1) > currentTime:
            e = currentTime + self.ttl
            self.expiry[tokenId] = e              # ! 更新真相表
            heapq.heappush(self.heap, (e, tokenId))   # ! 旧条目留在堆里，靠校验识别

    def countUnexpiredTokens(self, currentTime: int) -> int:
        self._purge(currentTime)
        return self.alive


if __name__ == "__main__":
    import random

    for cls in (AuthenticationManager_1, AuthenticationManager_2, AuthenticationManager_3):
        # ! LeetCode 官方样例（ttl = 5）
        a = cls(5)
        a.renew("aaa", 1)                       # ! 不存在 ⟹ no-op
        a.generate("aaa", 2)                    # ! expiry = 7
        assert a.countUnexpiredTokens(6) == 1   # ! 7 > 6 ⟹ 活着
        a.generate("bbb", 7)                    # ! expiry = 12
        a.renew("aaa", 8)                       # ! aaa 的 expiry 是 7，7 > 8 为假 ⟹ no-op
        a.renew("bbb", 10)                      # ! 12 > 10 ⟹ 续期到 15
        assert a.countUnexpiredTokens(15) == 0  # ! 15 > 15 为假 ⟹ 恰好过期，不计入

        # ! 「恰好到期」的边界：expiry == now 时必须算已过期
        b = cls(5)
        b.generate("t", 1)                      # ! expiry = 6
        assert b.countUnexpiredTokens(5) == 1   # ! 6 > 5 ⟹ 活
        assert b.countUnexpiredTokens(6) == 0   # ! 6 > 6 ⟹ 死（这里写 >= 就错）

        # ! renew 一个恰好过期的 token 不能复活它
        c = cls(5)
        c.generate("t", 1)                      # ! expiry = 6
        c.renew("t", 6)                         # ! 6 > 6 为假 ⟹ no-op
        assert c.countUnexpiredTokens(6) == 0
        assert c.countUnexpiredTokens(7) == 0

        # ! ttl = 1：下一个时刻就过期
        d = cls(1)
        d.generate("x", 10)                     # ! expiry = 11
        assert d.countUnexpiredTokens(10) == 1
        assert d.countUnexpiredTokens(11) == 0

        # ! 所有 token 都过期
        e = cls(2)
        e.generate("p", 1); e.generate("q", 1)
        assert e.countUnexpiredTokens(2) == 2
        assert e.countUnexpiredTokens(3) == 0

    a = AuthenticationManager_1(5)
    a.generate("aaa", 2)
    print("ttl=5, generate('aaa', 2) ⟹ expiry = 7")
    print("  count(6) =", a.countUnexpiredTokens(6), "(7 > 6 ⟹ 活)")
    print("  count(7) =", a.countUnexpiredTokens(7), "(7 > 7 ⟹ 恰好过期，死)")

    for _ in range(3000):                       # ! 随机对拍（currentTime 单调不减）
        ttl = random.randint(1, 6)
        ops, t = [], 0
        tokens = ["a", "b", "c"]
        for _ in range(random.randint(1, 30)):
            t += random.randint(0, 3)           # ! 时间单调不减（题目保证）
            r = random.random()
            if r < 0.4:
                ops.append(("gen", random.choice(tokens), t))
            elif r < 0.7:
                ops.append(("renew", random.choice(tokens), t))
            else:
                ops.append(("count", None, t))
        outs = []
        for cls in (AuthenticationManager_1, AuthenticationManager_2, AuthenticationManager_3):
            m = cls(ttl)
            seq = []
            for op, tok, tt in ops:
                if op == "gen":
                    m.generate(tok, tt); seq.append(None)
                elif op == "renew":
                    m.renew(tok, tt); seq.append(None)
                else:
                    seq.append(m.countUnexpiredTokens(tt))
            outs.append(seq)
        # ! 独立真值：照定义维护一张 dict，count 时现场过滤
        truth, exp = [], {}
        for op, tok, tt in ops:
            if op == "gen":
                exp[tok] = tt + ttl; truth.append(None)
            elif op == "renew":
                if exp.get(tok, -1) > tt:
                    exp[tok] = tt + ttl
                truth.append(None)
            else:
                truth.append(sum(1 for v in exp.values() if v > tt))
        assert outs[0] == outs[1] == outs[2] == truth, (ttl, ops, outs, truth)
    print("随机对拍 3000 组通过 ✓（懒清理 == 计数时清理 == 堆+懒删除 == 定义真值）")
