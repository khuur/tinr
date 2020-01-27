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

def collisionDetection(object1, object2):
    if (str(object1.player)) == (str(object2.player)):
        return False

    sum_r = object1.r + object2.r  # Sum of both radius
    distance = euclideanDistance(object1, object2)   # Actual distance between objects

    # if radius is larger than acutal distance, means that they are colideing
    return sum_r > distance

def nafiliMrezo(all_static_objects, start, end, changed = 0):
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
            "{0}. {1} - {2}".format(str(i + 1), str(player["name"]), str(player["score"])))  # and append as '1. Krisjan - 320'
    return return_best


def highscoreToTxt(player):

    URL = "http://173.212.198.11:3000/test/addHighscore"

    tocke = 0
    for unit in player.army:
        tocke += unit.exp * 100

    PARAMS = {'name': str(player.name), 'score': int(tocke)}

    # sending get request and saving the response as response object
    r = requests.post(url=URL, params=PARAMS)

def highscoreToDatabase():





    # extracting data in json format
    data = r.json()

def setPoints(player):
    points[player] = 0

def addPoints(player, points):
    points[player] += int(points)
