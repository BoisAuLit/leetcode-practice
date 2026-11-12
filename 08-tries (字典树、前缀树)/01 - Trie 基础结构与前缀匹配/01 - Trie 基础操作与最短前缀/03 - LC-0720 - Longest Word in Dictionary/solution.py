"""LC-0720 - Longest Word in Dictionary（第二轮自主新增）

Level 1 · 01 Trie 基础结构与前缀匹配 —— **「每一步都必须是合法单词」的链式约束**
题目在问：找最长的单词 w，使得 w 的**每一个前缀**都在 words 里出现过；
         长度相同时返回**字典序最小**的。

为什么新增它（它补的是哪个缺口）：
  LC-0208 只教「这个前缀存在吗」，LC-0648 只教「第一个完整单词在哪」。
  这道题要求**路径上的每一个节点都是 `is_end`** —— 一个「链式约束」。
  它逼你从「查一个点」升级到「查一整条路径的性质」，
  而且只需要在 LC-0208 的 Trie 上加一个 DFS 条件，成本极低。
  这是「能不能一个字符一个字符地把单词造出来」这类问题的原型。

决定性观察：
  1. 条件「w 的每个前缀都在 words 里」= 在 Trie 中从根到 w 的路径上，
     **每一个节点的 `is_end` 都是 True**。
  2. 所以做一次 DFS：只沿着 `is_end == True` 的 child 往下走，走不动就停。
     走过的最深路径就是候选。
  3. **字典序最小**：按 `'a'..'z'` 的顺序遍历 children，
     并且只在「严格更长」时才更新答案 —— 这样同长度时先到达的（字典序小的）会被保留。

**不用 Trie 的等价解法**（面试里先说这个也很好）：
  把 words 排序后放进 set，再遍历：
  `if len(w) == 1 or w[:-1] in seen: seen.add(w)` 并更新答案。
  排序保证了「短的先处理」和「同长度按字典序」。O(Σ|w| log n)。
  Trie 版的价值在于把「前缀是否存在」变成 O(1) 的指针跳转。

复杂度：建 Trie O(Σ|w|)，DFS O(Trie 节点数)。空间 O(Trie 节点数)。

边界：
  - 没有任何单词满足（比如所有词长度都 > 1 且前缀缺失）→ 返回 `""`
  - 多个同样长的答案 → 取字典序最小（`["a","banana","app","appl","ap","apply","apple"]` → `"apple"`）
  - 单字符单词
  - 空输入
"""

from typing import Dict, List


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end = False


##################################################################################################
##### ! Solution 1: Trie + 只沿 is_end 链往下的 DFS
##### ! 时间复杂度: O(Σ|w|)   空间复杂度: O(Trie 节点数)
##### ! 适用：「路径上每一步都必须合法」类约束；比「查单点」高一级
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def longestWord(self, words: List[str]) -> str:
        root = TrieNode()
        for w in words:
            node = root
            for c in w:
                node = node.children.setdefault(c, TrieNode())
            node.is_end = True

        best = ""

        def dfs(node, path):
            nonlocal best
            if len(path) > len(best):        # ! 只在严格更长时更新 → 同长度保留先到的（字典序小）
                best = path
            for c in sorted(node.children):  # ! 按字典序遍历
                child = node.children[c]
                if child.is_end:             # ! 链式约束：每一步都必须是完整单词
                    dfs(child, path + c)

        dfs(root, "")
        return best


##################################################################################################
##### ! Solution 2: 排序 + Hash Set 增量构建（不用 Trie，面试里同样标准）
##### ! 时间复杂度: O(Σ|w| log n)   空间复杂度: O(Σ|w|)
##### ! 适用：排序保证「短的先处理、同长按字典序」，所以一遍扫描就够
##################################################################################################


class Solution_2:
    def longestWord(self, words: List[str]) -> str:
        seen = set()
        best = ""
        for w in sorted(words):              # ! 字典序排序：短的一定排在它的扩展之前
            if len(w) == 1 or w[:-1] in seen:
                seen.add(w)
                if len(w) > len(best):
                    best = w
        return best


##################################################################################################
##### ! Solution 3: 暴力 —— 对每个词检查它的所有前缀（基准答案，用来对拍）
##### ! 时间复杂度: O(Σ|w|^2)   空间复杂度: O(Σ|w|)
##### ! 适用：正确性参照，直接翻译题面定义
##################################################################################################


class Solution_3:
    def longestWord(self, words: List[str]) -> str:
        s = set(words)
        best = ""
        for w in words:
            if all(w[:i] in s for i in range(1, len(w) + 1)):
                if len(w) > len(best) or (len(w) == len(best) and w < best):
                    best = w
        return best


if __name__ == "__main__":
    import random

    cases = [["w", "wo", "wor", "worl", "world"],
             ["a", "banana", "app", "appl", "ap", "apply", "apple"],
             ["abc", "bc", "ab", "qwe"], [], ["a"], ["ab"]]
    for words in cases:
        a = Solution_1().longestWord(words)
        b = Solution_2().longestWord(words)
        c = Solution_3().longestWord(words)
        assert a == b == c, (words, a, b, c)
        print(f"{words} -> {a!r}")

    for _ in range(1000):
        words = list({"".join(random.choice("ab") for _ in range(random.randint(1, 4)))
                      for _ in range(random.randint(0, 10))})
        a = Solution_1().longestWord(words)
        b = Solution_2().longestWord(words)
        c = Solution_3().longestWord(words)
        assert a == b == c, (words, a, b, c)
    print("随机对拍 1000 组通过 ✓（含同长度取字典序最小）")
