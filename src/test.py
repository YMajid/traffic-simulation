from concurrent.futures import ProcessPoolExecutor as PoolExecutor, as_completed
from multiprocessing import cpu_count
from tqdm import tqdm

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


def velocity_to_density_lanes(delta=0.1, steps=1, prob=0.5):
    # mean_velocity = {'1': [], '2': [], '3': [], '4': []}
    mean_velocity = {'3': []}
    print(mean_velocity)
    densities = np.arange(0, 1 + delta, delta)
    print(densities)

    print("!!")
    for lane in mean_velocity:
        print("1!!!")
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

    return "DONE BITCH"


def validation():
    futures = []
    print("!_!")
    with PoolExecutor(max_workers=cpu_count()) as executor:
        with tqdm() as progress:
            print("!")
            future = executor.submit(velocity_to_density_lanes)
            future.add_done_callback(lambda _: progress.update())
            futures.append(future)
            for future in as_completed(futures):
                print(future.result())
            executor.shutdown(wait=True)


def pr():
    print("HH")
    return "!!"


def main():
    print("1")
    futures = []
    with PoolExecutor(max_workers=cpu_count()) as executor:
        futures.append(executor.submit(pr))
        for future in as_completed(futures):
            print(future.result())
        executor.shutdown(wait=True)
    print("DONE")


if __name__ == "__main__":
    import time
    import warnings

    print("H")
    print("----------")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        start = time.time()
        # main()
        validation()
        end = time.time()

    print(end - start)
