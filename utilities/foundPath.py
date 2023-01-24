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
    """
    Input Example:
    [
        [1, 1, 0, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
        [1, 1, 0, 1]
    ]
    
    Output Example:
    Graph=
    {
        (0, 0): [("S", (1, 0), 1), ("E", (0, 1), 1)],
        (0, 1): [("W", (0, 0), 1), ("E", (0, 2), 1), ("S", (1, 1), 1)],
        (0, 2): [("W", (0, 1), 1)],
        (0, 3): [],
        (1, 0): [("N", (0, 0), 1), ("S", (2, 0), 1)],
        (1, 1): [("N", (0, 1), 1), ("E", (1, 2), 1)],
        (1, 2): [("W", (1, 1), 1), ("E", (1, 3), 1)],
        (1, 3): [("W", (1, 2), 1)],
        (2, 0): [("N", (1, 0), 1), ("S", (3, 0), 1)],
        (2, 1): [("N", (1, 1), 1), ("E", (2, 2), 1)],
        (2, 2): [("W", (2, 1), 1), ("E", (2, 3), 1)],
        (2, 3): [("W", (2, 2), 1)],
        (3, 0): [("N", (2, 0), 1)],
        (3, 1): [("N", (2, 1), 1)],
        (3, 2): [("N", (2, 2), 1)],
        (3, 3): [("W", (3, 2), 1)]
    }
    Convert the matrix in graph for found path
    
    Questa funzione definisce un metodo chiamato "maze2graph()" che converte un labirinto rappresentato
    come un array bidimensionale (self.__maze) in un grafo. Il grafo viene rappresentato come un dizionario, 
    dove ogni chiave è una tupla che rappresenta le coordinate di una cella del labirinto, e il valore è una lista di tuple 
    che rappresentano gli archi che collegano quella cella alle celle adiacenti. L'altezza e la larghezza del labirinto 
    vengono determinate trovando la lunghezza dell'array esterno e interno, rispettivamente. 
     
     Quindi, per ogni cella del labirinto che non è vuota, viene aggiunta una lista vuota al dizionario come valore
     per le coordinate della cella come chiave. Il codice quindi controlla le celle a sud ed est di ogni cella e 
     aggiunge archi al grafo per le celle che non sono vuote. Gli archi sono rappresentati come tuple contenenti una 
     stringa che indica la direzione dell'arco, le coordinate della cella adiacente e il valore della cella corrente. 
     La funzione restituisce il grafo.
     
     Ho deciso di usufruire della convenzione che i muri assumessero il valore 0 e il percorso percorribile il valore 1 
     o superiore in caso di caselle di colr grigio in base alla gradazione si pone il valore da modificare. 
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

    """
    Il metodo chiamato "heuristic()" che calcola una stima della distanza tra la cella attuale e la cella obiettivo.
    La funzione utilizza l'algoritmo di euristica "Manhattan Distance", che calcola la distanza come la somma delle
    differenze assolute tra le coordinate x e y della cella attuale e quella obiettivo. In altre parole, la funzione
    restituisce la somma delle differenze assolute tra la coordinata x della cella attuale e quella obiettivo più
    la somma delle differenze assolute tra la coordinata y della cella attuale e quella obiettivo.
    
    Questo fornisce una stima approssimativa della distanza tra le due celle, che può essere utilizzata in un algoritmo
    di ricerca come A* per determinare la cella più vicina all'obiettivo.
        
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