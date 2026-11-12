"""
Hierholzer 欧拉路径: 后序入栈再反转

画面:   一笔画: 从起点顺着机票一张张飞, 飞到没票可用的机场就 "卡住";
        卡住的机场一定是终点 (或某个绕回来的小圈的尽头), 把它写下来, 退回上一站继续飞剩下的票。
        写下的顺序反过来, 就是一笔画的路线。
动作:   ① 整理票 (邻接表; 要字典序最小就把目的地倒序排, 方便 pop 出最小的)
        ② 顺着飞 (只要还有票就 pop 一张走过去; 票用一张少一张, 这就是 visited)
        ③ 卡住入栈 (没票了就把当前机场压进 path)
        ④ 反转 (path[::-1])
动作对代码: 见下面 # ! 注释
签名题: LC-332 Reconstruct Itinerary
决策句: "每条边恰好走一次" 用它 (欧拉路径); "每个点恰好走一次" 是哈密顿路径, 那是 NP 难, 只能回溯。
        起点: 有向图选 out - in = 1 的点, 没有就任选 (LC-332 规定 JFK)。
改一行: 和 02 DFS 比, visited 从 "点" 变成 "边" (pop 一张票 = 这条边走过了), 答案在退出来时记 (后序), 不是进去时。
        和 07 三色 DFS 比, 都是 "后序入栈再反转", 只是 07 记点的完成顺序, 这里记边的走完顺序。
"""
from collections import defaultdict
from typing import List


def find_itinerary_recursive(tickets: List[List[str]]) -> List[str]:
    adj = defaultdict(list)
    for u, v in sorted(tickets, reverse=True):
        adj[u].append(v)                                # ! ① 倒序放, pop 出来的就是字典序最小的
    path = []

    def fly(u: str) -> None:
        while adj[u]:
            fly(adj[u].pop())                           # ! ② 顺着飞: pop 一张票就是用掉一条边
        path.append(u)                                  # ! ③ 卡住入栈 (后序)

    fly("JFK")
    return path[::-1]                                   # ! ④ 反转


def find_itinerary_iterative(tickets: List[List[str]]) -> List[str]:
    adj = defaultdict(list)
    for u, v in sorted(tickets, reverse=True):
        adj[u].append(v)                                # ! ①
    stack = ["JFK"]
    path = []
    while stack:
        while adj[stack[-1]]:
            stack.append(adj[stack[-1]].pop())          # ! ② 顺着飞
        path.append(stack.pop())                        # ! ③ 卡住入栈
    return path[::-1]                                   # ! ④


if __name__ == "__main__":
    t1 = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    print(find_itinerary_recursive(t1))     # ['JFK', 'MUC', 'LHR', 'SFO', 'SJC']
    t2 = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    print(find_itinerary_recursive(t2))     # ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO']
    print(find_itinerary_iterative(t2))     # ['JFK', 'ATL', 'JFK', 'SFO', 'ATL', 'SFO']
