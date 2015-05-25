import os
import math

def get_driver_points_from_file(abs_file_path):
    path_list = []
    try:
        with open(abs_file_path, 'r') as myfile:
            myfile.readline() # info line

            while True:
                line = myfile.readline()
                if line == "":
                    break
                point = Point.from_file_line(line)
                path_list.append(point)
    except IOError:
        print("Error reading file!")
    return path_list


def count_avg_speed_on_path(path):
    distance = float(0.0)
    part_counter = int(0)

    a = iter(path)
    p1 = next(a)
    for p2 in a:
        part_counter += 1
        distance += p1.distance(p2)
        p1 = p2
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
        return str("(" + str(self.x) + "," + str(self.y) + ")")

if __name__ == "__main__":
    drivers_path = os.path.abspath('/home/lgadawski/_studia/drivers/')

    for root, dirs, files in os.walk(drivers_path):
        for path in files:
            abs_driver_path = root + '/' + path
            print(abs_driver_path)
            print("avg speed: " + str(count_avg_speed_on_path(get_driver_points_from_file(abs_driver_path))))
