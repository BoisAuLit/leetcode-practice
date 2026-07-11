from collections import Counter


class TwoSum:
    def __init__(self):
        self.array = []
        self.counter = Counter()

    def add(self, number: int) -> None:
        self.array.append(number)
        self.counter.update({number: 1})

    def find(self, value: int) -> bool:
        if len(self.array) < 2:
            return False
        for v, count in self.counter.items():
            complement = value - v
            if v == complement:
                if count >= 2:
                    return True
            elif complement in self.counter:
                return True
        return False


