"""LC-1472 - Design Browser History

Level 1 · 05 有状态 API、缓冲区与模拟 —— **Array Cursor（数组 + 游标）**
API：
  - `BrowserHistory(homepage)`：从 `homepage` 开始
  - `visit(url)`：访问 `url`，并**清空所有前进历史**
  - `back(steps) -> str`：最多后退 `steps` 步，返回当前页
  - `forward(steps) -> str`：最多前进 `steps` 步，返回当前页

---

## 决定性观察：**一个数组 + 一个游标 + 一个「有效长度」**

```python
self.history = [homepage]      # ! 历史序列
self.cur = 0                   # ! 当前位置的下标
self.last = 0                  # ! 最后一个有效下标（前进的上界）
```

三个操作各一行核心逻辑：

```python
def visit(url):
    self.cur += 1
    self.history[self.cur] = url      # ! 覆盖写（或 append）
    self.last = self.cur              # ! ⚠️ 关键：把前进历史「作废」

def back(steps):
    self.cur = max(0, self.cur - steps)         # ! 夹到 0
    return self.history[self.cur]

def forward(steps):
    self.cur = min(self.last, self.cur + steps) # ! 夹到 last
    return self.history[self.cur]
```

---

## 三个必须想清的点

### ① `visit` 为什么要「清空前进历史」—— 而且怎么做到 O(1)？

真实浏览器的行为：你后退几步再打开一个新页面，**原来的前进历史就没了**。

**不要真的删除数组元素**（那是 O(n)）。
只需要把 `last = cur` —— 之后 `forward` 的上界就是 `cur`
⟹ **旧的前进历史在逻辑上不可达了**，物理上留在数组里也没关系。

> **这是整道题的关键技巧：用「有效长度」代替「真删除」。**
> 同样的思路出现在所有「逻辑删除 / 墓碑标记」的设计里。

**如果用 `list.append` + `del`**：
```python
self.history = self.history[:self.cur + 1]   # ! O(n) 切片
self.history.append(url)
```
能跑对，但 `visit` 变成 **O(n)**。题目有 `5 * 10^4` 次操作 ⟹ 最坏 O(n²)。
**用游标 + `last` 才是 O(1)。**

### ② `back` / `forward` 为什么用 `max` / `min` 而不是报错？

题目说「**最多**后退 `steps` 步」——
不够退就退到头（`index 0`），不够进就进到尾（`index last`）。
`max(0, ...)` 和 `min(last, ...)` 一行搞定，**不需要任何 if**。

### ③ 为什么需要 `last` 而不是只用 `len(history)`？

因为**采用「覆盖写」策略时，数组长度不等于有效长度**。
例如：visit 了 5 个页面（`len == 6`），然后 `back(3)`（`cur == 2`），
再 visit 一个新页面 ⟹ 写在下标 3，`last = 3`。
此时 `len(history)` 可能还是 6（下标 4、5 是**作废的旧数据**）
⟹ 必须用 `last` 而不是 `len - 1` 当前进上界。

---

## 两种实现的取舍

| | **数组 + 游标**（解法 1、2） | **双栈**（解法 3） |
|---|---|---|
| `visit` | **O(1)** | **O(1)**（清空 forward 栈是 O(k)，但均摊 O(1)） |
| `back(steps)` | **O(1)** ⟹ 直接跳 | **O(steps)** ⟹ 要一个个搬 |
| `forward(steps)` | **O(1)** | **O(steps)** |
| 空间 | O(访问总数) | O(访问总数) |
| 直观性 | 需要想清 `last` | 更像「浏览器」的心智模型 |

> **数组 + 游标在 `back(steps)` 上严格更优**（O(1) vs O(steps)）。
> 双栈版保留在本文件里，因为它是**面试里最常被先想到的方案**，
> 而「发现它的 back 是 O(steps)，然后换成游标」正是这道题想考的推理。

**双栈版的 `visit` 为什么是均摊 O(1)？**
清空 `forward` 栈的代价是 O(k)，但这 `k` 个元素每个都是之前某次 `back`
推进去的，每个元素一生最多被清空一次 ⟹ **均摊 O(1)**。

---

## 和本 Level 2 另一题的共同点

| | [LC-0348 Tic-Tac-Toe](<../01 - LC-0348 - Design Tic-Tac-Toe>) | **LC-1472** 本题 |
|---|---|---|
| 跨调用的状态 | 每行/列/对角线的**计数** | **历史数组 + 游标 + 有效长度** |
| 核心技巧 | **更新时就算好**（不扫棋盘判胜负） | **逻辑删除**（不真删前进历史） |
| 共同点 | 都把 O(n) 的查询变成 **O(1)** | 同 |

> **设计题的通用套路：把「查询时才做的工作」挪到「更新时」，
> 或者把「真实的删除」换成「标记为不可达」。**

---

复杂度：

| 操作 | 解法 1/2（游标） | 解法 3（双栈） |
|---|---|---|
| `visit` | **O(1)** | O(1) 均摊 |
| `back(steps)` | **O(1)** | **O(steps)** |
| `forward(steps)` | **O(1)** | **O(steps)** |
| 空间 | **O(访问总数)** | O(访问总数) |

边界：
  - `back(100)` 在首页 → 停在 homepage（**不报错**）
  - `forward(100)` 在最新页 → 停在最新页
  - `visit` 之后立刻 `forward(1)` → **停在原地**（前进历史已作废）
  - `back(0)` / `forward(0)` → 原地不动
  - 只有 homepage，没 visit 过 → `back` / `forward` 都返回 homepage
  - 后退几步后 visit 新页，再后退 → 走的是**新**路径
  - 反复 `visit` 同一个 url → 每次都是新的历史项
"""


##################################################################################################
##### ! Solution 1: 数组 + 游标 cur + 有效长度 last（三个操作全 O(1)）
##### ! 时间复杂度: visit / back / forward 全部 O(1)   空间复杂度: O(访问总数)
##### ! 适用：所有「历史导航 / undo-redo」设计题。关键是用 last 做逻辑删除
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class BrowserHistory_1:
    def __init__(self, homepage: str):
        self.history = [homepage]
        self.cur = 0                            # ! 当前页的下标
        self.last = 0                           # ! 最后一个有效下标（forward 的上界）

    def visit(self, url: str) -> None:
        self.cur += 1
        if self.cur < len(self.history):
            self.history[self.cur] = url        # ! 覆盖写，复用已有空间
        else:
            self.history.append(url)
        self.last = self.cur                    # ! ⚠️ 前进历史作废（逻辑删除，O(1)）

    def back(self, steps: int) -> str:
        self.cur = max(0, self.cur - steps)     # ! 不够退就退到头
        return self.history[self.cur]

    def forward(self, steps: int) -> str:
        self.cur = min(self.last, self.cur + steps)   # ! 不够进就进到尾
        return self.history[self.cur]


##################################################################################################
##### ! Solution 2: 数组 + 游标，visit 时真的截断列表（代码更短，visit 退化成 O(n)）
##### ! 时间复杂度: visit O(n)，back / forward O(1)   空间复杂度: O(访问总数)
##### ! 适用：对照用。能过 LeetCode，但 5*10^4 次 visit 最坏是 O(n^2)
##################################################################################################


class BrowserHistory_2:
    def __init__(self, homepage: str):
        self.history = [homepage]
        self.cur = 0

    def visit(self, url: str) -> None:
        del self.history[self.cur + 1 :]        # ! 真删除 ⟹ O(n)，不如解法 1 的 last
        self.history.append(url)
        self.cur = len(self.history) - 1

    def back(self, steps: int) -> str:
        self.cur = max(0, self.cur - steps)
        return self.history[self.cur]

    def forward(self, steps: int) -> str:
        self.cur = min(len(self.history) - 1, self.cur + steps)
        return self.history[self.cur]


##################################################################################################
##### ! Solution 3: 双栈（back 栈 + forward 栈）—— 面试最常先想到的方案
##### ! 时间复杂度: visit O(1) 均摊；back / forward **O(steps)**   空间复杂度: O(访问总数)
##### ! 适用：心智模型最贴近"浏览器"；但 back(steps) 要一个个搬 ⟹ 不如游标版
##################################################################################################


class BrowserHistory_3:
    def __init__(self, homepage: str):
        self.cur_page = homepage
        self.back_stack = []                    # ! 后退历史
        self.fwd_stack = []                     # ! 前进历史

    def visit(self, url: str) -> None:
        self.back_stack.append(self.cur_page)
        self.cur_page = url
        self.fwd_stack.clear()                  # ! 清空前进历史（均摊 O(1)）

    def back(self, steps: int) -> str:
        while steps > 0 and self.back_stack:    # ! 一个个搬 ⟹ O(steps)
            self.fwd_stack.append(self.cur_page)
            self.cur_page = self.back_stack.pop()
            steps -= 1
        return self.cur_page

    def forward(self, steps: int) -> str:
        while steps > 0 and self.fwd_stack:
            self.back_stack.append(self.cur_page)
            self.cur_page = self.fwd_stack.pop()
            steps -= 1
        return self.cur_page


if __name__ == "__main__":
    import random

    for cls in (BrowserHistory_1, BrowserHistory_2, BrowserHistory_3):
        # ! LeetCode 官方样例
        b = cls("leetcode.com")
        b.visit("google.com")
        b.visit("facebook.com")
        b.visit("youtube.com")
        assert b.back(1) == "facebook.com"
        assert b.back(1) == "google.com"
        assert b.forward(1) == "facebook.com"
        b.visit("linkedin.com")                     # ! youtube 的前进历史作废
        assert b.forward(2) == "linkedin.com"       # ! 停在原地
        assert b.back(2) == "google.com"
        assert b.back(7) == "leetcode.com"          # ! 退过头 ⟹ 停在 homepage

        # ! 只有 homepage
        h = cls("home")
        assert h.back(5) == "home"
        assert h.forward(5) == "home"

        # ! back(0) / forward(0) 原地不动
        z = cls("a")
        z.visit("b")
        assert z.back(0) == "b"
        assert z.forward(0) == "b"

        # ! visit 之后立刻 forward
        v = cls("a")
        v.visit("b"); v.visit("c")
        assert v.back(1) == "b"
        v.visit("d")                                # ! c 作废
        assert v.forward(1) == "d"                  # ! 停在原地

        # ! 反复 visit 同一个 url
        r = cls("a")
        r.visit("x"); r.visit("x"); r.visit("x")
        assert r.back(1) == "x" and r.back(2) == "a"

    b = BrowserHistory_1("leetcode.com")
    b.visit("google.com"); b.visit("facebook.com"); b.visit("youtube.com")
    print("back(1)    ->", b.back(1))
    print("back(1)    ->", b.back(1))
    print("forward(1) ->", b.forward(1))
    b.visit("linkedin.com")
    print("visit 后 forward(2) ->", b.forward(2), "(前进历史已作废，停在原地)")

    for _ in range(3000):                           # ! 随机对拍 + 与「列表切片真值」比较
        urls = [f"u{i}" for i in range(6)]
        ops = []
        for _ in range(random.randint(1, 30)):
            r = random.random()
            if r < 0.4:
                ops.append(("visit", random.choice(urls)))
            elif r < 0.7:
                ops.append(("back", random.randint(0, 4)))
            else:
                ops.append(("forward", random.randint(0, 4)))
        outs = []
        for cls in (BrowserHistory_1, BrowserHistory_2, BrowserHistory_3):
            b = cls("home")
            seq = []
            for op, arg in ops:
                if op == "visit":
                    b.visit(arg); seq.append(None)
                elif op == "back":
                    seq.append(b.back(arg))
                else:
                    seq.append(b.forward(arg))
            outs.append(seq)
        # ! 独立真值：用最朴素的「列表 + 下标 + 真截断」重算
        hist, cur, truth = ["home"], 0, []
        for op, arg in ops:
            if op == "visit":
                hist = hist[: cur + 1] + [arg]; cur = len(hist) - 1; truth.append(None)
            elif op == "back":
                cur = max(0, cur - arg); truth.append(hist[cur])
            else:
                cur = min(len(hist) - 1, cur + arg); truth.append(hist[cur])
        assert outs[0] == outs[1] == outs[2] == truth, (ops, outs, truth)
    print("随机对拍 3000 组通过 ✓（游标+last == 真截断 == 双栈 == 朴素真值）")
