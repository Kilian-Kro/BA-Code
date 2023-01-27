import string

from geopy.distance import geodesic

from base_classes.sector import Sector


class WJTHC:
    def __init__(self, sector):
        self.sector: Sector = sector
        self.min_sep_horizontal = 10  # nautical miles
        self.min_sep_vertical = 1000  # feet

    def sector_volume(self):
        return self.sector.sector_volume()

    def aircraft_count(self):
        return len(self.sector.get_planes())  # / max([len(planes) for time, planes in self.sector.history_planes])

    # The occupied volume was calculated as an ellipsoid with the following dimensions:
    # Height: 0,164579 nm (=1000 ft)
    # Circumference: 10 nm
    # This represents the "bubble" around the aircraft that is occupied by the aircraft, which must not be entered
    # by another aircraft, thus being occupied.
    def aircraft_density_one(self):
        occupied_volume_per_plane = 68.94  # nm^3
        return len(self.sector.get_planes()) * occupied_volume_per_plane / self.sector.sector_volume()

    def aircraft_density_two(self):
        return len(self.sector.get_planes()) / self.sector.sector_volume()
        # aircraft_density_one

    # go through all pairs of planes in the sector and calculate their convergence angles
    def convergence_recognition_index(self):
        def conv_ang(heading1, heading2):
            delta = abs(heading1 - heading2)
            angle = min(delta, 360 - delta)
            return angle

        cri = 0
        conv_angle = 0.
        for plane in self.sector.get_planes():
            for other_plane in self.sector.get_planes():
                if plane != other_plane:
                    conv_angle = conv_ang(plane.get_heading(), other_plane.get_heading())
                    cri = cri + (7 - (conv_angle / 30)) ** 2
        return cri

    def separation_criticality_index(self):
        sci = 0
        for plane in self.sector.get_planes():
            for other_plane in self.sector.get_planes():
                if plane != other_plane:
                    dist_hor = self.dist_horizontal(plane, other_plane)
                    dist_vert = self.dist_vertical(plane, other_plane)
                    sih = dist_hor / self.min_sep_horizontal
                    siv = dist_vert / self.min_sep_vertical
                    si = (sih + siv) / 2
                    sci = sci + (3 - si) ** 2

        return sci

    def degrees_of_freedom_index(self):
        # ToDO: define DOF, especially the vertical component is unclear
        dofi = 0
        potential_conf_buffer_vert = 1000  # feet
        potential_conf_buffer_hori = 3  # nautical miles
        for plane in self.sector.get_planes():
            for other_plane in self.sector.get_planes():
                if plane != other_plane:
                    dist_hor = self.dist_horizontal(plane, other_plane)
                    dist_vert = self.dist_vertical(plane, other_plane)
                    if dist_hor < self.min_sep_horizontal + potential_conf_buffer_hori or \
                            dist_vert < self.min_sep_vertical + potential_conf_buffer_vert:
                        dofi = dofi + 1
        #  ToDo find all planes that limit DOF
        pass

    # idea: distance to sector boundary (is heading here important?) time to reach the points in question is easy, since
    # speed and distance are known
    def coordination_taskload_index(self):
        ccp = 2.5  # miles to sector border before hand-off has to be completed

        cti = 0
        cti2 = 0
        for plane in self.sector.get_planes():
            dist_to_border = self.sector.distance_to_border(plane)
            # 1 knot == 0,000277778 nm/s
            speed = plane.get_speed() * 0.000277778

            time_to_border = dist_to_border / speed
            time_to_ccp = (dist_to_border - ccp) / speed

            if time_to_ccp <= 600:  # 10 minutes in seconds
                # Calculation Option 1
                cti = cti + (1 / time_to_ccp + (time_to_border - time_to_ccp) ** 2)

                # Calculation Option 2
                cti2 = cti2 + (10 - time_to_border) ** 2

        return cti

    @staticmethod
    def dist_horizontal(plane1, plane2):
        distance_2d = geodesic((plane1.position_x, plane1.position_y), (plane2.position_x, plane2.position_y)).nautical
        return distance_2d

    @staticmethod
    def dist_vertical(plane1, plane2):
        alt1 = plane1.altitude
        alt2 = plane2.altitude
        return max(alt1, alt2) - min(alt1, alt2)
