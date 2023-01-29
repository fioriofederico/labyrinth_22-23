from heapq import heappop, heappush
import numpy as np
import json
import os
import time


class FoundPath:
    # Nota fondamentale il primo valore rappresenta la riga il secondo la colonna essendo un array si conta sempre a partite da 0
    __visited = {}
    __path_return = []
    __mydict = {}
    pass

    def __init__(self, maze, start, goal):
        self.__path_returned_json = None
        self.__maze = maze
        self.__start = start
        self.__goal = goal

    pass
    
    def maze2graph(self):
        height = len(self.__maze)
        width = len(self.__maze[0]) if height else 0
        graph = {(i, j): [] for j in range(width) for i in range(height) if self.__maze[i][j]}
        for row, col in graph.keys():
            if row < height - 1 and self.__maze[row + 1][col]:
                graph[(row, col)].append(("S", (row + 1, col), self.__maze[row][col]))
                graph[(row + 1, col)].append(("N", (row, col), self.__maze[row][col]))
            if col < width - 1 and self.__maze[row][col + 1]:
                graph[(row, col)].append(("E", (row, col + 1), self.__maze[row][col]))
                graph[(row, col + 1)].append(("W", (row, col), self.__maze[row][col]))
        return graph

    def heuristic(self, cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    #Ultima opzione di codice
    def find_multi_path_astar_return_visited(self, num_paths=3):
        goal = self.__goal
        for start in self.__start:
            pr_queue = []
            heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
            visited = [start]
            graph: dict = self.maze2graph()
            while len(self.__path_return) < num_paths * len(self.__start) and pr_queue:
                _, cost, path, current = heappop(pr_queue)
                if current == goal:
                    self.__path_return.append((start, goal, path, cost))
                    new_element = "percorso" + str(start)
                    if new_element not in self.__mydict:
                        self.__mydict[f"{new_element}"] = {}
                    self.__mydict[f"{new_element}"]["start"] = start
                    self.__mydict[f"{new_element}"]["goal"] = goal
                    self.__mydict[f"{new_element}"]["cost"] = cost
                    self.__mydict[f"{new_element}"]["path"] = path
                    self.__mydict[f"{new_element}"]["pathVisited"] = visited
                    self.__path_returned_json = json.dumps(self.__mydict)
                    self.__visited[start] = visited
                for direction, neighbour, real_cost in graph[current]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + real_cost,
                                            path + direction, neighbour))
        if len(self.__path_return) < num_paths * len(self.__start):
            self.__path_return.append("NO WAY!")
        return self.__path_return

    def getPathVisited(self):
        return self.__visited

    def getPathRetunrJson(self):
        return self.__path_returned_json

    def ensure_path_exists(self, file_path):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def unique_file_name(self, file_name):
        timestamp = int(time.time())
        unique_name = f"{file_name}_{timestamp}"+'.json'
        return unique_name

    def write_json_file(self, data, file_path, file_name):
        self.ensure_path_exists(file_path)
        name = self.unique_file_name(file_name)
        with open(file_path+name, "w") as json_file:
            json.dump(data, json_file)
            #json.loads(data, json_file)