import os
import Point

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
    """return avg speed on given path, distance, time"""
    distance = float(0.0)
    time = int(0)

    a = iter(path)
    p1 = next(a)
    for p2 in a:
        time += 1
        distance += p1.distance(p2)
        p1 = p2
    return distance / time, distance, time


if __name__ == "__main__":
    drivers_path = os.path.abspath('/home/lgadawski/_studia/drivers/')

    for root, dirs, files in os.walk(drivers_path):
        for path in files:
            abs_driver_path = root + '/' + path
            print(abs_driver_path)
            print("avg speed: " + str(count_avg_speed_on_path(get_driver_points_from_file(abs_driver_path))))
