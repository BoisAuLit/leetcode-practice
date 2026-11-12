"""LC-0093 - Restore IP Addresses

Level 1 · 03 字符串构造与分割 —— **固定段数**的字符串分割 + 片段合法性剪枝
题目在问：给一串数字，插入 3 个点把它分成 **4 段**，每段是合法的 0–255 且**无前导零**，
         返回所有可能的 IP 地址。

和 LC-0131 Palindrome Partitioning 的对照（同一个 Level 2 的原因）：

| | LC-0131 回文分割 | LC-0093 本题 |
|---|---|---|
| 段数 | **不固定**（任意多段） | **恰好 4 段** |
| 片段合法条件 | 是回文 | 0 ≤ 值 ≤ 255 且无前导零 |
| 片段长度 | 任意 | **1–3**（可以直接限制循环范围） |
| 剪枝 | 不回文就不递归 | 段数超了、剩余长度不够/过多 |

**共同骨架**：`dfs(start, 已切出的片段)`，枚举下一段的结束位置。

决定性观察：
  1. **每段只能是 1–3 个字符**（因为最大 255），所以内层循环只跑 3 次 ——
     这让搜索空间立刻从指数级降到 3⁴ = 81 以内。
  2. **三条剪枝**，写全了这题就几乎没有分支爆炸：
     - 已经切了 4 段但还有剩余字符 ⟹ 失败
     - 切了 4 段且刚好用完 ⟹ 成功
     - **剩余长度检查**：剩下 `remaining_segments` 段，剩余字符数必须在
       `[remaining_segments, remaining_segments * 3]` 之间，否则直接返回
  3. **前导零规则**：`"0"` 合法，`"01"`、`"00"` 都**不合法**。
     判据：`len(seg) > 1 and seg[0] == '0'` ⟹ 非法。
     这是本题最常被漏掉的一条。

合法性判断完整版：
```python
def valid(seg):
    if len(seg) > 1 and seg[0] == '0':  # 前导零
        return False
    return int(seg) <= 255              # 长度已限制在 1-3，不会溢出
```

复杂度：**O(1)** —— 段数固定为 4、每段最多 3 种长度，搜索树节点数有上界 3⁴。
      说成 O(3^4) 或「常数级」都行，**不要说成 O(2^n)**。
      （字符串拼接的常数开销忽略。）

边界：
  - 长度 < 4 或 > 12 ⟹ 直接无解
  - `"0000"` → `["0.0.0.0"]`
  - `"101023"` → 5 个答案
  - `"255255255255"` → `["255.255.255.255"]`
  - `"010010"` → `["0.10.0.10","0.100.1.0"]`（前导零规则的硬核用例）
"""

from typing import List


##################################################################################################
##### ! Solution 1: 回溯分割 —— 每段枚举 1–3 个字符 + 三条剪枝
##### ! 时间复杂度: O(1)（段数和每段长度都有常数上界）   空间复杂度: O(1) 额外
##### ! 适用：固定段数的字符串分割；和 LC-0131 共用「枚举下一段结束位置」的骨架
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def restoreIpAddresses(self, s: str) -> List[str]:
        n = len(s)
        res: List[str] = []
        if n < 4 or n > 12:              # ! 4 段，每段 1-3 个字符
            return res

        def valid(seg: str) -> bool:
            if len(seg) > 1 and seg[0] == "0":   # ! 前导零：'0' 可以，'01' 不行
                return False
            return int(seg) <= 255

        def dfs(start: int, parts: List[str]) -> None:
            remaining = 4 - len(parts)
            if remaining == 0:
                if start == n:
                    res.append(".".join(parts))
                return
            left = n - start
            # ! 剩余长度剪枝：剩 remaining 段，字符数必须落在 [remaining, remaining*3]
            if left < remaining or left > remaining * 3:
                return
            for length in range(1, 4):
                if start + length > n:
                    break
                seg = s[start:start + length]
                if valid(seg):
                    parts.append(seg)
                    dfs(start + length, parts)
                    parts.pop()          # ! 回溯

        dfs(0, [])
        return res


##################################################################################################
##### ! Solution 2: 三重循环枚举三个点的位置（段数固定，可以直接枚举）
##### ! 时间复杂度: O(1)   空间复杂度: O(1)
##### ! 适用：段数很少且固定时，直接枚举比递归更直白；也是对拍基准
##################################################################################################


class Solution_2:
    def restoreIpAddresses(self, s: str) -> List[str]:
        n = len(s)
        res = []

        def valid(seg: str) -> bool:
            return bool(seg) and len(seg) <= 3 and not (len(seg) > 1 and seg[0] == "0") and int(seg) <= 255

        for i in range(1, 4):            # ! 第一个点的位置
            for j in range(i + 1, i + 4):
                for k in range(j + 1, j + 4):
                    if k >= n:
                        continue
                    a, b, c, d = s[:i], s[i:j], s[j:k], s[k:]
                    if all(valid(x) for x in (a, b, c, d)):
                        res.append(f"{a}.{b}.{c}.{d}")
        return res


if __name__ == "__main__":
    import random

    cases = ["25525511135", "0000", "101023", "255255255255", "010010", "1111", "1", "1" * 13]
    for s in cases:
        a = sorted(Solution_1().restoreIpAddresses(s))
        b = sorted(Solution_2().restoreIpAddresses(s))
        assert a == b, (s, a, b)
        print(f"{s!r} -> {a}")

    for _ in range(2000):                # ! 随机数字串对拍，专压前导零
        s = "".join(random.choice("0125") for _ in range(random.randint(1, 13)))
        assert sorted(Solution_1().restoreIpAddresses(s)) == sorted(Solution_2().restoreIpAddresses(s)), s
    print("随机对拍 2000 组通过 ✓（含大量前导零用例）")
