from geopy.distance import geodesic

from base_classes.sector import Sector


class NasaAdditional:
    def __init__(self, sector):
        self.sector: Sector = sector
        self.time_threshold = 2  # in minutes
        self.min_sep_hor = 10  # in nautical miles
        self.min_sep_vert_low = 1000  # in feet below 29,000 feet
        self.min_sep_vert_high = 2000  # in feet above 29,000 feet

    def numhorizon(self):
        # ToDo rewrite
        pass

    # Calculate the Variance of all aircraft headings in the sector
    def hdgvari(self):
        list_of_headings = []
        for plane in self.sector.get_planes():
            list_of_headings.append(plane.get_heading())
        mean = sum(list_of_headings) / len(list_of_headings)
        variance = sum((x - mean) ** 2 for x in list_of_headings) - 1 / len(list_of_headings)
        return variance

    def axishdg(self):
        pass

    def convconf(self):
        list_of_headings = []
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    if self.are_in_conflict(plane, plane2):
                        list_of_headings.append(plane.get_heading())
        if len(list_of_headings) == 0:
            return 0
        else:
            return (sum(list_of_headings) / 2) / len(list_of_headings)  # /2 because every pair is counted twice

    # ToDO define close proximity to a potential conflict
    def proxcount(self):
        list_of_potential_conflicts = []
        dist_hor = 0.
        dist_vert = 0.
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    dist_hor = self.dist_horizontal(plane, plane2)
                    dist_vert = self.dist_vertical(plane, plane2)
                    # Different vertical separation requirements depending on altitude
                    if plane.get_altitude() > 29000:
                        # horizontal sep requirement is not met
                        if dist_hor < self.min_sep_hor and self.min_sep_vert_high + 2000 > dist_vert > self.min_sep_vert_high:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)
                        # vertical sep requirement is not met
                        if self.min_sep_hor + 10 > dist_hor > self.min_sep_hor and dist_vert < self.min_sep_vert_high:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)
                    else:
                        # horizontal sep requirement is not met
                        if dist_hor < self.min_sep_hor and self.min_sep_vert_high + 1000 > dist_vert > self.min_sep_vert_low:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)
                        # vertical sep requirement is not met
                        if self.min_sep_hor + 10 > dist_hor > self.min_sep_hor and dist_vert < self.min_sep_vert_low:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)
        return len(list_of_potential_conflicts)

    def confcount(self):
        # ToDo rewrite
        pass

    # calculates the variance and mean of all altitudes in the sector
    def altvari(self):
        list_of_altitudes = []
        for plane in self.sector.get_planes():
            list_of_altitudes.append(plane.get_altitude())
        mean = sum(list_of_altitudes) / len(list_of_altitudes)
        variance = sum((x - mean) ** 2 for x in list_of_altitudes) - 1 / len(list_of_altitudes)
        return variance, mean

    def numbndy(self):
        threshold = 5
        count_of_planes = 0
        for plane in self.sector.get_planes():
            if self.sector.distance_to_border(plane) < threshold:
                count_of_planes += 1
        return count_of_planes

    def aspect(self):
        # ToDo rewrite
        pass

    # -------------------------------------------------------------
    # Helper functions
    # -------------------------------------------------------------

    def are_in_conflict(self, plane_1, plane_2):
        # ToDO which plane determines if below of above 29000 feet
        if plane_1.altitude > 29000:
            if self.dist_vertical(plane_1, plane_2) < self.min_sep_vert_high and \
                    self.dist_horizontal(plane_1, plane_2) < self.min_sep_hor:
                return True

        elif self.dist_vertical(plane_1, plane_2) < self.min_sep_vert_low and \
                self.dist_horizontal(plane_1, plane_2) < self.min_sep_hor:
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
        distance_2d = geodesic((plane1.position_x, plane1.position_y),
                               (plane2.position_x, plane2.position_y)).nautical
        return distance_2d
