from heapq import heappop, heappush
import numpy as np
import json


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
    """
    Convert the matrix in graph for found path
    """

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

    """
    A* is a widely used pathfinding algorithm and an extension of Edsger Dijkstra's 1959 algorithm.
    A* uses a greedy search and finds a least-cost path from the given initial node to one goal node out of one or more possibilities.
    As A* traverses the graph, it follows a path of the lowest expected total cost or distance,
    keeping a sorted priority queue of alternate path segments along the way.
    It uses a heuristic cost function of node to determine the order in which the search visits nodes in the graph.
    For A* we take the first node which has the lowest sum path cost and expected remaining cost.
    But heuristics must be admissible, that is, it must not overestimate the distance to the goal.
    The time complexity of A* depends on the heuristic.
    
    For Python, we can use "heapq" module for priority queuing and add the cost part of each element.
    For a maze, one of the most simple heuristics can be "Manhattan distance".
    """

    def heuristic(self, cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    """
    Input: 
        Maze is all matrix with position wall and course
        Start Just with 2 parameter (row, column)
        Goal Just with 2 parameter (row, column)
        
    Output: 
        Movement wih North East South West
        And Cost for moviment
    """
    # Versione lasciata da rimuove
    def find_path_astar(self):
        start_input = self.__start
        goal = self.__goal
        path_return = []
        for i in range(len(start_input)):
            start = start_input[i]
            pr_queue = []
            heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
            visited = set()
            graph: dict = self.maze2graph()
            while pr_queue:
                _, cost, path, current = heappop(pr_queue)
                if current == goal:
                    path_return.append((path, cost))
                if current in visited:
                    continue
                visited.add(current)
                for direction, neighbour, real_cost in graph[current]:
                    heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + real_cost,
                                        path + direction, neighbour))
            path_return.append("NO WAY!")

        return path_return

    #Versione lasciata da rimuovere
    def find_multi_path_astar(self, num_paths = 3):
        goal = self.__goal
        path_return = []
        for start in self.__start:
            pr_queue = []
            heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
            visited = set()
            graph: dict = self.maze2graph()
            while len(path_return) < num_paths*len(self.__start) and pr_queue:
                _, cost, path, current = heappop(pr_queue)
                if current == goal:
                    path_return.append((start, goal, path, cost))
                if current in visited:
                    continue
                visited.add(current)
                for direction, neighbour, real_cost in graph[current]:
                    heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + real_cost,
                                        path + direction, neighbour))
        if len(path_return) < num_paths*len(self.__start):
            path_return.append("NO WAY!")

        return path_return

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




