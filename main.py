import numpy as np
import numpy.random as rand
from itertools import product


class NSModel:
    def __init__(self,
                 n_lanes=3,
                 lane_len=100,
                 max_velocity=5,
                 lane_density=0.3):
        self.n_lanes = n_lanes
        self.lane_len = lane_len
        self.max_velocity = max_velocity
        self.lane_density = lane_density
        self.__initialize_highway()

    def main(self):
        print(self.highway)
        self.__update_velocity()
        print(self.highway)
        self.__update_position()
        print(self.highway)

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
        prob = rand.rand()
        for i, j in product(range(0, self.n_lanes), range(0, self.lane_len)):
            if self.highway[i, j] == -1:
                continue

            self.highway[i, j] = self.__get_max_velocity(i, j)

            if 1 <= self.highway[i, j] and rand.rand() < prob:
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
        updated_highway = -1 * np.ones(
            (self.n_lanes, self.lane_len), dtype=int)
        for i, j in product(range(0, self.n_lanes), range(0, self.lane_len)):
            if self.highway[i, j] == -1:
                continue

            updated_highway[i, (j + self.highway[i, j]) %
                            self.lane_len] = self.highway[i, j]

        self.highway = updated_highway

    def __change_lanes(self):
        if self.n_lanes == 1:
            return

        prob = rand.rand()
        for i, j in product(range(0, self.n_lanes), range(0, self.lane_len)):
            if rand.rand() < prob:
                continue
            direction = -1 if rand.rand() < 0.5 else 1
            if self.__can_switch_lane(direction, i, j) and rand.rand() < prob:
                self.highway[(i + direction) % self.n_lanes,
                             j] = self.highway[i, j]
                self.highway[i, j] = -1

    def __can_switch_lane(self, direction=0, lane=0, pos=0):
        if direction == 0 or self.highway[(lane + direction) % self.n_lanes,
                                          pos] == -1:
            return False

        curr_max_velocity = self.__get_max_velocity(lane, pos)
        alt_max_velocity = self.__get_max_velocity(
            (lane + direction) % self.n_lanes, pos)

        if alt_max_velocity < curr_max_velocity or self.highway[
            (lane + 2 * direction) % self.n_lanes,
                pos] != -1 or self.__can_pass_prev_car(
                    (lane + direction) % self.lane_len, pos):
            return False

        return True

    def __can_pass_prev_car(self, lane, pos):
        distance = 1
        while self.highway[lane, (pos - distance) % self.lane_len] == -1:
            distance += 1
        max_velocity = self.__get_max_velocity(lane, (pos - distance) %
                                               self.lane_len)
        return max_velocity < distance


if __name__ == "__main__":
    x = NSModel()
    x.main()
