from datetime import timedelta

from geopy import Point
from geopy.distance import geodesic
from shapely import LineString

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

    # number of potential crossings (irrespective of the aircraft direction on their trajectories)
    # with angle greater than 20 degrees.
    # Potential is defined as 5 minute Window
    # ToDO fix type error
    def inter_hori(self):
        timeframe = 5
        potential_crossings = 0

        def get_distance(speed_knts):
            speed_in_ms = speed_knts * 0.514444  # converts speed from knots to m/s
            distance = speed_in_ms * (timeframe * 60)  # 10 seconds
            return distance / 1000

        if len(self.sector.get_planes()) > 1:
            return 1

        for plane in self.sector.get_planes():
            for other_plane in self.sector.get_planes():
                if plane != other_plane and other_plane.get_altitude() - 200 < plane.get_altitude() < other_plane.get_altitude() + 200:

                    p_plane = Point(plane.get_position_x(), plane.get_position_y())
                    p_other_plane = Point(other_plane.get_position_x(), other_plane.get_position_y())

                    new_pos_plane = geodesic(kilometers=get_distance(plane.get_speed())).destination(
                        p_plane, plane.get_heading())
                    new_pos_other_plane = geodesic(
                        kilometers=get_distance(other_plane.get_speed())).destination(
                        p_other_plane, other_plane.get_heading())

                    if LineString([Point(p_plane), new_pos_plane]).intersects(
                            LineString(
                                [Point(p_other_plane), new_pos_other_plane])) and not other_plane.get_heading().subtract(
                        20) < plane.get_heading() < other_plane.get_heading().add(20):
                        print("Intersects")
                        potential_crossings += 1

        return potential_crossings

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
