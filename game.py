import pygame
import os
from math import sqrt
import units
from functions import *
import time


def updateScreen():
    for object_on_screen in all_static_objects:
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

player1 = units.Player('player1', screen)
player2 = units.Player('player2', screen)
all_static_objects.append(player1.addSoldier())
clock = pygame.time.Clock()

while not done:  # main game loop

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

    if pressed[pygame.K_r]:
        player1.addSoldier()

    if pressed[pygame.K_t]:
        pass

    if mouse_clicks != pygame.mouse.get_pressed():

        # al je nekdo pritisnu na miško al pa spustu knof
        lev, sredn, desn = mouse_clicks
        x1, y1 = mouse_position

        # I need new values
        mouse_clicks = pygame.mouse.get_pressed()
        x2, y2 = pygame.mouse.get_pos()

        if lev + desn + sredn > sum(mouse_clicks):
            for object in list(all_static_objects + all_moveable_objects):
                # Če bo spodnji if true, pomeni to, da je ta objekt selectan
                print("ja pa pizda, da sm enga selectu")
                if x1 < object.x < x2 and y1 < object.y < y2:

                    print("ja AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAu")
                    object.selected = 1
                    object.setDestination(object.x, object.y)

                else:
                    # Zdej si dobu ukaz, da se premakn tja kamor miška zdej kaže
                    if sredn:
                        for selected_object in all_static_objects:
                            if selected_object.selected:
                                selected_object.setDestination(x2, y2)
                                selected_object.goTo()
                    else:
                        object.selected = 0

    for selected_object in all_static_objects:
        if selected_object.selected:
            selected_object.goTo()

    x, y = mouse_position

    lev, sredn, desn = mouse_clicks
    screen.blit(background_image, [0, 0])
    screen.blit(user_interface, [640, 0])
    updateScreen()

    pygame.display.flip()
    clock.tick(60)
