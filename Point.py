import math

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def from_file_line(cls, line):
        p1_line = [x.strip() for x in line.split(',')]
        return cls(float(p1_line[0]), float(p1_line[1]))

    def distance(self, p2):
        return math.sqrt(pow((p2.x - self.x), 2) + pow((p2.y - self.y), 2))

    def __str__(self):
        return str("(" + str(self.x) + "," + str(self.y) + ")")