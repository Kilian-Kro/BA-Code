from datetime import timedelta

from geopy.distance import geodesic


class WorkloadTwo:
    def __init__(self, sector):
        self.sector = sector

    def wl_mon(self):
        maximum_flight_time = 60  # convert to minutes
        wl_mon = 4.18 * len(self.sector.get_planes()) * maximum_flight_time
        return round(wl_mon, 2)

    def wl_cdr(self):
        # Weighting factor * conflict resolution time * number of conflicts
        cdr1 = 3.61 * 127.76  # conflicts between aircraft on the same track and level
        cdr2 = 4.20 * 145.84  # conflicts between aircraft on crossing tracks at the same level
        cdr3 = 3.88 * 123.90  # conflicts between climbing or descending aircraft on the same track
        cdr4 = 4.39 * 132.18  # conflicts between climbing or descending aircraft on crossing tracks
        cdr5 = 4.64 * 188.59  # conflicts between climbing or descending aircraft on reciprocal tracks

        for plane in self.sector.get_planes():
            for other_plane in self.sector.get_planes():
                if plane != other_plane and self.are_in_conflict(plane, other_plane):
                    if plane.get_altitude() - 100 < other_plane.get_altitude() < plane.get_altitude() + 100:
                        if plane.get_heading() - 35 < other_plane.get_heading() < plane.get_heading() + 35:
                            cdr1 += 1
                        else:
                            cdr2 += 1
                    else:
                        if plane.get_heading() - 35 < other_plane.get_heading() < plane.get_heading() + 35:
                            cdr3 += 1
                        elif plane.get_heading() + 35 < other_plane.get_heading() < 135 or plane.get_heading() - 35 > other_plane.get_heading() > plane.get_heading() - 135:
                            cdr4 += 1
                        else:
                            cdr5 += 1

        wl_cdr = 4.69 * (cdr1 + cdr2 + cdr3 + cdr4 + cdr5)
        return round(wl_cdr, 2)

    def wl_cor(self):
        cor1 = 3.81 * 25.00  # Same ACC
        cor2 = 3.93 * 28.55  # Different ACC
        cor3 = 4.60 * 56.38  # Military units
        cor4 = 4.14 * 41.18  # Adjacent ACC

        # NOT IMPLEMENTED
        # Not viable in this Thesis, since it would require multiple sectors
        # And military aircraft, both are not in scope

        wl_cdr = 4.61 * (cor1 + cor2 + cor3 + cor4)
        return round(wl_cdr, 2)

    def wl_acm(self):
        # Weighting factor * clearance time * number of aircraft
        acm1 = 4.49 * 23.99  # flight level change
        acm2 = 3.53 * 19.07  # speed change
        acm3 = 4.17 * 23.31  # heading change
        # NOT IMPLEMENTED, as there is no way to measure this in the current setup
        acm4 = 3.43 * 16.29  # route originally filed in the flight plan, is changed by the aircraft or the controller

        count_acm1 = 0
        count_acm2 = 0
        count_acm3 = 0

        # No timedelta for "change" was specified, but as it is impossible to look into the future, changes are measured
        # form now compared to two minutes ago.
        time_p = self.sector.get_passed_time() - timedelta(minutes=2)
        # Save the list of planes from 2 minutes ago
        past_planes = []
        for time, planes in self.sector.get_history_planes():
            if time == time_p:
                past_planes = planes

        # if the parameter X of a plane is not the same as the parameter X of the same plane 2 minutes ago, add 1 to the
        # counter for that parameter
        for plane in self.sector.get_planes():
            for plane2 in past_planes:
                if plane == plane2:
                    # Buffer of 200 feet +/- to account for incorrect altitude readings
                    if not plane.get_altitude() - 200 < plane2.get_altitude() < plane.get_altitude() + 200:
                        count_acm1 += 1
                    # Buffer of 10 knots +/- to account for incorrect speed readings
                    if not plane.get_speed() - 10 < plane2.get_speed() < plane.get_speed() + 10:
                        count_acm2 += 1
                    # Buffer of 5 degrees +/- to account for incorrect heading readings
                    if not plane.get_heading() - 5 < plane2.get_heading() < plane.get_heading() + 5:
                        count_acm3 += 1

        wl_acm = 4.29 * (acm1 * count_acm1 + acm2 * count_acm2 + acm3 * count_acm3)
        return round(wl_acm, 2)

    def workload(self):
        return self.wl_mon() + self.wl_cdr() + self.wl_acm()  # + self.wl_cor()

    def __str__(self):
        return "Workload: " + str(self.workload()) + "in Sector" + self.sector.name

    # Checks if aircraft are in conflict
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
    def dist_vertical(plane1, plane2):
        alt1 = plane1.altitude
        alt2 = plane2.altitude
        return max(alt1, alt2) - min(alt1, alt2)

    @staticmethod
    def dist_horizontal(plane1, plane2):
        distance_2d = geodesic((plane1.position_x, plane1.position_y), (plane2.position_x, plane2.position_y)).nautical
        return distance_2d
