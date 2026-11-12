"""LC-0432 - All O`one Data Structure

Level 1 · 02 Cache 与 O(1) 淘汰策略 → Level 2 · 02 LFU Cache 与频率桶

题目在问：`inc(key)`、`dec(key)`（减到 0 删除）、`getMaxKey()`、`getMinKey()`，**全部 O(1)**。

### 这题就是 LFU Cache 的「频率桶双向链表」单独拿出来考

把计数相同的 key 放进同一个桶（bucket），桶按计数**有序地串成双向链表**：

    head ⇄ [cnt=1: {a, b}] ⇄ [cnt=3: {c}] ⇄ [cnt=7: {d}] ⇄ tail
    getMinKey = head.next 里任意一个 key      getMaxKey = tail.prev 里任意一个 key

`inc(key)`：key 从 cnt 桶挪到 cnt+1 桶。cnt+1 桶**如果存在一定是紧挨着的下一个**（否则就插一个新桶在它后面）；
`dec` 对称。桶空了就从链表摘掉。每一步都只碰相邻节点 ⟹ O(1)。

### 为什么「相邻」能保证

链表里只放**非空**桶，计数值严格递增。key 当前在 cnt 桶，变成 cnt+1 之后应该去的位置就在 cnt 桶的右边：
要么右边那个桶恰好是 cnt+1（直接加入），要么右边那个桶 > cnt+1（在中间插一个新桶）—— 不可能再远。

### 对比：不用链表行不行

- `count → set(keys)` 的哈希表 + 维护 `maxCount / minCount` 两个整数：inc 时 max 只会 +1，没问题；
  但 **dec 把最大桶清空时**，新的 max 要往下找，最坏 O(n)。所以只有链表（或者有序结构）才真是 O(1)。
- 用 `SortedDict`：O(log n)，面试里只配做备胎。
"""
from collections import defaultdict


class _Bucket:
    __slots__ = ("cnt", "keys", "prev", "next")

    def __init__(self, cnt: int):
        self.cnt, self.keys, self.prev, self.next = cnt, set(), None, None


##################################################################################################
##### ! Solution 1: 频率桶双向链表 + key → 桶 的哈希表
##### ! 时间复杂度: 四个操作全部 O(1)   空间复杂度: O(不同 key 的数量)
##### ! 适用：面试标准答案（和 LC-0460 LFU 的桶链表同构）。
#####         两个哨兵 head(cnt=0) / tail(cnt=∞) 省掉所有空链表判断
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self):
        self.head, self.tail = _Bucket(0), _Bucket(float("inf"))
        self.head.next, self.tail.prev = self.tail, self.head
        self.where: dict = {}                     # ! key → 它所在的桶

    def _insert_after(self, node: _Bucket, cnt: int) -> _Bucket:
        b = _Bucket(cnt)
        b.prev, b.next = node, node.next
        node.next.prev = b
        node.next = b
        return b

    def _remove_if_empty(self, b: _Bucket) -> None:
        if not b.keys:
            b.prev.next, b.next.prev = b.next, b.prev

    def inc(self, key: str) -> None:
        if key not in self.where:                 # ! 新 key：计数 1，放进 head 右边的「cnt=1 桶」
            b = self.head
            target = b.next if b.next.cnt == 1 else self._insert_after(b, 1)
        else:
            b = self.where[key]
            b.keys.remove(key)
            target = b.next if b.next.cnt == b.cnt + 1 else self._insert_after(b, b.cnt + 1)
            self._remove_if_empty(b)
        target.keys.add(key)
        self.where[key] = target

    def dec(self, key: str) -> None:
        b = self.where[key]                       # ! 题目保证 key 存在
        b.keys.remove(key)
        if b.cnt == 1:
            del self.where[key]                   # ! 减到 0：彻底删除
        else:
            target = b.prev if b.prev.cnt == b.cnt - 1 else self._insert_after(b.prev, b.cnt - 1)
            target.keys.add(key)
            self.where[key] = target
        self._remove_if_empty(b)

    def getMaxKey(self) -> str:
        return next(iter(self.tail.prev.keys)) if self.tail.prev is not self.head else ""

    def getMinKey(self) -> str:
        return next(iter(self.head.next.keys)) if self.head.next is not self.tail else ""


##################################################################################################
##### ! Solution 2: 哈希表 count → set(keys) + 维护 maxc / minc 两个整数（几乎 O(1)）
##### ! 时间复杂度: inc O(1)；dec 最坏 O(n)（最大桶或「计数 1」桶被清空时要重新扫一遍桶）   空间复杂度: O(n)
##### ! 适用：面试里 10 分钟就能写出来、也能通过 LeetCode 的版本。要主动说出它的最坏情况在哪，
#####         然后给出 Solution_1 作为真 O(1) 的升级
##################################################################################################


class Solution_2:
    def __init__(self):
        self.cnt = defaultdict(int)
        self.bucket = defaultdict(set)
        self.maxc = self.minc = 0

    def inc(self, key: str) -> None:
        c = self.cnt[key]
        if c:
            self.bucket[c].discard(key)
            if not self.bucket[c]:
                del self.bucket[c]
        self.cnt[key] = c + 1
        self.bucket[c + 1].add(key)
        self.maxc = max(self.maxc, c + 1)
        if c == 0:
            self.minc = 1                         # ! 新 key 计数 1，必是全局最小
        elif c == self.minc and c not in self.bucket:
            self.minc = c + 1                     # ! 最小桶被搬空：新最小值恰好是 c+1（这个 key 刚去的地方）

    def dec(self, key: str) -> None:
        c = self.cnt[key]
        self.bucket[c].discard(key)
        if not self.bucket[c]:
            del self.bucket[c]
        if c == 1:
            del self.cnt[key]
        else:
            self.cnt[key] = c - 1
            self.bucket[c - 1].add(key)
        if not self.bucket:
            self.maxc = self.minc = 0
            return
        if c > 1:
            self.minc = min(self.minc, c - 1)     # ! 这个 key 降到 c-1，可能成为新最小
        elif self.minc not in self.bucket:
            self.minc = min(self.bucket)          # ! 计数 1 的桶被清空：O(不同计数的数量)，最坏 O(n)
        if c == self.maxc and c not in self.bucket:
            self.maxc = max(self.bucket)          # ! 同理，最坏 O(n)

    def getMaxKey(self) -> str:
        return next(iter(self.bucket[self.maxc])) if self.bucket else ""

    def getMinKey(self) -> str:
        return next(iter(self.bucket[self.minc])) if self.bucket else ""


##################################################################################################
##### ! Solution 3: 朴素计数字典（真值基线）
##### ! 时间复杂度: inc/dec O(1)，getMax/getMin O(n)   空间复杂度: O(n)
##### ! 适用：只用来对拍。注意同计数的 key 可以返回任意一个，所以对拍比较的是「返回的 key 的计数」
##################################################################################################


class Solution_3:
    def __init__(self):
        self.cnt = defaultdict(int)

    def inc(self, key: str) -> None:
        self.cnt[key] += 1

    def dec(self, key: str) -> None:
        self.cnt[key] -= 1
        if self.cnt[key] == 0:
            del self.cnt[key]

    def getMaxKey(self) -> str:
        return max(self.cnt, key=self.cnt.get) if self.cnt else ""

    def getMinKey(self) -> str:
        return min(self.cnt, key=self.cnt.get) if self.cnt else ""


if __name__ == "__main__":
    import random
    random.seed(432)
    for cls in (Solution_1, Solution_2, Solution_3):
        o = cls()
        o.inc("hello"); o.inc("hello")
        assert o.getMaxKey() == "hello" and o.getMinKey() == "hello"
        o.inc("leet")
        assert o.getMaxKey() == "hello" and o.getMinKey() == "leet", cls.__name__

    # ! 随机对拍：同计数的 key 任返回一个都算对，所以比较「返回 key 的计数」是否等于真值的最大/最小计数
    keys = list("abcdefg")
    for _ in range(40):
        a, b, truth = Solution_1(), Solution_2(), Solution_3()
        for _ in range(1500):
            r = random.random()
            if r < 0.45:
                k = random.choice(keys)
                a.inc(k); b.inc(k); truth.inc(k)
            elif r < 0.75 and truth.cnt:
                k = random.choice(list(truth.cnt))
                a.dec(k); b.dec(k); truth.dec(k)
            else:
                for f in ("getMaxKey", "getMinKey"):
                    want = getattr(truth, f)()
                    for im in (a, b):
                        got = getattr(im, f)()
                        if want == "":
                            assert got == "", (f, got)
                        else:
                            assert truth.cnt[got] == truth.cnt[want], (im.__class__.__name__, f, got, want, dict(truth.cnt))
    print("所有测试通过 ✓（样例 + 40 × 1500 步随机对拍）")
