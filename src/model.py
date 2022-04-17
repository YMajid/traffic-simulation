import numpy as np
import numpy.random as rand


class NSModel:
    def __init__(self,
                 prob=0.5,
                 n_lanes=3,
                 lane_len=100,
                 max_velocity=5,
                 lane_density=0.3,
                 lane_changes=True,
                 initialize_highway=True):
        self.prob = prob
        self.n_lanes = n_lanes
        self.lane_len = lane_len
        self.max_velocity = max_velocity
        self.lane_density = lane_density
        self.lane_changes = lane_changes
        self.flow_count = 0

        if initialize_highway:
            self.initialize_highway()
        # print("Original")
        # self.print_highway()

    def simulate(self):
        if self.lane_changes:
            self.update_lanes()
            # print("Lane Change")
            # self.print_highway()

        self.update_velocity()
        # print("Velocity Change")
        # self.print_highway()

        self.update_position()
        # print("Position Change")
        # self.print_highway()
        # print(self.car_count())

    def print_highway(self):
        for lane in self.highway:
            print(''.join('.' if p == -1 else '*' if p == -2 else str(p)
                          for p in lane))

    def car_count(self):
        counter = 0
        for lane in self.highway:
            counter += len(lane[0 <= lane])
        return counter

    def lane_velocity(self):
        return np.array([lane[lane != -1].mean() for lane in self.highway])

    def highway_velocity(self):
        return self.lane_velocity().mean()

    def highway_structure(self):
        return -1 * np.ones((self.n_lanes, self.lane_len), dtype=int)

    def populate_highway(self):
        n_cars = int(self.lane_len * self.lane_density)
        for lane in range(0, self.n_lanes):
            indices = rand.choice(self.lane_len, size=n_cars, replace=False)
            for index in indices:
                self.highway[lane,
                             index] = rand.randint(0, self.max_velocity + 1)

    def initialize_highway(self):
        self.highway = self.highway_structure()
        self.populate_highway()

    def update_velocity(self):
        for i in range(0, self.n_lanes):
            for j in range(0, self.lane_len):
                if self.highway[i, j] < 0:
                    continue

                self.highway[i, j] = self.get_max_velocity(i, j)

                if 1 <= self.highway[i, j] and rand.rand() < self.prob:
                    self.highway[i, j] -= 1

    def get_distance(self, lane, pos):
        distance = 1
        while self.highway[lane, (pos + distance) % self.lane_len] == -1:
            distance += 1
        return distance

    def will_crash(self, lane, pos):
        distance = self.get_distance(lane, pos)
        max_velocity = self.get_max_velocity(lane,
                                             (pos - distance) % self.lane_len)
        return distance <= max_velocity

    def get_max_velocity(self, lane, pos):
        if self.highway[lane, pos] < 0:
            return self.highway[lane, pos]

        distance = self.get_distance(lane, pos)

        max_velocity = self.highway[lane, pos]
        if distance <= self.highway[lane, pos] + 1:
            max_velocity = distance - 1
        elif self.highway[lane, pos] < self.max_velocity:
            max_velocity = self.highway[lane, pos] + 1

        return max_velocity

    def update_position(self):
        updated_highway = self.highway.copy()
        for lane in updated_highway:
            lane[lane != -2] = -1

        for i in range(0, self.n_lanes):
            for j in range(0, self.lane_len):
                if self.highway[i, j] < 0:
                    continue

                if self.lane_len <= j + self.highway[i, j]:
                    self.flow_count += 1

                updated_highway[i, (j + self.highway[i, j]) %
                                self.lane_len] = self.highway[i, j]

        self.highway = updated_highway

    def update_lanes(self):
        if self.n_lanes == 1:
            return

        for i in range(0, self.n_lanes):
            for j in range(0, self.lane_len):
                if rand.rand() < self.prob or self.highway[i, j] == -2:
                    continue

                direction = -1 if rand.rand() < 0.5 else 1
                if self.can_switch_lane(
                        direction, i,
                        j) and rand.rand() < self.prob and self.highway[
                            (i + direction) % self.n_lanes, j] != -2:
                    self.highway[(i + direction) % self.n_lanes,
                                 j] = self.highway[i, j]
                    self.highway[i, j] = -1

    def can_switch_lane(self, direction=0, lane=0, pos=0):
        new_lane = lane + direction
        if (direction == 0 or new_lane < 0 or self.n_lanes <= new_lane
                or 0 <= self.highway[new_lane, pos]
                or self.will_crash(new_lane, pos) or self.get_max_velocity(
                    new_lane, pos) > self.get_max_velocity(lane, pos)):
            return False
        return True
