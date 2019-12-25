import pygame
import os
from math import sqrt
import units
from functions import *
import time
from datetime import datetime


class Unit:
    speed: float

    def __init__(self, screen, x, y, image_path, name):
        self.x = x # kje na screenu sploh je
        self.y = y
        self.speed = 1.5 # njegova hitrost
        self.direction_x = 0 # kam more it
        self.direction_y = 0
        self.selected = 0 # a je ta unit selectan?
        self.moveable = 0 # a se sploh lahko premika?
        self.distance = 0 # Kok stran od cilja j e
        self.name = name  # Kako je temu unitu bolj natančno ime
        self.screen = screen  # kam sploh rišeš
        self.image = pygame.image.load(image_path)  # prvi sprite
        self.image_selected = pygame.image.load(image_path)  # prvi sprite

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.center_x = self.x + (self.rect[2] // 2) # Center tega unita
        self.center_y = self.y + (self.rect[3] // 2)

        self.r = (self.rect[2] // 2 + self.rect[3] // 2) // 2 # Radij tega unita

        self.max_hp = 30
        self.hp = self.max_hp
        self.attack = 5

    def print(self):
        print("Name: ", self.name)
        print("X : ", self.x)
        print("Y : ", self.y)
        print("R : ", self.r)
        print("SELECTED : ", self.selected)
        time.sleep(0.3)
        print("\n")

    def updateCenter(self):
        self.center_x = self.x + (self.rect[2] // 2)
        self.center_y = self.y + (self.rect[3] // 2)

    def move(self, direction):

        if direction == "up":
            self.y -= self.speed
        elif direction == "down":
            self.y += self.speed
        elif direction == "left":
            self.x -= self.speed
        elif direction == "right":
            self.x += self.speed

        self.updateCenter()

    def changeImage(self, which_one, path):
        if which_one == "main":
            self.image = getImage(path)
        elif which_one == "selected":
            self.image_selected = getImage(path)

    def goTo(self):
        """
        Ta funkcija premakne ta unit tja kamor je namenjen (direction_x, y)
        :return: razdaljo od cilja
        """
        self.distance = sqrt((self.direction_x - self.center_x) ** 2 + (self.direction_y - self.center_y) ** 2)

        if self.distance < 10:
            return self.distance

        if self.center_x < self.direction_x:
            self.move("right")
        else:
            self.move("left")

        if self.center_y > self.direction_y:
            self.move("up")
        else:
            self.move("down")

        self.distance = sqrt((self.direction_x - self.center_x) ** 2 + (self.direction_y - self.center_y) ** 2)
        return self.distance

    def setDestination(self, dest_x, dest_y):
        self.direction_x = dest_x
        self.direction_y = dest_y

    def setHp(self, hp):
        self.hp = hp

class Soldier(Unit):
    def __init__(self, screen, x, y, image_path, name):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name)
        self.moveable = 1

    def fight(self):
        print("now i'm fighting")
        print("HP : ", self.hp)
        print("Attack : ", self.attack)

    def levelUp(self):
        self.max_hp = self.max_hp * 2
        self.hp = self.max_hp


class House(Unit):

    def __init__(self, screen, x, y, image_path, name):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name)
        self.setHp(500)



class Player:

    def __init__(self, player, screen):
        self.player = player
        self.army = []
        self.buildings = []
        self.screen = screen
        self.last_soldier_added = time.time()

    def addSoldier(self):

        if time.time() - self.last_soldier_added > 3:
            soldier = Soldier(self.screen, 300 + len(self.army) * 30, 300 + len(self.army) * 30,
                              './data/' + str(self.player) + '/tank.png', 'Soldier' + str(len(self.army)))
            self.army.append(soldier)
            self.last_soldier_added = time.time()
            return soldier
        return 0


