from sklearn.ensemble.forest import RandomForestClassifier
import unittest
import os
from cmath import sqrt
from driver_functions import Point, get_driver_points_from_file, count_avg_speed_on_path


class TestDriverFunctions(unittest.TestCase):

    def test_example(self):
        row = [1]
        print(row[0])
        if(len(row) > 1):
            print(row[1])

    def test_count_distance(self):
        p1 = Point(0.0, 0.0)
        p2 = Point(1.0, 1.0)
        p3 = Point(0.0, 5.0)
        p4 = Point(4.0, 0.0)
        self.assertEqual(p1.distance(p2), sqrt(2))
        self.assertEqual(p1.distance(p3), 5.0)
        self.assertEqual(p1.distance(p4), 4.0)
        self.assertEqual(p2.distance(p1), sqrt(2))
        self.assertEqual(p3.distance(p1), 5.0)
        self.assertEqual(p4.distance(p1), 4.0)

    def test_avg_speed(self):
        points = get_driver_points_from_file(os.path.join(os.path.dirname(__file__), 'test_data.csv'))
        self.assertEqual(count_avg_speed_on_path(points)[0], 5)  ## avg speed
        self.assertEqual(count_avg_speed_on_path(points)[1], 20) ## distance
        self.assertEqual(count_avg_speed_on_path(points)[2], 4)  ## time

    def test_RandomForest(self):
        X = [[0, 1], [1, 1]]
        Y = [0, 1]

        regression = RandomForestClassifier(n_estimators=10)
        regression = regression.fit(X, Y)
        regression.predict_proba(X)


if __name__ == '__main__':
    unittest.main()
