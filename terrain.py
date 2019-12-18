import random


class Terrain:
    def __init__(self, width=20, height=15, data=None):
        if data is None:
            self.map = [[random.randint(0, 1)
                for _ in range(width)]
                    for _ in range(height)]
        else:
            self.map = [data[idx:idx + width]
                    for idx in range(0, len(data), width)]
        self.row = self.height = height
        self.col = self.width = width
