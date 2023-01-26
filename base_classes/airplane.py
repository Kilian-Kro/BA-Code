import string
from datetime import timedelta

from base_classes.Heading import Heading


# Represents an airplane in the simulation
class Airplane:
    def __init__(self, callsign, heading, altitude, groundspeed, climbrate, position_x, position_y):
        self.callsign: string = callsign
        # unit: degrees
        self.heading = Heading(heading)
        # unit: feet
        self.altitude = int(altitude)
        # unit: knots
        self.groundspeed = int(groundspeed)
        # unit: feet/minute
        self.climbrate = int(climbrate)
        # unit: decimal degree coordinates
        self.position_x = position_x
        self.position_y = position_y

        self.past_positions = []
        self.past_climbrates = []
        self.past_speeds = []
        self.past_altitudes = []
        self.past_headings = []

        self.sector_entered_at = timedelta()
        self.sector_left_at = timedelta()

    def get_callsign(self):
        return self.callsign

    def get_heading(self):
        return self.heading.get_heading()

    def get_altitude(self):
        return self.altitude

    def get_speed(self):
        return self.groundspeed

    def get_climbrate(self):
        return self.climbrate

    def get_position_x(self):
        return self.position_x

    def get_position_y(self):
        return self.position_y

    def sector_entered(self, time):
        self.sector_entered_at = time

    def sector_left(self, time):
        self.sector_left_at = time

    def update_position(self, position_x, position_y):
        self.position_x = position_x
        self.position_y = position_y
        self.past_positions.append((position_x, position_y))

    def update_altitude(self, altitude):
        self.altitude = int(altitude)
        self.past_altitudes.append(altitude)

    def update_speed(self, speed):
        self.groundspeed = int(speed)
        self.past_speeds.append(speed)

    def update_climbrate(self, climbrate):
        self.climbrate = int(climbrate)
        self.past_climbrates.append(climbrate)

    def update_heading(self, heading):
        self.heading.set_heading(heading)
        self.past_headings.append(heading)

    def get_heading_at(self, time):
        return self.past_headings[time]

    def get_altitude_at(self, time):
        return self.past_altitudes[time]

    def get_speed_at(self, time):
        return self.past_speeds[time]

    def get_climbrate_at(self, time):
        return self.past_climbrates[time]

    def get_position_at(self, time):
        return self.past_positions[time]

    def __str__(self):
        return f"Callsign: {self.callsign}, Heading: {self.heading}, Altitude: {self.altitude}, " \
               f"Groundspeed: {self.groundspeed}, Climbrate: {self.climbrate}, Position X: {self.position_x}, " \
               f"Position Y: {self.position_y}"
