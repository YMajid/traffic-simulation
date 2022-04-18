from src.zipper import Zipper
from src.validation import validation
from src.model import NSModel

if __name__ == "__main__":
    # model = NSModel(lane_changes=True)
    # model.simulate()
    # model.simulate()
    # model.simulate()
    zipper = Zipper(n_lanes=3, lane_density=0.1)
    for _ in range(20):
        print(zipper.highway_velocity())
        print(zipper.highway)
        zipper.simulate()

    # import time

    # start = time.time()
    # validation()
    # end = time.time()
