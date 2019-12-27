import pygame
import os
from math import sqrt
import units
from functions import *
import time


def updateScreen():
    for object_on_screen in all_static_objects:
        if object_on_screen.dead:
            all_static_objects.remove(object_on_screen)
        else:
            if object_on_screen.selected:
                screen.blit(object_on_screen.image_selected, (object_on_screen.x, object_on_screen.y))
            else:
                screen.blit(object_on_screen.image, (object_on_screen.x, object_on_screen.y))


# nevem čist točno zakaj mam to
_image_library = {}

all_static_objects = []  # to bo namenjen vsem objektom, ki bojo statični
all_moveable_objects = []  # to bo namenjem vsem objektom, ki se premikajo
selected_objects = []  # to so pa tisti objekti, ki so selectani

# širina in višina okna
WIDTH = 800
HEIGHT = 800

mouse_clicks = (0, 0, 0)
mouse_position = (411, 348)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_image = pygame.image.load("./data/map.jpg").convert()
user_interface = pygame.image.load("./data/user_interface1.png").convert()
done = False

players = [units.Player('player1', screen), units.Player('player2', screen)]

which_player = 0
clock = pygame.time.Clock()

while not done:  # main game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        players[which_player].army[0].move("up")
    if pressed[pygame.K_DOWN]:
        players[which_player].army[0].move("down")
    if pressed[pygame.K_LEFT]:
        players[which_player].army[0].move("left")
    if pressed[pygame.K_RIGHT]:
        players[which_player].army[0].move("right")

    if pressed[pygame.K_q]:
        which_player = 0

    if pressed[pygame.K_e]:
        which_player = 1

    if pressed[pygame.K_r]:
        print("*" * 50)
        for x in all_static_objects:
            x.print()

        print("*" * 50)
    if pressed[pygame.K_SPACE]:
        which_player = 1 - which_player

    if pressed[pygame.K_t]:
        for object in all_static_objects:
            object.print()

    if pygame.mouse.get_pressed()[0]:
        # torej je lev prtisjen
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # IF USERINTERFACE
        if 658 < mouse_x < 785:
            # pomeni, da pritiska nekje po tem UIju
            if 20 < mouse_y < 65:
                print("Players switched")
                which_player = 1 - which_player
            elif 100 < mouse_y < 222:
                print("Mini map")
            elif 235 < mouse_y < 285:
                print("GOLD : ")
            elif 317 < mouse_y < 373:
                #print("ADD Soldier")
                soldier = players[which_player].addSoldier()
                if soldier:
                    all_static_objects.append(soldier)
            elif 395 < mouse_y < 455:
                print("ADD Soldier2")
            elif 473 < mouse_y < 532:
                print("ADD Soldier3")
            elif 555 < mouse_y < 613:
                print("ADD Soldier4")
            elif 636 < mouse_y < 695:
                print("ADD Soldier5")

    if mouse_clicks != pygame.mouse.get_pressed():
        # al je nekdo pritisnu na miško al pa spustu knof
        lev, sredn, desn = mouse_clicks
        x1, y1 = mouse_position

        # print("Prej je blo tkole: ", lev, sredn, desn)
        mouse_clicks = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        x2, y2 = mouse_position

        x = sorted([x1, x2])
        y = sorted([y1, y2])

        if lev + desn + sredn > sum(mouse_clicks):

            for object in all_static_objects:
                if x[0] < object.center_x < x[1] and y[0] < object.center_y < y[1]:
                    # To pomeni, da je objekt znotraj recttangle-a, ki ga z miško obdaja
                    if (which_player == 0 and object.player == "player1") or (
                            which_player == 1 and object.player == "player2"):
                        # Če hoče taprav player premikat taprave unite
                        object.selected = 1
                    else:
                        object.selected = 0

                else:
                    # Zdej si dobu ukaz, da se premakn tja kamor miška zdej kaže
                    if sredn:
                        for selected_object in all_static_objects:
                            if selected_object.selected:
                                selected_object.setDestination(mouse_position[0], mouse_position[1])
                                selected_object.goTo(all_static_objects)
                    else:
                        object.selected = 0

    for selected_object in all_static_objects:
        if selected_object.distance > 10:
            selected_object.goTo(all_static_objects)

    x, y = mouse_position

    lev, sredn, desn = mouse_clicks
    screen.blit(background_image, [0, 0])
    screen.blit(user_interface, [640, 0])
    updateScreen()

    pygame.display.flip()
    clock.tick(60)
