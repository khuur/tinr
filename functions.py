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
    print("nafiliMrezo()")
    print(start)
    print(end)

    w, h = 1300, 800
    mreza = [[4 for x in range(w)] for y in range(h)]

    """
             3. vrstica
            10. stolpec
        mreza[3][10] = 122
        for i in range(h):
            for j in range(w):
                print(mreza[i][j], end = "")
            print("\n") 
            
            
        LEGENDA :     
        
         4 == path
        
        -1 == zid
        -2 == end
        -3 == start
         
                 
    """

    for objekt in all_static_objects:
        x1 = objekt.x
        y1 = objekt.y
        x2 = objekt.x + objekt.w
        y2 = objekt.y + objekt.h

        for i in range(int(y1), int(y2)):
            for j in range(int(x1), int(x2)):
                if objekt.selected == 0:
                    mreza[i][j] = -1

        # print("Sem dodal objekt : " + objekt.name)

    # print(start)
    # print(end)

    for i in range(int(end[1]) - 10, int(end[1]) + 10):
        for j in range(int(end[0]) - 10, int(end[0]) + 10):
            mreza[i][j] = -2

    for i in range(int(start[1]) - 10, int(start[1]) + 10):
        for j in range(int(start[0]) - 10, int(start[0]) + 10):
            mreza[i][j] = -3

    file = open("lab.txt", "w")

    zacetek = "-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1"

    file.write(zacetek + "\n")

    for i in range(0, h, 20):
        vrstica = "-1,"
        for j in range(0, w, 20):
            vrstica = vrstica + str(mreza[i][j]) + ","
        file.write(vrstica + "-1\n")

    file.write(zacetek + "\n")
    file.close()

    return mreza


def bestHighscores():
    file = open("highscore.txt", "r")

    return_best = []

    highscores = []

    for line in file:
        ime, score = line.split("%%")
        picka = (score, ime)
        highscores.append(picka)

    file.close()

    highscores = sorted(highscores, reverse=True)

    for i in range(3):
        score, name = highscores[i]
        return_best.append("{0}. {1} - {2}".format(str(i + 1), str(name), str(score)))

    return return_best


def highscoreToTxt(players):
    file = open("highscore.txt", "a")

    for player in players:
        tocke = 0
        for unit in player.army:
            tocke += unit.experience

        file.write(str(player.player) + "%%" + str(tocke) + "\n")

    file.close()
