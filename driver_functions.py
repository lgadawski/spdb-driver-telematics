import os
import math

def get_driver_avg_speed(filename):
    distance = float(0.0)
    part_counter = int(0)
    try:
        with open(filename, 'r') as myfile:
            myfile.readline() # info line

            p1 = Point.from_file_line(myfile.readline())
            while True:
                line = myfile.readline()
                if line == "":
                    break
                p2 = Point.from_file_line(line)
                part_counter += 1
                distance += p1.distance(p2)
                p1 = p2
    except IOError:
        print("Error reading file!")
    return distance / part_counter

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
        return str("(" + self.x + "," + self.y + ")")

if __name__ == "__main__":
    drivers_path = os.path.abspath('/home/lgadawski/_studia/drivers/')

    for root, dirs, files in os.walk(drivers_path):
        for path in files:
            abs_driver_path = root + '/' + path
            print(abs_driver_path)
            print("avg speed: " + str(get_driver_avg_speed(abs_driver_path)))
