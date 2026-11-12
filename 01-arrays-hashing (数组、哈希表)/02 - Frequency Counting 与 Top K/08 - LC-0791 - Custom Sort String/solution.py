"""LC-0791 - Custom Sort String

Level 1 · 02 Frequency Counting 与 Top K

题目在问：`order` 给出一组字母的自定义顺序，把 `s` 重排，使 `order` 里的字母按 `order` 的顺序出现；
不在 `order` 里的字母放哪都行。Meta 高频热身题。

### 两种思路，一个比较

| 思路 | 做法 | 复杂度 |
|---|---|---|
| **计数 + 按 order 输出**（桶排序思想） | 数 `s` 的频率；按 `order` 逐字母输出 `cnt[c]` 个；剩下的追加 | O(n + m)，m ≤ 26 |
| 自定义排序键 | `rank[c] = order 中的下标`（不在 order 里的给 26），`sorted(s, key=rank)` | O(n log n) |

计数版更优，而且**不需要稳定性**：同一个字母之间无法区分，顺序无所谓。
排序版一行写完，面试里当「第一版」说出来再升级即可。

### 一个容易忘的点

不在 `order` 里的字母**也要输出**（题目只约束 order 内字母的相对顺序）。计数版用「遍历 order 后再遍历剩余计数」保证不漏；
`Counter` 在 pop 过 order 字母之后，剩下的就是那些。
"""
from collections import Counter


##################################################################################################
##### ! Solution 1: 计数 + 按 order 输出（线性）
##### ! 时间复杂度: O(n + m)   空间复杂度: O(26)
##### ! 适用：面试标准答案。本质是 26 个桶的桶排序；order 决定桶的输出顺序
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def customSortString(self, order: str, s: str) -> str:
        cnt = Counter(s)
        out = []
        for c in order:
            out.append(c * cnt.pop(c, 0))              # ! 输出 cnt[c] 个 c；pop 掉表示已处理
        for c, k in cnt.items():                       # ! 不在 order 里的字母，任意顺序
            out.append(c * k)
        return "".join(out)


##################################################################################################
##### ! Solution 2: 自定义排序键
##### ! 时间复杂度: O(n log n)   空间复杂度: O(n)
##### ! 适用：一行版；rank 表把「order 中的下标」当键，不在 order 里的给一个大于所有下标的值放最后
##################################################################################################


class Solution_2:
    def customSortString(self, order: str, s: str) -> str:
        rank = {c: i for i, c in enumerate(order)}
        return "".join(sorted(s, key=lambda c: rank.get(c, len(order))))


##################################################################################################
##### ! Solution 3: 定长 26 数组计数（不用 Counter，C/Java 风格）
##### ! 时间复杂度: O(n + 26)   空间复杂度: O(26)
##### ! 适用：面试用不能带 Counter 的语言时的对应写法；逻辑与 Solution_1 完全一致
##################################################################################################


class Solution_3:
    def customSortString(self, order: str, s: str) -> str:
        cnt = [0] * 26
        for c in s:
            cnt[ord(c) - 97] += 1
        out = []
        for c in order:
            k = ord(c) - 97
            out.append(c * cnt[k]); cnt[k] = 0
        for k in range(26):
            if cnt[k]:
                out.append(chr(97 + k) * cnt[k])
        return "".join(out)


def _valid(order: str, s: str, t: str) -> bool:
    """检查 t 是 s 的重排，且 order 内字母的相对顺序符合 order。"""
    if sorted(t) != sorted(s):
        return False
    rank = {c: i for i, c in enumerate(order)}
    last = -1
    for c in t:
        if c in rank:
            if rank[c] < last:
                return False
            last = rank[c]
    return True


if __name__ == "__main__":
    import random
    for order, s in [("cba", "abcd"), ("bcafg", "abcd"), ("", "abc"), ("xyz", "aaa")]:
        for cls in (Solution_1, Solution_2, Solution_3):
            assert _valid(order, s, cls().customSortString(order, s)), (cls.__name__, order, s)
    assert Solution_1().customSortString("cba", "abcd").startswith("cba")   # ! 题目样例的一个合法答案是 "cbad"
    rng = random.Random(791)
    letters = "abcdefg"
    for _ in range(3000):
        order = "".join(rng.sample(letters, rng.randint(0, len(letters))))
        s = "".join(rng.choice(letters) for _ in range(rng.randint(0, 15)))
        for cls in (Solution_1, Solution_2, Solution_3):
            assert _valid(order, s, cls().customSortString(order, s)), (cls.__name__, order, s)
    print("所有测试通过 ✓")
