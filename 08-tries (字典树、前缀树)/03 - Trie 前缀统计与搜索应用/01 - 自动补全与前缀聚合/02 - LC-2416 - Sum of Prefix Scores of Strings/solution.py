"""LC-2416 - Sum of Prefix Scores of Strings

Level 1 · 03 Trie 前缀统计与搜索应用 —— **Trie Augmentation（在节点上挂附加信息）**
题目在问：一个字符串的 prefix score = 它的每个非空前缀，
         在整个 words 数组里「作为前缀出现」的次数之和。对每个 word 求这个分数。

这是 Trie 最值钱的一个用法：**节点本身可以携带统计量**。

决定性观察：
  1. Trie 的每个节点唯一对应一个前缀。
     在节点上存一个 `count` = **有多少个单词经过这个节点**（也就是以它为前缀）。
  2. 插入 `word` 时，沿路**每个节点的 count += 1**（包括中间节点，不只是末尾）。
  3. 查询 `word` 的分数 = 沿路把每个节点的 count **加起来**。
  4. 两步都是 O(|word|)，总共 O(Σ|word|)。

**为什么不能只统计完整单词的出现次数**：
  题目数的是「作为**前缀**出现的次数」。
  `words = ["abc","ab","bc","b"]` 里，前缀 `"ab"` 出现了 2 次（abc 和 ab），
  但完整单词 `"ab"` 只出现 1 次。只记 `is_end` 的计数会少算。
  **count 必须在插入时沿路累加，而不是只在终点加。**

**重复单词也要正确计数**：`["aa","aa"]` 中，`"aa"` 的分数是
  前缀 `"a"`（2 次）+ 前缀 `"aa"`（2 次）= 4。
  所以**不能用 set 去重**，每次插入都要照常累加。

复杂度：建 Trie O(Σ|word|)，查询 O(Σ|word|)，空间 O(Trie 节点数)。
      与 LC-0208 的区别只是多了一个 int 字段 —— 这就是 Augmentation 的典型形态。

和 LC-1268 的关系：两题都在 Trie 节点上挂东西 ——
      1268 挂「该前缀下字典序最小的前 3 个单词」，本题挂「经过次数」。
      **挂什么取决于你要查什么**，这是本 Level 2 的主旨。

边界：
  - 全部相同的单词 `["aa","aa"]` → `[4, 4]`
  - 互不相干的单词 → 每个单词的分数就是它自己的长度
  - 单字符单词
  - 一个单词是另一个的前缀
"""

from typing import Dict, List


class TrieNode:
    __slots__ = ("children", "count")

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.count = 0          # ! 有多少个单词经过这个节点（= 以这个前缀开头的单词数）


##################################################################################################
##### ! Solution 1: Trie 节点挂 count，插入时沿路 +1，查询时沿路求和
##### ! 时间复杂度: O(Σ|word|)   空间复杂度: O(Trie 节点数)
##### ! 适用：所有「前缀计数 / 前缀聚合」的题；Trie Augmentation 的标准范例
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        root = TrieNode()
        for w in words:
            node = root
            for c in w:
                node = node.children.setdefault(c, TrieNode())
                node.count += 1          # ! 沿路每个节点都要加，不能只在末尾加
        res = []
        for w in words:
            node, total = root, 0
            for c in w:
                node = node.children[c]  # ! 一定存在（自己插过）
                total += node.count      # ! 每个前缀的出现次数累加
            res.append(total)
        return res


##################################################################################################
##### ! Solution 2: 暴力 —— 用 Counter 统计所有单词的所有前缀（基准答案，用来对拍）
##### ! 时间复杂度: O(Σ|word|^2)   空间复杂度: O(Σ|word|^2)
##### ! 适用：正确性参照；也最直白地表达「分数 = 每个前缀出现次数之和」
##################################################################################################


class Solution_2:
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        from collections import Counter
        cnt = Counter()
        for w in words:
            for i in range(1, len(w) + 1):
                cnt[w[:i]] += 1
        return [sum(cnt[w[:i]] for i in range(1, len(w) + 1)) for w in words]


if __name__ == "__main__":
    import random

    cases = [["abc", "ab", "bc", "b"], ["abcd"], ["aa", "aa"], ["a", "a", "a"],
             ["ab", "abc", "abcd"], []]
    for words in cases:
        a = Solution_1().sumPrefixScores(words)
        b = Solution_2().sumPrefixScores(words)
        assert a == b, (words, a, b)
        print(f"{words} -> {a}")

    for _ in range(1000):                 # ! 随机对拍，含大量重复单词
        words = ["".join(random.choice("ab") for _ in range(random.randint(1, 5)))
                 for _ in range(random.randint(1, 8))]
        assert Solution_1().sumPrefixScores(words) == Solution_2().sumPrefixScores(words), words
    print("随机对拍 1000 组通过 ✓（含重复单词）")
