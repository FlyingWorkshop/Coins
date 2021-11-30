from __future__ import annotations
from typing import Iterable
import math

from matplotlib.patches import Circle
import numpy as np

BOUNDS = (0.0, 1.0)
DIGITS = 2
RNG = np.random.default_rng()
HEXAGONAL_SQUISH_FACTOR = math.sqrt(3) / 2


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.coords = (self.x, self.y)

    def dist_from(self, target: Point):
        a = self.x - target.x
        b = self.y - target.y
        c = math.sqrt(a**2 + b**2)
        return c

    def covered_by(self, coins: Iterable[Coin]) -> bool:
        return any(coin.covers(self) for coin in coins)

    def __str__(self):
        return str(self.coords)

    def __repr__(self):
        return str(self)


def make_random_point(x_bounds=BOUNDS, y_bounds=BOUNDS, digits=DIGITS) -> Point:
    x = round(RNG.uniform(*x_bounds), digits)
    y = round(RNG.uniform(*y_bounds), digits)
    p = Point(x, y)
    return p


def make_n_random_points(num_points: int, x_bounds=BOUNDS, y_bounds=BOUNDS, digits=DIGITS) -> set[Point]:
    """
    >>> len(make_n_random_points(10))
    10
    """
    assert(num_points >= 0)
    result = set()
    for _ in range(num_points):
        p = make_random_point(x_bounds=x_bounds, y_bounds=y_bounds, digits=digits)
        result.add(p)
    return result


def unzip_coords(points):
    """
    >>> unzip_coords([Point(0, 1), Point(0, 2), Point(0, 3)])
    ([0, 0, 0], [1, 2, 3])
    """
    x_coords = [p.x for p in points]
    y_coords = [p.y for p in points]
    return x_coords, y_coords


class Coin:
    DEFAULT_RADIUS = 0.3

    def __init__(self, center: Point, radius: float):
        assert (radius > 0)
        self.center = center
        self.radius = radius

    def covers(self, target: Point):
        return self.center.dist_from(target) <= self.radius

    def to_matplotlib_circle(self, alpha=0.1, facecolor="silver", edgecolor="black"):
        return Circle(xy=self.center.coords,
                      radius=self.radius,
                      alpha=alpha,  # controls color transparency
                      facecolor=facecolor,
                      edgecolor=edgecolor)


def coins_cover_all_points(coins: Iterable[Coin], points: Iterable[Point]) -> bool:
    for point in points:
        if not any(coin.covers(point) for coin in coins):
            return False
    else:
        return True


def generate_hexagonal_lattice(x_bounds=BOUNDS,
                               y_bounds=BOUNDS,
                               hexagon_radius=2 * Coin.DEFAULT_RADIUS):

    # generate square lattice
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    y_max *= (1 / HEXAGONAL_SQUISH_FACTOR)
    yv, xv = np.mgrid[y_min:y_max:hexagon_radius, x_min:x_max:hexagon_radius]

    # modify the lattice so that each point becomes the center of a regular hexagon in a hexagon tilling
    yv *= HEXAGONAL_SQUISH_FACTOR
    xv[1::2] += hexagon_radius / 2

    # convert into more user-friendly format
    hexagon_centers = []
    for x, y in zip(xv.flatten(), yv.flatten()):
        p = Point(x, y)
        hexagon_centers.append(p)
    return hexagon_centers


def generate_hexagonal_packing(x_bounds=BOUNDS,
                               y_bounds=BOUNDS,
                               overflow_bounds=True,
                               coin_radius=Coin.DEFAULT_RADIUS,
                               x_offset=0.0,
                               y_offset=0.0):
    hexagon_radius = 2 * coin_radius
    if overflow_bounds:
        x_bounds = (x_bounds[0] - coin_radius, x_bounds[1] + coin_radius)
        y_bounds = (y_bounds[0] - coin_radius, y_bounds[1] + coin_radius)
    x_bounds = (x + x_offset for x in x_bounds)
    y_bounds = (y + y_offset for y in y_bounds)
    points = generate_hexagonal_lattice(x_bounds, y_bounds, hexagon_radius)
    coins = [Coin(center=p, radius=coin_radius) for p in points]
    return coins


def find_hexagonal_packing(points: Iterable[Point],
                           x_bounds=BOUNDS,
                           y_bounds=BOUNDS,
                           overflow_bounds=True,
                           coin_radius=Coin.DEFAULT_RADIUS,
                           step_size=0.01,
                           max_loops=None) -> (set[Coin], bool, int):
    offsets = np.arange(0, coin_radius, step_size)
    coins, valid, loops = set(), False, 0
    for x_offset in offsets:
        for y_offset in offsets:
            if max_loops and loops >= max_loops:
                break
            loops += 1
            coins = generate_hexagonal_packing(x_bounds=x_bounds,
                                               y_bounds=y_bounds,
                                               coin_radius=coin_radius,
                                               overflow_bounds=overflow_bounds,
                                               x_offset=x_offset,
                                               y_offset=y_offset)
            if coins_cover_all_points(coins, points):
                valid = True
                break
        else:
            continue
        break
    return coins, valid, loops


