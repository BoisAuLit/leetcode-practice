"""LC-0648 - Replace Words

Level 1 · 01 Trie 基础结构与前缀匹配 —— **最短匹配前缀**（Shortest Matching Prefix）
题目在问：给一组词根 dictionary 和一个句子，把句子里每个单词替换成
         «能作为它前缀的、最短的那个词根»；没有词根能匹配就保留原词。

决定性观察：
  1. 这题**完全复用 LC-0208 的 Trie**，不需要任何新结构 ——
     唯一的新东西是「查找时什么时候停」。
  2. 从根沿着单词的字符往下走，**第一次踩到 `is_end=True` 的节点就停**。
     那条路径上的字符串就是**最短**的匹配词根。
  3. **为什么第一个就是最短的**：Trie 里从根往下走，路径长度单调递增。
     所以沿途遇到的第一个完整词根，一定是所有匹配前缀里最短的那个。
     （题目要求「如果有多个词根都能匹配，用最短的」—— 正好对应。）
  4. 走不动了（没有对应 child）或者走完整个单词都没碰到 `is_end`
     ⟹ 没有词根能匹配 ⟹ 保留原单词。

复杂度：
  - 建 Trie：O(Σ|root|)
  - 替换：O(Σ|word|)，每个单词最多沿 Trie 走它自己的长度
  整体 O(总字符数)，空间 O(Trie 节点数)。

对照：用 Hash Set 存所有词根、对每个单词枚举它的所有前缀去查，
      复杂度是 O(Σ|word|²)（枚举前缀 + 切片）。Trie 把这个平方项消掉了。

边界：
  - 没有任何词根匹配 → 原样保留
  - 词根本身就是整个单词
  - 多个词根能匹配（必须取最短：`["a","aa","aaa"]` + `"aaaa"` → `"a"`）
  - 空句子 / 空词典
"""

from typing import Dict, List


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end = False


##################################################################################################
##### ! Solution 1: Trie + 「第一次碰到 is_end 就停」
##### ! 时间复杂度: O(总字符数)   空间复杂度: O(Trie 节点数)
##### ! 适用：所有「找最短/最长匹配前缀」的题；是 LC-0208 的直接应用
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        root = TrieNode()
        for w in dictionary:                      # ! 建 Trie，和 LC-0208 的 insert 一模一样
            node = root
            for c in w:
                node = node.children.setdefault(c, TrieNode())
            node.is_end = True

        def shortest_root(word: str) -> str:
            node = root
            for i, c in enumerate(word):
                if c not in node.children:
                    return word                   # ! 走不动了，没有词根匹配
                node = node.children[c]
                if node.is_end:
                    return word[:i + 1]           # ! 第一次踩到完整词根 → 它就是最短的
            return word                           # ! 整个单词走完都没碰到 is_end

        return " ".join(shortest_root(w) for w in sentence.split())


##################################################################################################
##### ! Solution 2: Hash Set + 枚举每个单词的所有前缀（由短到长）
##### ! 时间复杂度: O(Σ|word|^2)   空间复杂度: O(Σ|root|)
##### ! 适用：词根很少、单词很短时够用；用来对照 Trie 省掉了哪一个平方项
##################################################################################################


class Solution_2:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        roots = set(dictionary)
        out = []
        for word in sentence.split():
            replaced = word
            for i in range(1, len(word) + 1):     # ! 由短到长，第一个命中的就是最短的
                if word[:i] in roots:
                    replaced = word[:i]
                    break
            out.append(replaced)
        return " ".join(out)


if __name__ == "__main__":
    import random
    import string

    cases = [
        (["cat", "bat", "rat"], "the cattle was rattled by the battery"),
        (["a", "b", "c"], "aadsfasf absbs bbab cadsfafs"),
        (["a", "aa", "aaa", "aaaa"], "a aa a aaaa aaa aaa aaa aaaaaa"),
        ([], "hello world"),
        (["xyz"], "hello world"),
    ]
    for d, s in cases:
        a = Solution_1().replaceWords(d, s)
        b = Solution_2().replaceWords(d, s)
        assert a == b, (d, s, a, b)
        print(f"{d} | {s!r} -> {a!r}")

    for _ in range(1000):                 # ! 随机对拍，专门构造「多个词根都能匹配」的情形
        d = ["".join(random.choice("ab") for _ in range(random.randint(1, 3)))
             for _ in range(random.randint(0, 5))]
        s = " ".join("".join(random.choice("ab") for _ in range(random.randint(1, 5)))
                     for _ in range(random.randint(1, 4)))
        assert Solution_1().replaceWords(d, s) == Solution_2().replaceWords(d, s), (d, s)
    print("随机对拍 1000 组通过 ✓（验证取的确实是最短词根）")
