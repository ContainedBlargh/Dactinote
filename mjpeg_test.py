import cv2
from numba.decorators import njit
from numba.special import prange
from numpy.core.fromnumeric import shape
from data_sources import MJPEG
from time import sleep
import numpy as np
from numba import jit, autojit
from sklearn.neighbors.nearest_centroid import NearestCentroid
from math import *
np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

@njit(cache=True, nogil=True)
def unit(vec: np.ndarray):
    return vec / np.linalg.norm(vec)

blue_vector = unit(np.array([0.0, 0.0, 255.0]))

@njit(cache=True, nogil=True)
def angle_to_blue(v: np.ndarray):
    v1_u = blue_vector
    v2_u = unit(v)
    m = np.linalg.det(
        np.stack((v1_u[-2:], v2_u[-2:]))
    )
    if m == 0:
        sign = 1
    else:
        sign = -np.sign(m)
    dot_p = np.dot(v1_u, v2_u)
    dot_p = min(max(dot_p, -1.0), 1.0)
    return sign * np.arccos(dot_p)

close = pi / 8

def find_blues(data: np.ndarray):
    # locate bluest pixels
    blues = []
    for y in prange(data.shape[1]):
        for x in prange(data.shape[2]):
            pixel = data[0, y, x]
            a = angle_to_blue(pixel.astype(float))
            if a <= close:
                blues.append([x, y, a])
    return np.array(blues)

images = []
blue_centers = []

def process_image(data: np.ndarray):
    print(f"data shape: {data.shape}")
    # remove blue components
    # no_blue = data[0, :, :, 0:2]
    
    # locate the triangle

    # find blue center
    blues = find_blues(data)
    local_centers = blues[:, :2].astype(int)
    # print(f"blues shape: {blues.shape}")
    # print(blues)
    # bmin = np.min(blues[:], axis=1)
    # print(f"max b: {np.max(blues[:, 2])}")
    # print(f"min b: {np.min(blues[:, 2])}")
    # blue_center = (int(bmin[0]), int(bmin[1]))
    # print(f"blue center: {blue_center}")
    blue_centers.append(local_centers)
    images.append(data[0])
    pass

ds = MJPEG("http://192.168.1.134:8080/stream/video.mjpeg", max_buffered=1)
ds.set_listener(process_image)

ds.enable()
sleep(5)
ds.disable()

print(len(list(zip(blue_centers, images))))
for i, bc_img in enumerate(zip(blue_centers, images)):
    (bcs, img) = bc_img
    for bc in bcs:
        cv2.circle(img, (bc[1], bc[0]), 2, (255, 255, 255), -1)
    cv2.imwrite(f"./test_images/img{i}.png", img)
