import statistics

from geopy import Point
from geopy.distance import geodesic

from base_classes.sector import Sector


class NasaAdditional:
    def __init__(self, sector):
        self.sector: Sector = sector
        self.time_threshold = 2  # in minutes
        self.min_sep_hor = 10  # in nautical miles
        self.min_sep_vert_low = 1000  # in feet below 29,000 feet
        self.min_sep_vert_high = 2000  # in feet above 29,000 feet

    # Look ahead 5 minutes and count the number of potential conflicts
    def numhorizon(self):
        timeframe = 5  # in minutes

        def get_distance(speed_knts):
            speed_in_ms = speed_knts * 0.514444  # converts speed from knots to m/s
            distance = speed_in_ms * (timeframe * 60)  # convert to seconds
            return distance / 1000  # convert to km

        predicted_conflicts = 0
        for plane in self.sector.get_planes():
            for other_plane in self.sector.get_planes():
                # Check if planes are in the same altitude range
                if plane != other_plane and other_plane.get_altitude() - 200 < plane.get_altitude() < other_plane.get_altitude() + 200:
                    p_plane = Point(plane.get_position_x(), plane.get_position_y())
                    p_other_plane = Point(other_plane.get_position_x(), other_plane.get_position_y())

                    # Calculate the new position of the plane after timeframe
                    new_pos_plane = geodesic(kilometers=get_distance(plane.get_speed())).destination(
                        p_plane, plane.get_heading())
                    new_pos_other_plane = geodesic(
                        kilometers=get_distance(other_plane.get_speed())).destination(
                        p_other_plane, other_plane.get_heading())

                    if geodesic(new_pos_plane, new_pos_other_plane).nautical < self.min_sep_hor:
                        predicted_conflicts += 1

        return predicted_conflicts / 2

    # Calculate the Variance of all aircraft headings in the sector
    def hdgvari(self):
        list_of_headings = []
        for plane in self.sector.get_planes():
            list_of_headings.append(plane.get_heading())
        mean = sum(list_of_headings) / len(list_of_headings)
        variance = statistics.variance(list_of_headings, mean)
        return variance

    # Squared difference between heading of each aircraft in a sector and direction of major axis
    # "Major Axis" not specified in the source, here defined as the median of the headings
    def axishdg(self):
        list_of_headings = []
        for plane in self.sector.get_planes():
            list_of_headings.append(plane.get_heading())
        median = sorted(list_of_headings)[len(list_of_headings) // 2]

        squared_difference = 0
        for heading in list_of_headings:
            squared_difference += (median - heading) ** 2
        return squared_difference

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

    # Number of aircraft in close proximity to conflict situations
    # Depending on the interpretation this is either the same as Metron.wconflict_nbrs()
    # Or it counts aircraft that are close to being in conflict themselves
    # As the same paper would likely not use the same definition for both, I chose the latter
    def proxcount(self):
        list_of_potential_conflicts = []
        dist_hor = 0.
        dist_vert = 0.
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    # Get the distance between the two planes
                    dist_hor = self.dist_horizontal(plane, plane2)
                    dist_vert = self.dist_vertical(plane, plane2)

                    # Different vertical separation requirements depending on altitude
                    if plane.get_altitude() > 29000:
                        # horizontal sep requirement is not met but vertical is met
                        if dist_hor < self.min_sep_hor and self.min_sep_vert_high + 2000 > dist_vert > self.min_sep_vert_high:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)
                        # vertical sep requirement is not met, but horizontal is met
                        if self.min_sep_hor + 10 > dist_hor > self.min_sep_hor and dist_vert < self.min_sep_vert_high:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)
                    # Essentially the same as above, but with different vertical separation requirements
                    else:
                        # horizontal sep requirement is not met, but vertical is met
                        if dist_hor < self.min_sep_hor and self.min_sep_vert_high + 1000 > dist_vert > self.min_sep_vert_low:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)
                        # vertical sep requirement is not met, but horizontal is met
                        if self.min_sep_hor + 10 > dist_hor > self.min_sep_hor and dist_vert < self.min_sep_vert_low:
                            self.add_to_list_no_duplicates(list_of_potential_conflicts, plane, plane2)

        # since the list should not contain duplicates a division by 2 not necessary
        return len(list_of_potential_conflicts)

    # Redundant metric, same as Metron.wconf_bound()
    def confcount(self):
        # return Metron.wconf_bound()
        return 0

    # calculates the variance and mean of all altitudes in the sector
    def altvari(self):
        list_of_altitudes = []
        for plane in self.sector.get_planes():
            list_of_altitudes.append(plane.get_altitude())
        mean = sum(list_of_altitudes) / len(list_of_altitudes)
        variance = statistics.variance(list_of_altitudes, mean)
        return variance + mean

    # Number of aircraft within a threshold distance of the sector boundary
    def numbndy(self):
        threshold = 5
        count_of_planes = 0
        for plane in self.sector.get_planes():
            if self.sector.distance_to_border(plane) < threshold:
                count_of_planes += 1
        return count_of_planes

    # Major axis length divided by minor axis length of a sector
    def aspect(self):
        # Set min to 0 so that the first distance is always larger than the min
        # Set max to inf so that the first distance is always smaller than the max
        max_aspect = 0.
        min_aspect = float('inf')
        # Measure the distance between all corner points and choose the longest and shortest distance
        for point1 in self.sector.get_corner_points():
            for point2 in self.sector.get_corner_points():
                if point1 != point2:
                    distance = geodesic(point1, point2).nautical
                    if distance > max_aspect:
                        max_aspect = distance
                    if distance < min_aspect:
                        min_aspect = distance

        return max_aspect / min_aspect

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
