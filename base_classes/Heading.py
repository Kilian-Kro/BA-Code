# Represents the Heading of an Airplane and is used in calculations
# This is done to simplify the code and avoids cases where the heading is greater than 360 or less than 0
class Heading:
    def __init__(self, heading):
        self.heading = int(heading) % 360

    # Subtracts the value from the heading and returns the new heading
    def subtract(self, value):
        value = value % 360
        if self.heading - value < 0:
            return 360 + self.heading - value
        else:
            return self.heading - value

    # Adds the value to the heading and returns the new heading
    def add(self, value):
        value = value % 360
        if self.heading + value > 360:
            return self.heading + value - 360
        else:
            return self.heading + value

    def get_heading(self):
        return self.heading

    def set_heading(self, heading):
        self.heading = int(heading) % 360

    # Returns the difference between the two headings
    @staticmethod
    def stat_sub(heading1, heading2):
        if heading1 - heading2 < 0:
            return 360 + heading1 - heading2
        else:
            return heading1 - heading2

    # Returns the sum of the two headings
    @staticmethod
    def stat_add(heading1, heading2):
        if heading1 + heading2 > 360:
            return heading1 + heading2 - 360
        else:
            return heading1 + heading2

    def __str__(self):
        return self.heading
