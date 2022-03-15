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
        print(self.highway)
        self.__update_velocity()
        print(self.highway)

    def __initialize_highway(self):
        self.highway = -1 * np.ones((self.n_lanes, self.lane_len))

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

            distance = 1
            while self.highway[i, (j + distance) % self.lane_len] == -1:
                distance += 1

            if distance <= self.highway[i, j] + 1:
                self.highway[i, j] = distance - 1
            elif self.highway[i, j] < self.max_velocity:
                self.highway[i, j] += 1

            if rand.rand() < prob:
                self.highway[i, j] -= 1

    def __update_position(self):
        pass

    def __change_lanes(self):
        if self.n_lanes == 1:
            return


if __name__ == "__main__":
    x = NSModel()
