import math
import statistics

import geopy.units
from geopy.distance import geodesic

from base_classes.sector import Sector


# Everything is based on this paper: https://arc.aiaa.org/doi/pdf/10.2514/6.2001-5242
# Looking through the Code a lot of potential for increasing performance is there
# Everything could be summarized in one function, but this is more readable this way
class NasaOne:
    def __init__(self, sector):
        self.sector: Sector = sector

    # The number of aircraft divided by the maximum number of aircraft
    def c_1(self):
        n = len(self.sector.get_planes())
        # n_max is the historical, or the acceptable, maximum number of aircraft in the sector
        # Currently no good way to determine this, so it is set to 100
        n_max = 100
        return n / n_max

    # Ratio of climbing aircraft to total number of aircraft in the sector
    def c_2(self):
        n = len(self.sector.get_planes())
        n_cl = 0
        for plane in self.sector.get_planes():
            # Allows for some tolerance, as the climb rate is not always exact
            if plane.get_climbrate() > 200:
                n_cl += 1
        return n_cl / n

    # Ratio of level aircraft to total number of aircraft in the sector
    def c_3(self):
        n = len(self.sector.get_planes())
        n_lv = 0
        for plane in self.sector.get_planes():
            if 200 > plane.get_climbrate() > -200:
                n_lv += 1
        return n_lv / n

    # Ratio of descending aircraft to total number of aircraft in the sector
    def c_4(self):
        n = len(self.sector.get_planes())
        n_ds = 0
        for plane in self.sector.get_planes():
            if plane.get_climbrate() < -200:
                n_ds += 1
        return n_ds / n

    # the mean weighted horizontal separation distance
    def c_5(self):
        n = len(self.sector.get_planes())
        # Scaling factor given in the paper
        s_h = 5 / 2000
        helper = 0.
        d_ij = 0.  # Horizontal distance between two planes
        h_ij = 0.  # Vertical distance between two planes
        w_ij = 0.  # Associated weighting factor
        w_ij_d_ij = 0.  # w_ij * d_ij
        for i in self.sector.get_planes():
            for j in self.sector.get_planes():
                if i != j:
                    d_ij = self.dist_horizontal(i, j)
                    h_ij = self.dist_vertical(i, j)
                    w_ij = w_ij + d_ij ** 2 + s_h ** 2 * h_ij ** 2  # Equation 6 in paper
                    w_ij_d_ij = w_ij * d_ij
                    helper = helper + (w_ij_d_ij / w_ij)  # Equation 5 in paper
                    w_ij = 0.  # Reset w_ij for next iteration
        if helper == 0:
            return 0
        return n / helper

    # The mean weighted vertical separation distance
    def c_6(self):
        n = len(self.sector.get_planes())
        # Minimum horizontal separation divided by minimum vertical separation
        s_h = geopy.units.nautical(5) / geopy.units.nautical(feet=2000)
        helper = 0.
        d_ij = 0.  # Horizontal distance between two planes
        h_ij = 0.  # Vertical distance between two planes
        w_ij = 0.  # Associated weighting factor
        w_ij_h_ij = 0.
        for i in self.sector.get_planes():
            for j in self.sector.get_planes():
                if i != j:
                    d_ij = self.dist_horizontal(i, j)
                    h_ij = self.dist_vertical(i, j)
                    w_ij = w_ij + d_ij ** 2 + s_h ** 2 * h_ij ** 2  # Equation 6 in paper
                    w_ij_h_ij = w_ij * h_ij
                    helper = helper + (w_ij_h_ij / w_ij)  # Equation 12 in paper
                    w_ij = 0.  # Reset w_ij for next iteration
        if helper == 0:
            return 0
        return n / helper

    # Minimum horizontal distance between two planes
    def c_7(self):
        delta_h = 300  # Unit: ft | An exact value is not specified in the paper
        counter = 0
        min_d = 0.
        c_7 = 0.
        # Find the closest plane to each plane within the same altitude band
        for i in self.sector.get_planes():
            counter = 0
            min_d = float('inf')
            for j in self.sector.get_planes():
                # Equation 13 in paper
                if i != j and i.get_altitude() - (delta_h / 2) < j.get_altitude() < i.get_altitude() + (delta_h / 2):
                    counter += 1
                    if self.dist_horizontal(i, j) < min_d:
                        min_d = self.dist_horizontal(i, j)
            if counter > 0:
                c_7 = c_7 + (counter / min_d)
            counter = 0
            min_d = float('inf')
        return c_7 / 2  # The value is halved, because the calculation is done twice for each plane (can be optimized)

    # Minimum vertical distance between two planes
    def c_8(self):
        r = 5  # Unit: nm | An exact value is not specified in the paper
        counter = 0
        min_h = 0.
        c_8 = 0.
        # Find the closest (vertical distance) plane for each plane within a radius of 5 nm
        for i in self.sector.get_planes():
            counter = 0
            min_h = float('inf')
            for j in self.sector.get_planes():
                # Equation 16 and 17 in the paper
                if i != j and self.dist_vertical(i, j) < r:
                    counter += 1
                    if abs(i.get_altitude() - j.get_altitude()) < min_h:
                        min_h = abs(i.get_altitude() - j.get_altitude())

            if min_h == 0:
                min_h = 1.  # Avoid division by zero
            if counter > 0:
                c_8 = c_8 + (counter / min_h)
            counter = 0
            min_h = float('inf')
        return c_8 / 2  # The value is halved, because the calculation is done twice for each plane (can be optimized)

    # Closest Horizontal distance between two planes, Equation 18 in paper
    def c_9(self):
        min_d = float('inf')
        for i in self.sector.get_planes():
            for j in self.sector.get_planes():
                if i != j and self.dist_horizontal(i, j) < min_d:
                    min_d = self.dist_horizontal(i, j)
        return 1 / min_d

    # Closest Vertical separation distance between two planes, Equation 19 in paper
    def c_10(self):
        min_h = float('inf')
        for i in self.sector.get_planes():
            for j in self.sector.get_planes():
                if i != j and abs(i.get_altitude() - j.get_altitude()) < min_h:
                    min_h = abs(i.get_altitude() - j.get_altitude())

        if min_h == 0:
            return 0
        return 1 / min_h

    # C11-C13 are not implemented here, as they were deemed to complex to implement in a reasonable amount of time
    def c_11(self):
        return 0

    def c_12(self):
        return 0

    def c_13(self):
        return 0

    # The variance of the speed of all planes in the sector, Equation 29 in paper
    def c_14(self):
        n = len(self.sector.get_planes())
        s = 0.
        list_of_speeds = []
        for plane in self.sector.get_planes():
            s += plane.get_speed()
            list_of_speeds.append(plane.get_speed())
        s = s / n
        # s is now the mean speed of all planes in the sector
        var = 0.
        # calculate variance
        var = statistics.variance(list_of_speeds, s)
        return var

    # The standard deviation of the speed of all planes in the sector divided by the mean speed, Equation 30 in paper
    def c_15(self):
        n = len(self.sector.get_planes())
        s = 0.
        list_of_speeds = []
        for plane in self.sector.get_planes():
            s += plane.get_speed()
            list_of_speeds.append(plane.get_speed())
        s = s / n
        # s is now the mean speed of all planes in the sector
        stdev = 0.
        # calculate standard deviation
        statistics.stdev(list_of_speeds)
        return stdev / s

    # Conflict resolution difficulty, Equation 32 in paper
    def c_16(self):
        delta_t = 3.  # An exact value is not specified in the paper

        def resolution_difficulty(alpha):
            # Normalized time of resolution initiation as a function of crossing angle
            # Assumes a maneuver that achieves the quickest resolution
            normalized_time = 0.0
            if alpha < 19:
                normalized_time = (10 / (math.pi / 180)) * alpha
            else:
                normalized_time = (53.47 / 19) * alpha - (53.47 / 19) * 19
            return normalized_time

        complexity = 0
        for i in range(len(self.sector.get_planes())):
            for j in range(i + 1, len(self.sector.get_planes())):
                # Heading angle for aircraft i and j
                xi = math.radians(self.sector.get_planes()[i].get_heading())
                xj = math.radians(self.sector.get_planes()[j].get_heading())

                # relative heading angle
                xij = xi - xj

                # time-to-go
                tij = abs(xij)

                # Checking if relative time to go is less than At threshold
                if tij < delta_t:
                    # converging a pair of aircraft
                    # calculating crossing angle
                    tau = min(abs(xij), 2 * math.pi - abs(xij))
                    complexity += resolution_difficulty(tau)

        return complexity

    @staticmethod
    def dist_horizontal(plane1, plane2):
        distance_2d = geodesic((plane1.position_x, plane1.position_y), (plane2.position_x, plane2.position_y)).nautical
        return distance_2d

    @staticmethod
    def dist_vertical(plane1, plane2):
        alt1 = plane1.altitude
        alt2 = plane2.altitude
        return max(alt1, alt2) - min(alt1, alt2)
