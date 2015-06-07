from utils import get_distance


class Path:

    def __init__(self, driverid, routeid):
        self.driverid = driverid
        self.routeid  = routeid
        self.route        = []
        self.distance     = 0
        self.time         = 0

    def get_path_features(self, start_id, end_id):
        total_distance = 0
        start_num = min(start_id, end_id)
        end_num = max(start_id, end_id)

        for cnt in range(start_num+2, end_num):
            x1 = self.route[cnt-2, 0]
            y1 = self.route[cnt-2, 1]

            x2 = self.route[cnt, 0]
            y2 = self.route[cnt, 1]

            distance1 = get_distance(x1, y1, x2, y2)
            distance1 = distance1 / 2.0

            if (distance1 > 200):
               distance1 = 200

            total_distance += distance1

            return total_distance
