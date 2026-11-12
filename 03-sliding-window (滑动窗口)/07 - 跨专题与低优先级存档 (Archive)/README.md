# 07 - 跨专题与低优先级存档 (Archive)

**这不是必刷目录。** 这里的题主算法不是滑动窗口，保留是为了不丢学习成果。

| | 题 | 难度 | 说明 |
|---|---|---|---|
| **P2** | [LC-3499 - Maximize Active Section with Trade I](01%20-%20%E8%BF%9E%E7%BB%AD%E5%AD%97%E7%AC%A6%E6%AE%B5%E4%B8%8E%E8%B4%AA%E5%BF%83/01%20-%20LC-3499%20-%20Maximize%20Active%20Section%20with%20Trade%20I) | M | Run-length 扫描 + 贪心 |

## LC-3499 为什么是 P2

它的核心是把 01 串压成「连续段」（run-length），再贪心地考虑把某一段 0 翻转后
能把左右两段 1 连起来。这是**段扫描 + 贪心**，不是定长也不是变长窗口模板。
保留全部代码和 PDF，不要求当成滑动窗口模板背。

## 原来的「01 - 单次扫描与股票题」去哪了

那里放的是 `NC - Best Time to Buy and Sell Stock`，它就是 **LC-0121**，
而 LC-0121 在 [12-dynamic-programming/stock-series](<../../12-dynamic-programming (动态规划)/07 - 股票与状态机 DP/01 - 单次与无限次交易/01 - LC-0121 - Best Time to Buy and Sell Stock>)
已经有正式版本。按「LC 和 NC 重复只保留 LeetCode 版」的规则，NC 那份已移入废纸篓，
本目录的 Level 2 相应地从两个减到一个。

**它为什么本来就不算滑动窗口**：标准解法是一边扫一边维护「到目前为止的最低价」，
没有需要收缩的窗口 —— 左端点只在遇到更低价时**跳到当前位置**，
而不是因为窗口不合法被迫右移。那属于 One-pass Running Minimum。
