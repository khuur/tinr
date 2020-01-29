import pygame
import os
from math import sqrt
import units
from functions import *
import time

debug = 1
# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------

def updateScreen():
    for object_on_screen in all_objects_on_screen:  # Gre čez vse objekte
        if object_on_screen.dead:  # Če je ta objekt "mrtu"
            all_objects_on_screen.remove(object_on_screen)  # Ga odstrani iz seznama prikazovanja

            if "Soldier" in object_on_screen.name:
                player.number_of_soldiers -= 1
            elif "Archer" in object_on_screen.name:
                player.number_of_archers -= 1
            elif "Tank" in object_on_screen.name:
                player.number_of_tanks -= 1

            #player.army.remove(object_on_screen)
            player.population -= 1

        else:  # Torej je objekt "živ"
            if object_on_screen.selected:  # Če ma atribut 'selected' na true
                screen.blit(object_on_screen.image,
                            # image_selected !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            (object_on_screen.x, object_on_screen.y))  # Izriše en 'selected' sprite
            else:
                screen.blit(object_on_screen.image,
                            (object_on_screen.x, object_on_screen.y))  # Drugače pa 'normaln' sprite

    font = pygame.font.SysFont("comicsansms", 25)

    text = font.render(player_name, True, (245, 245, 0))
    screen.blit(text, (WIDTH - 140, 24))

    text = font.render("Soldiers: " + str(player.number_of_soldiers), True, (245, 245, 0))
    screen.blit(text, (WIDTH - 140, 105))

    text = font.render("Archers: " + str(player.number_of_archers), True, (245, 245, 0))
    screen.blit(text, (WIDTH - 140, 135))

    text = font.render("Tanks: " + str(player.number_of_tanks), True, (245, 245, 0))
    screen.blit(text, (WIDTH - 140, 165))

    text = font.render(str(player.gold) + " G", True, (245, 245, 0))
    screen.blit(text, (WIDTH - 140, 242))


# ------------------------------------------------------------------------
# Starting data
# ------------------------------------------------------------------------
start_time = time.time()  # Da lahko trackam v keri sekundi igre sem
all_objects_on_screen = []  # to bo namenjen vsem objektom

WIDTH = 1300  # Širina okna
HEIGHT = 750  # Višina okna

mouse_clicks = (0, 0, 0)  # Keri knofi na miški so prtisjeni
mouse_position = (411, 348)  # Kje je miška trenutno

pygame.init()  # Da se pygame začne
#screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Kam bom sploh risu stvari
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Kam bom sploh risu stvari
pygame.display.set_caption("Kris's game")  # Da mam svoj caption :3

if pygame.display.get_surface().get_size() == (1300, 750):
    # Tuki notr bojo vse stvari, ki jih bom pol rabu in so load related
    background_image = pygame.image.load("./data/blurred_map.jpg").convert()  # Kar je v ozadju narisano
    user_interface = pygame.image.load("./data/user_interface1.png").convert()  # Da mam še UI na desni strani
    start_menu = pygame.image.load("./data/start_menu3.png").convert()  # Da mam še UI na desni strani
    settings_menu = pygame.image.load("./data/settings_menu.png").convert()  # Da mam še UI na desni strani

    check = pygame.image.load("./data/check.png").convert()  # Da mam še UI na desni strani
    check = pygame.transform.scale(check, (50, 50))  # prvi sprite
    cancel = pygame.image.load("./data/cancel.png").convert()  # Da mam še UI na desni strani
    cancel = pygame.transform.scale(cancel, (50, 50))  # prvi sprite

    highscore_menu = pygame.image.load("./data/highscore_menu.png").convert()  # Da mam še UI na desni strani
    soldier_image = pygame.image.load("./data/player1/soldier.png").convert()  # Da mam še UI na desni strani
    archer_image = pygame.image.load("./data/player1/archer.png").convert()  # Da mam še UI na desni strani
    tank_image = pygame.image.load("./data/player1/tank.png").convert()  # Da mam še UI na desni strani

    soldr = units.Soldier(screen, 300, 300, "./data/player1/soldier.png", "soldr", "player000")
    arcr = units.Archer(screen, 300, 300, "./data/player1/archer.png", "arcer", "player000")
    tenk = units.Tank(screen, 300, 300, "./data/player1/tank.png", "tenk", "player000")

done = False
player_name = "Kristjan"
player = units.Player(player_name, screen)
enemy  = units.Player('Enemy', screen)

setPoints(player)
clock = pygame.time.Clock()

boss = enemy.addBoss(screen, 900, 100, 200, "./data/chimp.bmp")
all_objects_on_screen.append(boss)

if not debug:
    selected = False
    game = ""
    highscore = ""
    settings = ""
else:
    selected = 1
    game = 1
    highscore = 0
    settings = 0

# ------------------------------------------------------------------------
# Main game loop
# ------------------------------------------------------------------------
font = pygame.font.SysFont("comicsansms", 25)

while not done:  # main game loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Preverim, če je nekdo prtisnu na križec
            done = True  # Če je, pol zaključi z igro
            highscoreToTxt(players)
            continue
    pressed = pygame.key.get_pressed()

    # ------------------------------------------------------------------------
    # Start menu
    # ------------------------------------------------------------------------

    while not selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Preverim, če je nekdo prtisnu na križec
                done = True  # Če je, pol zaključi z igro
                highscoreToTxt(players)
                continue
        pressed = pygame.key.get_pressed()

        if pygame.mouse.get_pressed()[0]:
            # torej je lev prtisjen
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if 285 < mouse_x < 1014:
                # pomeni, da pritiska nekje po tem UIju
                if 35 < mouse_y < 190:
                    selected = True
                    game = True
                elif 240 < mouse_y < 390:
                    selected = True
                    highscore = True
                    game = True
                elif 410 < mouse_y < 560:
                    selected = True
                    settings = True
                elif 580 < mouse_y < 725:
                    selected = True
                    done = True
        screen.blit(start_menu, (0, -20))
        pygame.display.flip()
        continue

    # ------------------------------------------------------------------------
    # Highscore menu
    # ------------------------------------------------------------------------

    if highscore:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Preverim, če je nekdo prtisnu na križec
                done = True  # Če je, pol zaključi z igrodone = True  # Če je, pol zaključi z igro
                highscoreToTxt(players)
                continue
        pressed = pygame.key.get_pressed()

        screen.blit(highscore_menu, (0, -20))
        highscores = bestHighscores()
        for i, hs in enumerate(highscores):
            text = font.render(hs.strip(), True, (220, 20, 60))
            screen.blit(text, (500, 242 + i * 50))
        pygame.display.flip()
        time.sleep(0.2)

        if pygame.mouse.get_pressed()[0]:
            # torej je lev prtisjen
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 285 < mouse_x < 1014:
                # pomeni, da pritiska nekje po tem UIju
                if 580 < mouse_y < 725:
                    selected = False
                    highscore = False
        # pygame.display.flip()
        if highscore:
            continue

    # ------------------------------------------------------------------------
    # Settings menu
    # ------------------------------------------------------------------------

    if settings:

        screen.blit(settings_menu, (0, -20))
        if player.sound_enabled:
            screen.blit(check, (700, 242))
        else:
            screen.blit(cancel, (750, 242))

        font = pygame.font.SysFont("comicsansms", 50)
        text = font.render("SOUND: ", True, (220, 20, 60))
        screen.blit(text, (500, 242))
        pygame.display.flip()
        time.sleep(0.2)

        if pygame.mouse.get_pressed()[0]:
            # torej je lev prtisjen
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 285 < mouse_x < 1014:
                # pomeni, da pritiska nekje po tem UIju
                if 580 < mouse_y < 725:
                    selected = False
                    settings = False

            if 242 < mouse_y < 292:
                # pomeni, da pritiska nekje po tem UIju
                if 700 < mouse_x < 750:
                    player.changeSoundSettings(0)
                if 750 < mouse_x < 800:
                    player.changeSoundSettings(1)
        # pygame.display.flip()
        if settings:
            continue

    if game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Preverim, če je nekdo prtisnu na križec
                done = True  # Če je, pol zaključi z igro
                highscoreToTxt(players)
                continue
        if pressed[pygame.K_UP]:
            enemy.army[0].move("up")
        if pressed[pygame.K_DOWN]:
            enemy.army[0].move("down")
        if pressed[pygame.K_LEFT]:
            enemy.army[0].move("left")
        if pressed[pygame.K_RIGHT]:
            enemy.army[0].move("right")

        if pressed[pygame.K_q]:
            which_player = 0

        if pressed[pygame.K_e]:
            which_player = 1

        if pressed[pygame.K_g]:
            a = player.addGoldmine()
            if a:
                all_objects_on_screen.append(a)

        if pressed[pygame.K_h]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            a = player.addHouse(mouse_x, mouse_y)
            if a:
                all_objects_on_screen.append(a)

        if pressed[pygame.K_r]:
            print("*" * 50)
            for x in all_objects_on_screen:
                x.print()
            print("*" * 50)

        if pygame.mouse.get_pressed()[0]:
            # torej je lev prtisjen
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # IF USER INTERFACE
            if (WIDTH - 150) < mouse_x < (WIDTH - 30):
                # pomeni, da pritiska nekje po tem UIju
                if 100 < mouse_y < 222:
                    print("Mini map")
                elif 235 < mouse_y < 285:
                    print("GOLD : ")
                elif 317 < mouse_y < 373:
                    soldier = player.addSoldier()
                    if soldier:
                        all_objects_on_screen.append(soldier)
                elif 395 < mouse_y < 455:
                    archer = player.addArcher()
                    if archer:
                        all_objects_on_screen.append(archer)
                elif 473 < mouse_y < 532:
                    tank = player.addTank()
                    if tank:
                        all_objects_on_screen.append(tank)
                elif 555 < mouse_y < 613:
                    print("ADD Soldier4")
                elif 636 < mouse_y < 695:
                    print("ADD Soldier5")

        rect = Rectangle(WIDTH/2,HEIGHT/2, WIDTH/2, HEIGHT/2)
        quadTree = QuadTree(rect, 4)

        for o in all_objects_on_screen:
            neki = Point(o.x, o.y, o.r)
            quadTree.insert(neki)


        if mouse_clicks != pygame.mouse.get_pressed():
            # al je nekdo pritisnu na miško al pa spustu knof
            lev, sredn, desn = mouse_clicks
            x1, y1 = mouse_position

            mouse_clicks = pygame.mouse.get_pressed()
            mouse_position = pygame.mouse.get_pos()

            x2, y2 = mouse_position

            x = sorted([x1, x2])
            y = sorted([y1, y2])

            if lev + desn + sredn > sum(mouse_clicks):  # Če je bil kerkol knof prtisjen
                for object in all_objects_on_screen:
                    if x[0] < object.center_x < x[1] and y[0] < object.center_y < y[1]:
                        # To pomeni, da je objekt znotraj recttangle-a, ki ga z miško obdaja
                        object.selected = 1
                    else:
                        # Zdej si dobu ukaz, da se premakn tja kamor miška zdej kaže
                        if sredn:
                            for selected_object in all_objects_on_screen:
                                if selected_object.selected:
                                    selected_object.setDestination(mouse_position[0], mouse_position[1])
                                    selected_object.goTo(all_objects_on_screen, quadTree)
                        else:
                            object.selected = 0
                            object.move_times = 0
                            object.moving = 0

        for selected_object in all_objects_on_screen:
            if selected_object.moveable and selected_object.distance > 10:
                selected_object.goTo(all_objects_on_screen, quadTree)
            else:
                selected_object.moving = 0

        x, y = mouse_position

        lev, sredn, desn = mouse_clicks
        screen.blit(background_image, [0, 0])
        screen.blit(user_interface, [WIDTH - 160, 0])
        screen.blit(soldr.image, [WIDTH - 100, 320])
        screen.blit(arcr.image, [WIDTH - 100, 400])
        screen.blit(tenk.image, [WIDTH - 100, 480])

        updateScreen()

        pygame.display.flip()
        clock.tick(60)

        if time.time() - player.got_gold > 1:
            player.gold += player.gold_per_second
            player.got_gold = time.time()
