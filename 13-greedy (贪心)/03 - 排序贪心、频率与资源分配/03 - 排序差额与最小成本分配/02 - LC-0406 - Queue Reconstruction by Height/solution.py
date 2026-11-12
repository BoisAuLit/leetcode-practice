"""LC-0406 - Queue Reconstruction by Height（第二轮自主新增）

Level 1 · 03 排序贪心 —— **排序 + 按位置插入**（一个非常独特的贪心）
题目在问：每个人 `[h, k]`，h 是身高、k 是「前面比我高或等高的人数」。还原队列。

为什么新增它（它补的是哪个缺口）：
  本章其他题排序之后就是**线性扫描**。这道题排序之后要**按下标插入** ——
  利用了一个漂亮的性质：**矮的人插进去不影响高的人的 k 值**。
  这个「先确定一部分、后来的插入不破坏已确定部分」的思路非常独特，
  本专题原本没有这个视角。

决定性观察（排序规则 + 插入的正确性）：
  1. **排序：身高降序；身高相同时 k 升序。**
     ```python
     people.sort(key=lambda p: (-p[0], p[1]))
     ```
  2. **按顺序把每个人插到下标 k 的位置**：`res.insert(k, person)`。
  3. **为什么这样是对的**（这是全题的灵魂）：
     - 我们从**最高**的人开始放。放第 i 个人时，已经放进去的**都不比他矮**。
     - 所以他的 k 值（前面有几个 ≥ 他的人）**恰好等于他在当前列表里应该占的下标**。
     - 而**后来插入的人都比他矮或等高但 k 更大**，插在他前面也不会增加他的 k
       （比他矮的不计数）；插在他后面更不影响。
       ⟹ **一旦放好就不会被破坏**。∎
  4. **为什么身高相同时 k 要升序**：同身高的人互相计数。
     k 小的必须排在前面，所以先插 k 小的。
     如果 k 降序，先插的 k 大的会被后插的 k 小的挤到后面，位置就错了。

复杂度：**O(n²)**（`list.insert` 是 O(n)），空间 O(n)。
      用树状数组 / 平衡树可以做到 O(n log n)，但面试 O(n²) 完全够（n ≤ 2000）。

**注意不能反过来排（身高升序）**：那样插入时「已放好的人」比当前的人矮，
当前这个人的 k 和下标就没有对应关系了。

边界：
  - 所有人同身高 → 按 k 升序排好即可
  - 所有 k 都是 0 → 身高降序？不，是按身高升序排列（每个人前面都没有更高的）
  - 单个人
  - `[[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]]` → `[[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]`
"""

from typing import List


##################################################################################################
##### ! Solution 1: 身高降序 + 同高 k 升序，然后按 k 插入
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：「先确定一部分，后来的插入不破坏已确定部分」类贪心
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        # ! 身高降序；同身高时 k 升序（k 小的必须先插，否则会被挤到后面）
        people = sorted(people, key=lambda p: (-p[0], p[1]))
        res: List[List[int]] = []
        for h, k in people:
            res.insert(k, [h, k])     # ! 已放好的都不比他矮 ⟹ k 就是他该占的下标
        return res


##################################################################################################
##### ! Solution 2: 身高升序 + 找「第 k+1 个空位」（另一种经典写法）
##### ! 时间复杂度: O(n^2)   空间复杂度: O(n)
##### ! 适用：从矮到高放；每个人要留出 k 个空位给比他高的人
##################################################################################################


class Solution_2:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        n = len(people)
        # ! 身高升序；同身高时 k 降序（同高的人里 k 大的先占位）
        people = sorted(people, key=lambda p: (p[0], -p[1]))
        res: List[List[int] | None] = [None] * n
        for h, k in people:
            # ! 在空位里找第 k+1 个：前面要留 k 个空位给比他高的人
            seen = 0
            for i in range(n):
                if res[i] is None:
                    if seen == k:
                        res[i] = [h, k]
                        break
                    seen += 1
        return [p for p in res if p is not None]


##################################################################################################
##### ! Solution 3: 暴力枚举所有排列（基准答案，用来对拍；只适合很少的人）
##### ! 时间复杂度: O(n! · n^2)   空间复杂度: O(n)
##### ! 适用：正确性参照 —— 直接按题面定义验证每个人的 k 值
##################################################################################################


class Solution_3:
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        from itertools import permutations
        for perm in permutations(people):
            ok = True
            for i, (h, k) in enumerate(perm):
                if sum(1 for j in range(i) if perm[j][0] >= h) != k:
                    ok = False
                    break
            if ok:
                return [list(p) for p in perm]
        return []


if __name__ == "__main__":
    import random

    def valid(queue):
        for i, (h, k) in enumerate(queue):
            if sum(1 for j in range(i) if queue[j][0] >= h) != k:
                return False
        return True

    cases = [[[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]],
             [[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]],
             [[1, 0]], [[2, 0], [1, 1]]]
    for people in cases:
        a = Solution_1().reconstructQueue([p[:] for p in people])
        b = Solution_2().reconstructQueue([p[:] for p in people])
        assert valid(a) and valid(b), (people, a, b)
        assert sorted(a) == sorted(people) and sorted(b) == sorted(people)
        print(f"{people}\n   -> {a}")

    for _ in range(300):                 # ! 随机构造一个合法队列，再打乱，验证能还原
        n = random.randint(1, 6)
        heights = [random.randint(1, 4) for _ in range(n)]
        random.shuffle(heights)
        queue = []
        for i, h in enumerate(heights):
            k = sum(1 for j in range(i) if heights[j] >= h)
            queue.append([h, k])
        shuffled = queue[:]
        random.shuffle(shuffled)
        a = Solution_1().reconstructQueue([p[:] for p in shuffled])
        b = Solution_2().reconstructQueue([p[:] for p in shuffled])
        assert valid(a), (shuffled, a)
        assert valid(b), (shuffled, b)
        assert sorted(a) == sorted(queue) and sorted(b) == sorted(queue)
    print("随机对拍 300 组通过 ✓（降序插入 == 升序找空位，结果都满足每个人的 k）")
