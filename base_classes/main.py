from KPIs.eurocontrol import Eurocontrol
from KPIs.gianzza import Gianazza
from KPIs.metron_aviation import Metron
from KPIs.nasa_additional import NasaAdditional
from KPIs.nasa_metric_one import NasaOne
from KPIs.nasa_metric_two import NasaTwo
from KPIs.wjthc import WJTHC
from KPIs.workload_one import WorkLoadOne
from KPIs.workloadtwo import WorkloadTwo
from base_classes.airplane import Airplane
from sector import Sector


def main():
    sector1 = Sector('Test Sector', 10000, 30000, [(48., 11.),
                                               (49., 11.),
                                               (49., 12.),
                                               (48., 12.)])

    # Callsign, Heading, Altitude, Speed, climbrate, pos_x, pos_y
    scenario1 = [Airplane("Plane1", 180, 11000, 350, 0, 48.9275265, 11.1110859),
                 Airplane("Plane2", 180, 15000, 400, 0, 48.9094778, 11.4530354),
                 Airplane("Plane3", 180, 20000, 450, 0, 48.8462561, 11.7304402),
                 Airplane("Plane4", 180, 25000, 500, 0, 48.8760706, 11.6494160),
                 Airplane("Plane5", 180, 12000, 550, 0, 48.6588329, 11.5093403),
                 Airplane("Plane6", 360, 15000, 400, 0, 48.1918610, 11.1365969),
                 Airplane("Plane7", 360, 20000, 450, 0, 48.1222367, 11.5211184),
                 Airplane("Plane8", 360, 25000, 430, 0, 48.0745445, 11.8342287),
                 Airplane("Plane9", 360, 29000, 410, 0, 48.2942932, 11.6392214),
                 Airplane("Plane10", 270, 27000, 700, 0, 48.5567486, 11.5719301)]

    # 50 % More aircraft
    scenario2 = [Airplane("Plane1", 180, 11000, 350, 0, 48.9275265, 11.1110859),
                 Airplane("Plane2", 180, 15000, 400, 0, 48.9094778, 11.4530354),
                 Airplane("Plane3", 180, 20000, 450, 0, 48.8462561, 11.7304402),
                 Airplane("Plane4", 180, 25000, 500, 0, 48.8760706, 11.6494160),
                 Airplane("Plane5", 180, 12000, 550, 0, 48.6588329, 11.5093403),
                 Airplane("Plane6", 360, 15000, 400, 0, 48.1918610, 11.1365969),
                 Airplane("Plane7", 360, 20000, 450, 0, 48.1222367, 11.5211184),
                 Airplane("Plane8", 360, 25000, 430, 0, 48.0745445, 11.8342287),
                 Airplane("Plane9", 360, 29000, 410, 0, 48.2942932, 11.6392214),
                 Airplane("Plane10", 270, 27000, 700, 0, 48.5567486, 11.5719301),
                 Airplane("Plane11", 180, 125000, 350, 0, 48.9052291, 11.2704345),
                 Airplane("Plane12", 360, 25000, 400, 0, 48.3196103, 11.3294860),
                 Airplane("Plane13", 360, 15000, 450, 0, 48.4727979, 11.6906616),
                 Airplane("Plane14", 180, 29000, 500, 0, 48.7370498, 11.2457153),
                 Airplane("Plane15", 180, 11000, 550, 0, 48.2602175, 11.5190002)]

    # Altitude Variation
    scenario3 = [Airplane("Plane1", 180, 11000, 350, -3000, 48.9275265, 11.1110859),
                 Airplane("Plane2", 180, 15000, 400, 2000, 48.9094778, 11.4530354),
                 Airplane("Plane3", 180, 20000, 450, -1000, 48.8462561, 11.7304402),
                 Airplane("Plane4", 180, 25000, 500, 2000, 48.8760706, 11.6494160),
                 Airplane("Plane5", 180, 12000, 550, -3000, 48.6588329, 11.5093403),
                 Airplane("Plane6", 360, 15000, 400, 2000, 48.1918610, 11.1365969),
                 Airplane("Plane7", 360, 20000, 450, -1000, 48.1222367, 11.5211184),
                 Airplane("Plane8", 360, 25000, 430, 2000, 48.0745445, 11.8342287),
                 Airplane("Plane9", 360, 29000, 410, -3000, 48.2942932, 11.6392214),
                 Airplane("Plane10", 270, 27000, 700, 2000, 48.5567486, 11.5719301),
                 Airplane("Plane11", 180, 125000, 350, -1000, 48.9052291, 11.2704345),
                 Airplane("Plane12", 360, 25000, 400, 2000, 48.3196103, 11.3294860),
                 Airplane("Plane13", 360, 15000, 450, -3000, 48.4727979, 11.6906616),
                 Airplane("Plane14", 180, 29000, 500, 2000, 48.7370498, 11.2457153),
                 Airplane("Plane15", 180, 11000, 550, -1000, 48.2602175, 11.5190002)]

    # Heading Variation
    scenario4 = [Airplane("Plane1", 270, 11000, 350, -3000, 48.9275265, 11.1110859),
                 Airplane("Plane2", 120, 15000, 400, 2000, 48.9094778, 11.4530354),
                 Airplane("Plane3", 290, 20000, 450, -1000, 48.8462561, 11.7304402),
                 Airplane("Plane4", 230, 25000, 500, 2000, 48.8760706, 11.6494160),
                 Airplane("Plane5", 250, 12000, 550, -3000, 48.6588329, 11.5093403),
                 Airplane("Plane6", 30, 15000, 400, 2000, 48.1918610, 11.1365969),
                 Airplane("Plane7", 10, 20000, 450, -1000, 48.1222367, 11.5211184),
                 Airplane("Plane8", 80, 25000, 430, 2000, 48.0745445, 11.8342287),
                 Airplane("Plane9", 120, 29000, 410, -3000, 48.2942932, 11.6392214),
                 Airplane("Plane10", 320, 27000, 700, 2000, 48.5567486, 11.5719301),
                 Airplane("Plane11", 110, 125000, 350, -1000, 48.9052291, 11.2704345),
                 Airplane("Plane12", 75, 25000, 400, 2000, 48.3196103, 11.3294860),
                 Airplane("Plane13", 5, 15000, 450, -3000, 48.4727979, 11.6906616),
                 Airplane("Plane14", 150, 29000, 500, 2000, 48.7370498, 11.2457153),
                 Airplane("Plane15", 170, 11000, 550, -1000, 48.2602175, 11.5190002)]

    # Conflicts: Plane 4 auf 20000, now Conflict with Plane 3
    # Plane 7 now at 11000, Plane 15 Conflict
    # Plane 5 auf 27000, now Conflict with Plane 10
    # Plane1 moved, so now Conflict with Plane 11
    scenario5 = [Airplane("Plane1", 270, 12500, 350, -3000, 48.8965293, 11.3518952),
                 Airplane("Plane2", 120, 15000, 400, 2000, 48.9094778, 11.4530354),
                 Airplane("Plane3", 290, 20000, 450, -1000, 48.8462561, 11.7304402),
                 Airplane("Plane4", 230, 20000, 500, 2000, 48.8760706, 11.6494160),
                 Airplane("Plane5", 250, 27000, 550, -3000, 48.6588329, 11.5093403),
                 Airplane("Plane6", 30, 15000, 400, 2000, 48.1918610, 11.1365969),
                 Airplane("Plane7", 10, 11000, 450, -1000, 48.1222367, 11.5211184),
                 Airplane("Plane8", 80, 25000, 430, 2000, 48.0745445, 11.8342287),
                 Airplane("Plane9", 120, 29000, 410, -3000, 48.2942932, 11.6392214),
                 Airplane("Plane10", 320, 27000, 700, 2000, 48.5567486, 11.5719301),
                 Airplane("Plane11", 110, 125000, 350, -1000, 48.9052291, 11.2704345),
                 Airplane("Plane12", 75, 25000, 400, 2000, 48.3196103, 11.3294860),
                 Airplane("Plane13", 5, 15000, 450, -3000, 48.4727979, 11.6906616),
                 Airplane("Plane14", 150, 29000, 500, 2000, 48.7370498, 11.2457153),
                 Airplane("Plane15", 170, 11000, 550, -1000, 48.2602175, 11.5190002)]

    sector1.set_current_planes(scenario5)

    print("=====================================")

    euro = Eurocontrol(sector1)
    print("Euro")
    print(euro.complexity_score())

    print("=====================================")

    print("Metron")

    metron = Metron(sector1)
    # print(metron.wact())
    # print(metron.wden())
    # print(metron.wclap())
    # print(metron.wconvang())
    # print(metron.wconflict_nbrs())
    # print(metron.wconf_bound())
    # print(metron.walc())
    # print(metron.wheadvar())
    # print(metron.wbprox())
    # print(metron.wasp_vdf())
    print(round(
        metron.wact() + metron.wden() + metron.wclap() + metron.wconvang() + metron.wconflict_nbrs() + metron.wconf_bound() + metron.walc() + metron.wheadvar() + metron.wbprox() + metron.wasp_vdf(), 2))

    print("=====================================")

    print("Nasa Additional")
    nasa_add = NasaAdditional(sector1)
    # print(nasa_add.numhorizon())
    # print(nasa_add.hdgvari())
    # print(nasa_add.axishdg())
    # print(nasa_add.convconf())
    # print(nasa_add.proxcount())
    # print(nasa_add.confcount())
    # print(nasa_add.altvari())
    # print(nasa_add.numbndy())
    # print(nasa_add.aspect())
    print(round(
        nasa_add.numhorizon() + nasa_add.hdgvari() + nasa_add.axishdg() + nasa_add.proxcount() + nasa_add.confcount() + nasa_add.altvari() + nasa_add.numbndy() + nasa_add.aspect(), 2))

    print("=====================================")

    print("Nasa One")
    nasa_one = NasaOne(sector1)
    #  print(nasa_one.c_1())
    #  print(nasa_one.c_2())
    #  print(nasa_one.c_3())
    #  print(nasa_one.c_4())
    #  print(nasa_one.c_5())
    #  print(nasa_one.c_6())
    #  print(nasa_one.c_7())
    #  print(nasa_one.c_8())
    #  print(nasa_one.c_9())
    #  print(nasa_one.c_10())
    #  print(nasa_one.c_11())
    #  print(nasa_one.c_12())
    #  print(nasa_one.c_13())
    #  print(nasa_one.c_14())
    #  print(nasa_one.c_15())
    #  print(nasa_one.c_16())
    print(round(
        nasa_one.c_1() + nasa_one.c_2() + nasa_one.c_3() + nasa_one.c_4() + nasa_one.c_5() + nasa_one.c_6() + nasa_one.c_7() + nasa_one.c_8() + nasa_one.c_9() + nasa_one.c_10() + nasa_one.c_11() + nasa_one.c_12() + nasa_one.c_13() + nasa_one.c_14() + nasa_one.c_15() + nasa_one.c_16(), 2))

    print("=====================================")

    print("Nasa Two")
    nasa_two = NasaTwo(sector1)
    # print(nasa_two.traffic_density_n())
    # print(nasa_two.heading_change_nh())
    # print(nasa_two.speed_change_ns())
    # print(nasa_two.altitude_change_na())
    # print(nasa_two.distance_between_0_and_5_s5())
    # print(nasa_two.distance_between_5_and_10_s10())
    # print(nasa_two.distance_between_0_and_25_s25())
    # print(nasa_two.distance_between_25_and_40_s40())
    # print(nasa_two.distance_between_40_and_70_s70())
    print(round(
        nasa_two.traffic_density_n() + nasa_two.heading_change_nh() + nasa_two.speed_change_ns() + nasa_two.altitude_change_na() + nasa_two.distance_between_0_and_5_s5() + nasa_two.distance_between_5_and_10_s10() + nasa_two.distance_between_0_and_25_s25() + nasa_two.distance_between_25_and_40_s40() + nasa_two.distance_between_40_and_70_s70(), 2))

    print("=====================================")

    print("WJTHC")
    wjthc = WJTHC(sector1)
    # print(wjthc.sector_volume())
    # print(wjthc.aircraft_count())
    # print(wjthc.aircraft_density_one())
    # print(wjthc.aircraft_density_two())
    # print(wjthc.convergence_recognition_index())
    # print(wjthc.separation_criticality_index())
    # print(wjthc.degrees_of_freedom_index())
    # print(wjthc.coordination_taskload_index())
    print(round(
        wjthc.sector_volume() + wjthc.aircraft_count() + wjthc.aircraft_density_one() + wjthc.aircraft_density_two() + wjthc.convergence_recognition_index() + wjthc.separation_criticality_index() + wjthc.degrees_of_freedom_index() + wjthc.coordination_taskload_index(), 2))

    print("=====================================")

    print("Gianazza")
    gianazza = Gianazza(sector1)
    print(gianazza.v())
    # print(gianazza.nb())
    # print(gianazza.avg_vs())
    # print(gianazza.f15(5))
    # print(gianazza.f60(5))
    # print(gianazza.inter_hori())
    print(round(gianazza.nb() + gianazza.avg_vs() + gianazza.f15(5) + gianazza.f60(5) + gianazza.inter_hori(), 2))

    print("=====================================")

    print("Workload 1")
    workload1 = WorkLoadOne(sector1)
    print(round(workload1.compute_workload(), 2))
    print(round(workload1.compute_workload_percentage(), 2))

    print("=====================================")

    print("Workload 2")
    workload2 = WorkloadTwo(sector1)
    print(round(workload2.workload(), 2))

    print("=====================================")


if __name__ == "__main__":
    main()
