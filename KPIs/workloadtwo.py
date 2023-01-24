from geopy.distance import geodesic

from base_classes.Heading import Heading


class WorkloadTwo:
    def __init__(self, sector):
        self.sector = sector

    def wl_mon(self):
        maximum_flight_time = 60  # convert to minutes
        wl_mon = 4.18 * len(self.sector.get_planes()) * maximum_flight_time
        return round(wl_mon, 2)

    def wl_cdr(self):
        cdr1 = 3.61 * 127.76
        cdr2 = 4.20 * 145.84
        cdr3 = 3.88 * 123.90
        cdr4 = 4.39 * 132.18
        cdr5 = 4.64 * 188.59

        for plane in self.sector.get_planes():
            for other_plane in self.sector.get_planes():
                if plane != other_plane and self.are_in_conflict(plane, other_plane):
                    if plane.get_altitude() - 100 < other_plane.get_altitude() < plane.get_altitude() + 100:
                        if Heading.stat_sub(plane.get_heading(), 35) < other_plane.get_heading() < Heading.stat_add(
                                plane.get_heading(), 35):
                            cdr1 += 1
                        else:
                            cdr2 += 1
                    else:
                        if Heading.stat_sub(plane.get_heading(), 35) < other_plane.get_heading() < Heading.stat_add(
                                plane.get_heading(), 35):
                            cdr3 += 1
                        elif Heading.stat_add(plane.get_heading(), 35) < other_plane.get_heading() < Heading.stat_add(
                                plane.get_heading(), 135) or Heading.stat_sub(plane.get_heading(),
                                                                              35) < other_plane.get_heading() < Heading.stat_sub(
                            plane.get_heading(), 135):
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

        # Not viable in this Thesis, since it would require multiple sectors

        wl_cdr = 4.61 * (cor1 + cor2 + cor3 + cor4)
        return round(wl_cdr, 2)

    def wl_acm(self):
        acm1 = 4.49 * 23.99
        acm2 = 3.53 * 19.07
        acm3 = 4.17 * 23.31
        acm4 = 3.43 * 16.29

        # ToDo: rewrite using new History data structure

        wl_acm = 4.29 * (acm1 + acm2 + acm3 + acm4)
        return round(wl_acm, 2)

    def workload(self):
        return self.wl_mon() + self.wl_cdr() + self.wl_acm()  # + self.wl_cor()

    def __str__(self):
        return "Workload: " + str(self.workload()) + "in Sector" + self.sector.name

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
