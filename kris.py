import pygame
import os
from math import sqrt
import units
import time

_image_library = {}
# coord_x, coord_y, width, height
all_static_objetcts = []
selected_objects = []
WIDTH = 800
HEIGHT = 800


def collisionDetection(object1, object2, be):
    # Returns True if object ARE IN eachother
    return False
    """
    
"""


def getImage(path):
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


def euclideanDistance(object1, object2):
    x1 = object1.x
    y1 = object1.y
    x2 = object2.x
    y2 = object2.y

    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def updateScreen():
    for object_on_screen in all_static_objetcts:
        if object_on_screen.selected:
            screen.blit(object_on_screen.image_selected, (object_on_screen.x, object_on_screen.y))
        else:
            screen.blit(object_on_screen.image, (object_on_screen.x, object_on_screen.y))



class Player:

    def __init__(self, player, screen):
        self.player = player
        self.army = []
        self.buildings = []
        self.screen = screen

    def addSoldier(self):
        soldier = units.Soldier(self.screen, 300 + len(self.army) * 30, 300 + len(self.army) * 30, './data/' + str(self.player) +'/tank.png', 'Soldier' + str(len(self.army)))
        self.army.append(soldier)
        all_static_objetcts.append(soldier)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
done = False

player1 = Player('player1', screen)
player2 = Player('player2', screen)

player1.addSoldier()

#soldier = Soldier(screen, 500, 500, './data/sword2.png', 'Soldier')
house = House(screen, 300, 300, './data/house.png', 'House')
corn = Corn(screen, 100, 100, './data/corn/idle_0.png', 'Corn')
pikca = Pikca(screen, 700, 100, './data/krogec.png', 'Krogec')

player1.army[0].changeImage("selected", './data/sword2_right.png')
pikca.changeImage("selected", './data/krogec_selected.png')
corn.changeImage("selected", './data/corn/idle_1.png')

all_static_objetcts.append(house)
all_static_objetcts.append(corn)
all_static_objetcts.append(pikca)

mouse_clicks = (0, 0, 0)
mouse_position = (411, 348)

clock = pygame.time.Clock()
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player1.army[0].move("up")
    if pressed[pygame.K_DOWN]:
        player1.army[0].move("down")
    if pressed[pygame.K_LEFT]:
        player1.army[0].move("left")
    if pressed[pygame.K_RIGHT]:
        player1.army[0].move("right")

    if pressed[pygame.K_q]:
        for object in all_static_objetcts:
            object.print()
    if pressed[pygame.K_e]:
        for a, b in zip(all_static_objetcts, all_static_objetcts[1:]):
            print(a)
            print(b)
            if collisionDetection(a, b, True):
                print("neki ni kul")
    if pressed[pygame.K_r]:
        player1.addSoldier()
    if pressed[pygame.K_t]:
        pass

    if pressed[pygame.K_i]:
        player1.army[1].move("up")
    if pressed[pygame.K_k]:
        player1.army[1].move("down")
    if pressed[pygame.K_j]:
        player1.army[1].move("left")
    if pressed[pygame.K_l]:
        player1.army[1].move("right")


    if pressed[pygame.K_w]:
        pikca.move("up")
    if pressed[pygame.K_s]:
        pikca.move("down")
    if pressed[pygame.K_a]:
        pikca.move("left")
    if pressed[pygame.K_d]:
        pikca.move("right")

    if (mouse_clicks != pygame.mouse.get_pressed()):
        # al je nekdo pritisnu na miško al pa spustu knof
        lev, sredn, desn = mouse_clicks
        x1, y1 = mouse_position

        # print("Prej je blo tkole: ", lev, sredn, desn)
        mouse_clicks = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        x2, y2 = mouse_position

        if (lev + desn + sredn > sum(mouse_clicks)):
            """
            print("released")
            print("Rectangle coordinates: ")
            print(x1, y1)
            print(x2, y2)
            """

            print("Kdo je kle notr?")
            for object in all_static_objetcts:
                if x1 < object.x < x2 and y1 < object.y < y2:
                    object.selected = 1
                    object.print()
                    object.setDestination(mouse_position[0], mouse_position[1])
                else:
                    # Zdej si dobu ukaz, da se premakn tja kamor miška zdej kaže
                    if sredn:
                        for selected_object in all_static_objetcts:
                            if selected_object.selected:
                                selected_object.setDestination(mouse_position[0], mouse_position[1])
                                selected_object.goTo()
                    else:
                        # jebiga
                        object.selected = 0

    for selected_object in all_static_objetcts:
        if selected_object.selected:
            #selected_object.setDestination(mouse_position[0], mouse_position[1])
            selected_object.goTo()
    x, y = mouse_position

    lev, sredn, desn = mouse_clicks
    # print("Zdej je pa tko: ", lev, sredn, desn)
    # print("\n")

    # print(pygame.mouse.get_pos())

    """
        if pressed[pygame.K_w]:     pikca.move("up")
        if pressed[pygame.K_s]:     pikca.move("down")
        if pressed[pygame.K_a]:     pikca.move("left")
        if pressed[pygame.K_d]:     pikca.move("right")
        if pressed[pygame.K_SPACE]:
            pikca.print()
            house.print()
            soldier.print()
            corn.print()
    """
    screen.fill((0, 0, 0))
    updateScreen()
    """
    screen.blit(house.image, (house.x, house.y))
    screen.blit(corn.images[corn.stage % 5], (corn.x, corn.y))
    screen.blit(pikca.image, (pikca.x, pikca.y))
    """
    pygame.display.flip()
    clock.tick(60)
