"""LC-0721 - Accounts Merge

阶段 2 · 并查集 · 分组（并查集分派后按组输出） ○ 核心
题目在问：有相同邮箱的账户是同一个人，合并后输出每个人的 名字 + 排好序的邮箱
点是什么：一个账户下标（解法 1）/ 一个邮箱（解法 2）   边是什么：同一个邮箱出现在两个账户里
和签名题比改了哪一行：323 union 完只数块数；本题 union 完要按根分组（dict: 根 -> 邮箱集合），
                      每组邮箱排序、名字放最前面再输出；组与组之间的顺序随意
"""
from typing import List


class UnionFind:  # 路径减半 + 按 size 合并，union 返回 bool（成功合并才 True）
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


##################################################################################################
##### ! Solution 1: Union-Find，账户下标当点
##### ! 时间复杂度: O(M · α(k) + M log M)，k = 账户数，M = 邮箱总数（排序占大头）   空间复杂度: O(M)
##### ! 适用：面试首选；点只有 k 个，邮箱只做"谁先见过这个邮箱"的字典
##### ! ⭐️⭐️⭐️⭐️⭐️ Preferred Solution
##################################################################################################


class Solution_1:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        uf = UnionFind(len(accounts))
        owner = {}  # 邮箱 -> 第一次见到它的账户下标
        for i, acc in enumerate(accounts):
            for email in acc[1:]:
                if email in owner:
                    uf.union(i, owner[email])  # ! 同一个邮箱又出现了：这两个账户是同一个人
                else:
                    owner[email] = i

        groups = {}  # 根 -> 这一派的所有邮箱（set 顺便去重）
        for i, acc in enumerate(accounts):
            groups.setdefault(uf.find(i), set()).update(acc[1:])  # ! 按根分组

        return [[accounts[r][0]] + sorted(emails) for r, emails in groups.items()]  # 名字取根那个账户的


##################################################################################################
##### ! Solution 2: DFS，邮箱当点
##### ! 时间复杂度: O(M + M log M)   空间复杂度: O(M)
##### ! 适用：想直接拿到每个连通块的成员时；同一账户里把第一个邮箱和其余的连成星形就够了
##################################################################################################


class Solution_2:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        adj = {}  # 邮箱 -> 相邻邮箱
        name_of = {}  # 邮箱 -> 名字
        for acc in accounts:
            name, emails = acc[0], acc[1:]
            for e in emails:
                name_of[e] = name
                adj.setdefault(e, [])
            for e in emails[1:]:  # ! 星形连边：第一个邮箱连其余每个，账户内就连通了
                adj[emails[0]].append(e)
                adj[e].append(emails[0])

        seen = set()
        res = []
        for start in adj:
            if start in seen:
                continue
            seen.add(start)
            stack = [start]  # 用栈代替递归，邮箱最多 1e4 个，链状会爆递归
            comp = []
            while stack:
                e = stack.pop()
                comp.append(e)
                for nxt in adj[e]:
                    if nxt not in seen:
                        seen.add(nxt)
                        stack.append(nxt)
            res.append([name_of[start]] + sorted(comp))  # ! 一个连通块就是一个人
        return res


s = Solution_1()
accounts = [
    ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
    ["John", "johnsmith@mail.com", "john00@mail.com"],
    ["Mary", "mary@mail.com"],
    ["John", "johnnybravo@mail.com"],
]
result = s.accountsMerge(accounts)
print(result)
# [['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com'],
#  ['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com']]   组的顺序可以任意
