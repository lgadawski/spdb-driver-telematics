import csv
import os
import numpy
import Path as p
import time

#https://github.com/PrincipalComponent/AXA_Telematics/blob/master/Features/generate_featureSet2.py

## this fun reads a CSV file and return header, and a list that
## has been converted to float
# returns headers ("x, y") and coords list:
# [[x1,y1], [x2,y2], ...[xn,yn]]
def read_csv_float_with_header(file1, list1):
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

def get_quintiles(float_list):
    float_list.sort()

    quintiles = []
    list_length = len(float_list)

    if (list_length > 5):
        for x in range(10, 110, 20):
            index1 = int(list_length * x / 100.)
            value1 = float_list[index1]

            quintiles.append(value1)

    else:
        quintiles = [0, 0, 0, 0, 0]

    return quintiles

def mainloop(driver_id, final_out_csv, drivers_path):
    start_time = time.time()

    list_of_paths = []
    list_of_lengths = []

    print("starttime %d" % start_time)

    ## read all driver's routes
    for cnt in range(1, 201):

        # init current path
        path = p.Path(1, cnt)

        input_coords =[]

        file_name = os.path.join(drivers_path, str(driver_id), str(cnt) + '.csv')

        header, input_coords = read_csv_float_with_header(file_name, input_coords)

        # converts input_coords list to array
        path_array = numpy.array(input_coords)
        path.route = path_array
        path.time = len(path.route) ## 1 sec per data file

        path.distance = path.get_route_distance(0, path.time)

        path.speed_quintiles = get_quintiles(path.speed)

        list_of_lengths.append(path.distance)

        list_of_paths.append(path)

    for cnt1, path1 in enumerate(list_of_paths):
        path1.distance = round(path1.distance, 4)
        path1.time = round(path1.time, 4)

        speed1 = round(path1.speed_quintiles[0], 4)
        speed2 = round(path1.speed_quintiles[1], 4)
        speed3 = round(path1.speed_quintiles[2], 4)
        speed4 = round(path1.speed_quintiles[3], 4)
        speed5 = round(path1.speed_quintiles[4], 4)

        final_out_csv.writerow(
            [driver_id, path1.routeid, path1.distance, path1.time, speed1, speed2, speed3, speed4, speed5])

    end_time = time.time()
    print("Elapsed: %d \n" % (end_time - start_time))



if __name__ == "__main__":
    drivers_path = os.path.abspath('/home/lgadawski/_studia/drivers/')

    final_out = open("featurematrix2.csv", 'wb')
    final_out_csv = csv.writer(final_out)
    final_out_csv.writerow(
        ['driver','route','distance','time', 'speed10pct','speed30pct','speed50pct','speed70pct','speed90pct'])

    for driver_id in range(1, 3613): ##
        try:
            file_name = os.path.join(drivers_path, str(driver_id), str(1) + ".csv")
            fileopen = open(file_name, "rb")
            fileopen.close()

            print("Processing driver %d" % driver_id)
            mainloop(driver_id, final_out_csv, drivers_path)
        except IOError:
            x = 1

    final_out.close()

    print("featurematrix2 csv created!")