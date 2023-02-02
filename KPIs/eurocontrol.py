import geopy
import numpy as np
from geopy.units import nm
from shapely import LineString
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import split

from base_classes.Heading import Heading


class Eurocontrol:
    def __init__(self, sector):
        self.sector = sector
        # ToDo Add subdivision of the sector into a grid

    def avg_time_in_cell(self):
        # Has to be claculated for each airspace to be analysed individually
        avg_time_in_cell = 1 / 20  # of an hour
        return avg_time_in_cell

    # Counts the number of planes cruising, climbing and descending
    def v_dif(self):
        asc_pl = 0
        desc_pl = 0
        cru_pl = 0
        for plane in self.sector.get_planes():
            if plane.get_climbrate() > 500:
                asc_pl += 1
            if plane.get_climbrate() < -500:
                desc_pl += 1
            if 500 > plane.get_climbrate() > -500:
                cru_pl += 1
        vert_inter = (asc_pl * (desc_pl + cru_pl)) + (desc_pl * (asc_pl + cru_pl)) + (cru_pl * (asc_pl + desc_pl))
        hours_vert = vert_inter * (self.avg_time_in_cell() ** 2)
        return hours_vert

    # Counts all interactions between planes whose headings differ by more than 20 degrees
    def h_dif(self):
        interactions = 0
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    # if plane.getHeading differs by more than 20 degrees from plane2.getHeading
                    if Heading.stat_sub(plane.get_heading(), plane2.get_heading()) > 20:
                        interactions += 1

        interactions = interactions / 2  # because each interaction is counted twice
        hours_heading = interactions * (self.avg_time_in_cell() ** 2)
        return hours_heading

    # Counts all interactions between planes whose speeds differ by more than 35 knots
    def s_dif(self):
        interactions = 0
        # If the speed of two planes differs by more than 35 knots, count an interaction
        for plane in self.sector.get_planes():
            for plane2 in self.sector.get_planes():
                if plane != plane2:
                    if plane.get_speed() - plane2.get_speed() > 35 or plane.get_speed() - plane2.get_speed() < -35:
                        interactions += 1

        interactions = interactions / 2  # because each interaction is counted twice
        hours_speed = interactions * (self.avg_time_in_cell() ** 2)
        return hours_speed

    def flight_hours(self):
        fh = self.v_dif() + self.h_dif() + self.s_dif()
        if fh == 0:
            return 1  # to avoid division by zero in later functions
        return fh

    def v_dif_total(self):
        return self.v_dif() / self.flight_hours()

    def h_dif_total(self):
        return self.h_dif() / self.flight_hours()

    def s_dif_total(self):
        return self.s_dif() / self.flight_hours()

    def adj_density(self):
        total_hours_of_interactions = 7
        return total_hours_of_interactions / self.flight_hours()

    def complexity_score(self):
        adj_den = self.adj_density()
        s_i = (self.v_dif_total() / adj_den) + (self.h_dif_total() / adj_den) + (self.s_dif_total() / adj_den)
        complexity_score = adj_den * s_i
        return round(complexity_score, 2)

    # An Algorithm to divide a rectangle into squares of equal area
    # Currently not used
    def get_squares_from_rect(self):
        """
        Divide a Rectangle (Shapely Polygon) into squares of equal area.

        `side_length` : required side of square

        """
        coords = {i: (lat, lon) for i, (lat, lon) in enumerate(self.sector.corner_points)}
        obj = Polygon([coords[i][1], coords[i][0]] for i in range(len(coords)))

        side_length = geopy.units.meters(nm(20))
        rect_coords = np.array(obj.boundary.coords.xy)
        y_list = rect_coords[1]
        x_list = rect_coords[0]
        y1 = min(y_list)
        y2 = max(y_list)
        x1 = min(x_list)
        x2 = max(x_list)
        width = x2 - x1
        height = y2 - y1

        xcells = int(np.round(width / side_length))
        ycells = int(np.round(height / side_length))

        yindices = np.linspace(y1, y2, ycells + 1)
        xindices = np.linspace(x1, x2, xcells + 1)
        horizontal_splitters = [
            LineString([(x, yindices[0]), (x, yindices[-1])]) for x in xindices
        ]
        vertical_splitters = [
            LineString([(xindices[0], y), (xindices[-1], y)]) for y in yindices
        ]
        result = obj
        for splitter in vertical_splitters:
            result = MultiPolygon(split(result, splitter))
        for splitter in horizontal_splitters:
            result = MultiPolygon(split(result, splitter))

        square_polygons = result.geoms

        return square_polygons

    # returns the score, name and sector
    def __str__(self):
        return f"Sector: {self.sector.name}, Complexity Score: {self.complexity_score()}"
