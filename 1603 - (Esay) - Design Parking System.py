class ParkingSystem:
    def __init__(self, big: int, medium: int, small: int):
        self.counter = [big, medium, small]

    def addCar(self, carType: int) -> bool:
        if self.counter[carType - 1] == 0:
            return False
        self.counter[carType - 1] -= 1
        return True
