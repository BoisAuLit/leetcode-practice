"""LC-1024 - Video Stitching

Level 1 · 01 跳跃、可达性与区间覆盖 —— **Jump Game II 换了层皮**
题目在问：给一堆视频片段 `[start, end]`，最少用几个能覆盖 `[0, time]`？不能覆盖返回 -1。

决定性观察（它和 LC-0045 是同一道题）：
  1. 把「片段 `[s, e]`」看成「**从位置 s 出发，最远能跳到 e**」。
     于是「最少用几个片段覆盖 `[0, time]`」就是「**最少跳几次从 0 到 time**」
     ⟹ **LC-0045 Jump Game II**。
  2. 预处理：`reach[s] = max(e)` —— 从每个起点出发最远能到哪。
     （多个片段可能有同一个 start，取最远的那个。）
  3. 然后就是 LC-0045 的分层贪心：
     ```
     curr_end = 当前这层能覆盖到的最右端
     curr_far = 再用一个片段最远能到哪
     走到 i == curr_end 就必须再用一个片段
     ```

**和 LC-0045 的两个区别**（都要处理）：
  - **可能不可达** ⟹ 需要判断 `curr_far <= i`（卡住了）就返回 -1。
    LC-0045 题目保证可达，所以不用判。
  - 覆盖的是**区间** `[0, time]` 而不是「到达下标 n-1」⟹ 循环到 `time` 为止。

```python
reach = [0] * time
for s, e in clips:
    if s < time: reach[s] = max(reach[s], e)
ans = curr_end = curr_far = 0
for i in range(time):
    curr_far = max(curr_far, reach[i])
    if i == curr_end:
        if curr_far <= i: return -1       # ★ 卡住了，覆盖不到
        ans += 1
        curr_end = curr_far
return ans
```

**另一种等价写法**：按 start 排序后扫描（Solution_2）。
两者复杂度不同：数组版 O(n + time)，排序版 O(n log n)。
`time ≤ 100` 时数组版更快；time 很大时排序版更好。

### 这个「区间覆盖 ⟹ 跳跃」的转化还能用在
| 题 | 对应关系 |
|---|---|
| **LC-0045** Jump Game II | 原型 |
| **LC-1024** 本题 | 片段 = 跳跃范围 |
| **LC-1326** Minimum Taps to Water a Garden | 水龙头 `[i-r, i+r]` = 覆盖区间 |
| **LC-0452** Minimum Arrows | 反过来：求最少的「点」刺穿所有区间（见 14-intervals） |

复杂度：**O(n + time)** 时间，O(time) 空间。

边界：
  - `time = 0`（不需要任何片段）→ 0
  - 没有以 0 开头的片段 → -1
  - 中间有空隙 → -1
  - 一个片段就能覆盖全程 → 1
  - 片段重叠严重
"""

from typing import List


##################################################################################################
##### ! Solution 1: 转成 Jump Game II —— reach[s] 数组 + 分层贪心
##### ! 时间复杂度: O(n + time)   空间复杂度: O(time)
##### ! 适用：所有「最少用几个区间覆盖一段」的题；和 LC-0045 共用同一个分层贪心
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        if time == 0:
            return 0
        reach = [0] * time                   # ! reach[s] = 从 s 出发最远能到哪
        for s, e in clips:
            if s < time:
                reach[s] = max(reach[s], e)
        ans = curr_end = curr_far = 0
        for i in range(time):
            curr_far = max(curr_far, reach[i])
            if i == curr_end:
                if curr_far <= i:            # ! 卡住了：再怎么选也过不去
                    return -1
                ans += 1
                curr_end = curr_far
        return ans


##################################################################################################
##### ! Solution 2: 按 start 排序后扫描（time 很大时更好）
##### ! 时间复杂度: O(n log n)   空间复杂度: O(1)
##### ! 适用：time 远大于片段数时；思路相同，只是用排序代替 reach 数组
##################################################################################################


class Solution_2:
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        clips = sorted(clips)
        ans, curr_end, curr_far, i, n = 0, 0, 0, 0, len(clips)
        while curr_end < time:
            # ! 把所有「起点不超过当前覆盖右端」的片段都考虑一遍
            while i < n and clips[i][0] <= curr_end:
                curr_far = max(curr_far, clips[i][1])
                i += 1
            if curr_far <= curr_end:         # ! 没有任何片段能把覆盖范围往前推
                return -1
            ans += 1
            curr_end = curr_far
        return ans


##################################################################################################
##### ! Solution 3: BFS / DP 暴力（基准答案，用来对拍）
##### ! 时间复杂度: O(n · time)   空间复杂度: O(time)
##### ! 适用：正确性参照；把它看成「从 0 到 time 的最短路」
##################################################################################################


class Solution_3:
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        INF = float("inf")
        dp = [INF] * (time + 1)
        dp[0] = 0
        for t in range(1, time + 1):
            for s, e in clips:
                if s < t <= e and dp[s] + 1 < dp[t]:
                    dp[t] = dp[s] + 1
        return -1 if dp[time] == INF else dp[time]


if __name__ == "__main__":
    import random

    cases = [([[0, 2], [4, 6], [8, 10], [1, 9], [1, 5], [5, 9]], 10, 3),
             ([[0, 1], [1, 2]], 5, -1),
             ([[0, 1], [6, 8], [0, 2], [5, 6], [0, 4], [0, 3], [6, 7], [1, 3],
               [4, 7], [1, 4], [2, 5], [2, 6], [3, 4], [4, 5], [5, 7], [6, 9]], 9, 3),
             ([[0, 4]], 0, 0), ([[1, 5]], 5, -1), ([[0, 5]], 5, 1)]
    for clips, time, want in cases:
        a = Solution_1().videoStitching([c[:] for c in clips], time)
        b = Solution_2().videoStitching([c[:] for c in clips], time)
        c = Solution_3().videoStitching([c[:] for c in clips], time)
        assert a == b == c == want, (clips, time, a, b, c, want)
        print(f"time={time} -> {a}")

    for _ in range(800):
        n = random.randint(1, 8)
        clips = []
        for _ in range(n):
            s = random.randint(0, 8)
            clips.append([s, s + random.randint(0, 5)])
        time = random.randint(0, 10)
        a = Solution_1().videoStitching([c[:] for c in clips], time)
        b = Solution_2().videoStitching([c[:] for c in clips], time)
        c = Solution_3().videoStitching([c[:] for c in clips], time)
        assert a == b == c, (clips, time, a, b, c)
    print("随机对拍 800 组通过 ✓（reach 数组 == 排序扫描 == 最短路 DP）")
