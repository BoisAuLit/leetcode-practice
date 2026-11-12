# 04 - 回文与字符串双指针 (Palindrome)

## 算法定义

回文的定义天生对称，所以有两种对偶的指针用法：

- **向内收**（验证）：`l = 0, r = n-1`，一边比较一边向中间走 → 判断是不是回文
- **向外扩**（枚举）：固定一个中心，`l` 左走 `r` 右走 → 找出或数出所有回文

## Pointer Movement Rules

| 子类 | 规则 |
|---|---|
| 验证（0125）| 两端相向；遇到不该比较的字符**只移动那一侧** |
| 容错验证（0680）| 首次不匹配时分叉成两种尝试：跳过左边 or 跳过右边 |
| 中心扩展（0005、0647）| 枚举 2n-1 个中心，每个中心两端同时外扩直到不等 |
| 过滤反转（0345、0917）| 两端相向，**两侧都停在合法字符上**才交换 |

## Loop Invariants

- 验证类：`s[0:l]` 和 `s[r+1:]` 已经确认互为镜像。
- 中心扩展：进入 while 时 `s[l:r+1]` 已经是回文。
- 过滤反转：`[0, l)` 和 `(r, n-1]` 已经交换完毕。

## 必备模板

```python
# 验证（LC-0125）
l, r = 0, len(s) - 1
while l < r:
    while l < r and not s[l].isalnum():   # ! 只移动不合法的那一侧
        l += 1
    while l < r and not s[r].isalnum():
        r -= 1
    if s[l].lower() != s[r].lower():
        return False
    l += 1
    r -= 1
return True

# 容错一次（LC-0680）
def ok(l, r):
    while l < r:
        if s[l] != s[r]:
            return False
        l += 1
        r -= 1
    return True

l, r = 0, len(s) - 1
while l < r:
    if s[l] != s[r]:
        return ok(l + 1, r) or ok(l, r - 1)   # ! 只有这两种分支
    l += 1
    r -= 1
return True
```

**为什么 0680 只需要两个分支**：第一次出现 `s[l] != s[r]` 时，这两个字符**至少要删一个**
（留着它们就不可能对称），而配额只有一次，所以要么删左要么删右，没有第三种可能；
在这之前的部分已经匹配，不需要回头。

## 本家族题目

| | 题 | 难度 | 这一题新增的东西 |
|---|---|---|---|
| **P0** | [LC-0125 - Valid Palindrome](01%20-%20%E5%9B%9E%E6%96%87%E9%AA%8C%E8%AF%81%E4%B8%8E%E5%AE%B9%E9%94%99/01%20-%20LC-0125%20-%20Valid%20Palindrome) 📦 | E | 过滤 + 大小写归一化 |
| **P0** | [LC-0680 - Valid Palindrome II](01%20-%20%E5%9B%9E%E6%96%87%E9%AA%8C%E8%AF%81%E4%B8%8E%E5%AE%B9%E9%94%99/02%20-%20LC-0680%20-%20Valid%20Palindrome%20II) | E | 一次容错 ⇒ 两个分支的分叉证明 |
| **P0** | [LC-0005 - Longest Palindromic Substring](02%20-%20%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95%20%28Expand%20Around%20Center%29/01%20-%20LC-0005%20-%20Longest%20Palindromic%20Substring) | M | 枚举 **2n-1 个中心**，向外扩 |
| **P1** | [LC-0647 - Palindromic Substrings](02%20-%20%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95%20%28Expand%20Around%20Center%29/02%20-%20LC-0647%20-%20Palindromic%20Substrings) | M | 同一个 expand，把「取最长」换成「计数」 |
| **P2** | [LC-0345 - Reverse Vowels of a String](03%20-%20%E5%AD%97%E7%AC%A6%E8%BF%87%E6%BB%A4%E4%B8%8E%E5%8F%8D%E8%BD%AC/01%20-%20LC-0345%20-%20Reverse%20Vowels%20of%20a%20String) | E | 两侧都要停在合法字符上才交换 |
| **P2** | [LC-0917 - Reverse Only Letters](03%20-%20%E5%AD%97%E7%AC%A6%E8%BF%87%E6%BB%A4%E4%B8%8E%E5%8F%8D%E8%BD%AC/02%20-%20LC-0917%20-%20Reverse%20Only%20Letters) | E | 和 0345 同一个模板，只换「合法」的定义 |

**LC-0005**（P0）和 **LC-0647**（P1）原以 NeetCode 版本放在动态规划专题，现已搬入本家族 ——
它们现有的解法本来就是中心扩展，区间 DP 版作为 `Solution_2` 保留。完整讲解、2n-1 个中心的
来历和模板见 [02 - 中心扩展 (Expand Around Center)/README.md](02%20-%20%E4%B8%AD%E5%BF%83%E6%89%A9%E5%B1%95%20%28Expand%20Around%20Center%29/README.md)。

## 最容易出错的地方

- 跳过非法字符的内层 while 忘了带 `l < r` 条件 → 越界。
- `"0P"` 这类用例：`isalnum()` 对数字也返回 True，必须 `lower()` 后再比，不能用 `isalpha()`。
- 中心扩展**漏掉偶数中心**（只枚举了 n 个而不是 2n-1 个）。
- 0680 的两个分支写成 `and` 而不是 `or`。

## 与相邻家族的区别

- **Level 01 对撞**：靠「有序」排除候选；回文类靠「对称」做比较，不需要有序。
- **Level 05 多序列**：两个指针在**两个不同的序列**上；本家族两个指针在同一个序列上。
- 链表上的回文（LC-0234）要先用快慢指针找中点再反转后半段，属于 Level 06，文件夹在
  [06-linked-list/fast-slow-pointers](<../../06-linked-list (链表)/02 - 双指针、固定间距与链表中点/03 - 中点、反转与双端重组/01 - LC-0234 - Palindrome Linked List>)。
