import pygame
import os
from math import sqrt
import units
from functions import *
import time


def euclideanDistance(object1, object2):
    return sqrt((object2.x - object1.x) ** 2 + (object2.y - object1.y) ** 2)


def collisionDetection(object1, object2):
    if (str(object1.player) + str(object1.name)) == (str(object2.player) + str(object2.name)):
        return False

    sum_r = object1.r + object2.r  # Sum of both radius
    distance = euclideanDistance(object1, object2)  # Actual distance between objects

    # if radius is larger than acutal distance, means that they are colideing
    return sum_r > distance



def getImage(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image
