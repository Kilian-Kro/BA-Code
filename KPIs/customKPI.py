from datetime import timedelta

from geopy.distance import geodesic

from base_classes.sector import Sector


class CustomKPI:
    def __init__(self, sector):
        self.sector: Sector = sector
        self.all_unique_planes = set()
        for time, planes in self.sector.history_planes:
            for plane in planes:
                self.all_unique_planes.add(plane)

    def distance_one_plane(self, plane_in_question):
        # Search in sector_history for the first and last time the plane is registered
        plane_time = []
        for time, planes in self.sector.history_planes:
            for plane in planes:
                if plane.get_callsign() == plane_in_question.get_callsign():
                    plane_time.append((time, plane))

        # Calculate the distance between the first and last time the plane is registered
        distance = geodesic((plane_time[0][1].get_position_x(), plane_time[0][1].get_position_y()),
                            (plane_time[-1][1].get_position_x(), plane_time[-1][1].get_position_y())).nm
        return distance

    def average_in_sector_distance(self):
        total_distance = 0.
        for plane in self.all_unique_planes:
            self.distance_one_plane(plane)
            total_distance += self.distance_one_plane(plane)

        return total_distance / len(self.all_unique_planes)

    def time_one_plane(self, plane_in_question):
        # Search in sector_history for the first and last time the plane is registered
        plane_time = []
        for time, planes in self.sector.history_planes:
            for plane in planes:
                if plane.get_callsign() == plane_in_question.get_callsign():
                    plane_time.append((time, plane))

        # Calculate the time between the first and last time the plane is registered
        time = plane_time[-1][0] - plane_time[0][0]
        return time

    def average_in_sector_flight_time(self):
        total_time = timedelta()
        for plane in self.all_unique_planes:
            self.time_one_plane(plane)
            total_time += self.time_one_plane(plane)

        return total_time.total_seconds() / len(self.all_unique_planes)

