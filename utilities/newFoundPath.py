from typing import List, Tuple
from heapq import heappop, heappush

#Definizione della funzione principale "dijkstra", che accetta come argomenti il labirinto,
#la posizione di partenza (o più posizioni di partenza) e la posizione di destinazione.
def deikstra(maze: List[List[int]], start: List[Tuple[int, int]], goal: Tuple[int, int]):
    # Definizione delle variabili ROW e COL che
    # rappresentano rispettivamente il numero di righe e colonne del labirinto.
    ROW, COL = len(maze), len(maze[0])
    #Definizione della lista "directions" che rappresenta le direzioni
    # possibili da esplorare nel labirinto (Est, Ovest, Nord, Sud).
    directions = ["E", "W", "N", "S"]


    #Definizione della funzione "is_valid" che verifica se una posizione
    # è valida (all'interno dei limiti del labirinto e non bloccata da un muro).
    def is_valid(x, y):
        return 0 <= x < ROW and 0 <= y < COL and maze[x][y] != 0

    #Definizione della funzione "heuristic" che calcola la distanza
    # euristica tra la posizione corrente e la posizione di destinazione
    def heuristic(current, goal):
        x1, y1 = current
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def bfs(start):
        # Inizializza la coda con la priorità, che in questo caso è la somma del costo attuale e dell'euristica dalla posizione corrente al goal
        pr_queue = []
        heappush(pr_queue, (0 + heuristic(start, goal), 0, "", "", start))

        # Inizializza la lista dei nodi visitati
        visited = set()

        # Inizializza la lista dei percorsi trovati
        paths = []

        # Inizializza il dizionario che conterrà tutti i percorsi
        dictPath = {}

        # Continua a ciclare finché non sono stati trovati 3 percorsi o la coda è vuota
        while len(paths) < 3 and pr_queue:
            # Prendi il nodo con priorità minima dalla coda
            _, cost, path, path_cords, current = heappop(pr_queue)

            # Se il nodo corrente è il goal, aggiungi il percorso alla lista dei percorsi e al dizionario
            if current == goal:
                paths.append((start, goal, path, cost))
                string = 'Opzione' + f'{len(paths)}'
                if start not in dictPath:
                    dictPath[start] = {}
                if string not in dictPath:
                    dictPath[start][string] = {}
                dictPath[start][string]["start"] = start
                dictPath[start][string]["goal"] = goal
                dictPath[start][string]["path"] = path
                dictPath[start][string]["cost"] = cost

            # Se il nodo è già stato visitato, salta al prossimo
            if current in visited:
                continue

            # Aggiungi il nodo corrente alla lista dei nodi visitati
            visited.add(current)

            # Espandi il nodo corrente in tutte le direzioni possibili
            x, y = current
            for direction in directions:
                if direction == "E":
                    if is_valid(x, y + 1):
                        heappush(pr_queue, (cost + maze[x][y + 1] + heuristic((x, y + 1), goal), cost + maze[x][y + 1],
                                            path + direction, path_cords + str((x, y + 1)), (x, y + 1)))
                if direction == "W":
                    if is_valid(x, y - 1):
                        heappush(pr_queue, (cost + maze[x][y - 1] + heuristic((x, y - 1), goal), cost + maze[x][y - 1],
                                            path + direction, path_cords + str((x, y - 1)), (x, y - 1)))
                if direction == "N":
                    if is_valid(x - 1, y):
                        heappush(pr_queue, (cost + maze[x - 1][y] + heuristic((x - 1, y), goal), cost + maze[x - 1][y],
                                            path + direction, path_cords + str((x - 1, y)), (x - 1, y)))
                if direction == "S":
                    if is_valid(x + 1, y):
                        heappush(pr_queue, (cost + maze[x + 1][y] + heuristic((x + 1, y), goal), cost + maze[x + 1][y],
                                            path + direction, path_cords + str((x + 1, y)), (x + 1, y)))

        #Viene ritornato o il percorso o No WAY
        return dictPath or ["NO WAY!"]

    paths = []
    for s in start:
        path = bfs(s)
        if not path == ['NO WAY!']:
            number_of_options = 0
            for key, value in path.items():
                number_of_options = len(value)
                if number_of_options <= 3:
                    l = 3 - number_of_options
                    for i in range(l):
                        i = number_of_options+i+1
                        string = 'Opzione'+f'{i}'
                        if string not in path:
                            path[key][string] = {}
                            path[key][string] = "NO WAY!"
            paths.append(path)
        else:
            paths.append("NO WAY!")
    return paths



maze = [[1, 0, 1, 1, 1, 1],
        [4, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1],
        [0, 0, 1, 1, 4, 1],
        [1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1]]

start = [(0, 0), (2, 2), (4, 4)]
goal = (5, 5)

print(deikstra(maze, start, goal))
