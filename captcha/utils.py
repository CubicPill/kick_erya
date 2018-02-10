from PIL import Image
import random
import math
from copy import deepcopy
import hashlib

DIST_INF = 442  # distance from (0,0,0) to (255,255,255), rounded up


def calc_distance(color1: list or tuple, color2: list or tuple) -> float:
    """
    calculate distance between colors (r,g,b) using Euclidean distance
    :param color1:
    :param color2:
    :return:
    """
    return math.sqrt(sum([(c[0] - c[1]) ** 2 for c in zip(color1, color2)]))


def calc_center(cluster: list) -> tuple:
    return tuple([int(sum(c) / len(cluster)) for c in zip(*cluster)])


def merge_seeds(seeds: list):
    """
    merge the closest seeds into one (taking their average)
    :param seeds:
    :return: new seed set
    """
    seeds = deepcopy(seeds)
    min_dist, min_pair = DIST_INF, None
    for i in range(len(seeds)):
        for j in range(i + 1, len(seeds)):
            distance = calc_distance(seeds[i], seeds[j])
            if distance < min_dist:
                min_dist = distance
                min_pair = [seeds[i], seeds[j]]
    seeds.remove(min_pair[0])
    seeds.remove(min_pair[1])
    seeds.append((int((min_pair[0][0] + min_pair[1][0]) / 2),
                  int((min_pair[0][1] + min_pair[1][1]) / 2),
                  int((min_pair[0][2] + min_pair[1][2]) / 2)))
    return seeds


def pick_color(color: tuple, seeds: list) -> tuple:
    min_dist, chosen_seed = DIST_INF, None
    for s in seeds:
        distance = calc_distance(color, s)
        if distance < min_dist:
            min_dist = distance
            chosen_seed = s
    return tuple(deepcopy(chosen_seed))


def split_image(image: Image.Image):
    """
    split digits using k-means in RGB color space
    :param image: PIL.Image.Image instance
    :return:
    """
    image_data = list(image.getdata())
    colors = list(set(image_data))
    seeds = random.choices(colors, k=int(len(colors) * 0.02) if len(colors) >= 100 else 10)
    # randomly choose 2% of the colors as seed (at least 10)
    while len(seeds) > 5:
        old_seeds = None
        while old_seeds != seeds:
            # repeat calculation until stable
            old_seeds = deepcopy(seeds)
            clusters = [list() for i in range(len(seeds))]
            for c in colors:
                min_dist, seed_index = DIST_INF, None
                for i, s in enumerate(seeds):
                    distance = calc_distance(s, c)
                    if distance < min_dist:
                        min_dist = distance
                        seed_index = i
                clusters[seed_index].append(c)
            seeds = [calc_center(cluster) for cluster in clusters if cluster]
        seeds = merge_seeds(seeds)
    new_image_data = [pick_color(d, seeds) for d in image_data]
    new_image = Image.new('RGB', (123, 40), 255)
    new_image.putdata(new_image_data)
    new_image.save('out.bmp')


