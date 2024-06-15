class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None


class Solution:
    def lowestCommonAncestor(self, p: 'Node', q: 'Node') -> 'Node':
        ancestors_p = {p.val}
        ancestors_q = {q.val}
        while True:
            new_p = new_q = None
            if p.parent:
                p = p.parent
                new_p = p
                ancestors_p.add(p.val)
            if q.parent:
                q = q.parent
                new_q = q
                ancestors_q.add(q.val)

            if new_p and new_p.val in ancestors_q:
                return new_p
            if new_q and new_q.val in ancestors_p:
                return new_q
