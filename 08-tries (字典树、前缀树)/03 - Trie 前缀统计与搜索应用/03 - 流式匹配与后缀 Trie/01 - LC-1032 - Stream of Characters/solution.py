"""LC-1032 - Stream of Characters（第二轮自主新增）

Level 1 · 03 Trie 前缀统计与搜索应用 —— **反向（后缀）Trie + 流式查询**
题目在问：设计一个类，不断 `query(letter)` 喂进字符；
         每次返回「**最近**的若干个字符（即当前流的某个**后缀**）是否构成 words 里的某个单词」。

为什么新增它（它补的是哪个缺口 —— 这是本题的全部价值）：
  前面所有 Trie 题匹配的都是**前缀**（从单词开头往后走）。
  这道题匹配的是**后缀**：我们关心「流的结尾那几个字符」。
  解决办法漂亮得令人印象深刻：**把 words 倒着插进 Trie**，
  查询时把流也**倒着走**（从最新的字符往回看）—— 后缀问题立刻变成前缀问题。

  「**反转 ⟹ 后缀变前缀**」是一个能迁移到很多题的技巧
  （LC-0745 Prefix and Suffix Search、各种回文/后缀匹配题都用它）。
  本专题原本完全没有这个视角。

决定性观察：
  1. 把每个 word **反转**后插入 Trie。
  2. 维护已收到的字符流 `stream`。
     `query(c)` 时把 c 追加进去，然后**从最后一个字符往前**沿 Trie 走：
     走到某个 `is_end` 节点就说明「流的某个后缀 == 某个 word」⟹ True。
     走不动（没有对应 child）就可以**立刻停止**。
  3. **剪枝很重要**：往回最多只需要走 `max(len(w) for w in words)` 步 ——
     再往前的字符不可能构成任何 word。
     而且「走不动就 break」让平均情况远快于最坏。

复杂度：
  - 建 Trie：O(Σ|word|)
  - 单次 `query`：**O(L)**，L 是最长单词长度（最坏），不是 O(流长度)。
    n 次查询总共 O(n · L)。
  - 空间：O(Σ|word|) 的 Trie + O(流长度) 的历史
    （历史其实只需要保留最后 L 个字符，见 Solution_1 用 deque 限长）。

**不要说成 O(1)**：每次查询确实要沿 Trie 往回走最多 L 步。

和普通 Trie 题的对照：

| | 普通 Trie（LC-0208/0648） | 本题 |
|---|---|---|
| 匹配的是 | 单词的**前缀** | 流的**后缀** |
| 插入 | 正着插 | **反着插** |
| 查询 | 从头往后走 | **从最新字符往回走** |

边界：
  - words 里有单字符单词 → 每次 query 都可能命中
  - 流比所有单词都长（必须靠 L 剪枝，否则退化）
  - 重复的 word
  - 一个 word 是另一个的后缀
"""

from collections import deque
from typing import Dict, List


class TrieNode:
    __slots__ = ("children", "is_end")

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end = False


##################################################################################################
##### ! Solution 1: 反向 Trie + 限长 deque 保存最近 L 个字符
##### ! 时间复杂度: 建树 O(Σ|word|)，单次 query O(L)   空间复杂度: O(Σ|word| + L)
##### ! 适用：「流的后缀匹配」；核心技巧是「反转 ⟹ 后缀变前缀」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class StreamChecker_1:
    def __init__(self, words: List[str]):
        self.root = TrieNode()
        self.max_len = 0
        for w in words:
            self.max_len = max(self.max_len, len(w))
            node = self.root
            for c in reversed(w):                 # ! 反着插入
                node = node.children.setdefault(c, TrieNode())
            node.is_end = True
        self.stream = deque(maxlen=self.max_len)  # ! 只保留最近 L 个字符，再往前不可能有用

    def query(self, letter: str) -> bool:
        self.stream.append(letter)
        node = self.root
        for c in reversed(self.stream):           # ! 从最新的字符往回走
            if c not in node.children:
                return False                      # ! 走不动了，剪枝
            node = node.children[c]
            if node.is_end:
                return True                       # ! 找到一个 word == 流的某个后缀
        return False


##################################################################################################
##### ! Solution 2: 朴素 —— 每次把最近 L 个字符的所有后缀拿去 set 里查
##### ! 时间复杂度: 单次 query O(L^2)（切片 + 哈希）   空间复杂度: O(Σ|word|)
##### ! 适用：正确性参照；也说明 Trie 省掉的正是「枚举所有后缀并切片」这个平方项
##################################################################################################


class StreamChecker_2:
    def __init__(self, words: List[str]):
        self.words = set(words)
        self.max_len = max((len(w) for w in words), default=0)
        self.buf: List[str] = []

    def query(self, letter: str) -> bool:
        self.buf.append(letter)
        if len(self.buf) > self.max_len:
            self.buf.pop(0)
        s = "".join(self.buf)
        return any(s[i:] in self.words for i in range(len(s)))


if __name__ == "__main__":
    import random

    sc = StreamChecker_1(["cd", "f", "kl"])
    got = [sc.query(c) for c in "abcdefghijkl"]
    print("words=['cd','f','kl'] 流 'abcdefghijkl' ->", got)
    assert got == [False, False, False, True, False, True, False, False,
                   False, False, False, True]

    for _ in range(500):                 # ! 随机对拍：反向 Trie 版 == 朴素后缀枚举版
        words = ["".join(random.choice("ab") for _ in range(random.randint(1, 4)))
                 for _ in range(random.randint(1, 5))]
        a, b = StreamChecker_1(words), StreamChecker_2(words)
        for _ in range(40):
            c = random.choice("abc")
            ra, rb = a.query(c), b.query(c)
            assert ra == rb, (words, c, ra, rb)
    print("随机对拍 500 组 × 40 次 query 通过 ✓")
