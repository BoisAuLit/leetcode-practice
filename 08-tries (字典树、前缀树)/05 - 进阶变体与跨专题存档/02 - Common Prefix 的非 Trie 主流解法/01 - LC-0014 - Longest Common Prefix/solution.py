"""LC-0014 - Longest Common Prefix

Level 1 · 05 进阶变体与跨专题存档 → 02 Common Prefix 的非 Trie 主流解法

题目在问：给一组字符串，返回它们**最长的公共前缀**；没有公共前缀就返回 `""`。

记号：`n` = 单词个数，`m` = 最短单词的长度，`S = Σ len(word)` = 所有字符总数。

### 为什么这题会出现在 Trie 专题里（而又恰恰不该用 Trie 做）

把所有单词插进 Trie 之后，最长公共前缀就是**从根出发那条「不分叉」的链**：
一路往下走，直到某个节点 `linkCount != 1`（分叉了）或 `isEnd`（有单词在这里结束）。

这个对应关系很漂亮，是理解 Trie 结构的好教具 —— 但建树本身就要 O(S) 时间、O(S) 空间，
而直接扫描只要 O(S) 时间、O(1) 空间。
⟹ **只查询一次，就不要建 Trie**。Trie 的建树本钱必须靠「多次查询」摊销才划算，
这正是本专题 README 里「只查询一次 → 直接扫描」那条铁律的由来。

### 四个关键不变量（六种解法全部建立在它们之上）

1. **答案长度 ≤ m**（最短单词长度）⟹ 任何解法都不必看超过 m 个字符。
2. **答案一定是 `strs[0]` 的前缀** ⟹ 可以拿 `strs[0]` 当「候选上限」反复裁剪。
3. **LCP 可结合（associative）**：`LCP(a, b, c) == LCP(LCP(a, b), c)`，
   也等于 `common(LCP(左半), LCP(右半))` ⟹ 能分治，也能并行归并。
4. **前缀长度具有单调性**：若长度 k 的前缀是公共的，则所有 < k 的长度都是公共的
   ⟹ 「是否公共」关于 k 单调 ⟹ 能二分答案。

### 边界（这题最容易踩的三个）

- `strs == [""]` → `""`：`range(0)` 一次都不进，返回 `strs[0][0:0]`。
- `strs == ["a"]` → `"a"`：只有一个单词时答案是它自己，不能漏掉「走完全程」的返回。
- 某个单词是另一个的**真前缀**（`["ab", "a"]` → `"a"`）：
  纵向扫描必须先判 `i == len(strs[j])`，否则 `strs[j][i]` 直接越界；
  Trie 版必须判 `isEnd`，否则会穿过那个单词的结尾继续往下走。

### 六种解法的复杂度对照

| 解法 | 时间 | 空间 | 一句话 |
|---|---|---|---|
| `Solution`（Trie，原有） | O(S) 建树 + O(m) 查询 | **O(S)** | 存档教具；一次查询不划算 |
| `Solution_2` 横向扫描 | O(S) | O(1) | 拿 `strs[0]` 当前缀，逐词裁剪 |
| `Solution_3` 纵向扫描 ⭐️ | O(S)（早退后常常远小于） | O(1) | 按列比字符，一列不齐立刻返回 |
| `Solution_4` 分治 | O(S) | O(m·log n) 栈 | 用不变量③；真正可并行的那个 |
| `Solution_5` 二分答案 | O(S·log m) | O(1) | 用不变量④；比扫描更慢，当练习 |
| `Solution_6` 排序比首尾 | O(n·L·log n) | O(n·L) | 只需 `min(strs)` 和 `max(strs)` 的 LCP |

**纵向扫描为什么是首选**：最坏同样是 O(S)，但只要答案短就立刻返回 ——
`["abcdefghij...", "x"]` 只比一个字符就退出，而横向扫描得先把 `strs[0]` 整个端上来。
面试里写它，全部的坑就是那一行越界判断。

### 本文件的来源说明（跨专题合并）

`Solution_3` 的实现来自 `99-advanced (进阶专题)/divide-and-conquer (分治)/LC-0014 .../`
那份**另一个实体目录**（用户原有代码，原样搬入，未改动一个字符）。
那个目录的名字写的是「分治」，但里面的代码其实是纵向扫描 ——
真正的分治解法是本文件的 `Solution_4`。
合并后全仓库的 LC-0014 只保留这一份实体目录。
"""


from typing import List


##################################################################################################
##### ! Solution 1: Trie 的「不分叉链」（= 下面的 class Solution，用户原有代码，未改动）
##### ! 时间复杂度: O(S) 建树 + O(m) 查询   空间复杂度: O(S)
##### ! 适用：本专题的存档教具 —— 展示「LCP == 从根出发不分叉的那条链」。
#####         走到 linkCount != 1（分叉）或 isEnd（有单词在此结束）就停。一次查询时别选它
##################################################################################################


class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False
        self.linkCount = 0  # number of children

    def addChild(self, char: str):
        if char not in self.children:
            self.children[char] = TrieNode()
            self.linkCount += 1


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.addChild(ch)
            node = node.children[ch]
        node.isEnd = True


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        trie = Trie()
        
        for word in strs:
            trie.insert(word)
        
        
        node = trie.root
        prefix_chars = []

        while node.linkCount == 1 and not node.isEnd:
            # get the single child (char, child_node)
            (ch, child_node), = node.children.items()
            prefix_chars.append(ch)
            node = child_node

        return "".join(prefix_chars)


##################################################################################################
##### ! Solution 2: 横向扫描 Horizontal Scanning（逐词裁剪候选前缀）
##### ! 时间复杂度: O(S)   空间复杂度: O(1)
##### ! 适用：最直觉的写法。用不变量②把 strs[0] 当候选，每读一个词就把候选砍短。
#####         注意用下标 end 代替 prefix = prefix[:-1]：切片每次都重建字符串，
#####         那样写是 O(S + m²) 时间 + O(m) 空间，下面这版才是真正的 O(S) / O(1)
##################################################################################################


class Solution_2:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        end = len(strs[0])                      # ! 当前候选前缀 = strs[0][:end]
        for word in strs[1:]:
            end = min(end, len(word))           # ! 不变量①：答案长度 <= 最短单词长度
            k = 0
            while k < end and word[k] == strs[0][k]:
                k += 1
            end = k                             # ! 循环不变量：公共前缀只会变短，永不变长
            if end == 0:                        # ! 已经没得砍了，提前退出
                return ""
        return strs[0][:end]


##################################################################################################
##### ! Solution 3: 纵向扫描 Vertical Scanning（按「列」比字符，一列不齐立刻返回）
##### ! 时间复杂度: O(S)   空间复杂度: O(1)
##### ! 适用：面试首选。最坏和横向扫描同为 O(S)，但答案短时立刻返回 ——
#####         ["abcdefghij", "x"] 只比一个字符就退出，不必先把 strs[0] 整个取出来。
#####         唯一的坑是 i == len(strs[j])：某个词先结束了，必须在越界前返回
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##### ! 来源：99-advanced (进阶专题)/divide-and-conquer (分治)/ 下那份实体目录的原有代码，
#####         原样搬入，未改动一个字符（那个目录名写的是分治，代码其实是纵向扫描）
##################################################################################################


class Solution_3:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if strs is None or len(strs) == 0:
            return ""
        for i in range(len(strs[0])):
            c = strs[0][i]
            for j in range(1, len(strs)):
                if i == len(strs[j]) or strs[j][i] != c:
                    return strs[0][0:i]
        return strs[0]


##################################################################################################
##### ! Solution 4: 分治 Divide and Conquer（不变量③：LCP 可结合）
##### ! 时间复杂度: O(S)   空间复杂度: O(m·log n)（递归栈，每层持有一个长度 <= m 的中间串）
##### ! 适用：这才是「分治」该有的样子 —— LCP(全体) = common(LCP(左半), LCP(右半))。
#####         单机上比纵向扫描慢（多了递归和中间字符串），但归并步互不依赖，
#####         是唯一能真并行 / 分布式化的解法；也是「可结合运算 ⟹ 可分治」这一类套路的模板
##################################################################################################


class Solution_4:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""

        def common(a: str, b: str) -> str:      # ! 归并步：两个字符串的 LCP
            limit = min(len(a), len(b))
            k = 0
            while k < limit and a[k] == b[k]:
                k += 1
            return a[:k]

        def solve(lo: int, hi: int) -> str:     # ! 闭区间 [lo, hi]
            if lo == hi:                        # ! 单个单词的 LCP 就是它自己
                return strs[lo]
            mid = (lo + hi) // 2
            return common(solve(lo, mid), solve(mid + 1, hi))

        return solve(0, len(strs) - 1)


##################################################################################################
##### ! Solution 5: 二分答案 Binary Search on Length（不变量④：长度单调）
##### ! 时间复杂度: O(S·log m)   空间复杂度: O(1)
##### ! 适用：纯练习。「长度 k 可行 ⟹ 所有 < k 都可行」是典型的上界二分形态，
#####         但每次 check 都要把 n 个词各看 k 个字符 ⟹ 比直接扫描多乘一个 log m，
#####         属于「能二分但不该二分」的反例，留在这里就是为了记住这个判断
##################################################################################################


class Solution_5:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        first = strs[0]
        lo, hi = 0, min(len(w) for w in strs)   # ! 不变量①：答案不超过最短单词长度

        def shared(k: int) -> bool:             # ! 前 k 个字符是否人人相同
            return all(w[:k] == first[:k] for w in strs)

        while lo < hi:                          # ! 求「最大的可行 k」⟹ 上界二分
            mid = (lo + hi + 1) // 2            # ! +1 向上取整，否则 lo = mid 时死循环
            if shared(mid):
                lo = mid                        # ! mid 可行，答案在 [mid, hi]
            else:
                hi = mid - 1                    # ! mid 不可行，答案在 [lo, mid-1]
        return first[:lo]


##################################################################################################
##### ! Solution 6: 排序后只比首尾（本专题 README 点名的第四种主流解法）
##### ! 时间复杂度: O(n·L·log n) 排序 + O(m) 比较   空间复杂度: O(n·L)（Python sorted 不原地）
##### ! 适用：想一眼说清「为什么只比两端就够」时。字典序排序后，
#####         最小串和最大串的 LCP 就是全体的 LCP —— 因为任何夹在中间的串，
#####         其前 k 位必然也夹在这两者之间；当首尾前 k 位相同时，中间的别无选择。
#####         比扫描慢一个 log n，实战不选，但这个「只看两端」的论证值得记
##################################################################################################


class Solution_6:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ""
        lo, hi = min(strs), max(strs)           # ! 等价于排序后取首尾，但只需 O(n·L)
        limit = min(len(lo), len(hi))
        k = 0
        while k < limit and lo[k] == hi[k]:
            k += 1
        return lo[:k]


def _brute(strs: List[str]) -> str:
    # ! 按定义的真值：枚举 strs[0] 的每个前缀，取「人人都以它开头」的最长那个
    if not strs:
        return ""
    first, best = strs[0], ""
    for k in range(len(first) + 1):
        p = first[:k]
        if all(w.startswith(p) for w in strs):
            best = p
    return best


if __name__ == "__main__":
    import random

    IMPLS = [Solution, Solution_2, Solution_3, Solution_4, Solution_5, Solution_6]

    # ! 官方样例 + 三个边界（见文件头「边界」一节）
    CASES = [
        (["flower", "flow", "flight"], "fl"),       # ! 官方样例 1
        (["dog", "racecar", "car"], ""),            # ! 官方样例 2：第一个字符就不齐
        ([""], ""),                                 # ! 边界：唯一的词是空串
        (["a"], "a"),                               # ! 边界：只有一个词，答案是它自己
        (["ab", "a"], "a"),                         # ! 边界：真前缀，纵向扫描要防越界
        (["a", "ab"], "a"),                         # ! 同上，换个顺序（strs[0] 更短）
        (["", "b"], ""),                            # ! 空串参与
        (["ab", "ab"], "ab"),                       # ! 完全相同
        (["abc", "abc", "abc"], "abc"),
        (["c", "acc", "ccc"], ""),                  # ! 首字符分叉
        (["reflower", "flow", "flight"], ""),
    ]
    for strs, want in CASES:
        assert _brute(strs) == want, (strs, _brute(strs), want)   # ! 先确认真值自己是对的
        for cls in IMPLS:
            got = cls().longestCommonPrefix(list(strs))
            assert got == want, (cls.__name__, strs, got, want)

    # ! 随机对拍：五种解法 + 定义真值，两两必须一致
    random.seed(14)
    for _ in range(20000):
        n = random.randint(1, 6)
        alphabet = random.choice(["ab", "abc", "a"])
        if random.random() < 0.6:
            # ! 刻意制造一段共同前缀，让答案非空的样本足够多
            shared_prefix = "".join(random.choice(alphabet) for _ in range(random.randint(0, 4)))
        else:
            shared_prefix = ""
        strs = [
            shared_prefix + "".join(random.choice(alphabet) for _ in range(random.randint(0, 4)))
            for _ in range(n)
        ]
        want = _brute(strs)
        for cls in IMPLS:
            got = cls().longestCommonPrefix(list(strs))
            assert got == want, (cls.__name__, strs, got, want)

    print("六种解法 + 定义真值：11 组定点用例 + 20000 组随机对拍全部一致 ✓")
    print('LCP(["flower", "flow", "flight"]) =', Solution_3().longestCommonPrefix(["flower", "flow", "flight"]))
    print('LCP(["dog", "racecar", "car"])    =', repr(Solution_3().longestCommonPrefix(["dog", "racecar", "car"])))
    print('LCP(["ab", "a"])                  =', repr(Solution_3().longestCommonPrefix(["ab", "a"])))
