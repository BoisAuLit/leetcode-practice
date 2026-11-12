# 07 - 高阶字典序双指针 (Advanced Lexicographic)

## 算法定义

用两个候选起点互相比较，**一次比较排除一整段起点**，从而在 O(n) 内求出字典序最大的后缀或子串。
整体标记 **P2**：技巧性强、面试出现频率低，不要放进核心必背模板。

## Pointer Movement Rules（最大后缀，LC-1163）

维护当前最优起点 `i`、挑战者 `j`、偏移量 `k`：

```python
i, j, k = 0, 1, 0
while j + k < len(s):
    a, b = s[i + k], s[j + k]
    if a == b:
        k += 1                      # ! 还分不出胜负，往后多看一位
    elif a > b:
        j = j + k + 1               # ! 挑战者输了：j..j+k 全都不可能是答案
        k = 0
    else:
        i = max(i + k + 1, j)       # ! 当前最优输了：i..i+k 全都不可能
        j = i + 1
        k = 0
return s[i:]
```

**为什么能整段跳**：若 `s[i..i+k-1] == s[j..j+k-1]` 而 `s[i+k] > s[j+k]`，那么对任意
`0 <= t <= k`，以 `j + t` 开头的后缀都不优于以 `i + t` 开头的后缀，所以 `j..j+k`
这一整段起点可以一次性丢掉。每次比较要么 `k` 增加、要么某个指针至少前进 `k + 1`，总步数 O(n)。

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P2** | [LC-1163 - Last Substring in Lexicographical Order](01%20-%20%E6%9C%80%E5%A4%A7%E5%90%8E%E7%BC%80%E9%80%89%E6%8B%A9/01%20-%20LC-1163%20-%20Last%20Substring%20in%20Lexicographical%20Order) | H | 最大后缀的两候选互比 + 整段跳 |
| **P2** | [LC-3403 - Find the Lexicographically Largest String From the Box I](02%20-%20%E5%AD%97%E5%85%B8%E5%BA%8F%E6%9C%80%E5%A4%A7%E5%AD%90%E4%B8%B2%E4%B8%8E%E5%88%87%E5%88%86/01%20-%20LC-3403%20-%20Find%20the%20Lexicographically%20Largest%20String%20From%20the%20Box%20I) | M | 切分长度限制下取字典序最大的一段 |

两题的思想**相关但不等价**：1163 求最大**后缀**（长度不限），3403 在「必须切成 numFriends 段」
的限制下求最大的那一段，长度有上界；`numFriends == 1` 时答案是整个串，不要套 1163 的模板。

## 最容易出错的地方

- `i = max(i + k + 1, j)` 里的 `max` 不能省，否则 `i` 可能跳到 `j` 左边，造成重复比较甚至死循环。
- 每次换指针后 `k` 必须归零。
- 边界写成 `i + k < len(s)` 是错的，应该是 `j + k < len(s)`。

## 与相邻家族的区别

本家族比较的是**两个后缀**（两段子串）而不是两个元素，「移动指针」的含义是「淘汰一批起点」。
它更接近后缀数组 / Duval 算法的思想，和 Level 01 的对撞指针只是形式上都用了两个下标。
