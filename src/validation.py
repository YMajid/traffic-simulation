import numpy as np
from src.model import NSModel
from itertools import product
import matplotlib.pyplot as plt


def lane_velocity_check(highway):
    for i in range(len(highway)):
        count = 0
        velocity_sum = 0
        for j in range(len(highway[i])):
            if highway[i][j] != -1:
                count += 1
                velocity_sum += highway[i][j]
        print(velocity_sum / count)


def velocity_to_density(dt=0.01):
    time_arr = np.arange(0, 10 + dt, dt)
    densities = np.arange(0, 1 + dt, dt)
    # mean_velocity = {"0.0": [], "0.3": []}
    mean_velocity = {"0.3": []}
    for prob, density in product(mean_velocity.keys(), densities):
        curr_means = []
        model = NSModel(prob=float(prob),
                        n_lanes=1,
                        lane_len=100,
                        max_velocity=5,
                        lane_density=density)
        for _ in time_arr:
            model.simulate()
            curr_means.append(model.highway_velocity())
        mean_velocity[prob].append(sum(curr_means) / len(curr_means))

    for prob in mean_velocity.keys():
        plt.plot(densities, mean_velocity[prob], label=f"p={prob}")
    plt.xlabel("Density")
    plt.ylabel("Mean Velocity")
    plt.legend(loc="upper right")
    plt.show()


if __name__ == "__main__":
    velocity_to_density()
