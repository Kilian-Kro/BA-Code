import unittest

from base_classes.airplane import Airplane
from base_classes.sector import Sector


class MyTestCase(unittest.TestCase):
    def test_distance_between_two_planes(self):
        # Create two airplanes
        plane1 = Airplane('ABC123', 0, 10000, 500, 0, 40.0, 40.0)
        plane2 = Airplane('DEF456', 0, 10000, 500, 0, 40.0, 80.0)
        plane3 = Airplane('GHI789', 0, 10000, 0, 0, 40.0, 40.0)
        plane4 = Airplane('JKL012', 0, 10000, 18228.3, 0, 40.0, 41.0)
        plane5 = Airplane('MNO345', 0, 0, 18228.3, 0, 40.0, 40.0)
        plane6 = Airplane('PQR678', 0, 30380, 18228.3, 0, 40.0, 40.0)

        # Compute the distance between the two planes
        sector = Sector('Test Sector', 0, 10000, [(40.0, -80.0), (41.0, -80.0), (41.0, -79.0)])
        distance = sector.distance_between_two_planes(plane1, plane2)
        distance2 = sector.distance_between_two_planes(plane3, plane4)
        distance3 = sector.distance_between_two_planes(plane5, plane6)

        # Assert that the distance is correct
        # due to rounding an error is expected, especially with such high numbers
        self.assertAlmostEqual(round(distance, 0), 1828.0, 2)
        # here again a bit of error is expected
        self.assertAlmostEqual(round(distance2, 0), 46.0, 2)
        self.assertAlmostEqual(distance3, 5, 2)

    def test_sector_area_with_three_corner_points(self):
        # Create a sector with three corner points
        sector = Sector('Test Sector', 0, 10000, [(40.0, -80.0), (41.0, -80.0), (41.0, -79.0)])
        area = sector.sector_area()

        # Assert that the area is correct
        self.assertAlmostEqual(area, 3029.9584, 2)  # expected area is 1235.97 nautical miles^2

    def test_sector_area_with_four_corner_points(self):
        # Create a sector with four corner points
        sector = Sector('Test Sector', 0, 10000, [(11.381, 47.994),
                                                  (11.376, 48.284),
                                                  (11.860, 48.288),
                                                  (11.861, 47.998)])
        area = sector.sector_area()

        # Assert that the area is correct
        self.assertAlmostEqual(area, 340.9853, 2)  # expected area is 1235.97 nautical miles^2

    def test_sector_volume(self):
        # Create a sector
        sector = Sector('Test Sector', 0, 10000, [(40.0, -80.0), (41.0, -80.0), (41.0, -79.0)])
        volume = sector.sector_volume()

        # Assert that the volume is correct
        self.assertAlmostEqual(volume, 4986.6702, 2)  # expected volume is 4986.6702 cubic nautical miles


if __name__ == '__main__':
    unittest.main()
