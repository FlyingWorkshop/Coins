import statistics as stats

import numpy as np

import utils


def simulate_1():
    num_trials = 100  # specifies the num trials per unique coin_radius and num_points
    print(f"{num_trials=} (per each unique combination of coin_radius and num_points)")
    max_points = 15
    for coin_radius in np.arange(0.1, 1, 0.1):
        print(f"\t{coin_radius=}")
        for num_points in range(max_points):
            print(f"\t\t{num_points=}")
            valid_list = []
            loops_list = []
            for _ in range(num_trials):
                points = utils.make_n_random_points(num_points)
                coins, valid, loops = utils.find_hexagonal_packing(points, coin_radius=coin_radius)
                valid_list.append(valid)
                loops_list.append(loops)

            print(f"\t\t\t{stats.fmean(loops_list)=}\n" +
                  f"\t\t\t{stats.fmean(valid_list)=}")


def main():
    num_trials = 1000  # specifies the num trials per unique coin_radius and num_points
    print(f"{num_trials=} (per each unique combination of coin_radius and num_points)")
    num_points_list = [10, 20, 30, 40, 50, 100]
    for coin_radius in np.arange(0.1, 1 + 0.1, 0.1):
        print(f"\t{coin_radius=}")
        for num_points in num_points_list:
            print(f"\t\t{num_points=}")
            valid_list = []
            loops_list = []
            for _ in range(num_trials):
                points = utils.make_n_random_points(num_points)
                coins, valid, loops = utils.find_hexagonal_packing(points, coin_radius=coin_radius)
                valid_list.append(valid)
                loops_list.append(loops)

            print(f"\t\t\t{stats.fmean(loops_list)=}\n" +
                  f"\t\t\t{stats.fmean(valid_list)=}")


if __name__ == "__main__":
    main()
