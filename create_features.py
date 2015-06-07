import csv
import os
import numpy
import Path as p

## this fun reads a CSV file and return header, and a list that
## has been converted to float
# returns headers ("x, y") and coords list:
# [[x1,y1], [x2,y2], ...[xn,yn]]
from divide_features_file import divide_features_file
from random_forest import Start_RF

def read_csv_row_for_driver(file1, list1):
    fileopen = open(file1, 'rb')
    fileobject = csv.reader(fileopen)

    # get the header
    header = fileobject.next()

    # read each line in the CSV and convert the values to float
    # bedore appending to list1
    for row in fileobject:
        float_line = []
        for subrow in row:
            float_line.append(float(subrow))

        list1.append(float_line)

    fileopen.close()

    return header, list1

def start_creating_features(driver_id, final_out_csv, drivers_path):
    path_list = []

    ## read all driver's routes
    for cnt in range(1, 201):

        # init current path
        path = p.Path(1, cnt)

        coords =[]

        file_name = os.path.join(drivers_path, str(driver_id), str(cnt) + '.csv')

        header, coords = read_csv_row_for_driver(file_name, coords)

        # converts coords list to array
        path_array = numpy.array(coords)
        path.route = path_array
        path.time = len(path.route) ## 1 sec per data file

        path.distance = path.get_path_features(0, path.time)
        path.speed = (float(path.distance)) / (float(path.time))

        path_list.append(path)

    for cnt1, path1 in enumerate(path_list):
        path1.distance = round(path1.distance, 4)
        path1.time = round(path1.time, 4)
        path1.speed = round(path1.speed, 4)

        final_out_csv.writerow(
            [driver_id, path1.routeid, path1.distance, path1.time])

if __name__ == "__main__":
    drivers_path = os.path.abspath('/home/lgadawski/_studia/drivers/')

    feature_file = os.path.join(os.path.curdir, "features.csv")
    final_out = open("features.csv", 'wb')
    final_out_csv = csv.writer(final_out)
    final_out_csv.writerow(
        ['driver', 'route', 'distance', 'time'])

    for driver_id in range(1, 3613): ##
        try:
            file_name = os.path.join(drivers_path, str(driver_id), str(1) + ".csv")
            fileopen = open(file_name, "rb")
            fileopen.close()

            print("Processing driver %d" % driver_id)
            start_creating_features(driver_id, final_out_csv, drivers_path)

            # if (driver_id > 0 and driver_id % 200 == 0):
            #     print(driver_id)
            #     divide_features_file(feature_file)
            #     Start_RF(driver_id)
        except IOError:
            x = 1

    final_out.close()

    print("features csv created!")