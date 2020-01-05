import numpy as np
from collections import defaultdict
import math
import draw_manager

def calc_heuristics_manhattan(aPoint, bPoint):
    return abs(aPoint[0] - bPoint[0]) + abs(aPoint[1] - bPoint[1])

def calc_heuristics_kvazi_manthattan(aPoint, bPoint, lab):
    dist = 0
    prevPoint = aPoint.copy()
    while(abs(aPoint[0] - bPoint[0]) != 0):
        if(aPoint[0] > bPoint[0]):
            aPoint[0] -= 1
        else:
            aPoint[0] += 1

        if (lab[tuple(aPoint)] == -1 and lab[tuple(prevPoint)] != -1):
            dist += 2
        else:
            dist += 1
        prevPoint = aPoint.copy()


    while(abs(aPoint[1] - bPoint[1] != 0)):
        if (aPoint[1] > bPoint[1]):
            aPoint[1] -= 1
        else:
            aPoint[1] += 1

        if (lab[tuple(aPoint)] == -1 and lab[tuple(prevPoint)] != -1):
            dist += 2
        else:
            dist += 1
        prevPoint = aPoint.copy()

    return dist

def reconstruct_path(cameFrom, current):
    total_path = list()
    total_path.append(tuple(current))
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(tuple(current))
    return total_path

def get_neighbors(current):
    neighbors = list()
    current = list(current)
    original = current.copy()

    #levo
    current[1] -= 1
    if current[1] >= 0:
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append(tuple(current))
    current = original.copy()

    #desno
    current[1] += 1
    if current[1] < np.size(narray, 1):
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append(tuple(current))
    current = original.copy()

    #gor
    current[0] -= 1
    if current[0] >= 0:
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append(tuple(current))
    current = original.copy()

    #dol
    current[0] += 1
    if current[0] < np.size(narray, 0):
        if narray[tuple(current)] >= 0 or narray[tuple(current)] == -3:
            neighbors.append(tuple(current))
    current = original.copy()

    return neighbors

def find_path_recalc(end):
    closedSet = set()
    openSet = set()
    openSet.add(tuple(start))

    cameFrom = dict()

    gScore = defaultdict(lambda: math.inf)
    fScore = defaultdict(lambda: math.inf)

    currEnd = None
    for y, x in end:
        if (not (currEnd)):
            currEnd = (y, x)
        else:
            if (calc_heuristics_kvazi_manthattan(list(start), [x, y], narray) < calc_heuristics_kvazi_manthattan(
                    list(start), list(currEnd), narray)):
                currEnd = tuple([y, x])


    fScore[tuple(start)] = calc_heuristics_kvazi_manthattan(start, currEnd, narray)
    gScore[tuple(start)] = 0

    while (len(openSet) > 0):
        current = None
        for y, x in openSet:
            if (not (current)):
                current = (y, x)
            else:
                if (fScore[(y, x)] < fScore[current]):
                    current = tuple([y, x])

        end = np.argwhere(narray == -3)
        end = list(map(list, end))
        currEnd = None
        for y, x in end:
            if (not (currEnd)):
                currEnd = (y, x)
            else:
                if (calc_heuristics_kvazi_manthattan(list(current), [x, y], narray) < calc_heuristics_kvazi_manthattan(
                        list(current), list(currEnd), narray)):
                    currEnd = tuple([y, x])

        if (current == currEnd):
            return reconstruct_path(cameFrom, current)

        # print(current)
        openSet.remove(current)
        closedSet.add(current)
        neighbors = get_neighbors(current)
        # print(neighbors)
        for neighbor in neighbors:
            if neighbor in closedSet:
                continue

            tentative_gScore = gScore[current] + narray[neighbor]

            if neighbor not in openSet:
                openSet.add(neighbor)
            elif tentative_gScore >= gScore[neighbor]:
                continue

            cameFrom[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + calc_heuristics_kvazi_manthattan(list(neighbor), currEnd, narray)

def find_path_static(end):
    closedSet = set()
    openSet = set()
    openSet.add(tuple(start))

    cameFrom = dict()

    gScore = defaultdict(lambda: math.inf)
    fScore = defaultdict(lambda: math.inf)

    fScore[tuple(start)] = calc_heuristics_kvazi_manthattan(start.copy(), end, narray)
    gScore[tuple(start)] = 0

    while (len(openSet) > 0):
        current = None
        for y, x in openSet:
            if (not (current)):
                current = (y, x)
            else:
                if (fScore[(y, x)] < fScore[current]):
                    current = tuple([y, x])

        if (current == end):
            return reconstruct_path(cameFrom, current)

        # print(current)
        openSet.remove(current)
        closedSet.add(current)
        neighbors = get_neighbors(current)
        # print(neighbors)
        for neighbor in neighbors:
            if neighbor in closedSet:
                continue

            tentative_gScore = gScore[current] + narray[neighbor]

            if neighbor not in openSet:
                openSet.add(neighbor)
            elif tentative_gScore >= gScore[neighbor]:
                continue

            cameFrom[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + calc_heuristics_kvazi_manthattan(list(neighbor), end, narray)

def find_path_static_backtrace(end):
    openSet = set()
    openSet.add(tuple(start))

    cameFrom = dict()

    gScore = defaultdict(lambda: math.inf)
    fScore = defaultdict(lambda: math.inf)

    fScore[tuple(start)] = calc_heuristics_kvazi_manthattan(start.copy(), end, narray)
    gScore[tuple(start)] = 0

    while (len(openSet) > 0):
        current = None
        for y, x in openSet:
            if (not (current)):
                current = (y, x)
            else:
                if (fScore[(y, x)] < fScore[current]):
                    current = tuple([y, x])

        if (current == end):
            return reconstruct_path(cameFrom, current)

        # print(current)
        openSet.remove(current)
        neighbors = get_neighbors(current)
        # print(neighbors)
        for neighbor in neighbors:

            tentative_gScore = gScore[current] + narray[neighbor]

            if neighbor not in openSet:
                openSet.add(neighbor)
            elif tentative_gScore >= gScore[neighbor]:
                continue
            if neighbor in cameFrom:
                if gScore[neighbor] > tentative_gScore:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + calc_heuristics_kvazi_manthattan(list(neighbor), end, narray)
            else:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + calc_heuristics_kvazi_manthattan(list(neighbor), end, narray)


def calc_price(path):
    price = 0
    for step in path:
        if(narray[step] >= 0):
            price += narray[step]
    return price



import sys

narray = np.loadtxt("lab.txt", int, delimiter=",")
start = np.argwhere(narray == -2)
start = list(map(list, start))[0]
end = np.argwhere(narray == -3)
end = list(map(list,end))

recalc = find_path_recalc(end)
#print("path found when recalculating has price: {}".format(calc_price(recalc)))


ends = list()
start = np.argwhere(narray == -2)
start = list(map(list, start))[0]
#print("\n\nprices of static findings: ")
minEnd = None
minPrice = 0
for e in end:
	tmp = find_path_static(tuple(e))
	price = calc_price(tmp)
	if(not(minEnd)):
		minEnd = tmp.copy()
		minPrice = price
	else:
		if price < minPrice:
			minPrice = price
			minEnd = tmp.copy()

	ends.append(tmp)

file = open("path.txt", "w")
file.write(str(minEnd));
file.close();


print(minEnd)
sys.exit(0)