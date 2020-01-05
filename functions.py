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

        #print("Sem dodal objekt : " + objekt.name)

    #print(start)
    #print(end)


    for i in range(int(end[1])-10, int(end[1]) + 10):
        for j in range(int(end[0])-10, int(end[0]) + 10):
            mreza[i][j] = -2

    for i in range(int(start[1])-10, int(start[1]) + 10):
        for j in range(int(start[0])-10, int(start[0]) + 10):
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


class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, x, y, right=None, down=None, left=None, up=None):

        self.x = x
        self.y = y
        self.position = (x, y)
        self.value = -1

        self.desno = right
        self.dol = down
        self.levo = left
        self.gor = up

        self.st_sosedov = 0

        self.sosedi = []

        self.visited = 0
        self.previous = None

    def __eq__(self, other):
        return self.position == other.position

    def nafilajSosede(self):
        if dol is not None:
            self.st_sosedov += 1
            self.sosedi.append(dol)
        if levo is not None:
            self.st_sosedov += 1
            self.sosedi.append(levo)
        if desno is not None:
            self.st_sosedov += 1
            self.sosedi.append(desno)
        if gor is not None:
            self.st_sosedov += 1
            self.sosedi.append(gor)


class Labirint:
    pass


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
