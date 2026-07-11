# 区间问题 — 高频清单（盲区补齐）

> 你只做了 Merge/Insert 两题。区间是 FAANG 高频，必补。
> 核心信号：**"区间合并/重叠"、"会议室"、"最多不重叠"、"最少箭/点覆盖"**
> 通用套路：**先按起点或终点排序，再一次线性扫描 + 贪心**。

## 核心模式（一句话）
- 大多数区间题排序后线性扫一遍就解决。
- 排序键的选择（按起点 vs 按终点）决定题目难易——**贪心类常按终点排序**。

## 必做（按优先级）
- [ ] **0435 - Non-overlapping Intervals** ⭐️⭐️⭐️（NeetCode，未做，按终点排序的贪心经典）
- [ ] 0452 - Minimum Number of Arrows to Burst Balloons（和 0435 同一模式）
- [ ] 0986 - Interval List Intersections（双指针 + 区间）
- [ ] 0763 - Partition Labels（贪心 + 区间思想，NeetCode 未做）
- [ ] 1288 - Remove Covered Intervals
- [ ] **1851 - Minimum Interval to Include Each Query** ⭐️（NeetCode，未做，Hard，堆 + 区间，进阶）

## 复习（你已做过）
- [ ] 0056 - Merge Intervals（本文件夹）
- [ ] 0057 - Insert Interval（本文件夹）
- [ ] 0252 - Meeting Rooms（根目录）
- [ ] 0253 - Meeting Rooms II ⭐️（最经典，务必闭卷能写，堆 or 差分两种解法都要会）
