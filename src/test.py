from concurrent.futures import ProcessPoolExecutor as PoolExecutor, as_completed
from multiprocessing import cpu_count

import matplotlib.pyplot as plt
import numpy as np

from src.zipper import Zipper


def plt_helper(title, xlabel, ylabel, save=False):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc="upper right")

    if save:
        plt.savefig(f"./figures/{title}.png", format="png")
    else:
        plt.show()

    plt.cla()


def velocity_to_density_lanes(delta=0.01, steps=10, prob=0.5):
    mean_velocity = {'1': [], '2': [], '3': [], '4': []}
    densities = np.arange(0.01, 1 + delta, delta)

    for lane in mean_velocity:
        for density in densities:
            print(f"Lane:{lane} Density:{density}")
            curr_values = []
            model = Zipper(prob=prob,
                           n_lanes=int(lane),
                           lane_len=200,
                           max_velocity=5,
                           lane_density=density,
                           lane_changes=True,
                           n_blocked=0 if lane == '1' else 1,
                           portion_blocked=0.2)
            for _ in range(0, steps):
                for _ in range(0, 10):
                    model.simulate()
                    curr_values.append(model.highway_velocity())
            mean_velocity[lane].append(np.average(curr_values))

    for lane in mean_velocity.keys():
        plt.plot(densities, mean_velocity[lane], label=f"N={lane}")

    plt_helper("Mean Velocity vs. Density for N highway lanes",
               "Density (cars/lane)", "Mean Velocity (m/s)", False)


def validation():
    futures = []
    with PoolExecutor(max_workers=cpu_count()) as executor:
        futures.append(executor.submit(velocity_to_density_lanes))
        for future in as_completed(futures):
            print(future.result())
        executor.shutdown(wait=True)


if __name__ == "__main__":
    import time
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        start = time.time()
        validation()
        end = time.time()

    print(end - start)
