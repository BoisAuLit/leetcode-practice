"""LC-0692 - Top K Frequent Words

Level 1 · 01 Heap 基础与 Top K —— Top K + **Tie Breaking（平局规则）**
题目在问：返回出现频率最高的 k 个单词；**频率相同时按字典序升序**。

这道题的价值不在「用堆」，而在 **Tie Breaking 和堆的方向怎么配合**。

决定性观察：
  1. 排序键是 `(-count, word)`：频率**降序**、字典序**升序**。
     注意两个维度的方向**相反** —— 这是本题所有坑的来源。
  2. 用「大小为 k 的堆」做 Top K 时，堆里要放的是「**最差**的那个在堆顶」，
     这样才能在超出 k 个时弹掉最差的。
     对于我们要的 `(-count, word)` 升序排列，最差 = 这个键最大的那个
     ⟹ 需要一个**最大堆**，而 Python 的 `heapq` 只有最小堆
     ⟹ 要把键**整体取反**：`(count, ReverseStr(word))`。
     字符串没法直接取负，所以需要一个包装类（见 Solution_2）。
  3. **因此本题最省事的写法反而是「全量建堆 + 弹 k 次」**（Solution_1）：
     键直接用 `(-count, word)`，弹 k 次就是答案。
     O(n + k log n)，代码短且不会把方向搞反。

三种解法的复杂度对比（n 是不同单词数）：

| 解法 | 时间 | 空间 | 说明 |
|---|---|---|---|
| Solution_1 全量堆 + 弹 k 次 | O(n + k log n) | O(n) | **推荐**，`heapify` 是 O(n) |
| Solution_2 大小为 k 的堆 | O(n log k) | O(k) | k 远小于 n 时更省空间，但要处理字符串反向比较 |
| Solution_3 直接排序 | O(n log n) | O(n) | 最短；k 接近 n 时反而最优 |

**什么时候「大小 k 的堆」才真的更好**：k << n 且内存受限。
面试里应该说清楚这个权衡，而不是无脑说「Top K 就用大小 k 的堆」。

和 LC-0347 Top K Frequent Elements 的区别：
  347 **没有** tie-breaking 要求（任意顺序即可），所以可以用
  **Bucket Sort** 做到 O(n)：按频率分桶，从高频桶往低频桶取。
  本题因为要求字典序，桶内还得排序，优势就没那么明显了。
  LC-0347 的实体目录在 01-arrays-hashing（跨专题索引）。

边界：
  - 所有单词频率相同 → 纯按字典序
  - k == 不同单词数
  - 单个单词
  - 大小写（题目保证全小写）
"""

import heapq
from collections import Counter
from typing import List


##################################################################################################
##### ! Solution 1: 全量建堆（键 = (-count, word)）+ 弹 k 次
##### ! 时间复杂度: O(n + k log n)   空间复杂度: O(n)
##### ! 适用：Top K 带 tie-breaking 时最不容易出错的写法；heapify 是 O(n)
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        # ! 键的两个维度方向相反：频率降序用 -count，字典序升序直接用 word
        heap = [(-c, w) for w, c in cnt.items()]
        heapq.heapify(heap)                      # ! O(n)，比逐个 push 的 O(n log n) 好
        return [heapq.heappop(heap)[1] for _ in range(k)]


##################################################################################################
##### ! Solution 2: 维护大小为 k 的堆（k << n 时更省空间）
##### ! 时间复杂度: O(n log k)   空间复杂度: O(k)
##### ! 适用：k 远小于 n、内存受限时；代价是要用包装类让字符串「反向比较」
##################################################################################################


class _ReverseStr:
    """让字符串按字典序**降序**参与最小堆比较（这样堆顶才是「最差」的那个）。"""

    __slots__ = ("s",)

    def __init__(self, s: str):
        self.s = s

    def __lt__(self, other: "_ReverseStr") -> bool:
        return self.s > other.s                  # ! 故意反过来

    def __eq__(self, other) -> bool:
        return self.s == other.s


class Solution_2:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        heap = []                                # ! 最小堆，堆顶是「当前最差的候选」
        for w, c in cnt.items():
            # ! 最差 = 频率最低；频率相同时字典序最大 → 所以第二维用 _ReverseStr
            heapq.heappush(heap, (c, _ReverseStr(w)))
            if len(heap) > k:
                heapq.heappop(heap)              # ! 弹掉最差的
        # ! 堆里是 Top K，但顺序是「从最差到最好」，所以倒序输出
        out = []
        while heap:
            c, rw = heapq.heappop(heap)
            out.append(rw.s)
        return out[::-1]


##################################################################################################
##### ! Solution 3: 直接按 (-count, word) 排序取前 k 个（基准答案，用来对拍）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：正确性参照；k 接近 n 时它反而是最优解，面试里值得提一句
##################################################################################################


class Solution_3:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        cnt = Counter(words)
        return sorted(cnt, key=lambda w: (-cnt[w], w))[:k]


if __name__ == "__main__":
    import random
    import string

    cases = [(["i", "love", "leetcode", "i", "love", "coding"], 2),
             (["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4),
             (["a"], 1), (["b", "a"], 2), (["aa", "aa", "bb"], 1)]
    for words, k in cases:
        a = Solution_1().topKFrequent(words, k)
        b = Solution_2().topKFrequent(words, k)
        c = Solution_3().topKFrequent(words, k)
        assert a == b == c, (words, k, a, b, c)
        print(f"{words}, k={k} -> {a}")

    for _ in range(1000):                # ! 小字母表随机对拍，专门压「频率相同比字典序」
        words = ["".join(random.choice("ab") for _ in range(random.randint(1, 2)))
                 for _ in range(random.randint(1, 12))]
        k = random.randint(1, len(set(words)))
        a = Solution_1().topKFrequent(words, k)
        b = Solution_2().topKFrequent(words, k)
        c = Solution_3().topKFrequent(words, k)
        assert a == b == c, (words, k, a, b, c)
    print("随机对拍 1000 组通过 ✓（三种写法的 tie-breaking 完全一致）")
