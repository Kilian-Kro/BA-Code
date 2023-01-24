class WorkLoadOne:
    def __init__(self, sector):
        self.sector = sector
        self.planes = sector.get_planes()

        # workload constants
        self.intercept = 193.921
        self.cruise = 45.225
        self.ascend = 46.201
        self.descend_cruise = 3.820
        self.ascend_cruise = 1.560
        self.descend_ascend = 5.337

    def compute_workload(self):
        c = 0
        a = 0
        d = 0
        for plane in self.planes:
            if -200 <= plane.get_climbrate() <= 200:
                c += 1
            if plane.get_climbrate() > 200:
                a += 1
            if plane.get_climbrate() < -200:
                d += 1

        workload = self.intercept + self.cruise * c + self.ascend * a + self.descend_cruise * d * c + self.descend_ascend * d * a + self.ascend_cruise * a * c
        # right now workload is in seconds, convert to minutes
        workload = workload / 60

        return workload

    # As 42 is the maximum workload, the workload can be expressed as a percentage of 42
    def compute_workload_percentage(self):
        workload = self.compute_workload()
        workload_percentage = (workload / 42) * 100
        return workload_percentage

    def __str__(self):
        return f"Workload: {self.compute_workload()}"
