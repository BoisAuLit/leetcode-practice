# 03 - 变长窗口之最短满足条件 (Minimum Valid Window)

## 核心定义

right 扩张直到窗口**满足**条件；然后**在满足的前提下**尽量收缩 left，
每次收缩前用当前长度更新答案。

## 和 Level 02 的区别（本专题最容易写反的地方）

| | Level 02 最长合法 | Level 03 最短满足 |
|---|---|---|
| while 的条件 | **不**合法 | **合法** |
| 收缩的目的 | 恢复合法 | 找更短的解 |
| 答案更新时机 | 收缩**之后** | 每次收缩**之前** |
| 答案 | `max(长度)` | `min(长度)` |

```python
# Level 02                              # Level 03
while not valid():                      while valid():
    shrink()                                best = min(best, right - left + 1)
best = max(best, right - left + 1)          shrink()
```

两段代码只差了「条件取反」和「更新位置」，但解决的是完全相反的问题。

## 决定性观察

1. 和 Level 02 一样，依赖**单调性**：窗口变长只会更容易满足条件。
   对 LC-0209 来说这等价于 **`nums[i] > 0`**。
2. 一旦允许负数，这套就塌了 —— 见 LC-0862：
   它改用**前缀和 + 单调队列**，把「找最短」变成「对每个右端找最靠右的合法左端」。
3. LC-0076 把「满足条件」从一个数值阈值换成「覆盖一张频率表」，
   用一个 `have` 计数（已经凑够数量的字符种类数）把判断降到 O(1)。

## Loop Invariant

进入内层 while 时窗口满足条件；吐掉左端之前先更新答案，吐完若仍满足就继续吐。

## Answer Update Timing

**在收缩之前**（此时窗口还是合法的）。写在收缩之后会把一个不合法的窗口记进答案。

## Python 模板

```python
left = 0
best = float("inf")
for right, x in enumerate(nums):
    add(x)
    while valid():                              # ! 合法才收缩
        best = min(best, right - left + 1)      # ! 先更新
        remove(nums[left])                      # ! 再吐
        left += 1
return best if best != float("inf") else 0
```

## LC-0076 的 have / need 计数

```python
need = Counter(t)
missing = len(need)          # 还有几种字符的数量没凑够
for right, ch in enumerate(s):
    need[ch] -= 1
    if need[ch] == 0:        # ! 恰好凑够才算一种（> 0 不算，< 0 是多余的）
        missing -= 1
    while missing == 0:      # 窗口合法，开始收缩
        ...更新答案...
        need[s[left]] += 1
        if need[s[left]] > 0:    # ! 吐出后不够了，种类数回退
            missing += 1
        left += 1
```

判断「恰好等于 0」而不是「<= 0」是关键：重复字符会让计数变成负数，
只有从 0 变成正数的那一刻才说明这一种真的缺了。

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P0** | [LC-0209 - Minimum Size Subarray Sum](01%20-%20%E6%95%B0%E5%80%BC%E9%98%88%E5%80%BC%E4%B8%8E%E6%9C%80%E7%9F%AD%E5%8C%BA%E9%97%B4/01%20-%20LC-0209%20-%20Minimum%20Size%20Subarray%20Sum) | M | 最短窗口的签名题；**依赖全正数** |
| **P1** | [LC-0862 - Shortest Subarray with Sum at Least K](01%20-%20%E6%95%B0%E5%80%BC%E9%98%88%E5%80%BC%E4%B8%8E%E6%9C%80%E7%9F%AD%E5%8C%BA%E9%97%B4/02%20-%20LC-0862%20-%20Shortest%20Subarray%20with%20Sum%20at%20Least%20K) | H | **有负数**：窗口单调性失效，改用前缀和 + 单调队列 |
| **P0** | [LC-0076 - Minimum Window Substring](02%20-%20%E5%AD%97%E7%AC%A6%E9%A2%91%E7%8E%87%E8%A6%86%E7%9B%96%E4%B8%8E%E6%9C%80%E5%B0%8F%E7%AA%97%E5%8F%A3/01%20-%20LC-0076%20-%20Minimum%20Window%20Substring) 📦 | H | Hard 里最重要的一道；need/have 计数 |

## 常见错误与边界

- while 条件写成「不合法」（变成了 Level 02）。
- 答案在收缩之后更新。
- 没找到时 0209 返回 0、0862 返回 -1、0076 返回空串 —— 三题的「失败值」都不一样。
- 0076 的 `need[ch] == 0` 写成 `<= 0`，重复字符就会算错。
- 在有负数的数组上套 0209 的模板（这正是 0862 存在的意义）。
