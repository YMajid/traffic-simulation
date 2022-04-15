import numpy as np
from src.model import NSModel
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor as PoolExecutor


def plt_helper(title, xlabel, ylabel, save=False):
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(loc="upper right")

    if save:
        plt.savefig(f"../figures/{title}.png", format="png")
    else:
        plt.show()

    plt.cla()


def velocity_to_density(delta=0.01, steps=200):
    mean_velocity = {"0.0": [], "0.5": []}
    densities = np.arange(0, 1 + delta, delta)

    for prob in mean_velocity.keys():
        for density in densities:
            curr_values = []
            model = NSModel(prob=float(prob),
                            n_lanes=1,
                            lane_len=200,
                            max_velocity=5,
                            lane_density=density,
                            lane_changes=False)
            for _ in range(0, steps + 1):
                for _ in range(0, 10):
                    model.simulate()
                    curr_values.append(model.highway_velocity())
            mean_velocity[prob].append(np.average(curr_values))

    for prob in mean_velocity.keys():
        plt.plot(densities, mean_velocity[prob], label=f"p={prob}")

    plt_helper("Mean Velocity vs. Density", "Density", "Mean Velocity", True)


def flow_rate_to_density(delta=0.01, steps=10000, lane_len=200):
    flow_rates = {"1": [], "3": [], "5": []}
    densities = np.arange(0, 1 + delta, delta)

    for max_velocity in flow_rates.keys():
        for density in densities:
            curr_values = []
            for _ in range(0, steps + 1):
                model = NSModel(prob=0.5,
                                n_lanes=1,
                                lane_len=lane_len,
                                max_velocity=int(max_velocity),
                                lane_density=density,
                                lane_changes=False)
                for _ in range(0, lane_len):
                    model.simulate()
                curr_values.append(model.flow_count / lane_len)
            flow_rates[max_velocity].append(np.average(curr_values))

    for max_velocity in flow_rates.keys():
        plt.plot(densities,
                 flow_rates[max_velocity],
                 label=f"Max Velocity={max_velocity}")

    plt_helper("Flow Rate vs. Density", "Density", "Flow Rate", True)


def cars_per_site(steps=200, lane_len=200):
    model = NSModel(prob=0.5,
                    n_lanes=1,
                    lane_len=lane_len,
                    max_velocity=5,
                    lane_density=0.5,
                    lane_changes=False)

    values = []
    for _ in range(0, steps + 1):
        curr_values = []
        model.simulate()
        for v in model.highway[0]:
            curr_values.append(v)
        values.append(curr_values)

    plt.imshow(values, cmap="Blues", interpolation="nearest")
    plt_helper("Cars per Site", "Site", "Step", True)


def validation():
    with PoolExecutor(max_workers=2) as executor:
        executor.submit(velocity_to_density())
        executor.submit(flow_rate_to_density())
        executor.submit(cars_per_site())


if __name__ == "__main__":
    import time

    start = time.time()
    validation()
    end = time.time()

    print(end - start)
