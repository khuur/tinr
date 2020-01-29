import os
import time

import pygame
from Astar import *
from functions import *
from math import sqrt


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
        self.moving = 0
        self.distance = 0  # Kok stran od cilja j e
        self.name = name  # Kako je temu unitu bolj natančno ime
        self.screen = screen  # kam sploh rišeš
        self.image = pygame.image.load(image_path)  # prvi sprite
        self.image = pygame.transform.scale(self.image, (50, 50))  # prvi sprite
        self.image_selected = pygame.image.load(image_path)  # prvi sprite

        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.level = 1

        self.center_x = self.x + (self.rect[2] // 2)  # Center tega unita
        self.center_y = self.y + (self.rect[3] // 2)

        self.w = self.rect[2]
        self.h = self.rect[3]
        self.r = sqrt(self.w ** 2 + self.h ** 2)

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

        self.next_moves = []
        self.move_times = 0
        self.sound_enabled = 0

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
        print("move_times : ", self.move_times)
        print("destination : ", self.direction_x)
        print("destination : ", self.direction_y)
        print("moving : ", self.moving)
        time.sleep(0.3)
        print("\n")

    def scalePicture(self, scale):
        self.image = pygame.transform.rotozoom(self.image, 0, scale)
        self.rect = self.image.get_rect()
        self.updateCenter()
        self.r = (self.rect[2] // 2 + self.rect[3] // 2) // 2  # Radij tega unita

    def updateCenter(self):
        self.w = self.rect[2]
        self.h = self.rect[3]
        self.center_x = self.x + (self.w // 2)
        self.center_y = self.y + (self.h // 2)
        self.r = sqrt(self.w ** 2 + self.h ** 2)

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

    def goTo(self, all_static_objects, quadTree):
        """
        Ta funkcija premakne ta unit tja kamor je namenjen (direction_x, y)
        :return: razdaljo od cilja
        """

        a_se_zabijam_v_koga = []

        if self.moveable == 0:  # Če je prišlo do "napake" in želim prestaviti objekt, ki je statičen
            return -1

        if self.moving == 0: # Če sem mu nekje diseable-u move
            self.next_moves = [] # Nimaš kam naprej za hodit
            self.distance = sqrt((self.direction_x - self.center_x) ** 2 + (self.direction_y - self.center_y) ** 2) # Povej kolk stran si
            return self.distance # in to vrni

        # Če nimam naslednjih move-ov, pomeni, da jih morm nekak dobit
        if not self.next_moves:
            # Najprej zračunam kok stran sploh sm
            self.distance = sqrt((self.direction_x - self.center_x) ** 2 + (self.direction_y - self.center_y) ** 2)

            if self.distance < 10:
                self.moving = 0
                self.next_moves = []
                return self.distance

            if self.moving == 1:
                print("iscem nove komande kam morem it")
                mreza = nafiliMrezo(all_static_objects, (self.x, self.y), (self.direction_x, self.direction_y))

                for vrstica in mreza:
                    for celica in vrstica:
                        print(celica, end=" ")
                    print("")
                os.system('powershell.exe python a_star.py')
                self.fromCoordinatesGetDirections()
                return self.distance
            else:
                # Če se ne premikam pomeni, da morem vn iz te metode
                return self.distance
        else:
            if len(self.next_moves) < 3:
                self.next_moves = []
                self.moving = 0
                return self.distance
            rect = Rectangle(self.x, self.y, self.w, self.h)
            vse_tocke_v_mojem_obmocju = quadTree.query(rect)

            print(vse_tocke_v_mojem_obmocju)

            for object in all_static_objects:

                a_sm_se_zabil = collisionDetection(self, object)
                if a_sm_se_zabil:
                    if self.player != object.player:
                        # pomen, da sm se zabil v nasprotnika
                        self.fight(object)
                    # torej sem najdu v koga se zabijam
                    # torej morm pogruntat kam se morm umaknt
                a_se_zabijam_v_koga.append(a_sm_se_zabil)

            if any(a_se_zabijam_v_koga):
                return self.distance

            kam = self.next_moves[0]
            self.speed = 10
            time.sleep(0.05)
            self.move(kam)
            self.next_moves = self.next_moves[1:]
            self.updateCenter()
            self.distance = sqrt((self.direction_x - self.center_x) ** 2 + (self.direction_y - self.center_y) ** 2)
            return self.distance

    def setDestination(self, dest_x, dest_y):

        self.moving = 1
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
            # print("enga sm užgau")
            self.hp -= object.attack
            object.hp -= self.attack
            self.last_attack = time.time()
            object.last_attack = time.time()
            if self.sound_enabled:
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
        if self.sound_enabled:
            crash_sound = pygame.mixer.Sound("./data/secosmic_lo.wav")
            pygame.mixer.Sound.play(crash_sound)

        #f.addPoints(self.player, int(self.exp))

    def fromCoordinatesGetDirections(self):

        file = open("path.txt", "r")
        coordinates = file.readline()

        coordinates = coordinates[2:-2].split("), (")
        # print("\n\n\n")
        # print(coordinates)

        for terka1, terka2 in zip(coordinates, coordinates[1:]):
            x1, y1 = terka1.split(", ")
            x2, y2 = terka2.split(", ")

            if x1 == x2:
                if y1 < y2:
                    self.next_moves.append("right")
                else:
                    self.next_moves.append("left")
            else:
                if x1 < x2:
                    self.next_moves.append("down")
                else:
                    self.next_moves.append("up")

        # print(self.next_moves)
        # print("\n\n\n")


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
        self.moveable = 1

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
        self.moveable = 1

    def levelUp(self):
        self.max_hp = self.max_hp * 2
        self.attack *= 1.5
        self.hp = self.max_hp
        self.range *= 1.1
        self.scalePicture(1.2)
        self.level += 1

class Boss(Unit):
    def __init__(self, screen, x, y, image_path, name, player):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name, player)
        self.moveable = 0
        self.hp = 200
        self.max_hp = 200
        self.attack = 10
        self.range = 20
        self.cost = 70
        self.reload_time = 1.5
        self.moveable = 1
        self.scalePicture(3)

    def levelUp(self):
        pass

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
        self.moveable = 1

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

class Goldmine(Unit):

    def __init__(self, screen, x, y, image_path, name, player):
        """Initialize the soldier and set its starting position."""
        super().__init__(screen, x, y, image_path, name, player)
        self.setHp(500)
        self.moveable = 0

class Player:

    def __init__(self, name, screen):
        self.name = name
        self.army = []
        self.buildings = []
        self.screen = screen
        self.gold = 30000
        self.gold_per_second = 1
        self.got_gold = time.time()
        self.number_of_soldiers = 0
        self.number_of_archers = 0
        self.number_of_tanks = 0
        self.number_of_goldmines = 0
        self.number_of_bosses = 0
        self.number_of_houses = 0

        self.population = 0
        self.max_population = 5

        self.last_soldier_added = time.time()
        self.soldier_spawn_rate = 0.4

        self.last_archer_added = time.time()
        self.archer_spawn_rate = 0.4

        self.last_tank_added = time.time()
        self.tank_spawn_rate = 0.4

        self.last_goldmine_added = time.time()
        self.goldmine_spawn_rate = 1

        self.last_house_added = time.time()
        self.house_spawn_rate = 1

        self.experience = 0
        self.sound_enabled = 0

    def addSoldier(self):
        if time.time() - self.last_soldier_added > self.soldier_spawn_rate and (self.gold - 50) > 0 and self.population < self.max_population:
            soldier = Soldier(self.screen, 200 + len(self.army) * 30, 300 + len(self.army) * 30,
                              './data/player1/soldier.png', 'Soldier' + str(len(self.army)),
                              self.name)
            self.army.append(soldier)
            self.last_soldier_added = time.time()
            self.gold -= 50
            crash_sound = pygame.mixer.Sound("./data/whiff.wav")
            if self.sound_enabled:
                pygame.mixer.Sound.play(crash_sound)
            self.number_of_soldiers += 1
            self.population += 1
            return soldier

        return 0

    def addArcher(self):
        if time.time() - self.last_soldier_added > self.archer_spawn_rate and (self.gold - 70) > 0 and self.population < self.max_population:
            soldier = Archer(self.screen, 200 + len(self.army) * 30, 300 + len(self.army) * 30,
                             './data/player1/archer.png', 'Archer' + str(len(self.army)),
                             self.name)
            self.army.append(soldier)
            self.last_soldier_added = time.time()
            self.gold -= 70
            if self.sound_enabled:
                crash_sound = pygame.mixer.Sound("./data/whiff.wav")
                pygame.mixer.Sound.play(crash_sound)
            self.number_of_archers += 1
            return soldier
        return 0

    def addTank(self):
        if time.time() - self.last_soldier_added > self.tank_spawn_rate and (self.gold - 200) > 0 and self.population < self.max_population:
            soldier = Tank(self.screen, 200 + len(self.army) * 30, 300 + len(self.army) * 30,
                           './data/player1/tank.png', 'Tank' + str(len(self.army)),
                           self.name)
            self.army.append(soldier)
            self.last_soldier_added = time.time()
            self.gold -= 200
            self.number_of_tanks += 1
            self.population += 1
            return soldier
        return 0

    def addBoss(self, screen, x, y, hp, image_path):
        boss = Boss(screen, x, y, image_path, "BOSS", "Enemy")
        boss.setHp(hp)
        self.army.append(boss)
        if self.sound_enabled:
            crash_sound = pygame.mixer.Sound("./data/whiff.wav")
            pygame.mixer.Sound.play(crash_sound)
        self.number_of_bosses += 1
        return boss

    def addGoldmine(self):
        if time.time() - self.last_goldmine_added > 20 and (self.gold - 200) > 0:

            x = [200, 260, 715]
            y = [620, 240, 425]

            goldmine = Goldmine(self.screen, x[self.number_of_goldmines], y[self.number_of_goldmines],
                             './data/goldmine.png', 'Goldmine' + str(self.number_of_goldmines), self.name)
            goldmine.scalePicture(2)
            self.buildings.append(goldmine)
            self.last_goldmine_added = time.time()
            self.gold -= 200
            if self.sound_enabled:
                crash_sound = pygame.mixer.Sound("./data/whiff.wav")
                pygame.mixer.Sound.play(crash_sound)
            self.number_of_goldmines += 1
            self.gold_per_second += 3
            return goldmine
        return 0

    def addHouse(self, x, y):
        if time.time() - self.last_house_added > 10 and (self.gold - 500) > 0:

            house = House(self.screen, x-50, y-50,
                             './data/house.png', 'House' + str(self.number_of_houses), self.name)
            house.scalePicture(2)
            self.buildings.append(house)
            self.last_house_added = time.time()
            self.gold -= 500
            if self.sound_enabled:
                crash_sound = pygame.mixer.Sound("./data/whiff.wav")
                pygame.mixer.Sound.play(crash_sound)
            self.number_of_houses += 1
            self.max_population += 5
            return house
        return 0



    def changeSoundSettings(self, sound_enabled):
        self.sound_enabled = sound_enabled
        for x in self.army:
            x.sound_enabled = sound_enabled

