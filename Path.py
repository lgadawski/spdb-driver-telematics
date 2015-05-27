from utils import get_distance


class Path:

    def __init__(self, driverid, routeid):
        self.driverid = driverid
        self.routeid  = routeid
        self.route        = []
        self.distance     = 0    # start with traveling zero distance
        self.time         = 0    # start with traveling for zero time

        self.feature_loc  = []
        self.angles       = []

        self.speed =    []
        self.speed_quintiles = []
        self.acceleration = []
        self.acceleration_quintiles = []
        self.total_energy = 0
        self.energy_per_distance = 0
        self.energy_per_time = 0

        self.time_in_speed = [0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0]

        self.angle_distances = []  # the distances between each of the angles

        self.comparison   = []

        self.matched      = -10   # default to not being matched

        self.is_zero      = 0  # if it is a zero distance route

        self.print_flag   = 0

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

            for cnt5 in range(0,len(speed_range)-2):
                if ( distance1 >= speed_range[cnt5] and distance1 < speed_range[cnt5+1]):
                    self.time_in_speed[cnt5] += 1.0

            if (cnt > start_num+2):
                acceleration = self.speed[-1] - self.speed[-2]
                self.acceleration.append(acceleration)

                energy =  abs( self.speed[-1]**2 - self.speed[-2]**2)
                self.total_energy += energy

            total_distance += distance1

            return total_distance
