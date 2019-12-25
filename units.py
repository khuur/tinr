import pygame
import os
from math import sqrt
import units
from functions import *
import time


class Unit:
    speed: float

    def __init__(self, screen, x, y, image_path, name):
        self.x = x
        self.y = y
        self.speed = 0.4
        self.direction_x = 0
        self.direction_y = 0
        self.selected = 0
        self.moveable = 0
        self.distance = 0
        self.name = name
        self.screen = screen  # kam sploh rišeš
        self.image = pygame.image.load(image_path)  # prvi sprite
        self.image_selected = pygame.image.load(image_path)  # prvi sprite

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.center_x = self.x + (self.rect[2] // 2)
        self.center_y = self.y + (self.rect[3] // 2)

        self.r = (self.rect[2] // 2 + self.rect[3] // 2) // 2

        # Set a variable for each movement.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def print(self):
        print("Name: ", self.name)
        print("X : ", self.x)
        print("Y : ", self.y)
        print("R : ", self.r)
        print("SELECTED : ", self.selected)
        time.sleep(0.3)
        print("\n")

    def move(self, direction):
        neki = True
        if neki:
            if direction == "up":
                self.y -= self.speed
            elif direction == "down":
                self.y += self.speed
            elif direction == "left":
                self.x -= self.speed
            elif direction == "right":
                self.x += self.speed
        else:
            for object in all_static_objetcts:
                if collisionDetection(self, object, False):
                    print("fak")
                    print(object.name)
                    print(self.x)
                    print(self.y)

            self.x = 730
            self.y = 730

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):

        if self.rect.right <= self.screen_rect.right and self.moving_right:
            self.rect.centerx += 3

        if self.rect.left > 0 and self.moving_left:
            self.rect.centerx -= 3

        if self.rect.top > 0 and self.moving_up:
            self.rect.bottom -= 3

        if self.rect.bottom <= self.screen_rect.bottom and self.moving_down:
            self.rect.bottom += 3

    def changeImage(self, which_one, path):
        if which_one == "main":
            self.image = getImage(path)
        elif which_one == "selected":
            self.image_selected = getImage(path)

    def goTo(self):

        mouse_x = self.direction_x
        mouse_y = self.direction_y

        self.distance = sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)

        if self.distance < 20:
            return None


        if self.x < mouse_x:
            self.move("right")
        else:
            self.move("left")

        if self.y > mouse_y:
            self.move("up")
        else:
            self.move("down")
			
        self.distance = sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)
        return sqrt((mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2)

    def setDestination(self, dest_x, dest_y):
        self.direction_x = dest_x
        self.direction_y = dest_y


class Soldier(Unit):
    def __init__(self, screen, x, y, image_path, name):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name)
        self.moveable = 1


class House(Unit):

    def __init__(self, screen, x, y, image_path, name):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name)


class Corn(Unit):
    def __init__(self, screen, x, y, image_path, name):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name)


class Pikca(Unit):

    def __init__(self, screen, x, y, image_path, name):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name)
        self.moveable = 1

    def move(self, direction):
        neki = True
        for object in all_static_objetcts:
            if collisionDetection(self, object, False):
                neki = False

        if neki:
            if direction == "up":
                self.y -= 3
            elif direction == "down":
                self.y += 3
            elif direction == "left":
                self.x -= 3
            elif direction == "right":
                self.x += 3
        else:
            for object in all_static_objetcts:
                if collisionDetection(self, object, False):
                    print("fak")
                    print(object.name)
                    print(self.x)
                    print(self.y)
                    print(self.selected)

            self.x = 730
            self.y = 730

class Player:

    def __init__(self, player, screen):
        self.player = player
        self.army = []
        self.buildings = []
        self.screen = screen

    def addSoldier(self):
        soldier = Soldier(self.screen, 300 + len(self.army) * 30, 300 + len(self.army) * 30, './data/' + str(self.player) +'/tank.png', 'Soldier' + str(len(self.army)))
        self.army.append(soldier)
        return soldier