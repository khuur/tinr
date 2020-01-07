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


def nafiliMrezo(all_static_objects, start, end):
    w, h = 1300, 800
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
                if not objekt.selected: # Da ne jebe samga sebe
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
    file = open("highscore.txt", "r")

    return_best = []
    highscores = []
    for line in file:
        ime, score = line.split("%%")  # Prebere vsako vrstico v file-u
        terka = (score, ime)  # In ju zapiše v terko
        highscores.append(terka)  # Ki ju nato appenda v seznam
    file.close()
    highscores = sorted(highscores, reverse=True)  # Da ga lahko na tej točki sortam

    for i in range(3):  # best 3 highscores
        score, name = highscores[i]  # unpack from (320, 'Kristjan')
        return_best.append(
            "{0}. {1} - {2}".format(str(i + 1), str(name), str(score)))  # and append as '1. Krisjan - 320'
    return return_best


def highscoreToTxt(players):
    file = open("highscore.txt", "a")  # a stands for append

    for player in players:
        tocke = 0
        for unit in player.army:
            tocke += unit.exp

        file.write(str(player.player) + "%%" + str(tocke) + "\n")
    file.close()
