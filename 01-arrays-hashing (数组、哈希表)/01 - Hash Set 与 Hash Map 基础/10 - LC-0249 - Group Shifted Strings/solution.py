"""LC-0249 - Group Shifted Strings

Level 1 · 01 Hash Set 与 Hash Map 基础

题目在问：把能通过「每个字母同时平移 k 位（环绕）」互相转换的字符串分到一组。"abc" → "bcd" → … → "xyz" 是一组。
Meta 高频。它和 LC-0049 Group Anagrams 是同一个套路：**设计一个「规范化键」，同组的字符串键相同**。

### 规范化键：相邻字母的差（mod 26）

平移不改变相邻字母的差：`"abc"` 的差是 (1, 1)，`"bcd"` 也是 (1, 1)。
所以 `key(s) = tuple((ord(s[i+1]) − ord(s[i])) % 26 for i)`。

**`% 26` 是全部考点**：`"az"` 的差是 25，`"ba"` 的差是 −1 ≡ 25 (mod 26) —— 两者确实互为平移（a→b, z→a），不取模就会被分开。
Python 的 `%` 对负数返回非负结果，直接用；Java/C++ 要 `(d + 26) % 26`。

### 另一种键：平移到以 'a' 开头

`key(s) = 把 s 整体平移使 s[0] == 'a'`，`"bcd"` → `"abc"`。同样要 mod 26。
两种键等价；差分键的好处是不用生成新字符串，长度为 1 的字符串键是空元组 —— 所有单字母天然一组（正确：任意两个单字母互为平移）。

### 和 LC-0049 的对照

| | LC-0049 Group Anagrams | LC-0249 Group Shifted |
|---|---|---|
| 不变量 | 字母多重集 | 相邻字母差 |
| 键 | `tuple(sorted(s))` 或 26 位计数 | `tuple(差 mod 26)` 或平移到 'a' 开头 |
"""
from collections import defaultdict
from typing import List


##################################################################################################
##### ! Solution 1: 相邻字母差（mod 26）作为键
##### ! 时间复杂度: O(Σ|s|)   空间复杂度: O(Σ|s|)
##### ! 适用：面试标准答案；键是元组，可哈希；% 26 处理环绕
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strings:
            key = tuple((ord(s[i + 1]) - ord(s[i])) % 26 for i in range(len(s) - 1))   # ! 差 mod 26
            groups[key].append(s)
        return list(groups.values())


##################################################################################################
##### ! Solution 2: 平移到以 'a' 开头的字符串作为键
##### ! 时间复杂度: O(Σ|s|)   空间复杂度: O(Σ|s|)
##### ! 适用：键更直观（就是「这组的代表元」）；shift = ord(s[0]) - ord('a')，每个字母减去 shift 再 mod 26
##################################################################################################


class Solution_2:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        groups = defaultdict(list)
        for s in strings:
            shift = ord(s[0]) - 97
            key = "".join(chr((ord(c) - 97 - shift) % 26 + 97) for c in s)   # ! 整体平移，首字母变 'a'
            groups[key].append(s)
        return list(groups.values())


##################################################################################################
##### ! Solution 3: 按定义暴力分组（真值基线）—— 两两判断「是否互为平移」
##### ! 时间复杂度: O(n² · L)   空间复杂度: O(n)
##### ! 适用：只用来对拍；is_shift(a, b)：长度相同且所有位置的 (ord(b[i]) - ord(a[i])) % 26 相同
##################################################################################################


class Solution_3:
    def groupStrings(self, strings: List[str]) -> List[List[str]]:
        def is_shift(a: str, b: str) -> bool:
            if len(a) != len(b):
                return False
            d = {(ord(y) - ord(x)) % 26 for x, y in zip(a, b)}
            return len(d) <= 1
        groups: List[List[str]] = []
        for s in strings:
            for g in groups:
                if is_shift(g[0], s):
                    g.append(s); break
            else:
                groups.append([s])
        return groups


def _normalize(groups):
    return sorted(sorted(g) for g in groups)


if __name__ == "__main__":
    import random
    for strings in [["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"], ["a"], ["az", "ba"], ["abc", "abd"]]:
        outs = [_normalize(cls().groupStrings(strings)) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (strings, outs)
    assert _normalize(Solution_1().groupStrings(["az", "ba"])) == [["az", "ba"]]      # ! 环绕：必须同组
    rng = random.Random(249)
    for _ in range(2000):
        strings = ["".join(rng.choice("abcxyz") for _ in range(rng.randint(1, 3))) for _ in range(rng.randint(1, 10))]
        outs = [_normalize(cls().groupStrings(strings)) for cls in (Solution_1, Solution_2, Solution_3)]
        assert outs[0] == outs[1] == outs[2], (strings, outs)
    print("所有测试通过 ✓")
