import pygame
import os
from math import sqrt
import units
from functions import *
import time
from datetime import datetime

class Unit:
    speed: float

    def __init__(self, screen, x, y, image_path, name, player):
        self.x = x  # kje na screenu sploh je
        self.y = y
        self.player = player
        self.speed = 1.5  # njegova hitrost
        self.direction_x = 0  # kam more it
        self.direction_y = 0
        self.selected = 0  # a je ta unit selectan?
        self.moveable = 0  # a se sploh lahko premika?
        self.moving = True
        self.distance = 0  # Kok stran od cilja j e
        self.name = name  # Kako je temu unitu bolj natančno ime
        self.screen = screen  # kam sploh rišeš
        self.image = pygame.image.load(image_path)  # prvi sprite
        self.image = pygame.transform.scale(self.image,( 50, 50))  # prvi sprite
        self.image_selected = pygame.image.load(image_path)  # prvi sprite

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.level = 1

        self.center_x = self.x + (self.rect[2] // 2)  # Center tega unita
        self.center_y = self.y + (self.rect[3] // 2)

        self.w = self.rect[2]
        self.h = self.rect[3]

        self.r = (self.rect[2] // 2 + self.rect[3] // 2) // 2  # Radij tega unita

        self.cost = 0

        self.max_hp = 30
        self.hp = self.max_hp
        self.attack = 5
        self.range = 10
        self.exp = 0
        self.exp_worth = 10
        self.next_level = 15

        self.dead = False
        self.last_attack = time.time()

    def print(self):
        print("Player: ", self.player)
        print("Name: ", self.name)
        print("X : ", self.x)
        print("Y : ", self.y)
        print("W : ", self.rect[2])
        print("H : ", self.rect[3])
        print("R : ", self.r)
        print("hp : {} / {}".format(self.hp, self.max_hp))
        print("exp : {} / {}".format(self.exp, self.next_level))
        print("attack : {} ".format(self.attack))
        print("dead : ", self.dead)
        print("SELECTED : ", self.selected)
        time.sleep(0.3)
        print("\n")

    def scalePicture(self, scale):

        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.updateCenter()
        self.r = (self.rect[2] // 2 + self.rect[3] // 2) // 2  # Radij tega unita


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

    def goTo(self, all_static_objects):
        """
        Ta funkcija premakne ta unit tja kamor je namenjen (direction_x, y)
        :return: razdaljo od cilja
        """

        self.moving = True
        self.distance = sqrt((self.direction_x - self.center_x) ** 2 + (self.direction_y - self.center_y) ** 2)

        a_se_zabijam_v_koga = []

        for object in all_static_objects:

            a_sm_se_zabil = collisionDetection(self, object)
            if a_sm_se_zabil:
                if self.player != object.player:
                    # pomen, da sm se zabil v nasprotnika
                    self.fight(object)
                # torej sem najdu v koga se zabijam
                # torej morm pogruntat kam se morm umaknt
                if object.x < self.x:
                    self.x += 5
                else:
                    self.x -= 5

                if object.y < self.y:
                    self.y += 5
                else:
                    self.y -= 5

                self.updateCenter()

            a_se_zabijam_v_koga.append(a_sm_se_zabil)

        if any(a_se_zabijam_v_koga):
            #print("zabiu sm se v nekoga")
            return self.distance

        if self.distance < 10:
            self.moving = False
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

    def getExp(self, exp):
        self.exp += exp
        if self.exp >= self.next_level:
            self.next_level *= 2.5
            self.levelUp()

    def fight(self, object):

        if time.time() - self.last_attack > self.reload_time:
            #print("enga sm užgau")
            self.hp -= object.attack
            object.hp -= self.attack
            self.last_attack = time.time()
            object.last_attack = time.time()

            crash_sound = pygame.mixer.Sound("./data/punch.wav")
            pygame.mixer.Sound.play(crash_sound)


            if self.hp <= 0:
                self.die()
                object.getExp(self.exp_worth)

            if object.hp <= 0:
                object.die()
                self.getExp(object.exp_worth)

    def die(self):
        self.dead = True
        print("I died in battle for Azeroth!")
        crash_sound = pygame.mixer.Sound("./data/secosmic_lo.wav")
        pygame.mixer.Sound.play(crash_sound)


class Soldier(Unit):
    def __init__(self, screen, x, y, image_path, name, player):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name, player)
        self.moveable = 1
        self.hp = 20
        self.max_hp = 20
        self.attack = 10
        self.range = 15
        self.cost = 50
        self.reload_time = 1

    def levelUp(self):
        self.max_hp = self.max_hp * 2
        self.attack *= 1.2
        self.hp = self.max_hp
        self.scalePicture(1.2)
        self.level += 1


class Archer(Unit):
    def __init__(self, screen, x, y, image_path, name, player):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name, player)
        self.moveable = 1
        self.hp = 20
        self.max_hp = 20
        self.attack = 10
        self.range = 50
        self.cost = 70
        self.reload_time = 1.5

    def levelUp(self):
        self.max_hp = self.max_hp * 2
        self.attack *= 1.5
        self.hp = self.max_hp
        self.range *= 1.1
        self.scalePicture(1.2)
        self.level += 1


class Tank(Unit):
    def __init__(self, screen, x, y, image_path, name, player):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name, player)
        self.moveable = 1
        self.hp = 300
        self.speed = 0.5
        self.attack = 20
        self.range = 70
        self.cost = 200
        self.reload_time = 3

    def levelUp(self):
        self.max_hp = self.max_hp * 2
        self.attack *= 1.8
        self.hp = self.max_hp
        self.scalePicture(1.2)
        self.level += 1

class House(Unit):

    def __init__(self, screen, x, y, image_path, name, player):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name, player)
        self.setHp(500)


class Player:

    def __init__(self, player, screen):
        self.player = player
        self.army = []
        self.buildings = []
        self.screen = screen
        self.gold = 30000
        self.number_of_soldiers = 0
        self.number_of_archers  = 0
        self.number_of_tanks    = 0

        self.last_soldier_added = time.time()
        self.soldier_spawn_rate = 3

        self.last_archer_added = time.time()
        self.archer_spawn_rate = 2

        self.last_tank_added = time.time()
        self.tank_spawn_rate = 5

    def addSoldier(self):
        if time.time() - self.last_soldier_added > self.soldier_spawn_rate and (self.gold - 50) > 0:
            soldier = Soldier(self.screen, 300 + len(self.army) * 30, 300 + len(self.army) * 30,
                              './data/' + str(self.player) + '/soldier.png', 'Soldier' + str(len(self.army)), self.player)
            self.army.append(soldier)
            self.last_soldier_added = time.time()
            self.gold -= 50
            crash_sound = pygame.mixer.Sound("./data/whiff.wav")
            pygame.mixer.Sound.play(crash_sound)
            self.number_of_soldiers += 1
            return soldier

        return 0

    def addArcher(self):
        if time.time() - self.last_soldier_added > self.archer_spawn_rate and (self.gold - 70) > 0:
            soldier = Archer(self.screen, 300 + len(self.army) * 30, 300 + len(self.army) * 30,
                              './data/' + str(self.player) + '/archer.png', 'Archer' + str(len(self.army)),
                              self.player)
            self.army.append(soldier)
            self.last_soldier_added = time.time()
            self.gold -= 70
            crash_sound = pygame.mixer.Sound("./data/whiff.wav")
            pygame.mixer.Sound.play(crash_sound)
            self.number_of_archers += 1
            return soldier
        return 0

    def addTank(self):
        if time.time() - self.last_soldier_added > self.tank_spawn_rate and (self.gold - 200) > 0:
            soldier = Tank(self.screen, 300 + len(self.army) * 30, 300 + len(self.army) * 30,
                              './data/' + str(self.player) + '/tank.png', 'Tank' + str(len(self.army)),
                              self.player)
            self.army.append(soldier)
            self.last_soldier_added = time.time()
            self.gold -= 200
            self.number_of_tanks += 1
            return soldier
        return 0

