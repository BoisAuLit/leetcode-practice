# 单调栈 / 单调队列 — 高频清单（盲区补齐）

> 这是你的空文件夹。单调栈是 FAANG 高频，必补。
> 核心信号：**"下一个更大/更小的元素"、"向左/右第一个比它大/小的"、"柱状图/矩形"、"窗口最值"**
> 做完打勾，并在每题写一句"信号 → 模式"。

## 核心模式（一句话）
- 单调栈 = 维护一个"单调递增或递减"的栈，新元素入栈前把破坏单调性的弹出，**被弹出的那一刻就是答案**。
- 单调队列 = 滑动窗口里的最值，队头永远是当前窗口最优。

## 必做（按优先级）
- [ ] **0084 - Largest Rectangle in Histogram** ⭐️⭐️⭐️（NeetCode，未做，单调栈的巅峰题，必吃透）
- [ ] **0853 - Car Fleet** ⭐️（NeetCode，未做）
- [ ] 0503 - Next Greater Element II（环形数组）
- [ ] 0901 - Online Stock Span
- [ ] 0085 - Maximal Rectangle（0084 的二维推广）
- [ ] 0907 - Sum of Subarray Minimums（贡献法 + 单调栈，进阶）

## 复习（你已做过，用单调栈视角重做一遍）
- [ ] 0739 - Daily Temperatures（在 04-stack-queue/002-stack，经典模板）
- [ ] 0496 - Next Greater Element I（本文件夹 04-stack-queue/monotonic-stack）
- [ ] 0239 - Sliding Window Maximum（单调队列，在 03-sliding-window）
- [ ] 0316 - Remove Duplicate Letters（本文件夹，单调栈应用）
- [ ] 0402 - Remove K Digits（本文件夹，单调栈应用）
- [ ] 0042 - Trapping Rain Water（本文件夹，也可双指针解，体会另一种视角）
