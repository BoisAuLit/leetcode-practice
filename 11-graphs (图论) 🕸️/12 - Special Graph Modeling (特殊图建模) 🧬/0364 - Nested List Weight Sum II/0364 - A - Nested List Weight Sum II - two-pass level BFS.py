class Solution:
    def depthSumInverse(self, nestedList) -> int:
        # Step 1： Use bfs to get max depth, bfs is so cute
        level = nestedList
        max_depth = 0
        while level:
            max_depth += 1
            next_level = []
            for elem in level:
                if not elem.isInteger():
                    next_level.extend(elem.getList())
            level = next_level

        # Step 2: Do bfs again to get the final result
        level = nestedList
        curr_depth = 0
        res = 0
        while level:
            curr_depth += 1
            next_level = []
            for elem in level:
                if not elem.isInteger():
                    next_level.extend(elem.getList())
                else:
                    res += elem.getInteger() * (max_depth - curr_depth + 1)
            level = next_level
        return res
