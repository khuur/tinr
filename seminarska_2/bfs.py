import numpy as np
import draw_manager


def prices(path, prices):
    total_price = 0
    for x in path[-1]:
        total_price += prices[x]
    return total_price


def bfs_paths(graph, start, goal):
    total_price = 0
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            total_price += price[next]
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))


def bfs(graph, start, goal):
    visited, queue = set(), [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            queue.extend(graph[vertex] - visited)
        if vertex == goal:
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
#dfs = list(dfs_paths(adj_list, start[0], end))-
print("-------------Breadth first search-------------")
for i in range(len(end)):
    bfsPath = list(bfs_paths(adj_list, start[0], end[i]))
    curr_price = prices(bfsPath, price)
    if curr_price < min_price or min_price == 0:
        min_price = curr_price
        lastPath = bfsPath
        lastEnd = i


#bfsPath = list(bfs_paths(adj_list, start[0], end)
#lastPath = bfsPath
#min_price = prices(bfsPath, price)
#bfs(adj_list, start[0], end)

bfs(adj_list, start[0], end[lastEnd])
print("Najcenejša pot stane: " + str(min_price))
#print("Last path: " + str(lastPath[0]))
print("Dolžina poti: " + str(len(lastPath[0])))
dm = draw_manager.DrawManager(narray)
dm.draw_lab()
dm.draw_end_path(lastPath[0])
dm.call_sys_exit()