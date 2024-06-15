from typing import List

"""
Time complexity: O()
Space complexity: O()
"""


class Solution:
    def imageSmoother(self, img: List[List[int]]) -> List[List[int]]:
        m = len(img)
        n = len(img[0])

        nine_cells = []
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                nine_cells.append([x, y])
        print(nine_cells)

        for i in range(m):
            for j in range(n):
                sum_ = 0
                count = 0
                for a, b in nine_cells:
                    x = i + a
                    y = j + b
                    if (not 0 <= x <= m - 1) or (not 0 <= y <= n - 1):
                        continue

                    if a == -1 or (b == -1 and a == 0):
                        sum_ += img[x][y] % 256
                    else:
                        sum_ += img[x][y]
                    count += 1

                smoothed_vamue = sum_ // count
                img[i][j] = smoothed_vamue * 256 + img[i][j]
        for i in range(m):
            for j in range(n):
                img[i][j] = img[i][j] // 256
        return img


s = Solution()
# input_ = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
input_ = [[100, 200, 100], [200, 50, 200], [100, 200, 100]]
result = s.imageSmoother(input_)
print(result)
