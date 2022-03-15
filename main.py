import numpy as np
import numpy.random as rand


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
        self.initialize_highway()

    def initialize_highway(self):
        self.highway = np.zeros((self.n_lanes, self.lane_len))

        for lane in range(0, self.n_lanes):
            indices = rand.choice(self.lane_len,
                                  size=int(self.lane_len * self.lane_density),
                                  replace=False)
            for index in indices:
                self.highway[lane,
                             index] = rand.randint(0, self.max_velocity + 1)


if __name__ == "__main__":
    x = NSModel()
    print(x.highway)
