import numpy as np
import draw_manager


def prices(path, prices):
    total_price = 0
    for x in path[-1]:
        total_price += prices[x]
    return total_price


def dfs_paths(graph, start, goal):
    total_price = 0
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            total_price += price[next]
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))


def dfs(graph, start, goal):
    max_depth = 0
    visited, stack = set(), [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)
            if max_depth < len(stack):
                max_depth = len(stack)
        if vertex == goal:
            print("Največja globina: " + str(max_depth))
            print("Število obdelanih vozlišč: " + str(len(visited)))
            break
    return visited

narray = np.loadtxt(open("labyrinth_12.txt"), int, delimiter=",")

sx,sy = np.where(narray == -2)
ex,ey = np.where(narray == -3)
start = [(sx[0],sy[0])]
end = list(zip(ex,ey))

#print(narray)
d = [-1, 0 ,1]
adj_list = {}
price = {}
for i in range(1, len(narray) - 1):
    for j in range(1, len(narray[i]) - 1):
        coords = (i, j)
        if narray[i, j] != -1:
            if narray[i, j] < -1:
                price[coords] = 0
            else:
                price[coords] = narray[i, j]
            for dx in range(len(d)):
                for dy in range(len(d)):
                    if narray[i+d[dx], j+d[dy]] != -1 and (d[dx] != d[dy]) and (d[dx] != 1 or d[dy] != -1)  and (d[dx] != -1 or d[dy] != 1):
                        if coords in adj_list:
                            adj_list[coords].add((i+d[dx], j+d[dy]))
                        else:
                            adj_list[coords] = {(i+d[dx], j+d[dy])}


min_price = 0
curr_price = 0
lastEnd = 0
lastPath = []
print("-------------Depth first search-------------")
for i in range(len(end)):
    bfsPath = list(dfs_paths(adj_list, start[0], end[i]))
    curr_price = prices(bfsPath, price)
    if curr_price < min_price or min_price == 0:
        min_price = curr_price
        lastPath = bfsPath
        lastEnd = i

#dfsPath = list(dfs_paths(adj_list, start[0], end)
#lastPath = dfsPath
#min_price = prices(dfsPath, price)
#dfs(adj_list, start[0], end)

dfs(adj_list, start[0], end[lastEnd])
print("Najcenejša pot stane: " + str(min_price))
#print("Last path: " + str(lastPath[0]))
print("Dolžina poti: " + str(len(lastPath[0])))

dm = draw_manager.DrawManager(narray)
dm.draw_lab()
dm.draw_end_path(lastPath[0])
dm.call_sys_exit()