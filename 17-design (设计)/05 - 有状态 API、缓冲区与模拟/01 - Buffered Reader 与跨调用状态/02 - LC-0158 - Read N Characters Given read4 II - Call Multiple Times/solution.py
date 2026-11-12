"""LC-0158 - Read N Characters Given read4 II - Call Multiple Times  (LeetCode Premium)

Level 1 · 05 有状态 API、缓冲区与模拟 —— **跨调用的持久化缓冲区**
API：给定 `read4(buf4) -> int`（每次最多从文件读 4 个字符，返回实际读到的个数），
     实现 `read(buf, n) -> int`，把最多 `n` 个字符读进 `buf`。
     **`read` 会被调用多次**，必须正确续读。

---

## LC-0157 和 LC-0158 的唯一区别，就是整道题

| | [LC-0157](<../01 - LC-0157 - Read N Characters Given Read4>) | **LC-0158** 本题 |
|---|---|---|
| `read` 调用次数 | **一次** | **多次** |
| `read4` 多读出来的字符 | **可以直接丢掉** | **必须留到下一次 `read` 用** |
| 需要的状态 | 无（纯局部变量） | **实例字段：缓冲区 + 指针** |

**为什么多读的字符不能丢？**
`read4` 的粒度是 4，而 `n` 可以是任意数。
若 `n = 1`，一次 `read4` 读回 4 个字符 —— 本次只能用 1 个，
**剩下 3 个必须留着**，否则下一次 `read` 会从文件的第 5 个字符开始 ⟹ **丢数据**。

**反例**（文件是 `"abcdefg"`，连续调用 `read(buf, 1)` 四次）：
- 正确输出：`a`, `b`, `c`, `d`
- 丢掉多读字符：`a`, `e`（第二次 `read4` 从 `e` 开始）⟹ **b, c, d 永久丢失** ❌

---

## 决定性观察：只需要三个实例字段

```python
self.buf4 = [''] * 4      # ! 上一次 read4 的结果
self.i    = 0             # ! buf4 中下一个可消费字符的下标
self.cnt  = 0             # ! buf4 中有效字符的个数（read4 的返回值）
```

**核心不变量**：
> **`buf4[i : cnt]` 恒为「已从文件读出但尚未交付给调用方」的字符。**
> 这个区间**跨 `read` 调用持久存在**。

主循环只有两种动作：

```python
while written < n:
    if self.i == self.cnt:                # ! 缓冲区空了 ⟹ 去文件再抓一批
        self.cnt = read4(self.buf4)
        self.i = 0
        if self.cnt == 0:                 # ! 文件到底了 ⟹ 提前返回
            break
    buf[written] = self.buf4[self.i]      # ! 从缓冲区消费一个
    self.i += 1
    written += 1
return written
```

**为什么 `i == cnt` 就是「缓冲区空」？**
由不变量，可用区间是 `[i, cnt)`；`i == cnt` ⟺ 区间为空。∎

**为什么 `cnt == 0` 必须 break 而不是 continue？**
`read4` 返回 0 表示**文件已读完**。不 break 会无限调用 `read4` ⟹ **死循环**。
⚠️ 这是本题最容易写出的 bug。

**为什么返回 `written` 而不是 `n`？**
文件可能比 `n` 短 ⟹ 实际读到的字符数可能小于 `n`。
题目要求返回**实际**读取数。

---

## 为什么 `cnt < 4` 不代表文件结束

很多实现会写 `if self.cnt < 4: break` —— **这是错的**。
`read4` 的契约只保证「最多 4 个」，**不保证「只要没到文件尾就一定给 4 个」**
（真实的 I/O 可能因为缓冲、网络分片等原因少给）。
**只有 `cnt == 0` 才代表文件结束。**

> 虽然 LeetCode 的测试桩里 `read4` 确实「能给 4 就给 4」，
> 但按契约编程是面试里会被追问的点。**本文件按 `cnt == 0` 判终止。**

---

## 和 LRU / Hit Counter 的共同点：**状态属于实例，不属于方法**

本 Level 1 的所有题都在练同一件事：

| 题 | 跨调用需要记住什么 |
|---|---|
| **LC-0158** 本题 | **未交付的缓冲字符** `buf4[i:cnt]` |
| [LC-0348 Tic-Tac-Toe](<../../02 - 棋盘状态与历史导航/01 - LC-0348 - Design Tic-Tac-Toe>) | 每行/每列/两条对角线的计数 |
| [LC-1472 Browser History](<../../02 - 棋盘状态与历史导航/02 - LC-1472 - Design Browser History>) | 历史栈 + 当前游标 |
| [LC-1396 Underground System](<../../03 - 多对象状态与增量平均值/01 - LC-1396 - Design Underground System>) | 在途乘客 + 每条线路的累计和与计数 |

> **设计题的核心问题永远是：「两次调用之间，我必须记住什么？」**
> 想清这一句，字段就定了，代码就只是搬运。

---

## 题面来源说明

LC-0158 是 **LeetCode Premium** 题目，本仓库无法合法抓取官方题面，
因此该文件夹**没有 `problem.pdf` / `problem_dark.pdf`**。
本文件的题意描述为公开通行表述，实现与证明均自撰，未复制官方题面。

复杂度：**O(n)** 时间（每个字符恰好被写入一次）、**O(1)** 额外空间
       （缓冲区固定 4 个字符，与 `n` 无关）。
       `read4` 的调用次数是 **⌈n/4⌉ + O(1)**。

边界：
  - `n = 0` → 返回 0，不调用 `read4`
  - 文件比 `n` 短 → 返回实际读到的数量
  - **`n` 不是 4 的倍数**（如 `n = 1`）→ 多读的字符必须留存
  - 连续多次 `read` → 必须正确续读，不丢不重
  - 文件为空 → 第一次就返回 0
  - 文件读完后继续 `read` → 恒返回 0
"""

from typing import List


def _make_read4(file_content: str):
    """构造一个 read4 闭包（模拟 LeetCode 给的那个 API）。"""
    pos = [0]

    def read4(buf4: List[str]) -> int:
        n = min(4, len(file_content) - pos[0])
        for i in range(n):
            buf4[i] = file_content[pos[0] + i]
        pos[0] += n
        return n

    return read4


##################################################################################################
##### ! Solution 1: 实例持有 buf4 + 指针 i + 有效长度 cnt（跨调用持久化缓冲区）
##### ! 时间复杂度: 每次 read O(n)   空间复杂度: O(1)（缓冲区固定 4 个字符）
##### ! 适用：所有「底层 API 粒度固定、上层要任意长度」的缓冲读取问题
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self, read4):
        self.read4 = read4
        self.buf4 = [""] * 4          # ! 上一次 read4 的结果
        self.i = 0                    # ! 下一个可消费字符的下标
        self.cnt = 0                  # ! buf4 中有效字符个数
        # ! 不变量：buf4[i:cnt] 恒为「已读出但尚未交付」的字符，跨调用持久存在

    def read(self, buf: List[str], n: int) -> int:
        written = 0
        while written < n:
            if self.i == self.cnt:            # ! 缓冲区空了 ⟹ 去文件抓一批
                self.cnt = self.read4(self.buf4)
                self.i = 0
                if self.cnt == 0:             # ! 只有 0 才代表文件结束（不是 < 4！）
                    break
            buf[written] = self.buf4[self.i]  # ! 从缓冲区消费一个
            self.i += 1
            written += 1
        return written                        # ! 返回实际读到的个数，不是 n


##################################################################################################
##### ! Solution 2: 用 collections.deque 当缓冲区（语义更直白，空间同阶）
##### ! 时间复杂度: 每次 read O(n)   空间复杂度: O(1)（deque 最多存 3 个残留字符）
##### ! 适用：想让「缓冲区」这个概念更显式时；popleft 是 O(1)
##################################################################################################


class Solution_2:
    def __init__(self, read4):
        from collections import deque

        self.read4 = read4
        self.pending = deque()        # ! 已读出但未交付的字符（最多残留 3 个）

    def read(self, buf: List[str], n: int) -> int:
        written = 0
        while written < n:
            if not self.pending:
                tmp = [""] * 4
                cnt = self.read4(tmp)
                if cnt == 0:
                    break
                self.pending.extend(tmp[:cnt])
            buf[written] = self.pending.popleft()
            written += 1
        return written


##################################################################################################
##### ! Solution 3: 错误实现（丢掉多读的字符）—— 保留作为反面教材
##### ! 时间复杂度: O(n)   空间复杂度: O(1)
##### ! 适用：仅用于演示。它是 LC-0157 的正确解，但对 LC-0158 会丢数据
##################################################################################################


class Solution_3_BROKEN:
    def __init__(self, read4):
        self.read4 = read4

    def read(self, buf: List[str], n: int) -> int:
        written = 0
        while written < n:
            tmp = [""] * 4
            cnt = self.read4(tmp)
            if cnt == 0:
                break
            # ! BUG：本次只取需要的部分，剩下的直接丢了 ⟹ 下次 read 会跳过它们
            take = min(cnt, n - written)
            for k in range(take):
                buf[written] = tmp[k]
                written += 1
        return written


if __name__ == "__main__":
    import random

    def run(cls, content: str, ns: List[int]) -> List[str]:
        """按 ns 里的长度依次调用 read，返回每次读到的字符串。"""
        sol = cls(_make_read4(content))
        out = []
        for n in ns:
            buf = [""] * max(n, 1)
            got = sol.read(buf, n)
            out.append("".join(buf[:got]))
        return out

    for cls in (Solution_1, Solution_2):
        # ! 官方样例：文件 "abc"，read(1) -> "a"，read(2) -> "bc"，read(1) -> ""
        assert run(cls, "abc", [1, 2, 1]) == ["a", "bc", ""]
        # ! 核心用例：n=1 连续四次，多读的字符必须留存
        assert run(cls, "abcdefg", [1, 1, 1, 1]) == ["a", "b", "c", "d"]
        # ! n = 0
        assert run(cls, "abc", [0, 3]) == ["", "abc"]
        # ! 文件比 n 短
        assert run(cls, "ab", [5]) == ["ab"]
        # ! 空文件
        assert run(cls, "", [3, 3]) == ["", ""]
        # ! 读完后继续读
        assert run(cls, "abcd", [4, 1, 1]) == ["abcd", "", ""]
        # ! n 不是 4 的倍数，跨多批
        assert run(cls, "abcdefghij", [3, 3, 3, 3]) == ["abc", "def", "ghi", "j"]
        # ! 恰好 4 的倍数
        assert run(cls, "abcdefgh", [4, 4, 4]) == ["abcd", "efgh", ""]

    print('文件 "abcdefg"，连续 read(buf,1) 四次 ->', run(Solution_1, "abcdefg", [1, 1, 1, 1]))
    print('文件 "abc"，read(1) read(2) read(1) ->', run(Solution_1, "abc", [1, 2, 1]))

    # ! 证明「丢掉多读字符」真的会丢数据（LC-0157 的解法用在 LC-0158 上就是错的）
    broken = run(Solution_3_BROKEN, "abcdefg", [1, 1, 1, 1])
    assert broken != ["a", "b", "c", "d"], "预期它丢数据"
    print("✗ 丢弃多读字符的版本 ->", broken, " ← b, c, d 永久丢失，这就是 158 与 157 的区别")

    for _ in range(3000):                      # ! 随机对拍 + 与「直接切片」的真值比较
        content = "".join(random.choice("abcdefghij") for _ in range(random.randint(0, 20)))
        ns = [random.randint(0, 6) for _ in range(random.randint(1, 6))]
        r1 = run(Solution_1, content, ns)
        r2 = run(Solution_2, content, ns)
        # ! 真值：把 content 按 ns 依次切片（这正是「多次 read 不丢不重」的定义）
        truth, pos = [], 0
        for n in ns:
            truth.append(content[pos : pos + n])
            pos = min(pos + n, len(content))
        assert r1 == r2 == truth, (content, ns, r1, r2, truth)
    print("随机对拍 3000 组通过 ✓（持久缓冲区 == deque 版 == 顺序切片真值）")
