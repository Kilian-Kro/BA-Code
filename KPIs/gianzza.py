from datetime import timedelta

from geopy import Point
from geopy.distance import geodesic
from shapely import LineString

from base_classes.Heading import Heading
from base_classes.sector import Sector


class Gianazza:
    def __init__(self, sector):
        self.sector: Sector = sector

    # V is the sector volume
    def v(self):
        return self.sector.sector_volume()

    # Nb is the number of aircraft in the sector
    def nb(self):
        return len(self.sector.get_planes())

    # Avg_vs  is simply the average vertical speed of controlled aircraft
    # All vetical speeds are summarized and then divided by total number of aircraft
    def avg_vs(self):
        vertical_count = 0
        for plane in self.sector.get_planes():
            vertical_count += abs(plane.get_climbrate())

        # Avoid division by zero for an empty sector
        if len(self.sector.get_planes()) == 0:
            return 0
        return vertical_count / len(self.sector.get_planes())

    # f15 is the incoming flows with time horizons of 15 minutes, no further information in paper so own interpretation
    def f15(self, point_in_time):
        return self.get_flows(point_in_time, 15)

    # f60 is the incoming flows with time horizons of 60 minutes, no further information in paper so own interpretation
    def f60(self, point_in_time):
        return self.get_flows(point_in_time, 60)

    # number of potential crossings with angle greater than 20 degrees.
    # Potential is defined as crossing that would take place within a 5-minute Window
    def inter_hori(self):
        timeframe = 5  # in minutes
        potential_crossings = 0

        # Helper function to calculate the distance a plane will travel in timeframe
        def get_distance(speed_knts):
            speed_in_ms = speed_knts * 0.514444  # converts speed from knots to m/s
            distance = speed_in_ms * (timeframe * 60)  # convert to seconds
            return distance / 1000  # convert to km

        # Avoid division by zero for an empty sector
        if len(self.sector.get_planes()) < 1:
            return 1

        # Iterate over all planes in the sector and check for potential crossings
        for plane in self.sector.get_planes():
            potential_crossings = 0
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

                    # Check if the planes will cross paths in timeframe and if the angle between the planes is greater than 20 degrees
                    # By checking if lines from their current position to their new position intersect
                    if LineString([(p_plane.longitude, p_plane.latitude),
                                   (new_pos_plane.longitude, new_pos_plane.latitude)]).intersects(
                        LineString([(p_other_plane.longitude, p_other_plane.latitude), (
                                new_pos_other_plane.longitude,
                                new_pos_other_plane.latitude)])) and not Heading.stat_sub(other_plane.get_heading(),
                                                                                          20) < plane.get_heading() < Heading.stat_add(
                        other_plane.get_heading(), 20):
                        potential_crossings += 1

        # Divide by two because each crossing is counted twice, since double for loop
        # a crossing between plane A and plane B and between plane B and plane A is the same, but counted twice
        return potential_crossings / 2

    # All other planes that appeared in the sector in the following time window are incoming flows
    # But if a plane is currently in the sector, it cannot be an incoming flow
    def get_flows(self, point_in_time, time_window):
        d_time = timedelta(seconds=point_in_time)
        current_planes = [plane for time, plane in self.sector.history_planes if d_time == time]
        unique_planes = set()
        # Get all unique planes that were in the sector at some point during the time window
        for time, planes in self.sector.history_planes:
            if d_time <= time <= d_time + timedelta(seconds=time_window * 6):
                unique_planes.update(planes)

        # Remove all planes that already were in the sector
        for planes in unique_planes:
            if planes in current_planes:
                unique_planes.remove(planes)

        return len(unique_planes)
