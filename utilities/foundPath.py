from heapq import heappop, heappush
import numpy as np
import json
import os
import time
from typing import List, Tuple
from heapq import heappop, heappush

"""
Classe che implementa le seguenti funzioni per individuare i percorsi migliori da/dai punto/i di start e stampa un json con gli stessi:

- def deikstra(self) --> funzione che implementa l'algoritmo di Dijkstra per individuare il percorso più breve
- def maze2graph(self) --> funzione che converte il labirinto in grafo per individuare il percorso.
- def find_multi_path_astar_return_visited(self, breadcrumps, num_paths=3) --> funzione che trova i 3 percorsi migliori per ogni punto di start

Alla fine i dati raccolti da queste funzioni vengono scritti in un file json
"""

class FoundPath:
    # Nota fondamentale il primo valore rappresenta la riga il secondo la colonna essendo un array si conta sempre a partite da 0
    __visited = {}
    __path_return = []
    __path = []
    __mydict = {}
    pass

    def __init__(self, maze: List[List[int]], start: List[Tuple[int, int]], goal: Tuple[int, int]):
        self.__path_returned_json = None
        self.__maze = maze
        self.__start = start
        self.__goal = goal

    pass


    """
    
    Questo codice implementa l'algoritmo di Dijkstra per trovare il percorso più breve in un labirinto.
    Il labirinto è rappresentato come una matrice dove i valori 0 rappresentano i muri e i valori diversi da 0 rappresentano i percorsi. 
    L'algoritmo utilizza una coda di priorità per tenere traccia dei nodi da visitare, dove la priorità di ogni nodo è la somma del costo attuale
    e della distanza euristica dalla posizione corrente al goal. Il codice utilizza la funzione "heappush" per inserire i nodi nella coda e "heappop"
    per prendere il nodo con priorità minima.

    La funzione "bfs" esegue l'algoritmo di Dijkstra, inizializzando la coda di priorità con la posizione di partenza,
    la lista dei nodi visitati e la lista dei percorsi trovati. Il codice continua a ciclare finché non sono stati trovati 3 percorsi
    o la coda è vuota. Se la posizione corrente è il goal, il percorso viene aggiunto alla lista dei percorsi e al dizionario.
    Se il nodo corrente è già stato visitato, il codice passa al prossimo.
    Altrimenti, espande il nodo corrente in tutte le direzioni possibili (Est, Ovest, Nord, Sud)
    e inserisce i nuovi nodi nella coda.
    
    """
    def deikstra(self):
        maze = self.__maze
        start = self.__start
        goal = self.__goal
        # Definizione delle variabili ROW e COL che
        # rappresentano rispettivamente il numero di righe e colonne del labirinto.
        ROW, COL = len(maze), len(maze[0])
        # Definizione della lista "directions" che rappresenta le direzioni
        # possibili da esplorare nel labirinto (Est, Ovest, Nord, Sud).
        directions = ["E", "W", "N", "S"]

        # Definizione della funzione "is_valid" che verifica se una posizione
        # è valida (all'interno dei limiti del labirinto e non bloccata da un muro).
        def is_valid(x, y):
            return 0 <= x < ROW and 0 <= y < COL and maze[x][y] != 0

        # Definizione della funzione "heuristic" che calcola la distanza
        # euristica tra la posizione corrente e la posizione di destinazione
        def heuristic(current, goal):
            x1, y1 = current
            x2, y2 = goal
            return abs(x1 - x2) + abs(y1 - y2)

        def bfs(start):
            # Inizializza la coda con la priorità, che in questo caso è la somma del costo attuale e
            # dell'euristica dalla posizione corrente al goal
            pr_queue = []
            heappush(pr_queue, (0 + heuristic(start, goal), 0, "", [], start))

            # Inizializza la lista dei nodi visitati
            visited = set()

            # Inizializza la lista dei percorsi trovati
            paths = []

            # Inizializza il dizionario che conterrà tutti i percorsi
            dictPath = {}

            # Inizializza la lista che conterrà i punti analizzati
            visitedPath = []

            # Continua a ciclare finché non sono stati trovati 3 percorsi o la coda è vuota
            while len(paths) < 3 and pr_queue:
                # Prendi il nodo con priorità minima dalla coda
                _, cost, path, path_cords, current = heappop(pr_queue)

                # Se il nodo corrente è il goal, aggiungi il percorso alla lista dei percorsi e al dizionario
                if current == goal:
                    paths.append((start, goal, path, cost))
                    #Qui sotto viene creato il dict nel solo caso si sia trovato il path
                    #Viene scritto con tutti i parametri per questioni di funzione
                    #Bisogna effettuare un controllo per poi settare l'elemento a vuoto
                    #Subito dopo tale dict viene scritto con i dati
                    nomeVar = 'PercorsoDa' + f'{start}'
                    string = 'Opzione' + f'{len(paths)}'
                    if nomeVar not in dictPath:
                        dictPath[nomeVar] = {}
                    if string not in dictPath:
                        dictPath[nomeVar][string] = {}
                    dictPath[nomeVar][string]["start"] = start
                    dictPath[nomeVar][string]["goal"] = goal
                    dictPath[nomeVar][string]["path"] = path
                    dictPath[nomeVar][string]["numberOfMoviment"] = len(path)
                    dictPath[nomeVar][string]["cost"] = cost
                    dictPath[nomeVar][string]["movimentPath"] = path_cords
                    #Aggiunto solo per verificare la uguale correttezza del path
                    #dictPath[nomeVar][string]["LenMovimentPath"] = len(path_cords)
                    #Scommentare per aggiungere il visited path al Json
                    #dictPath[nomeVar][string]["visited"] = visitedPath
                # Se il nodo è già stato visitato, salta al prossimo
                if current in visited:
                    continue

                # Aggiungi il nodo corrente alla lista dei nodi visitati
                visited.add(current)
                visitedPath.append(current)

                # Espandi il nodo corrente in tutte le direzioni possibili
                x, y = current
                for direction in directions:
                    if direction == "E":
                        if is_valid(x, y + 1):
                            heappush(pr_queue,
                                     (cost + maze[x][y + 1] + heuristic((x, y + 1), goal), cost + maze[x][y + 1],
                                      path + direction, path_cords + [(x, y + 1)], (x, y + 1)))
                    if direction == "W":
                        if is_valid(x, y - 1):
                            heappush(pr_queue,
                                     (cost + maze[x][y - 1] + heuristic((x, y - 1), goal), cost + maze[x][y - 1],
                                      path + direction, path_cords + [(x, y - 1)], (x, y - 1)))
                    if direction == "N":
                        if is_valid(x - 1, y):
                            heappush(pr_queue,
                                     (cost + maze[x - 1][y] + heuristic((x - 1, y), goal), cost + maze[x - 1][y],
                                      path + direction, path_cords + [(x - 1, y)], (x - 1, y)))
                    if direction == "S":
                        if is_valid(x + 1, y):
                            heappush(pr_queue,
                                     (cost + maze[x + 1][y] + heuristic((x + 1, y), goal), cost + maze[x + 1][y],
                                      path + direction, path_cords + [(x + 1, y)], (x + 1, y)))

            # Viene ritornato o il percorso o No WAY
            return dictPath or ["NO WAY!"]

        # La lista "paths" conterrà i risultati della ricerca per ogni punto di partenza
        paths = []
        #Se si vuole aggiunge breadcrumps al json
        #data = {"breadcrumps": list(self.__breadcrumps)}
        #paths.append(data)
        # Per ogni punto di partenza nella lista "start"
        for s in start:
            # Esegui la ricerca BFS per questo punto di partenza
            path = bfs(s)

            # Se la ricerca non restituisce "NO WAY!",
            if not path == ['NO WAY!']:
                # conta il numero di opzioni trovate
                number_of_options = 0
                for key, value in path.items():
                    number_of_options = len(value)

                    # Se il numero di opzioni è inferiore a 3,
                    if number_of_options <= 3:
                        # calcola la differenza per raggiungere 3
                        l = 3 - number_of_options

                        # e per ogni opzione mancante,
                        for i in range(l):
                            i = number_of_options + i + 1

                            # inserisci una voce "NO WAY!" nella lista
                            string = 'Opzione' + f'{i}'
                            if string not in path:
                                path[key][string] = {}
                                path[key][string] = "NO WAY!"

                # Aggiungi il risultato della ricerca a "paths"
                paths.append(path)

            # Se la ricerca restituisce "NO WAY!",
            else:
                #In caso non sia presente nessun path è essenziale creare
                #Oggetto da inserire nel json di ritorno
                #Questa parte di codice si occupa di questo
                dictPath = {}
                string = 'PercorsoDa' + f'{s}'
                if string not in dictPath:
                    dictPath[string] = {}
                dictPath[string]['Opzione1'] = "NO WAY!"
                dictPath[string]['Opzione2'] = "NO WAY!"
                dictPath[string]['Opzione3'] = "NO WAY!"
                # Aggiungi "NO WAY!" a "path"
                path.append("NO WAY!")
                paths.append(dictPath)
        # Restituisci il risultato della ricerca
        self.__path_return = paths
        return paths

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
        (0, 0): [('S', (1, 0), 1), ('E', (0, 1), 1)],
        (1, 0): [('N', (0, 0), 1)], 
        (3, 0): [('E', (3, 1), 1)],
        (0, 1): [('W', (0, 0), 1)], 
        (2, 1): [('S', (3, 1), 1), ('E', (2, 2), 1)], 
        (3, 1): [('W', (3, 0), 1), ('N', (2, 1), 1)], 
        (2, 2): [('W', (2, 1), 1), ('E', (2, 3), 1)], 
        (1, 3): [('S', (2, 3), 1)], 
        (2, 3): [('W', (2, 2), 1), ('N', (1, 3), 1), ('S', (3, 3), 1)], 
        (3, 3): [('N', (2, 3), 1)]
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
    Il metodo chiamato "find_multi_path_astar_return_visited()" che utilizza l'algoritmo A* per trovare più percorsi tra un insieme di punti di partenza
    e un punto di destinazione specifico. Il metodo accetta un parametro opzionale "num_paths" che specifica il numero di percorsi da trovare 
    (il valore predefinito è 3).
    Il metodo utilizza una coda di priorità per tenere traccia dei nodi da visitare e una lista "visitati"
    per evitare di ripercorrere i nodi già visitati. Per ogni punto di partenza specificato, l'algoritmo utilizza la funzione euristica definita precedentemente.
    Se il nodo corrente è uguale al nodo obiettivo, il percorso viene aggiunto alla lista di percorsi trovati e all'oggetto mydict.
    Se non sono stati trovati percorsi sufficienti, il metodo restituisce "NO WAY!"
    Inoltre, l'algoritmo ritorna una lista di tutti i nodi visitati durante la ricerca dei percorsi questo per permettere la continuazione del progetto per poi generare
    l'immagine tenendo traccia di quali sono i punti analizzati.
    
    Esempio di input data:
    
    maze = [    
        [1, 1, 0, 0],
        [1, 0, 0, 1],
        [0, 1, 1, 1],
        [1, 1, 0, 1]
    ]
    start = [(0, 0), (3, 3)]
    goal = (2, 2)
    
    Esempio di Output: 
    
    paths = [((0, 0), (2, 2), "SEEN", 5), ((3, 3), (2, 2), "WNW", 5)]
    visited = [[(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)], [(3, 3), (2, 3), (2, 2)]]
    
    
    Input: 
        Maze is all matrix with position wall and course
        Start Just with 2 parameter (row, column)
        Goal Just with 2 parameter (row, column)
        
    Output: 
        Movement wih North East South West
        And Cost for moviment
    """



    #Ultima opzione di codice
    def find_multi_path_astar_return_visited(self, breadcrumps, num_paths=3):
        goal = self.__goal
        for start in self.__start:
            pr_queue = []
            heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", "", start))
            visited = [start]
            graph: dict = self.maze2graph()
            while len(self.__path_return) < num_paths * len(self.__start) and pr_queue:
                _, cost, path, pathCordination, current = heappop(pr_queue)
                if current == goal:
                    self.__path_return.append((start, goal, path, pathCordination, cost))
                    new_element = "percorso" + str(start)
                    self.__new_element = new_element
                    self.__path.append(path)
                    if new_element not in self.__mydict:
                        self.__mydict[f"{new_element}"] = {}
                    self.__mydict[f"{new_element}"]["start"] = start
                    self.__mydict[f"{new_element}"]["goal"] = goal
                    self.__mydict[f"{new_element}"]["cost"] = cost
                    self.__mydict[f"{new_element}"]["path"] = path
                    self.__mydict[f"{new_element}"]["path_cord"] = pathCordination
                    self.__mydict[f"{new_element}"]["pathVisited"] = visited
                    self.__path_returned_json = json.dumps(self.__mydict)
                    self.__visited[start] = visited
                for direction, neighbour, real_cost in graph[current]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + real_cost,
                                            path + direction, pathCordination + str(neighbour), neighbour))
        if len(self.__path_return) < num_paths * len(self.__start):
            self.__path_return.append("NO WAY!")
        return self.__path_return


    def getPathVisited(self):
        return self.__visited

    def getPath(self):
        return self.__path

    def getPathRetunrJson(self):
        return self.__path_returned_json


    #Funzione di verifica se esiste il path di destinazione
    def ensure_path_exists(self, file_path):
        directory = os.path.dirname(file_path)
        # in caso il controllo fallisce viene creata la cartella aggiuntiva
        if not os.path.exists(directory):
            #creazione della directory che non esisteva
            os.makedirs(directory)

    #Con questa funzione avvalendosi del timestamp viene concetenato al nome del file una stringa timestemp che
    # permette di rendere univoco l'output
    def unique_file_name(self, file_name):
        timestamp = int(time.time())
        unique_name = f"{file_name}_{timestamp}"+'.json'
        return unique_name

    #Funzione che permette di scrivere un file json
    def write_json_file(self, file_path, file_name):
        #Si richiama al controllo dell'esistenza del file
        self.ensure_path_exists(file_path)
        # richiamata la funzione di unicità del file con aggiunta al nome del time stamp
        name = self.unique_file_name(file_name)
        # viene scritto il file nel percorso di destinazione
        path = file_path+name
        with open(path, "w") as json_file:
            json.dump(self.__path_return, json_file, indent=4)

            return path

        # Funzione che permette di scrivere un file json
    def write_json_file_from_dumps(self, data, file_path, file_name):
        # Si richiama al controllo dell'esistenza del file
        self.ensure_path_exists(file_path)
        # richiamata la funzione di unicità del file con aggiunta al nome del time stamp
        name = self.unique_file_name(file_name)
        # viene scritto il file nel percorso di destinazione
        with open(file_path + name, "w") as json_file:
            json.dump(data, json_file)