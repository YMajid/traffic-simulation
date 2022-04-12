import numpy as np
import numpy.random as rand
from itertools import product


class NSModel:
    def __init__(self,
                 prob=0.5,
                 n_lanes=3,
                 lane_len=100,
                 max_velocity=5,
                 lane_density=0.3):
        self.prob = prob
        self.n_lanes = n_lanes
        self.lane_len = lane_len
        self.max_velocity = max_velocity
        self.lane_density = lane_density
        self.__initialize_highway()

    def simulate(self):
        self.__change_lanes()
        self.__update_velocity()
        self.__update_position()

    def lane_velocity(self):
        return np.array([lane[lane != -1].mean() for lane in self.highway])

    def highway_velocity(self):
        return self.lane_velocity().mean()

    def __initialize_highway(self):
        self.highway = -1 * np.ones((self.n_lanes, self.lane_len), dtype=int)

        for lane in range(0, self.n_lanes):
            indices = rand.choice(self.lane_len,
                                  size=int(self.lane_len * self.lane_density),
                                  replace=False)
            for index in indices:
                self.highway[lane,
                             index] = rand.randint(0, self.max_velocity + 1)

    def __update_velocity(self):
        for i, j in product(range(0, self.n_lanes), range(0, self.lane_len)):
            if self.highway[i, j] == -1:
                continue

            self.highway[i, j] = self.__get_max_velocity(i, j)

            if 1 <= self.highway[i, j] and rand.rand() < self.prob:
                self.highway[i, j] -= 1

    def __get_max_velocity(self, lane, pos):
        distance = 1
        while self.highway[lane, (pos + distance) % self.lane_len] == -1:
            distance += 1

        max_velocity = self.highway[lane, pos]
        if distance < self.highway[lane, pos] + 1:
            max_velocity = distance - 1
        elif self.highway[lane, pos] < self.max_velocity:
            max_velocity = self.highway[lane, pos] + 1

        return max_velocity

    def __update_position(self):
        updated_highway = -1 * \
            np.ones((self.n_lanes, self.lane_len), dtype=int)
        for i, j in product(range(0, self.n_lanes), range(0, self.lane_len)):
            if self.highway[i, j] == -1:
                continue

            updated_highway[i, (j + self.highway[i, j]) %
                            self.lane_len] = self.highway[i, j]

        self.highway = updated_highway

    def __change_lanes(self):
        if self.n_lanes == 1:
            return

        for i, j in product(range(0, self.n_lanes), range(0, self.lane_len)):
            if rand.rand() < self.prob:
                continue

            direction = -1 if rand.rand() < 0.5 else 1
            if self.__can_switch_lane(direction, i,
                                      j) and rand.rand() < self.prob:
                self.highway[(i + direction) % self.n_lanes,
                             j] = self.highway[i, j]
                self.highway[i, j] = -1

    def __can_switch_lane(self, direction=0, lane=0, pos=0):
        new_lane = lane + direction
        next_lane = lane + 2 * direction
        if (direction == 0 or new_lane < 0 or self.n_lanes <= new_lane
                or self.highway[new_lane, pos] == -1):
            return False

        curr_max_velocity = self.__get_max_velocity(lane, pos)
        alt_max_velocity = self.__get_max_velocity(new_lane, pos)

        if (alt_max_velocity < curr_max_velocity or next_lane < 0
                or self.n_lanes <= next_lane
                or self.highway[next_lane, pos] != -1
                or self.__will_crash(new_lane, pos)):
            return False

        return True

    def __will_crash(self, lane, pos):
        distance = 1
        while self.highway[lane, (pos - distance) % self.lane_len] == -1:
            distance += 1
        max_velocity = self.__get_max_velocity(lane, (pos - distance) %
                                               self.lane_len)
        return max_velocity <= distance
