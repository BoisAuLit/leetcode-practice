class TicTacToe:
    def __init__(self, n: int):
        self.n = n
        self.horizontal = [[0] * 2 for _ in range(n)]
        self.verital = [[0] * 2 for _ in range(n)]
        self.diagonal = [[0] * 2 for _ in range(2)]

    def check_rows(self, row: int, player: int) -> bool:
        self.horizontal[row][player - 1] += 1
        return self.horizontal[row][player - 1] == self.n

    def check_cols(self, col: int, player: int) -> bool:
        self.verital[col][player - 1] += 1
        return self.verital[col][player - 1] == self.n

    def check_diags(self, row: int, col: int, player: int) -> bool:
        if row == col:
            if row * 2 + 1 == self.n:
                self.diagonal[1][player - 1] += 1

            self.diagonal[0][player - 1] += 1
            return (
                self.diagonal[1][player - 1] == self.n
                or self.diagonal[0][player - 1] == self.n
            )
        if row + col == self.n - 1:
            self.diagonal[1][player - 1] += 1
            return self.diagonal[1][player - 1] == self.n
        return False

    def move(self, row: int, col: int, player: int) -> int:
        if self.check_rows(row, player):
            return player
        if self.check_cols(col, player):
            return player
        if self.check_diags(row, col, player):
            return player

        return 0


# Your TicTacToe object will be instantiated and called as such:
obj = TicTacToe(3)
print(obj.move(0, 0, 1))
print(obj.move(0, 2, 2))
print(obj.move(2, 2, 1))
print(obj.move(1, 1, 2))
print(obj.move(2, 0, 1))
print(obj.move(1, 0, 2))
print(obj.move(2, 1, 1))
