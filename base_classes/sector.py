import random as rnd
import string
from datetime import timedelta
from math import sqrt

import geopy
import numpy as np
from geopy.distance import geodesic
from geopy.units import nm
from numpy import random
from shapely.geometry import Polygon, Point

from base_classes.airplane import Airplane


# Represents a sector in the airspace
class Sector:
    def __init__(self, name, floor, ceiling, corner_points):
        self.name: string = name
        # unit for floor and ceiling is feet
        self.floor: int = floor
        self.ceiling: int = ceiling
        # Should be a list of Tuples (lat, lon), i.e [(0., 1.), (2., 3.)]
        self.corner_points = corner_points
        self.current_planes = []
        # This is the most inefficient part of the code
        # The history is stored as a tuple of (time, planes), time being the current timedelta()
        # and planes being a list of planes, this leads to a lot of redundant stored information
        self.history_planes = []
        self.passed_time = timedelta()

        # Calculate the sector center, currently no further function in the code
        coords = {i: (lat, lon) for i, (lat, lon) in enumerate(self.corner_points)}
        obj = Polygon([coords[i][1], coords[i][0]] for i in range(len(coords)))
        self.sector_center = obj.centroid

        # Additional feature, if needed, currently not used
        self.total_number_of_neighbors = 0
        self.neighbor_sector_names = []

    # ToDO calculates area wrong
    def sector_area(self):
        """Compute the area of the sector based on the corner points.

               Returns:
                   float: the area of the sector in nautical miles squared
               """
        # Attempt No2
        # Create a Polygon object
        # poly = Polygon(self.corner_points)
        # area = poly.area
        # print(area)

        poly_coords = [(x2, y2, z2) for x2, y2, z2 in map(self.get_cartesian, [lat for lat, lon in self.corner_points],
                                                          [lon for lat, lon in self.corner_points])]
        poly2 = Polygon(poly_coords)
        area2 = poly2.area

        # area_km2 = area / 10 ** 6
        # return area * 4457.336319511756  # geopy.units.nautical(meters=area)
        return area2

    # ToDO calculates area wrong
    def sector_volume(self):
        """Compute the volume of the sector based on the floor and ceiling.

        Returns:
            float: the volume of the sector in cubic meters
        """
        # Convert floor and ceiling from feet to meters
        floor_m = geopy.units.nautical(feet=self.floor)
        ceiling_m = geopy.units.nautical(feet=self.ceiling)

        # Compute the volume of the sector
        volume = self.sector_area() * (ceiling_m - floor_m)

        # Unit is now nautical miles cubed
        return volume

    # ToDO probably wrnng as well
    def distance_to_border(self, plane):
        """Compute the distance of a plane from the closest sector border.

        Args:
            plane (Airplane): the plane to compute the distance for

        Returns:
            float: the distance from the plane to the closest sector border in nautical miles
        """

        distance_to_ceiling = (self.ceiling - plane.get_altitude())
        distance_to_floor = (plane.get_altitude() - self.floor)

        cords = self.get_cartesian(plane.get_position_x(), plane.get_position_y())

        poly_coords = [(x, y, z) for x, y, z in map(self.get_cartesian, [lat for lat, lon in self.corner_points],
                                                    [lon for lat, lon in self.corner_points])]
        poly = Polygon(poly_coords)
        # Shapely function, calculates the closest distance to the next border, only 2D
        distance_to_border = poly.exterior.distance(Point(cords))

        geopy.units.nautical(feet=distance_to_ceiling)
        geopy.units.nautical(feet=distance_to_floor)
        geopy.units.nautical(meters=distance_to_border)

        # the distance to the border is the minimum of the distance to the ceiling, floor and border
        return min(distance_to_ceiling, distance_to_floor, distance_to_border)

    # ToDo probably wrong as well
    def is_pos_in_sector(self, x, y):
        poly_coords = [(x2, y2, z2) for x2, y2, z2 in map(self.get_cartesian, [lat for lat, lon in self.corner_points],
                                                          [lon for lat, lon in self.corner_points])]
        poly = Polygon(poly_coords)
        return poly.contains(Point(self.get_cartesian(x, y)))

    # Convert decimal degree coordinates to cartesian coordinates
    @staticmethod
    def get_cartesian(lat, lon):
        lat, lon = np.deg2rad(lat), np.deg2rad(lon)
        r = 6371  # radius of the earth
        x = r * np.cos(lat) * np.cos(lon)
        y = r * np.cos(lat) * np.sin(lon)
        z = r * np.sin(lat)
        return x, y, z

    # @staticmethod
    # def get_cartesian(lat, lon):
    #     return lat, lon

    @staticmethod
    def distance_between_two_planes(plane1, plane2):
        """Compute the distance between two planes using GeoPy package
        This is not the correct way to compute the distance accurately since this approach does not
        take into account the curvature of the earth.
        Over a distance of 100 km, the error is about 750m

        Args:
            plane1 (Airplane): the first plane
            plane2 (Airplane): the second plane

        Returns:
            float: the distance between the two planes in nautical miles
        """
        alt1 = geopy.units.meters(feet=plane1.altitude)  # Convert from feet to meters
        alt2 = geopy.units.meters(feet=plane2.altitude)  # Convert from feet to meters

        # Calculate the distance between the two planes in 2D
        distance_2d = geodesic((plane1.position_x, plane1.position_y), (plane2.position_x, plane2.position_y)).meters

        # Calculate the distance between the two planes in 3D, using Pythagoras
        if alt1 > alt2:
            distance_3d = sqrt(distance_2d ** 2 + (alt1 - alt2) ** 2)
        else:
            distance_3d = sqrt(distance_2d ** 2 + (alt2 - alt1) ** 2)

        # Convert distance from kilometers to nautical miles
        return geopy.units.nautical(meters=distance_3d)

    def get_planes(self):
        return self.current_planes

    def get_passed_time(self):
        return self.passed_time

    def get_history_planes(self):
        return self.history_planes

    def get_name(self):
        return self.name

    def get_corner_points(self):
        return self.corner_points

    def get_sector_center(self):
        return self.sector_center

    def set_current_planes(self, planes):
        self.current_planes = planes

    def set_neighbor_sector_names(self, neighbor_sector_names):
        self.neighbor_sector_names = neighbor_sector_names
        total_number_of_neighbors = len(neighbor_sector_names)

    def update_current_planes(self, planes, time):
        self.history_planes.append((self.passed_time, self.current_planes))
        self.current_planes = planes
        self.passed_time += timedelta(seconds=time)

    def create_traffic_loop(self, number_of_planes, variance):
        variance = 0
        time = 10
        self.update_current_planes(self.current_planes, time)

        def get_random_callsign():
            # generate a random string consisting of 3 letters and 3 digits in that order
            letters = string.ascii_uppercase
            digit = string.digits
            result_str = ''.join(rnd.choice(letters) for i in range(3))
            result_str += ''.join(rnd.choice(digit) for i in range(3))
            return result_str

        def add_plane():
            # select a random corner point of the sector
            # random_corner = random.uniform(0, len(self.corner_points) - 1)
            pos_x = self.corner_points[0][0] + random.uniform(0, 1) * (
                    self.corner_points[2][0] - self.corner_points[0][0])
            pos_y = self.corner_points[0][1] + random.uniform(0, 1) * (
                    self.corner_points[2][1] - self.corner_points[0][1])
            # position = rnd.choice(self.corner_points)
            position = (pos_x, pos_y)
            name = get_random_callsign()
            altitude = random.uniform(self.floor, self.ceiling)
            speed1 = random.uniform(300, 700)
            if np.random.random() < 0.3:
                climbrate = random.uniform(-3000, 3000)
            else:
                climbrate = 0
            heading1 = int(random.uniform(0, 360))
            return Airplane(name, heading1, altitude, speed1, climbrate, position[0], position[1])

        def get_distance(speed_knts):
            speed_in_ms = speed_knts * 0.514444  # converts speed from knots to m/s
            distance = speed_in_ms * 10  # 10 seconds
            return distance / 1000

        for plane in self.current_planes:
            # Update the position of the plane
            current_pos = (plane.get_position_x(), plane.get_position_y())
            heading = plane.get_heading()
            speed = plane.get_speed()
            new_pos = geodesic(kilometers=get_distance(speed)).destination(current_pos, heading)

            if not self.is_pos_in_sector(new_pos[0], new_pos[1]):
                # If the plane is outside the sector, it is removed from the sector
                self.current_planes.remove(plane)
                continue

            # print("OLD X: " + str(plane.get_position_x()) + " Y: " + str(plane.get_position_y()))
            plane.update_position(new_pos.latitude, new_pos.longitude)
            # print("NEW X: " + str(plane.get_position_x()) + " Y: " + str(plane.get_position_y()))

            # Randomly update heading, climb rate, and speed
            if np.random.random() < 0.2:
                plane.update_heading(plane.get_heading() + np.random.randint(-5, 6))
            if np.random.random() < 0.1:
                plane.update_climbrate(np.random.randint(100, 500))
            if np.random.random() < 0.1:
                plane.update_speed(plane.get_speed() + np.random.randint(-20, 21))

        # Depending on the number of planes in the sector, the probability of a new plane entering the sector is
        # increased if the number gets lower (100% at number_of_planes - variance)
        # and decreases (0% at number_of_planes + variance)
        # Add the possibility that more than one or no plane enters the sector

        if len(self.current_planes) < number_of_planes - variance:
            while len(self.current_planes) < number_of_planes - variance:
                self.current_planes.append(add_plane())

        # if number_of_planes - variance <= len(self.current_planes) <= number_of_planes + variance:
        #     probability = len(self.current_planes) / (number_of_planes + variance)
        #     if np.random.random() > probability:
        #         self.current_planes.append(add_plane())

        current_num_planes = len(self.current_planes)
        if current_num_planes == number_of_planes - variance:
            prob = 0.9
        elif current_num_planes == number_of_planes + variance:
            prob = 0
        else:
            prob = (number_of_planes - abs(current_num_planes - number_of_planes)) / number_of_planes

        if np.random.random() < prob:
            self.current_planes.append(add_plane())


def __str__(self):
    current_planes_str = '\n'.join([str(plane) for plane in self.current_planes])
    history_planes_str = '\n'.join([f"Time: {time}, Planes: {[str(plane) for plane in planes]}"
                                    for time, planes in self.history_planes])
    return f"Name: {self.name}, Floor: {self.floor}, Ceiling: {self.ceiling}, " \
           f"Corner Points: {self.corner_points}\nCurrent Planes:\n{current_planes_str}\nHistory " \
           f"Planes:\n{history_planes_str}"
