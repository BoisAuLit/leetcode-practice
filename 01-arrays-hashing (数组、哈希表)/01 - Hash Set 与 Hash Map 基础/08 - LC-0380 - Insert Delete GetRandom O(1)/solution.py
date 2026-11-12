"""LC-0380 - Insert Delete GetRandom O(1)

Level 1 · 01 Hash Set 与 Hash Map 基础 —— Hash Map + Dynamic Array 的联合设计
题目在问：设计一个集合，insert / remove / getRandom 三个操作的平均时间复杂度都是 O(1)

核心观察：一个数据结构做不到，两个一起就行 ——
  - **数组**能 O(1) 随机取（`random.randrange(len)`），但删除中间元素要 O(n) 搬运
  - **哈希表**能 O(1) 删，但没有「第 i 个元素」的概念，没法等概率随机取
  合起来：数组存值，哈希表存「值 → 它在数组里的下标」，两份结构同步维护

不变量（invariant）：任意时刻 `vals[pos[v]] == v` 对集合里每个 v 都成立。
  只要每次改动后这条都还成立，三个操作就都正确。

删除的技巧（整道题唯一的技巧）：**要删的元素和数组末尾交换，再 pop 末尾**。
  末尾 pop 是 O(1)，交换只影响两个元素的下标，pos 里改一个值就同步好了。

坑：
  - 交换后别忘了更新**被换上来那个元素**的下标，只更新被删的那个是最常见的错
  - **顺序陷阱**：删的恰好是最后一个元素时，val 和 last 是同一个数。
    如果先 `pos.pop(val)` 再 `pos[last] = idx`，等于把刚删掉的键又写了回去，
    数组里已经没有它、哈希表里却还有，之后 insert(val) 会错误地返回 False。
    正确顺序是：先写 `pos[last]`，最后再 `del pos[val]`
  - getRandom 必须等概率：用 `random.choice(self.vals)`，不要 `random.choice(list(self.pos))`
    （那是 O(n)，题目要的是 O(1)）
  - insert / remove 的返回值是「这次操作是否真的改变了集合」，不是成功与否
"""

import random


##################################################################################################
##### ! Solution 1: Hash Map（值 → 下标）+ Dynamic Array，删除用「和末尾交换」
##### ! 时间复杂度: insert / remove / getRandom 均摊 O(1)   空间复杂度: O(n)
##### ! 适用：所有「要随机访问又要 O(1) 删」的设计题；LC-381（允许重复）只是把下标换成 set
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class RandomizedSet:
    def __init__(self):
        self.vals: list[int] = []        # ! 连续存储，为 getRandom 服务
        self.pos: dict[int, int] = {}    # ! val -> 它在 vals 里的下标，为 remove 服务

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)   # ! 永远追加到末尾，下标就是当前长度
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False
        idx = self.pos[val]
        last = self.vals[-1]
        self.vals[idx] = last            # ! 末尾那个顶替上来
        self.pos[last] = idx             # ! 关键：被顶上来的元素，下标也要改
        self.vals.pop()
        del self.pos[val]                # ! 必须放在最后，见下面「坑」的第二条
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)  # ! O(1)，而且天然等概率


Solution_1 = RandomizedSet  # LeetCode 上类名必须叫 RandomizedSet，这里给个别名方便对照


##################################################################################################
##### ! Solution 2: 只用一个 Hash Set（基线，说明为什么必须配一个数组）
##### ! 时间复杂度: insert / remove O(1)，**getRandom O(n)**   空间复杂度: O(n)
##### ! 适用：不满足题目要求，但值得写一遍 —— 它精确暴露了「哈希表没有第 i 个元素」这个缺陷
##################################################################################################


class RandomizedSetNaive:
    def __init__(self):
        self.s: set[int] = set()

    def insert(self, val: int) -> bool:
        if val in self.s:
            return False
        self.s.add(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.s:
            return False
        self.s.discard(val)
        return True

    def getRandom(self) -> int:
        # ! set 不支持按下标取，只能先摊成 list —— 这一行就是 O(n)，过不了本题的要求
        return random.choice(list(self.s))


Solution_2 = RandomizedSetNaive


if __name__ == "__main__":
    for cls in (RandomizedSet, RandomizedSetNaive):
        s = cls()
        assert s.insert(1) is True
        assert s.remove(2) is False
        assert s.insert(2) is True
        assert s.getRandom() in (1, 2)
        assert s.remove(1) is True
        assert s.insert(2) is False
        assert s.getRandom() == 2

        # ! 随机操作 + 和 Python set 对拍，顺带验证等概率
        import collections
        rng = random.Random(380)
        ref, obj = set(), cls()
        for _ in range(3000):
            v, op = rng.randrange(12), rng.random()
            if op < 0.5:
                assert obj.insert(v) == (v not in ref); ref.add(v)
            elif op < 0.9:
                assert obj.remove(v) == (v in ref); ref.discard(v)
            elif ref:
                assert obj.getRandom() in ref
        hist = collections.Counter()
        obj2 = cls()
        for v in range(5):
            obj2.insert(v)
        for _ in range(50000):
            hist[obj2.getRandom()] += 1
        assert all(8000 < c < 12000 for c in hist.values()), hist  # 等概率，期望 10000
    print("2 个解法全过（含 3000 次随机操作对拍 + 等概率检验）")
