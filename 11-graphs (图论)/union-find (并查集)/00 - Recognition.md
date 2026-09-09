# Recognition — Union-Find / Dynamic Connectivity

题目信号
- 边不断加入，反复问 "x, y 连通吗？" / "还有几组？" / "什么时候全连通？"
- 按下标分组（同组内可任意交换）
- 不需要路径、不需要距离、不需要删边

模板（`00 - UnionFind Template.py`）
- find 路径压缩：`root[x] = find(root[x])`（注意是 root[x] 不是 x）
- union by rank；count −= 1
- O(α(n)) ≈ O(1) 每次操作

本目录题目（UF 是核心解法）
- 1101 Earliest Moment Friends — 按时间排序 + union，count == 1 时返回
- 1202 Smallest String With Swaps — 按 root 分组，组内排序

其它用到 UF 的题只存一份，见 `Union-Find Applications.md`
