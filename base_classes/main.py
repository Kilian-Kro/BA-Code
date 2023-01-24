import geopy.units

from KPIs.gianzza import Gianazza
from sector import Sector


def main():
    """
    sector1 = Sector('Test Sector', 0, 50000, [(11.381, 47.994),
                                               (11.376, 48.284),
                                               (11.860, 48.288),
                                               (11.861, 47.998)])

    def fill_sector(sector, num_planes):
        planes = []
        for i in range(int(random.uniform(1, num_planes))):
            # Generate random position for the plane within the test_sector
            pos_x = sector.corner_points[0][0] + random.uniform(0, 1) * (
                    sector.corner_points[2][0] - sector.corner_points[0][0])
            pos_y = sector.corner_points[0][1] + random.uniform(0, 1) * (
                    sector.corner_points[2][1] - sector.corner_points[0][1])
            altitude = random.uniform(sector.floor, sector.ceiling)
            speed = random.uniform(0, 400)
            climbrate = random.uniform(-3000, 3000)
            heading = int(random.uniform(0, 3600))
            plane = Airplane(f'Plane {i}', heading, altitude, speed, climbrate, pos_x, pos_y)
            planes.append(plane)
        return planes

    sector1.update_current_planes(fill_sector(sector1, 10), 30)
    sector1.update_current_planes(fill_sector(sector1, 15), 30)
    sector1.update_current_planes(fill_sector(sector1, 20), 30)
    sector1.update_current_planes(fill_sector(sector1, 25), 30)
    sector1.update_current_planes(fill_sector(sector1, 30), 30)

    print("Euro")

    euro = Eurocontrol(sector1)
    print(euro.complexity_score())

    print("Metron")

    metron = Metron(sector1)
    print(metron.wact())
    print(metron.wden())
    print(metron.wclap())
    print(metron.wconvang())
    print(metron.wconflict_nbrs())
    print(metron.wconf_bound())
    print(metron.walc())
    print(metron.walc())
    print(metron.wheadvar())
    print(metron.wbprox())
    print(metron.wasp())

    print("Nasa Additional")
    nasa_add = NasaAdditional(sector1)
    print(nasa_add.numhorizon())
    print(nasa_add.hdgvari())
    print(nasa_add.axishdg())
    print(nasa_add.convconf())
    print(nasa_add.proxcount())
    print(nasa_add.confcount())
    print(nasa_add.altvari())
    print(nasa_add.numbndy())
    print(nasa_add.aspect())

    print("Nasa One")
    nasa_one = NasaOne(sector1)
    print(nasa_one.c_1())
    print(nasa_one.c_2())
    print(nasa_one.c_3())
    print(nasa_one.c_4())
    print(nasa_one.c_5())
    print(nasa_one.c_6())
    print(nasa_one.c_7())
    print(nasa_one.c_8())
    print(nasa_one.c_9())
    print(nasa_one.c_10())
    print(nasa_one.c_11())
    print(nasa_one.c_12())
    print(nasa_one.c_13())
    print(nasa_one.c_14())
    print(nasa_one.c_15())
    print(nasa_one.c_16())

    print("Nasa Two")
    nasa_two = NasaTwo(sector1)
    print(nasa_two.traffic_density_n())
    print(nasa_two.heading_change_nh())
    print(nasa_two.speed_change_ns())
    print(nasa_two.altitude_change_na())
    print(nasa_two.distance_between_0_and_5_s5())
    print(nasa_two.distance_between_5_and_10_s10())
    print(nasa_two.distance_between_0_and_25_s25())
    print(nasa_two.distance_between_25_and_40_s40())
    print(nasa_two.distance_between_40_and_70_s70())

    print("WJTHC")
    wjthc = WJTHC(sector1)
    print(wjthc.sector_volume())
    print(wjthc.aircraft_count())
    print(wjthc.aircraft_density_one())
    print(wjthc.aircraft_density_two())
    print(wjthc.convergence_recognition_index())
    print(wjthc.separation_criticality_index())
    print(wjthc.degrees_of_freedom_index())
    print(wjthc.coordination_taskload_index())
    """

    sector2 = Sector('Test Sector', 0, 50000,
                     [(47.79736992227051, 10.938828673978394), (48.72458082631016, 10.87423007609716),
                      (48.736504812479225, 12.332213499138453),
                      (47.83164829871676, 12.357166952827761)])  # 10883.69 km², 417.43 km

    # print(sector2.sector_area())
    # print("KM: 10883.69 NM: " + str(geopy.units.nautical(kilometers=10883.69)))

    # obj = dict(type='Polygon', coordinates=[
    #     [[48.0, 11.0], [49.0, 11.0], [49.0, 12.0], [48.0, 12.0]]])
    #
    # area_m2 = area(obj)
    #
    # area_km2 = area_m2 / 1e+6
    # print('area m2:' + str(area_m2))
    # print('area km2:' + str(area_km2))

    # loop for 50 times
    for i in range(100):
        sector2.create_traffic_loop(50, 20)

    g = Gianazza(sector2)
    g.f15(10)
    g.f60(10)
    g.inter_hori()


#
# customKPI = CustomKPI(sector2)
#
# print(customKPI.average_in_sector_flight_time())
# print(customKPI.average_in_sector_distance())


"""
    print(sector2.is_pos_in_sector(48.4506278, 11.3911521))  # yes
    print(sector2.is_pos_in_sector(48.5307198, 12.3304832))  # no
    print(sector2.is_pos_in_sector(47.7887274, 12.2865378))  # no
    print(sector2.is_pos_in_sector(48.0666264, 11.1027610))  # yes
    print(sector2.is_pos_in_sector(48.2436281, 11.9995844))  # yes
    print(sector2.is_pos_in_sector(48.243, 11.999))  # ?
    print(sector2.is_pos_in_sector(48.6152677,
                                   11.4047348))  # yes
    print(sector2.is_pos_in_sector(48.1775941,
                                   12.4484360))  # no
    print(sector2.is_pos_in_sector(49.0383776,
                                   11.6821396))  # no
"""

if __name__ == "__main__":
    main()
