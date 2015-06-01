from utils import get_distance


class Path:

    def __init__(self, driverid, routeid):
        self.driverid = driverid
        self.routeid  = routeid
        self.route        = []
        self.distance     = 0    # start with traveling zero distance
        self.time         = 0    # start with traveling for zero time

        self.speed =    []
        self.speed_quintiles = []

    #********************
    # This gets the distance traveled along a route
    #********************
    def get_route_distance(self, start_id, end_id):
        total_distance = 0
        start_num = min(start_id, end_id)
        end_num = max(start_id, end_id)

        speed_range = [0,3,6,9,12,15,20,25,30,35,40,45,50,60]

        for cnt in range( start_num+2, end_num):
            x1 = self.route[ cnt-2, 0]
            y1 = self.route[ cnt-2, 1]

            x2 = self.route[ cnt, 0]
            y2 = self.route[ cnt, 1]

            distance1 = get_distance(x1, y1, x2, y2)
            distance1 = distance1 / 2.0

            if (distance1 > 200):
               distance1 = 200

            self.speed.append(distance1)

            total_distance += distance1

            return total_distance
