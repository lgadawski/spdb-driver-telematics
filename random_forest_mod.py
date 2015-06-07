import csv
import numpy
import collections
from sklearn.ensemble import RandomForestClassifier

def Random_Forest(training_data, training_labels, test_data):
    print("Trainging data shape: " + str(training_data.shape))
    print("test data shape: " + str(test_data.shape))
    regression1 = RandomForestClassifier(n_estimators=300, max_depth=6)

    regression1.fit(training_data, training_labels)

    if (len(test_data) > 1):
        return regression1.predict_proba(test_data)

def prepare_training_set(feature_file):

    feature_input = open(feature_file, 'rb')
    feature_csv = csv.reader(feature_input)

    header = feature_csv.next()

    training_set = []
    for row in feature_csv:
        # if it is the generate training set, import routes number 5 and 110 for each driver
        if (len(row) > 1 and
                    (
                    #                     int(float(row[1])) == 5 or
                    # int(float(row[1])) == 110 or
                    int(float(row[0])) < 1000 and
                    int(float(row[1]) == 151))):
            training_set.append(row)

    # make a numpy array from the feature list
    training_set = numpy.array(training_set, dtype=numpy.float32)

    feature_input.close()

    return training_set

def get_driver_features(feature_file, driver_id, number_of_drivers_route_in_training_set):
    feature_input = open(feature_file, 'rb')
    features_csv = csv.reader(feature_input)

    header = features_csv.next()
    driver_routes = []
    for row in features_csv:
        # get all driver routes
        if (len(row) > 1 and (
                    int(float(row[0])) == driver_id
                and int(float(row[1])) <= (number_of_drivers_route_in_training_set+1)
        )):
            driver_routes.append(row)

    driver_routes = numpy.array(driver_routes, dtype=numpy.float32)

    feature_input.close()

    return driver_routes

def import_features(feature_file):

    feature_input = open(feature_file, 'rb')
    feature_csv = csv.reader(feature_input)
    header = feature_csv.next()
    features = []
    for row in feature_csv:
        features.append(row)

    # RandomForest need float values
    features = numpy.array(features, dtype=numpy.float32)

    feature_input.close()

    return features

def start():
    feature_file = "features.csv"
    features = import_features(feature_file)

    # preparing the set of drivers that don't match
    training_set = prepare_training_set(feature_file)

    print ("finished the set of drivers that don't match")
    print (" training set size: ", len(training_set), " routes")

    result_file = open("result.csv",'wb')
    result_csv = csv.writer(result_file)
    result_csv.writerow(['driver', 'trip_prob'])

    aggregated_result_file = open("result_aggregated.csv",'wb')
    aggregated_result_csv = csv.writer(aggregated_result_file)
    aggregated_result_csv.writerow(['driver', 'routes_prob'])

    n_o_drivers_route_in_training_set = 175
    driver_count = 0

    # loop through this many blocks of drivers
    # for data_block in data_blocks:
    for driver_id in range(1, 3613):

        current_driver_features = get_driver_features(feature_file, driver_id, n_o_drivers_route_in_training_set)
        print "Processing driver: ", driver_id

        if(len(current_driver_features) == 0): # brak kierowcy o danym id
            continue

        # set of samples current processing driver's routes need for training set
        test_data2 = current_driver_features[:, 2:]
        print(len(test_data2))

        # wszystkie rozne od aktualnie przetwarzanego, 2: -> czyli faktyczne cechy do przetworzenia
        training_data = training_set[numpy.where(training_set[:, 0] != driver_id)[0], 2:]

        concntenated_training_data = numpy.concatenate((test_data2, training_data), axis=0)

        training_labels = numpy.zeros(len(concntenated_training_data), dtype=numpy.float32)
        for x in range(0, n_o_drivers_route_in_training_set):
            training_labels[x] = 1.0

        test_data = features[numpy.where(features[:, 0] == driver_id)[0], 2:]

        results = Random_Forest(concntenated_training_data, training_labels, test_data)
        if isinstance(results, collections.Iterable):
            n_o_routes_above_50_proc = 0
            for cnt2, result in enumerate(results):
                if round(result[1], 2) > 0.50:
                    n_o_routes_above_50_proc = n_o_routes_above_50_proc + 1
                result_csv.writerow([str(int(driver_id)) + "_" + str(cnt2 + 1), result[1]])

            driver_count = driver_count + 1

            aggregated_result_csv.writerow([str(int(driver_count)), round((float(n_o_routes_above_50_proc)/200), 2)])

        result_file.flush()
        aggregated_result_file.flush()

    result_file.close()
    aggregated_result_file.close()

start()