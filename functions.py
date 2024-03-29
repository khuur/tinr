import pygame
import os
from math import sqrt
import units
from functions import *
import requests
import time

points = {}


def euclideanDistance(object1, object2):
    return sqrt((object2.x - object1.x) ** 2 + (object2.y - object1.y) ** 2)


def getImage(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def collisionDetection1(object1, object2):
    if (str(object1.player)) == (str(object2.player)):
        return False

    sum_r = object1.r + object2.r  # Sum of both radius
    distance = euclideanDistance(object1, object2)  # Actual distance between objects

    # if radius is larger than acutal distance, means that they are colideing
    return sum_r > distance


def collisionDetection(object1, object2):
    # :return TRUE IF they are coliding
    if (str(object1.player)) == (str(object2.player)):
        return False

    sum_r = (object1.r + object2.r) * (object1.r + object2.r)
    distance = (object2.x - object1.x) ** 2 + (object2.y - object1.y) ** 2

    if sum_r > distance:
        return True
    return False


def nafiliMrezo(all_static_objects, start, end):
    w, h = 1300, 750
    # Mreza bo velikosti 130 x 80
    mreza = [[4 for x in range(0, w // 10)] for y in range(0, h // 10)]

    """
             3. vrstica
            10. stolpec
        mreza[3][10] = 122
        LEGENDA :     
         4 == path
        
        -1 == zid
        -2 == end
        -3 == startwher                
    """

    for objekt in all_static_objects:
        x1 = int(objekt.x) // 10  # Da dobim iz 523 => 52
        y1 = int(objekt.y) // 10
        x2 = int(objekt.x + objekt.w) // 10
        y2 = int(objekt.y + objekt.h) // 10

        for i in range(y1, y2):
            for j in range(x1, x2):
                if not objekt.selected and objekt.moveable == 0:  # Da ne jebe samga sebe
                    mreza[i][j] = -1

    start_x = start[0] // 10
    start_y = start[1] // 10
    end_x = end[0] // 10
    end_y = end[1] // 10

    # Tole je pomoje narobe, ampak na tak način dela, tko da bom pustu tko kt je
    mreza[end_y][end_x] = -2
    mreza[start_y][start_x] = -3

    file = open("lab.txt", "w")

    zacetek = "-1," * (w // 10 + 2)

    file.write(zacetek[:-1] + "\n")

    for i in range(0, h // 10):
        vrstica = "-1,"
        for j in range(0, w // 10):
            vrstica = vrstica + str(mreza[i][j]) + ","
        file.write(vrstica + "-1\n")

    file.write(zacetek[:-1] + "\n")
    file.close()

    return mreza


def bestHighscores():
    """
    This function returns best 3 highscores
    :return: ['1. Krisjan - 320', '2. Janez - 120', '3. Miha - 110']
    """

    URL = "http://173.212.198.11:3000/test/highscores"

    r = requests.get(url=URL)
    return_best = []

    data = r.json()
    for i, player in enumerate(data["message"]):
        return_best.append(
            "{0}. {1} - {2}".format(str(i + 1), str(player["name"]),
                                    str(player["score"])))  # and append as '1. Krisjan - 320'
    return return_best


def highscoreToTxt(player):
    URL = "http://173.212.198.11:3000/test/addHighscore"

    tocke = 0
    for unit in player.army:
        tocke += unit.exp * 100

    PARAMS = {'name': str(player.name), 'score': int(tocke)}

    # sending get request and saving the response as response object
    r = requests.post(url=URL, params=PARAMS)


def highscoreToDatabase(player_name):

    URL = "http://173.212.198.11:3000/test/addHighscore/" + player_name + "&" + str(points[player_name])

    requests.get(url=URL)

def setPoints(player):
    points[player] = 0

def addPoints(player, point):
    points[player] += int(point)


class Point:
    def __init__(self, x, y, r, unit):
        self.x = x
        self.y = y
        self.r = r
        self.highlight = False
        self.unit = unit

    def intersects(self, other):
        return euclideanDistance(self, other) < (self.r + other.r)

    def setHighlight(self, what):
        self.highlight = what

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersects(self, range):
        return not (
                range.x - range.w > self.x + self.w or
                range.x + range.w < self.x - self.w or
                range.y - range.h > self.y + self.h or
                range.y + range.h < self.y - self.h
        )

    def contains(self, point):
        return (self.x - self.w < point.x < self.x + self.w and
                self.y - self.h < point.y < self.y + self.h)

class QuadTree:
    def __init__(self, rect, capacity):
        self.boundary = rect
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):

        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(x + w / 2, y - h / 2, w / 2, h / 2)
        self.northeast = QuadTree(ne, self.capacity)

        nw = Rectangle(x - w / 2, y - h / 2, w / 2, h / 2)
        self.northwest = QuadTree(nw, self.capacity)

        se = Rectangle(x + w / 2, y + h / 2, w / 2, h / 2)
        self.southeast = QuadTree(se, self.capacity)

        sw = Rectangle(x - w / 2, y + h / 2, w / 2, h / 2)
        self.southwest = QuadTree(sw, self.capacity)

        self.divided = True

    def insert(self, point):

        if not self.boundary.contains(point):
            return

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            self.subdivide()

        inserted = [False]

        if not any(inserted):
            inserted.append(self.northeast.insert(point))
            return True

        if not any(inserted):
            inserted.append(self.northwest.insert(point))
            return True

        if not any(inserted):
            inserted.append(self.southeast.insert(point))
            return True

        if not any(inserted):
            inserted.append(self.southwest.insert(point))
            return True

    def query(self, range):

        found = []

        if not self.boundary.intersects(range):
            return found

        for point in self.points:
            if range.contains(point):
                found.append(point)

        if self.divided:
            for point in self.northwest.query(range):
                found.append(point)
            for point in self.northeast.query(range):
                found.append(point)

            for point in self.southwest.query(range):
                found.append(point)
            for point in self.southeast.query(range):
                found.append(point)

        return found
