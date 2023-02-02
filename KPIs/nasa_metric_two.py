from datetime import timedelta

from geopy.distance import geodesic

from base_classes.sector import Sector


class NasaTwo:
    def __init__(self, sector):
        self.sector: Sector = sector
        # The time threshold is not specified in the paper, so it was set to 2 minutes here
        # This means that for every indicator where a "change" in something is measured,
        # the change between now and two minutes ago is measured
        self.time_threshold = 2  # in minutes
        self.min_sep_hor = 10  # in nautical miles
        self.min_sep_vert = 1000  # in feet

    # Number of planes in the sector
    def traffic_density_n(self):
        return len(self.sector.get_planes())

    def heading_change_nh(self):
        count_of_changed_headings = 0
        # get the heading of the plane now and compare it to the heading two minutes ago
        # look for the time value and the corresponding list in history_planes
        for plane in self.sector.get_planes():
            for time, planes in self.sector.history_planes:
                if time == self.sector.passed_time - timedelta(minutes=self.time_threshold):
                    for plane_ago in planes:
                        # check if the heading changed more than 15 degrees
                        if abs(plane.get_heading() - plane_ago.get_heading()) > 15 and plane.get_callsign() == plane_ago.get_callsign():
                            count_of_changed_headings += 1
                    break
        return count_of_changed_headings

    # similar to the heading change function this function checks if the speed changed more than 10 knots
    # The current structure of past planes is a list of tuples (time, list of planes), which makes this function
    # a bit more complicated
    def speed_change_ns(self):
        count_of_changed_speeds = 0
        for plane in self.sector.get_planes():
            for time, planes in self.sector.history_planes:
                if time == self.sector.passed_time - timedelta(minutes=self.time_threshold):
                    for plane_ago in planes:
                        if abs(plane.get_speed() - plane_ago.get_speed()) > 10 and plane.get_callsign() == plane_ago.get_callsign():
                            count_of_changed_speeds += 1
                    break
        return count_of_changed_speeds

    # similar to the heading change function this function checks if the altitude changed more than 750 feet
    def altitude_change_na(self):
        count_of_changed_altitudes = 0
        for plane in self.sector.get_planes():
            for time, planes in self.sector.history_planes:
                if time == self.sector.passed_time - timedelta(minutes=self.time_threshold):
                    for plane_ago in planes:
                        if abs(plane.get_altitude() - plane_ago.get_altitude()) > 750 and plane.get_callsign() == plane_ago.get_callsign():
                            count_of_changed_altitudes += 1
                    break
        return count_of_changed_altitudes

    # Number of planes that are in proximity of 0 to 5 miles horizontally but not in violation
    def distance_between_0_and_5_s5(self):
        count_of_planes = 0
        for plane in self.sector.get_planes():
            for plane_2 in self.sector.get_planes():
                if plane != plane_2:
                    if self.sector.distance_between_two_planes(plane, plane_2) < 5 and self.are_not_in_violation(plane,
                                                                                                                 plane_2):
                        count_of_planes += 1
        return count_of_planes / 2

    # Number of planes that are in proximity of 5 to 10 miles horizontally but not in violation
    def distance_between_5_and_10_s10(self):
        count_of_planes = 0
        for plane in self.sector.get_planes():
            for plane_2 in self.sector.get_planes():
                if plane != plane_2:
                    if 5 < self.sector.distance_between_two_planes(plane, plane_2) < 10 and self.are_not_in_violation(
                            plane, plane_2):
                        count_of_planes += 1
        return count_of_planes / 2

    # Number of planes that are in proximity of 10 to 25 miles horizontally but not in violation
    def distance_between_0_and_25_s25(self):
        count_of_planes = 0
        for plane in self.sector.get_planes():
            for plane_2 in self.sector.get_planes():
                if plane != plane_2:
                    if plane.altitude > 29000 and plane_2.altitude > 29000:
                        if self.dist_horizontal(plane, plane_2) < 25 and self.dist_vertical(plane, plane_2) < 2000:
                            count_of_planes += 1
                    else:
                        if self.dist_horizontal(plane, plane_2) < 25 and self.dist_vertical(plane, plane_2) < 1000:
                            count_of_planes += 1
        return count_of_planes / 2

    # Number of planes that are in proximity of 25 to 40 miles horizontally but not in violation
    def distance_between_25_and_40_s40(self):
        count_of_planes = 0
        for plane in self.sector.get_planes():
            for plane_2 in self.sector.get_planes():
                if plane != plane_2:
                    if plane.altitude > 29000 and plane_2.altitude > 29000:
                        if 25 < self.dist_horizontal(plane, plane_2) < 40 and self.dist_vertical(plane, plane_2) < 2000:
                            count_of_planes += 1
                    else:
                        if 25 < self.dist_horizontal(plane, plane_2) < 40 and self.dist_vertical(plane, plane_2) < 1000:
                            count_of_planes += 1
        return count_of_planes / 2

    # Number of planes that are in proximity of 40 to 70 miles horizontally but not in violation
    def distance_between_40_and_70_s70(self):
        count_of_planes = 0
        for plane in self.sector.get_planes():
            for plane_2 in self.sector.get_planes():
                if plane != plane_2:
                    if plane.altitude > 29000 and plane_2.altitude > 29000:
                        if 40 < self.dist_horizontal(plane, plane_2) < 70 and self.dist_vertical(plane, plane_2) < 2000:
                            count_of_planes += 1
                    else:
                        if 40 < self.dist_horizontal(plane, plane_2) < 70 and self.dist_vertical(plane, plane_2) < 1000:
                            count_of_planes += 1
        return count_of_planes / 2

    # ----------------------------------------------------------------------------------------------------
    # helper functions
    # ----------------------------------------------------------------------------------------------------
    def are_not_in_violation(self, plane_1, plane_2):
        # Which plane determines if below of above 29000 feet -> what happens if one plane is above and the other below
        if plane_1.altitude > 29000:
            if self.dist_vertical(plane_1, plane_2) > self.min_sep_vert and self.dist_horizontal(plane_1,
                                                                                                 plane_2) > self.min_sep_hor:
                return True
        else:
            return False

    @staticmethod
    def dist_vertical(plane1, plane2):
        alt1 = plane1.altitude
        alt2 = plane2.altitude
        return max(alt1, alt2) - min(alt1, alt2)

    @staticmethod
    def dist_horizontal(plane1, plane2):
        distance_2d = geodesic((plane1.position_x, plane1.position_y), (plane2.position_x, plane2.position_y)).nautical
        return distance_2d
