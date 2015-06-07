import os
import csv

blockresults = os.path.join("blocks","results")
blockfeatures = os.path.join("blocks","features")

def divide_features_file(feature_file):

    counter = 0
    counter2 = 1
    current_driver = 0
    output_file = open(os.path.join(blockfeatures, "features_block_" + str(counter2) + ".csv"), 'wb')
    output_csv = csv.writer(output_file)
    counter2 = 0

    feature_input = open(feature_file, 'rb')
    feature_csv = csv.reader(feature_input)

    header = feature_csv.next()

    for row in feature_csv:
        current_csv_driver = int(float(row[0]))
        if (current_csv_driver != current_driver):
            current_driver = current_csv_driver
            counter += 1
            print("doing driver ", current_driver)

            if (counter % 100 == 1):
                counter2 += 1
                output_file.close()
                output_file = open(os.path.join(blockfeatures, "features_block_" + str(counter2) + ".csv"), 'wb')
                output_csv = csv.writer(output_file)

        for counter3, item in enumerate(row):
            if ('nan' in row[counter3]):
                row[counter3] = 0.
            else:
                row[counter3] = float(row[counter3])

        if (len(row) == 4):
            output_csv.writerow(row)

    output_file.close()
    return

features_file = os.path.join(os.path.curdir, "features.csv")
