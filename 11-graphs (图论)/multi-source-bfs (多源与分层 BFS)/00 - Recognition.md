# Recognition — Multi-Source & Level BFS（多个源同时扩散 / 每一层 = 1 单位时间或距离）

题目信号
- "all rotten oranges spread at the same time", "distance to the nearest gate for every cell", "minutes until …", "level by level", "shortest bridge between two islands"

模板
- 把所有 source 一次性入队（distance 0）= 虚拟超级源点；一次 BFS 得到每个点到最近源的距离
- 分层：`for _ in range(len(queue))` 后 level += 1
- 反向思考：从目标集合往回扩散（0417 / 0130 在 `01`）

题目
- 0994 Rotting Oranges — 多源 + 分层计时
- 0286 Walls and Gates (Islands and Treasure) — 从所有 gate 出发
- 0934 Shortest Bridge — flood fill 找到岛 A，再以整座岛为源 BFS
- 0317 Shortest Distance from All Buildings — 每栋楼一次 BFS，累加距离
- 0429 N-ary Tree Level Order — 分层
- 0116 Populating Next Right Pointers — 分层 / O(1) 空间：用上一层的 next 指针
