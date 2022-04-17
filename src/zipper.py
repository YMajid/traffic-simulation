import numpy as np
import numpy.random as rand

from src.model import NSModel


class Zipper(NSModel):
    def __init__(self,
                 prob=0.5,
                 n_lanes=3,
                 lane_len=100,
                 max_velocity=5,
                 lane_density=0.3,
                 lane_changes=True,
                 n_blocked=1,
                 portion_blocked=0.2):
        super().__init__(prob, n_lanes, lane_len, max_velocity, lane_density,
                         lane_changes, False)
        self.n_blocked = n_blocked
        self.portion_blocked = portion_blocked
        self.blockages = {}
        self.initialize_highway()

    def block_lanes(self):
        blocked_len = int(self.portion_blocked * self.lane_len)
        blocked_lanes = rand.choice(self.n_lanes,
                                    size=self.n_blocked,
                                    replace=False)
        for lane in blocked_lanes:
            pt_one = rand.randint(0, self.lane_len)
            pt_two = (pt_one + blocked_len) % self.lane_len
            start = pt_one if pt_one < pt_two else pt_two
            end = pt_two if pt_one < pt_two else pt_one
            # TODO Make sure indices array is of the correct length in a less hacky way
            indices = np.arange(start, end)[:blocked_len]
            self.blockages[lane] = indices
            np.put(self.highway[lane], indices, [-2] * blocked_len)

    def populate_highway(self):
        n_cars = int(self.lane_len * self.lane_density)
        for lane in range(0, self.n_lanes):
            valid_range = np.setdiff1d(
                np.arange(0, self.lane_len),
                self.blockages[lane]) if lane in self.blockages else np.arange(
                    0, self.lane_len)
            # TODO Make sure we're alloting the correct number of cars
            indices = rand.choice(valid_range,
                                  size=min(n_cars, len(valid_range)),
                                  replace=False)
            for index in indices:
                self.highway[lane,
                             index] = rand.randint(0, self.max_velocity + 1)

    def initialize_highway(self):
        self.highway = super().highway_structure()
        self.block_lanes()
        self.populate_highway()

    def zipper_merge(self, direction, lane, pos):
        self.highway[(lane + direction) % self.n_lanes,
                     pos] = self.highway[lane, pos]
        self.highway[lane, pos] = -1

    def update_position(self):
        updated_highway = self.highway.copy()
        for lane in updated_highway:
            lane[lane != -2] = -1

        for i in range(0, self.n_lanes):
            for j in range(0, self.lane_len):
                if self.highway[i, j] < 0:
                    continue

                if self.highway[i, (j + self.highway[i, j]) %
                                self.lane_len] == -2:
                    direction = 1 if super().can_switch_lane(1, i, j) else - \
                        1 if super().can_switch_lane(-1, i, j) else 0
                    if direction == 0:
                        continue
                    self.zipper_merge(direction, i, j)

                if self.lane_len <= j + self.highway[i, j]:
                    self.flow_count += 1

                updated_highway[i, (j + self.highway[i, j]) %
                                self.lane_len] = self.highway[i, j]

        self.highway = updated_highway
