"""LC-1244 - Design A Leaderboard

Level 1 · 06 Heap + Hash Map 数据结构设计 → Level 2 · 02 动态优先级与 Lazy Deletion

题目在问：`addScore(id, score)` 累加分数；`top(K)` 返回前 K 高分之和；`reset(id)` 清零。
Amazon / Meta 高频「暖场设计题」，重点不在算法难度，而在**说清楚每个操作的复杂度取舍**。

### 三种实现对应三种「谁来付钱」

| 方案 | addScore | top(K) | reset | 适合的调用分布 |
|---|---|---|---|---|
| 哈希表 + top 时排序 | O(1) | O(n log n) | O(1) | add/reset 多、top 少 |
| 哈希表 + top 时大小为 K 的最小堆 | O(1) | **O(n log K)** | O(1) | 一般情形的面试答案 |
| 哈希表 + 有序容器（SortedList / TreeMap） | O(log n) | O(K) | O(log n) | top 多、K 大 |

Python 没有内置平衡树；面试里说「Java 用 TreeMap、Python 用 sortedcontainers」即可，
也可以用 `bisect` 维护一个有序列表（插入 O(n) 但常数极小，10^4 规模下比堆快）—— `Solution_3`。

### top(K) 用最小堆而不是最大堆

要「最大的 K 个」，维护一个**大小为 K 的最小堆**：每个分数进来，堆满了就和堆顶（当前第 K 大）比，
比它大就替换。结束时堆里就是前 K 大。O(n log K)，K ≪ n 时明显优于全排序。
"""
from bisect import bisect_left, insort
from collections import defaultdict
import heapq


##################################################################################################
##### ! Solution 1: 哈希表 + top(K) 时用大小为 K 的最小堆
##### ! 时间复杂度: addScore / reset O(1)，top(K) O(n log K)   空间复杂度: O(n)
##### ! 适用：面试标准答案。heapq.nlargest(K, values) 内部就是这个算法，
#####         但手写一遍才能回答「为什么是最小堆」
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def __init__(self):
        self.score = defaultdict(int)

    def addScore(self, playerId: int, score: int) -> None:
        self.score[playerId] += score

    def top(self, K: int) -> int:
        heap = []                                  # ! 最小堆，只保留当前最大的 K 个
        for s in self.score.values():
            if len(heap) < K:
                heapq.heappush(heap, s)
            elif s > heap[0]:
                heapq.heapreplace(heap, s)        # ! 弹掉第 K 大、放入更大的，一步完成
        return sum(heap)

    def reset(self, playerId: int) -> None:
        self.score.pop(playerId, None)            # ! 删掉而不是置 0：置 0 会让 top 里出现一堆 0 参与比较


##################################################################################################
##### ! Solution 2: 哈希表 + top 时全排序
##### ! 时间复杂度: addScore / reset O(1)，top(K) O(n log n)   空间复杂度: O(n)
##### ! 适用：面试「第一版」，两行写完；追问「n 很大 K 很小」时升级到 Solution_1
##################################################################################################


class Solution_2:
    def __init__(self):
        self.score = defaultdict(int)

    def addScore(self, playerId: int, score: int) -> None:
        self.score[playerId] += score

    def top(self, K: int) -> int:
        return sum(sorted(self.score.values(), reverse=True)[:K])

    def reset(self, playerId: int) -> None:
        self.score.pop(playerId, None)


##################################################################################################
##### ! Solution 3: 哈希表 + 始终有序的分数列表（bisect 维护；TreeMap 的 Python 替身）
##### ! 时间复杂度: addScore / reset O(n)（列表插入删除，但常数极小），top(K) O(K)   空间复杂度: O(n)
##### ! 适用：top 调用远多于 add/reset 的场景。有 sortedcontainers 时把 list 换成 SortedList 即得 O(log n)
##################################################################################################


class Solution_3:
    def __init__(self):
        self.score = defaultdict(int)
        self.sorted_scores = []                   # ! 升序；和 score 的 values 多重集合一致

    def addScore(self, playerId: int, score: int) -> None:
        old = self.score[playerId]
        if old:
            del self.sorted_scores[bisect_left(self.sorted_scores, old)]
        self.score[playerId] = old + score
        insort(self.sorted_scores, old + score)

    def top(self, K: int) -> int:
        return sum(self.sorted_scores[-K:])       # ! 末尾 K 个就是最大的 K 个

    def reset(self, playerId: int) -> None:
        old = self.score.pop(playerId, 0)
        if old:
            del self.sorted_scores[bisect_left(self.sorted_scores, old)]


if __name__ == "__main__":
    import random
    random.seed(1244)
    for cls in (Solution_1, Solution_2, Solution_3):
        lb = cls()
        for pid, s in ((1, 73), (2, 56), (3, 39), (4, 51), (5, 4)):
            lb.addScore(pid, s)
        assert lb.top(1) == 73
        lb.reset(1); lb.reset(2)
        lb.addScore(2, 51)
        assert lb.top(3) == 141, cls.__name__

    for _ in range(30):
        impls = [Solution_1(), Solution_2(), Solution_3()]
        alive = set()
        for _ in range(1000):
            r = random.random()
            if r < 0.5:
                pid, s = random.randint(1, 15), random.randint(1, 100)
                for im in impls:
                    im.addScore(pid, s)
                alive.add(pid)
            elif r < 0.7 and alive:
                pid = random.choice(sorted(alive)); alive.discard(pid)
                for im in impls:
                    im.reset(pid)
            elif alive:
                K = random.randint(1, len(alive))
                outs = [im.top(K) for im in impls]
                assert outs[0] == outs[1] == outs[2], outs
    print("所有测试通过 ✓（样例 + 30 × 1000 步随机对拍）")
