r"""LC-0318 - Maximum Product of Word Lengths     ★ 第二轮审核新增（Bitmask 表示集合）

Level 1 · 04 二进制分解与原地编码 —— **用一个 int 当「集合」**
题目在问：给定小写字母单词数组，找出**不共享任何字母**的两个单词，
         返回它们长度之积的最大值；不存在则返回 0。

### 决定性观察：26 个小写字母 ⟹ 一个 int 就是一个集合

```python
mask = 0
for ch in word:
    mask |= 1 << (ord(ch) - ord('a'))      # ! 第 k 位 = 1 表示「含有第 k 个字母」
```

于是：

| 集合操作 | 位运算 | 代价 |
|---|---|---|
| 「两个单词**没有**公共字母」 | **`mask1 & mask2 == 0`** | **O(1)** |
| 并集 | `mask1 \| mask2` | O(1) |
| 交集 | `mask1 & mask2` | O(1) |
| 「含有字母 `ch`」 | `mask >> (ord(ch)-97) & 1` | O(1) |
| 字母种类数 | `bin(mask).count('1')` | O(1) |

**朴素做法**是对每一对单词做字符集合比较 —— `O(n² · L)`。
**Bitmask 把「集合是否相交」从 O(L) 压到一次 `&`** ⟹ `O(n·L + n²)`。

这就是整道题的全部内容。**它不是一道字符串题，是一道「怎么表示集合」的题。**

---

## 为什么 `mask1 & mask2 == 0` 等价于「没有公共字母」

`mask1 & mask2` 的第 `k` 位为 1
⟺ 两个 mask 的第 `k` 位**都**是 1
⟺ **两个单词都含有**第 `k` 个字母。

所以 `mask1 & mask2 == 0` ⟺ 不存在任何一个字母同时出现在两个单词里。∎

**注意 mask 丢掉了「出现次数」**，只保留「是否出现」。
这正是本题需要的 —— 题目问的是「是否共享字母」，不关心各出现几次。
`"abb"` 和 `"ab"` 的 mask **完全相同**（都是 `0b11`）。
> **Bitmask 表示的是「集合」，不是「多重集」。** 需要次数就得换成 Counter。

---

## 一个重要优化：同一个 mask 只保留最长的单词

不同单词可能有相同的 mask（`"ab"`、`"ba"`、`"abab"`、`"aabb"` 都是 `0b11`）。
既然判定只看 mask，那对同一个 mask **只有最长的那个单词有用**：

```python
best = {}                                  # ! mask -> 该 mask 下的最大长度
for w in words:
    m = mask_of(w)
    best[m] = max(best.get(m, 0), len(w))
```

**为什么这样不会丢解？** 若 `(w1, w2)` 是最优解，
把 `w1` 换成「同 mask 的更长单词 `w1'`」后：
- 相容性不变（mask 相同 ⟹ `mask1' & mask2 == mask1 & mask2 == 0`）
- 乘积不减（`len(w1') >= len(w1)`）
⟹ 替换后仍是可行解且不更差。∎

**收益**：不同 mask 最多 `2^26` 个，但实际由 `n` 限制 ⟹
最坏仍是 O(n²)，但大量重复 mask 的输入上会快很多。
更重要的是 **它让「只需 mask + 长度」这件事变得显式**。

---

## 为什么这道题值得单独收录（第二轮审核的理由）

本专题原有的「编码」题（[LC-1470](<../../02 - In-place 编码与旧状态保护/01 - LC-1470 - Shuffle the Array>)、
[LC-1920](<../../02 - In-place 编码与旧状态保护/02 - LC-1920 - Build Array from Permutation>)）
都是**算术编码**（把两个数塞进一个数的高低位）。

**Bitmask 表示集合是完全不同的一类用法** —— 本专题原本一道都没有：

| 用法 | 一个 int 代表什么 | 本专题的题 |
|---|---|---|
| **算术编码** | 两个**数值**（高位 / 低位） | LC-1470、LC-1920 |
| **Bitmask 集合** | 一个**元素集合**（第 k 位 = 第 k 个元素在不在） | **LC-0318**（本题） |

**可迁移性**（条件 C）：Bitmask 集合是下面这一大批题的基础 ——
LC-1239 Max Length of Concatenated String、LC-2002 Max Product of Two Palindromic
Subsequences、LC-0847 Shortest Path Visiting All Nodes、
以及**所有 Bitmask DP / 状压 DP**。

> 按指令要求，本次**不扩充** Advanced Bitmask DP 和 SOS DP ——
> 只收这一道作为「Bitmask 当集合用」的入门，把概念打通就够。

---

复杂度：**O(n·L + n²)** 时间（`n` = 单词数，`L` = 平均长度）、**O(n)** 空间。
       ⚠️ **不是 O(n²·L)** —— 这正是 Bitmask 带来的改进。
       去重后，内层两两比较的对象数 `m <= min(n, 2^26)` ⟹ O(n·L + m²)。

边界：
  - 不存在相容的两个单词 → **0**（例如 `["a","aa","aaa"]`）
  - 只有一个单词 → **0**（需要**两个**不同的单词）
  - 空数组 → 0
  - 全部单词互不相交 → 最长两个的乘积
  - 重复单词 `["ab","ab"]` → **0**（它们共享字母，不相容）
  - 相同 mask 不同长度 `["ab","abab","cd"]` → `4 * 2 = 8`（去重优化生效）
  - 单字母单词 `["a","b"]` → `1`
  - 26 个字母全用满的单词
"""

from typing import List


##################################################################################################
##### ! Solution 1: 预计算 bitmask + 按 mask 去重保留最长 + 两两 & 判相容
##### ! 时间复杂度: O(n·L + m^2)，m = 去重后的 mask 数   空间复杂度: O(n)
##### ! 适用：所有「用一个 int 表示元素集合」的题；Bitmask DP 的入门
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def maxProduct(self, words: List[str]) -> int:
        best = {}                                  # ! mask -> 该 mask 下的最大长度
        for w in words:
            m = 0
            for ch in w:
                m |= 1 << (ord(ch) - 97)           # ! 第 k 位 = 含有第 k 个字母
            if len(w) > best.get(m, 0):
                best[m] = len(w)                   # ! 同 mask 只留最长的（不会丢解）
        items = list(best.items())
        ans = 0
        for i in range(len(items)):
            m1, l1 = items[i]
            for j in range(i + 1, len(items)):
                m2, l2 = items[j]
                if m1 & m2 == 0:                   # ! 一次 & 就判完「无公共字母」
                    ans = max(ans, l1 * l2)
        return ans


##################################################################################################
##### ! Solution 2: 不去重，直接对所有单词两两比较（更短，复杂度略差）
##### ! 时间复杂度: O(n·L + n^2)   空间复杂度: O(n)
##### ! 适用：面试速写版。去重只是常数优化，不影响最坏复杂度
##################################################################################################


class Solution_2:
    def maxProduct(self, words: List[str]) -> int:
        n = len(words)
        masks = [0] * n
        for i, w in enumerate(words):
            for ch in w:
                masks[i] |= 1 << (ord(ch) - 97)
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                if masks[i] & masks[j] == 0:
                    ans = max(ans, len(words[i]) * len(words[j]))
        return ans


##################################################################################################
##### ! Solution 3: 暴力基准（用 set 判交集，用于对拍）
##### ! 时间复杂度: O(n·L + n^2·L)   空间复杂度: O(n·L)
##### ! 适用：仅用于对拍。对比之下能看清 bitmask 省掉的那个 O(L)
##################################################################################################


class Solution_3:
    def maxProduct(self, words: List[str]) -> int:
        n = len(words)
        sets = [set(w) for w in words]
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                if not (sets[i] & sets[j]):        # ! set 交集：O(min(L1, L2))
                    ans = max(ans, len(words[i]) * len(words[j]))
        return ans


if __name__ == "__main__":
    import random
    import string

    for cls in (Solution_1, Solution_2, Solution_3):
        s = cls()
        assert s.maxProduct(["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]) == 16   # ! abcw * xtfn
        assert s.maxProduct(["a", "ab", "abc", "d", "cd", "bcd", "abcd"]) == 4       # ! ab * cd
        assert s.maxProduct(["a", "aa", "aaa", "aaaa"]) == 0                         # ! 全共享
        assert s.maxProduct(["a"]) == 0                                              # ! 只有一个
        assert s.maxProduct([]) == 0
        assert s.maxProduct(["ab", "ab"]) == 0                                       # ! 重复单词仍共享
        assert s.maxProduct(["a", "b"]) == 1
        assert s.maxProduct(["ab", "abab", "cd"]) == 8                               # ! 去重优化：abab * cd
        assert s.maxProduct([string.ascii_lowercase, "a"]) == 0                      # ! 26 字母全满
        assert s.maxProduct(["abc", "xyz"]) == 9

    print('["abcw","baz","foo","bar","xtfn","abcdef"] ->',
          Solution_1().maxProduct(["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]), "(abcw * xtfn)")
    print('["ab","abab","cd"] ->', Solution_1().maxProduct(["ab", "abab", "cd"]), "(abab * cd)")

    # ! 演示 bitmask 作为集合的几个操作
    def mask_of(w):
        m = 0
        for ch in w:
            m |= 1 << (ord(ch) - 97)
        return m
    assert mask_of("abb") == mask_of("ab") == 0b11      # ! 丢掉次数，只留「是否出现」
    assert mask_of("abc") & mask_of("xyz") == 0         # ! 无交集
    assert mask_of("abc") & mask_of("cde") == mask_of("c")
    assert bin(mask_of("hello")).count("1") == 4        # ! h, e, l, o
    print("bitmask 集合操作验证通过 ✓（'abb' 与 'ab' 同 mask；'abc'&'xyz'==0）")

    for _ in range(2000):                               # ! 随机对拍（小字母表 ⟹ 刻意制造冲突）
        alphabet = string.ascii_lowercase[:random.randint(2, 6)]
        words = [
            "".join(random.choice(alphabet) for _ in range(random.randint(1, 5)))
            for _ in range(random.randint(0, 8))
        ]
        a = Solution_1().maxProduct(words[:])
        b = Solution_2().maxProduct(words[:])
        c = Solution_3().maxProduct(words[:])
        assert a == b == c, (words, a, b, c)
    print("随机对拍 2000 组通过 ✓（去重 bitmask == 朴素 bitmask == set 交集暴力）")
