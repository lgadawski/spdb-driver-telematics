import csv
import numpy
import os
from sklearn.ensemble import RandomForestClassifier

def Random_Forest(training_data, traingin_labels, test_data):
    #https://github.com/PrincipalComponent/AXA_Telematics/blob/master/Features/train_featureSet2.py

    regression1 = RandomForestClassifier(n_estimators=350, max_depth=6)
    regression1.fit(training_data, traingin_labels)

    return regression1.predict_proba(test_data)

def import_features(feature_file):

    feature_input = open(feature_file, 'rb')
    feature_csv = csv.reader(feature_input)

    features = []
    for row in feature_csv:
        features.append(row)

    # make a numpy array from the feature list
    features = numpy.array(features, dtype=numpy.float32)

    feature_input.close()

    return features

def make_training_set(feature_file, driver_id):

    feature_input = open(feature_file, 'rb')
    feature_csv = csv.reader(feature_input)

    header = feature_csv.next()

    training_set = []
    for row in feature_csv:
        # if it is the generate training set, import routes number 5 and 110 for each driver
        if (driver_id == 0):
            if (int(float(row[1])) == 5 or
                int(float(row[1])) == 110  or
                int(float(row[1])) == 151 ):
                training_set.append(row)
        elif (driver_id > 0):
            # it it is the test set, import all for that drivers
            if( int(float(row[0])) == driver_id):
                training_set.append(row)

    ## make a numpy array from the feature list
    training_set = numpy.array(training_set, dtype=numpy.float32)

    feature_input.close()

    return training_set

FEATURES = os.path.join(os.path.curdir, 'Features')
blockresults = os.path.join(FEATURES, "blocks", "results")
blockfeatures = os.path.join(FEATURES, "blocks", "features")

def Main_Regression():
    feature_file = "featurematrix2.csv"

    ## preparing the set of drivers that don't match
    training_set = make_training_set(feature_file, 0)

    print ("finished the set of drivers that don't match")
    print (" total ",len(training_set)," routes")

    data_blocks = [1,2,3,4,5,6,7,8,9,10,11,12,23,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
    #
    # subset_range = [1,2,3,4,5,6,7,8,9,10]
    # data_blocks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    subset_range = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # loop through this many blocks of drivers
    for data_block in data_blocks:

        print "Making test set for data block ", data_block, "\n\n"

        feature_file = os.path.join(
            blockfeatures,
            "Scott_features_block_" + str(data_block) + ".csv")
        features = import_features(feature_file)

        print("Features %d" % len(features))
        print("-- Finished making test set for data block " + str(data_block))

        # drivers in the file
        drivers = features[:, 0]
        drivers = numpy.unique(drivers)
        print("\n There are %d different drivers \n" % len(drivers))

        for cnt, driver in enumerate(drivers):

            if (cnt % 10 == 0):
                if (cnt != 0):
                    try:
                        telematics_file.close()
                    except:
                        pass

                subset1 = int(cnt / 10) + 1

                if (subset1 in subset_range):
                    telematics_file = open(os.path.join(
                        blockresults,
                        "Telematics_results_Scott_features_Run1_block_"+str(data_block)+ "_subset_"+str(subset1)+".csv"),'wb')
                    telematics_csv = csv.writer(telematics_file)
                    telematics_csv.writerow(['driver', 'trip_prob'])

            if (subset1 in subset_range):
                for i in range(1, 9):
                    print("Starting Forest for driver %d" % driver)

                    start_num = (i - 1) * 25
                    end_num = i * 25

                    # these are all the features
                    test_block = features[numpy.where(features[:, 0] == driver)[0], 2:]

                    test_data = test_block[start_num:end_num, :]

                    if (i == 1):
                        test_data2 = test_block[end_num + 1 :, :]
                    elif (i == 10):
                        test_data2 = test_block[ : start_num, :]
                    else:
                        test_data3 = test_block[ : start_num, :]
                        test_data4 = test_block[end_num + 1 :, :]
                        test_data2 = numpy.concatenate((test_data3, test_data4), axis=0)

                    driver_id = driver

                    training_data = training_set[numpy.where(training_set[:, 0] != driver)[0], 2:]

                    joined_training_data = numpy.concatenate((test_data2, training_data), axis=0)

                    training_labels = numpy.zeros(len(joined_training_data), dtype=numpy.float32)
                    for x in range(0, 175):
                        training_labels[x] = 1.0

                    results = Random_Forest(joined_training_data, training_labels, test_data)

                    for cnt2, result in enumerate(results):
                        telematics_csv.writerow([str(int(driver)) + "_" + str(cnt2 + start_num + 1), result[1]])

                    telematics_file.flush()

        telematics_file.close()
        print("\n ********** Finished block ************\n %d", data_block)

Main_Regression()