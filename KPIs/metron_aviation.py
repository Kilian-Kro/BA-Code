from geopy.distance import geodesic

from base_classes.sector import Sector


class Metron:
    def __init__(self, sector):
        self.sector: Sector = sector
        self.time_threshold = 2  # in minutes
        self.min_sep_hor = 10  # in nautical miles
        self.min_sep_vert = 1000  # in feet

    def wact(self):
        return len(self.sector.get_planes())

    def wden(self):
        return len(self.sector.get_planes()) / self.sector.sector_volume()

    def wclap(self):
        threshold_min = 8
        threshold_max = 13
        count = 0  # for 8 one unit is added and half a unit is added, if the value is between 8 and 13
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    if self.dist_horizontal(plane, plane2) < threshold_min:
                        count += 1
                    elif threshold_min <= self.dist_horizontal(plane, plane2) < threshold_max:
                        count += 0.5
        return count / 2

    # The score then increases again to 1 for a convergence angle of 180
    def wconvang(self):
        score = 0
        list_of_planes = []
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    if self.are_in_conflict(plane, plane2):
                        conv_ang = max(plane.get_heading(), plane2.get_heading()) - min(plane.get_heading(),
                                                                                        plane2.get_heading())
                        # if convang is between 180 and 150 or between 0 and 30, score is 1
                        if (150 < conv_ang < 180) or (0 < conv_ang < 30):
                            score += 1
                        # if convang is between 150 and 110 or between 30 and 60, score is 0.5:
                        elif (110 < conv_ang < 150) or (30 < conv_ang < 60):
                            score += 0.5
                        # if convang is between 110 and 70 or between 60 and 90, score is 0.1
                        elif (70 < conv_ang < 110) or (60 < conv_ang < 90):
                            score += 0.1
                        # if convang is 90, score is 0:
                        elif conv_ang == 90:
                            score += 0
        return score

    def wconflict_nbrs(self):
        list_of_planes = []
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    if not self.are_in_conflict(plane, plane2) and self.dist_vertical(plane, plane2) < 2000 \
                            and self.dist_horizontal(plane, plane2) < 10:
                        self.add_to_list_no_duplicates(list_of_planes, plane, plane2)
        return len(list_of_planes)

    # Score 1 for each conflict within 10 miles
    # Score 0.5 for each conflict within 20 miles
    def wconf_bound(self):
        count = 0
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    if self.are_in_conflict(plane, plane2):
                        # Is this only counted for one aircraft or both? AND / OR
                        # E.g. what score is given if one plane is 9 miles and one 11 miles away?
                        if self.sector.distance_to_border(plane) < 10 and self.sector.distance_to_border(plane2) < 10:
                            count += 1
                        elif self.sector.distance_to_border(plane) < 20 and self.sector.distance_to_border(plane2) < 20:
                            count += 0.5
        return count

    # Count all aircraft where aircraft.getClimbrate != 0
    def walc(self):
        count = 0
        for plane in self.sector.get_planes():
            if plane.get_climb_rate() != 0:
                count += 1
        return count

    # Number of bearing changes above a certain threshold
    def wheadvar(self):
        # ToDo
        pass

    def wbprox(self):
        count = 0
        for plane in self.sector.get_planes():
            if self.sector.distance_to_border(plane) < 10:
                count += 1
        return count

    # The squared difference between the heading of each aircraft in a sector and the direction of the major axis
    # of the sector, weighted by the sector aspect ratio.
    def wasp(self):
        # ToDo
        pass

    # -------------------------------------
    # helper functions
    # -------------------------------------

    def are_in_conflict(self, plane_1, plane_2):
        min_sep_hor = 10  # in nautical miles
        min_sep_vert_low = 1000  # in feet below 29,000 feet
        min_sep_vert_high = 2000  # in feet above 29,000 feet

        if plane_1.altitude > 29000:
            if self.dist_vertical(plane_1, plane_2) < min_sep_vert_high and \
                    self.dist_horizontal(plane_1, plane_2) < min_sep_hor:
                return True

        elif self.dist_vertical(plane_1, plane_2) < min_sep_vert_low and \
                self.dist_horizontal(plane_1, plane_2) < min_sep_hor:
            return True

        return False

    @staticmethod
    def add_to_list_no_duplicates(list_planes, element1, element2):
        if element1 not in list_planes:
            list_planes.append(element1)
        if element2 not in list_planes:
            list_planes.append(element2)

    @staticmethod
    def dist_vertical(plane1, plane2):
        alt1 = plane1.altitude
        alt2 = plane2.altitude
        return max(alt1, alt2) - min(alt1, alt2)

    @staticmethod
    def dist_horizontal(plane1, plane2):
        distance_2d = geodesic((plane1.position_x, plane1.position_y), (plane2.position_x, plane2.position_y)).nautical
        return distance_2d
