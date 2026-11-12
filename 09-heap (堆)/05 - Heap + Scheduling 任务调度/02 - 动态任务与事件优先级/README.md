# Level 2 · 02 动态任务与事件优先级

本 Level 2 共 3 道题，其中 **LC-1353 的实体目录在 13-greedy**（见下）。

| # | 题 | 优先级 | 位置 |
|---|---|---|---|
| 01 | LC-1834 Single-Threaded CPU | P1 | 本目录 |
| — | LC-1353 Maximum Number of Events That Can Be Attended | P1 | **跨专题索引** → [13-greedy](<../../../13-greedy (贪心)/04 - 区间调度与有序集合/01 - 最早截止时间优先/01 - LC-1353 - Maximum Number of Events That Can Be Attended>) |
| 02 | LC-2402 Meeting Rooms III | P1 | 本目录 |

## 为什么 LC-1353 只建索引
13-greedy 早就有这道题的完整资料（含用户的实现和一份讲解 PDF）。
一道题在题库里只能有一个实体文件夹，否则复习队列会重复。
本次重构把补充的「可跳跃天数」版本和暴力对拍**并入了那份 solution.py**，
用户原有实现一字未改。

它的 Primary Pattern 确实是 **Greedy（Earliest Deadline First）**，
堆只是用来快速拿到「当前可参加的会议里结束最早的那个」—— 归在 greedy 更准确。

## 三道题的共同骨架：事件驱动模拟

```python
tasks.sort(key=按到达时间)
heap, now, i = [], 0, 0
while 还有未完成的:
    while i < n and tasks[i].arrive <= now:
        heapq.heappush(heap, (优先级, ...)); i += 1
    if not heap:
        now = tasks[i].arrive       # ★ 时间跳跃，绝不逐秒推进
        continue
    取堆顶执行; now += 耗时
```

**时间跳跃是本节最关键的工程细节**：时间范围常达 10⁹，逐秒循环必然 TLE。

## 三道题的差异

| | 排序键 | 堆里放什么 | 特别之处 |
|---|---|---|---|
| **LC-1834** | enqueueTime | `(processingTime, index)` 最小堆 | 平局按**原始下标** ⟹ 排序前必须 `enumerate` |
| **LC-1353** | start | **end** 最小堆 | Earliest Deadline First；**每天只参加一个**，不是区间调度 |
| **LC-2402** | start | **两个堆**：free 按房间号 / busy 按结束时间 | 等待时新结束时间 = `e + (end - start)`，**时长不变** |

### LC-1834 和 LC-0502 IPO 是同一个骨架
「按某个维度排序**解锁** + 堆里选最优」。
区别只是解锁条件（到达时间 vs 资本）和最优方向（耗时最小 vs 利润最大）。

### LC-1353 最容易混的一点
它**不是**区间调度（LC-0435 那种按 end 排序贪心取不重叠）。
区间调度要求「占满整个区间」；本题**每个会议只占一天**，
所以同一个会议可以等到它区间里的任意一天再参加 ——
必须用堆**动态维护当前可选集合**，每天做一次选择。

### LC-2402 vs LC-0253 Meeting Rooms II
- **LC-0253** 只问「最少需要几个房间」⟹ 一个堆存 end 就够，不关心房间编号。
- **LC-2402** 房间数固定、要**具体分配**、还要**排队等待** ⟹ 必须两个堆。

LC-0253 的实体目录在 [14-intervals](<../../../14-intervals (区间)/>)。

## 常见错误
- 逐秒推进时间（TLE）。
- LC-1834 排序后丢了原始下标。
- LC-1353 套用区间调度；或忘了清理过期会议。
- LC-2402 等待时把结束时间写成 `end` 而不是 `e + (end - start)`。
- LC-2402 平局时没取编号最小的房间。
