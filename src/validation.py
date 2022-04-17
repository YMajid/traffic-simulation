from concurrent.futures import ProcessPoolExecutor as PoolExecutor, as_completed
from multiprocessing import cpu_count

import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import append

from src.model import NSModel
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


def init_model(model,
               prob=0.5,
               n_lanes=3,
               lane_len=200,
               max_velocity=5,
               lane_density=0.5,
               lane_changes=False,
               initialize_highway=True,
               n_blocked=1,
               portion_blocked=0.2):
    if type(model).__name__ == "NSModel":
        return NSModel(prob=prob,
                       n_lanes=n_lanes,
                       lane_len=lane_len,
                       max_velocity=max_velocity,
                       lane_density=lane_density,
                       lane_changes=lane_changes,
                       initialize_highway=initialize_highway)
    return Zipper(prob=prob,
                  n_lanes=n_lanes,
                  lane_len=lane_len,
                  max_velocity=max_velocity,
                  lane_density=lane_density,
                  lane_changes=lane_changes,
                  n_blocked=n_blocked,
                  portion_blocked=portion_blocked)


def velocity_to_density(delta=0.01, steps=200, model=NSModel):
    mean_velocity = {"0.0": [], "0.5": []}
    densities = np.arange(0, 1 + delta, delta)

    for prob in mean_velocity.keys():
        for density in densities:
            curr_values = []
            model = init_model(NSModel, prob=float(prob), lane_density=density)
            for _ in range(0, steps + 1):
                for _ in range(0, 10):
                    model.simulate()
                    curr_values.append(model.highway_velocity())
            mean_velocity[prob].append(np.average(curr_values))

    for prob in mean_velocity.keys():
        plt.plot(densities, mean_velocity[prob], label=f"p={prob}")

    plt_helper("Mean Velocity vs. Density", "Density (cars/lane)",
               "Mean Velocity (m/s)", True)


def flow_rate_to_density(delta=0.01, steps=100, model=NSModel):
    lane_len = 200
    flow_rates = {"1": [], "3": [], "5": []}
    densities = np.arange(0, 1 + delta, delta)

    for max_velocity in flow_rates.keys():
        for density in densities:
            curr_values = []
            for _ in range(0, steps + 1):
                model = init_model(model,
                                   max_velocity=int(max_velocity),
                                   lane_density=density)
                for _ in range(0, lane_len):
                    model.simulate()
                curr_values.append(model.flow_count / lane_len)
            flow_rates[max_velocity].append(np.average(curr_values))

    for max_velocity in flow_rates.keys():
        plt.plot(densities,
                 flow_rates[max_velocity],
                 label=f"Max Velocity={max_velocity}")

    plt_helper("Flow Rate vs. Density", "Density (cars/lane)",
               "Flow Rate (cars/step)", True)


def cars_per_site(steps=200, model=NSModel):
    model = init_model(NSModel)

    values = []
    for _ in range(0, steps):
        curr_values = []
        model.simulate()
        for v in model.highway[0]:
            curr_values.append(v)
        values.append(curr_values)

    plt.imshow(values, cmap="Blues", interpolation="nearest")
    plt_helper("Cars per Site", "Site", "Step", True)


def velocity_to_density_lanes(delta=0.01, steps=100, prob=0.5, model=NSModel):
    mean_velocity = {"1": [], "2": [], "3": [], "4": []}
    densities = np.arange(0.01, 1 + delta, delta)

    for lane in mean_velocity.keys():
        for density in densities:
            curr_values = []
            model = init_model(model,
                               prob=float(prob),
                               n_lanes=int(lane),
                               lane_density=density,
                               lane_changes=True,
                               n_blocked=0 if int(lane) == 1 else 1,
                               portion_blocked=0.2)
            for _ in range(0, steps):
                for _ in range(0, 10):
                    model.simulate()
                    curr_values.append(model.highway_velocity())
            mean_velocity[lane].append(np.average(curr_values))

    for lane in mean_velocity.keys():
        plt.plot(densities, mean_velocity[lane], label=f"N={lane}")

    plt_helper("Mean Velocity vs. Density for N highway lanes",
               "Density (cars/lane)", "Mean Velocity (m/s)", True)


def velocity_to_density_speedlim(steps=100,
                                 prob=0.5,
                                 delta=0.01,
                                 model=NSModel):
    mean_velocity = {"2": [], "4": [], "6": [], "8": []}
    densities = np.arange(0.01, 1 + delta, delta)

    for speedlim in mean_velocity.keys():
        for density in densities:
            curr_values = []
            model = init_model(model,
                               prob=float(prob),
                               max_velocity=int(speedlim),
                               n_lanes=2,
                               lane_density=density,
                               lane_changes=True,
                               n_blocked=1,
                               portion_blocked=0.2)
            for _ in range(0, steps):
                for _ in range(0, 10):
                    model.simulate()
                    curr_values.append(model.highway_velocity())
            mean_velocity[speedlim].append(np.average(curr_values))

    for speedlim in mean_velocity.keys():
        plt.plot(densities,
                 mean_velocity[speedlim],
                 label=f"Speed limit={speedlim} (m/s)")

    plt_helper("Mean Velocity vs. Density for varying speed limits",
               "Density (cars/lane)", "Mean Velocity (m/s)", True)


def flow_to_density(steps=100,
                    prob=0.5,
                    delta=0.05,
                    lane_len=200,
                    model=NSModel):
    flow_rates = {"1": [], "2": [], "3": [], "4": []}
    densities = np.arange(0.05, 1 + delta, delta)

    for lane in flow_rates:
        for density in densities:
            curr_values = []
            for _ in range(0, steps + 1):
                model = init_model(model,
                                   prob=float(prob),
                                   n_lanes=int(lane),
                                   lane_density=density,
                                   lane_changes=True,
                                   n_blocked=0 if int(lane) == 0 else 1,
                                   portion_blocked=0.2)
                for _ in range(0, lane_len):
                    model.simulate()
                curr_values.append(model.flow_count / lane_len)
            flow_rates[lane].append(np.average(curr_values))

    for lane in flow_rates.keys():
        plt.plot(densities, flow_rates[lane], label=f"N={lane}")

    plt_helper("Flow Rate vs. Density for N highway lanes",
               "Density (cars/lane)", "Flow Rate (cars/step)", True)


def validation():
    futures = []
    with PoolExecutor(max_workers=cpu_count()) as executor:
        futures.append(executor.submit(velocity_to_density()))
        futures.append(executor.submit(flow_rate_to_density()))
        futures.append(executor.submit(cars_per_site()))
        executor.shutdown(wait=True)


def main_NS():
    futures = []
    with PoolExecutor(max_workers=cpu_count()) as executor:
        futures.append(
            executor.submit(velocity_to_density_lanes(model=NSModel)))
        futures.append(
            executor.submit(velocity_to_density_speedlim(model=NSModel)))
        futures.append(executor.submit(flow_to_density(model=NSModel)))
        executor.shutdown(wait=True)


def main_Z():
    futures = []
    with PoolExecutor(max_workers=cpu_count()) as executor:
        futures.append(executor.submit(
            velocity_to_density_lanes(model=Zipper)))
        futures.append(
            executor.submit(velocity_to_density_speedlim(model=Zipper)))
        futures.append(executor.submit(flow_to_density(model=Zipper)))
        executor.shutdown(wait=True)


if __name__ == "__main__":
    import time

    start = time.time()
    validation()
    main_NS()
    main_Z()
    end = time.time()
    print(end - start)
