#TODO aggiungere i richiami alle funzioni di eleonora
#TODO fix problem generation destinazione fissa Vincenzo vedi se riesci


import numpy as np
import math
from utilities.maze import Maze
from utilities.foundPath import FoundPath

class menuOption:
    pass

    def __init__(self):
        pass


    #Funzione per prendere solo il nome del file che viene passatto da terminale
    def get_file_name(self, file_path):
        return file_path.split("/")[-1].split(".")[0]

    def GenerateInput(self, height, width, startpoints, endpoints, breadcrumbs):
        # Con la riga subito sotto viene instanziato un maze e passati i parametri per effettuare la sua crezione
        p = Maze(height, width, startpoints, endpoints, breadcrumbs)
        #generazione del maze
        p.generate()
        #viene anche creata l'immagine tiff per visualizzare l'esito dei parametri inseriti
        p.getMazeImage()
        #viene convertito la lista di liste in una lista di tuple
        start = [(x[0], x[1]) for x in p.startpoints]
        #il goal viene convertito in tupla
        goal = tuple(p.endpoints[0])
        # si richiama la struttura matrice del labirinto
        """ con la riga numero 55 avvalendosi del sistema di ricerca di numpy all'interno
            dei numpy array è possibile sostituire i valori delle w con un valore definito 
            in questo caso 0 e le c con 1 ecco l'esempio
                    Input:
                        [
                            ['w' 'w' 'w' ... 'w' 'w' 'w']
                            ['w' 'c' 'c' ... 'w' 'c' 'w']
                            ['w' 'c' 'w' ... 'w' 'c' 'w']
                            ...
                            ['w' 'w' 'w' ... 'w' 'c' 'w']
                            ['w' 'c' 'c' ... 'c' 'c' 'w']
                            ['w' 'w' 'w' ... 'w' 'w' 'w']
                        ]

                    Output:
                        [
                            [0 0 0 ... 0 0 0]
                            [0 1 1 ... 0 1 0]
                            [0 1 0 ... 0 1 0]
                            ...
                            [0 0 0 ... 0 1 0]
                            [0 1 1 ... 1 1 0]
                            [0 0 0 ... 0 0 0]
                        ]
                """
        maze = p.getValuebleMatrixWithBreadcrumbs()
        # viene convertito il tutto in lista
        maze = maze.tolist()
        # viene istanziato il foundpath
        foundPath = FoundPath(maze, start, goal)
        # viene creato il grafo per poi procedere alla ricerca del path
        foundPath.maze2graph()
        # viene cercato il path all'interno del maze
        foundPath.find_multi_path_astar_return_visited()
        # creata una stringa json
        json = foundPath.getPathRetunrJson()
        # creato il file output json
        foundPath.write_json_file(json, './output/', 'outputGenerated')

    #In questa funzione è possibile trovare il percorso a partire dall'immagine
    def ImageInput(self, imagePath):
        #Istanziamo oggetto MAZE
        p = Maze()
        #Funzione per la lettura dell'immagine
        p.readMazeImage(imagePath)
        #Con questa riga vengono convertiti i punti di start
        # da [[0, 29], [19, 60]] in un array di tuple [(0, 29), (19, 60)]
        print(p.startpoints)
        start = [(x[0], x[1]) for x in p.startpoints]
        #viene settato il goal dai endpoin in una tupla
        goal = tuple(p.endpoints[0])
        #viene presa e assegnata a maze la matrice ritornata dall'analisi
        p.getMaze()
        """ in questa riga avvalendosi del sistema di ricerca di numpy all'interno
            dei numpy array è possibile sostituire i valori delle w con un valore definito 
            in questo caso 0 e le c con 1 ecco l'esempio
            Input:
                [
                    ['w' 'w' 'w' ... 'w' 'w' 'w']
                    ['w' 'c' 'c' ... 'w' 'c' 'w']
                    ['w' 'c' 'w' ... 'w' 'c' 'w']
                    ...
                    ['w' 'w' 'w' ... 'w' 'c' 'w']
                    ['w' 'c' 'c' ... 'c' 'c' 'w']
                    ['w' 'w' 'w' ... 'w' 'w' 'w']
                ]
                    
            Output:
                [
                    [0 0 0 ... 0 0 0]
                    [0 1 1 ... 0 1 0]
                    [0 1 0 ... 0 1 0]
                    ...
                    [0 0 0 ... 0 1 0]
                    [0 1 1 ... 1 1 0]
                    [0 0 0 ... 0 0 0]
                ]
        """

        # la matrice del nostro labirinto viene sostituita con il labirinto corretto
        maze = p.getValuebleMatrixWithBreadcrumbs()
        # il labirinto viene convertito in una lista aggiunte le virgole tra i vari punti
        maze = maze.tolist()
        #Entra in azione la funzione per la ricerca del percorso migliore
        foundPath = FoundPath(maze, start, goal)
        # il nostro maze viene convertito per ottenere il grafo
        foundPath.maze2graph()
        #si procede alla ricerca del path con la funzione che usa l'algoritmo A*
        foundPath.find_multi_path_astar_return_visited()
        #viene generato una stringa json
        json = foundPath.getPathRetunrJson()
        #viene fatto output file json
        foundPath.write_json_file(json, './output/', self.get_file_name(imagePath))

    #Come il processo precedente in questo caso ci si aspetta un JSON in Input
    def JsonInput(self, jsonPath):
        # Istanziamo oggetto MAZE
        p = Maze()
        # Funzione per la lettura del file JSON
        p.readMazeJson(jsonPath)
        # Con questa riga vengono convertiti i punti di start
        # da [[0, 29], [19, 60]] in un array di tuple [(0, 29), (19, 60)]
        start = [(x[0], x[1]) for x in p.startpoints]
        # viene settato il goal dai endpoin in una tupla
        goal = tuple(p.endpoints[0])
        # viene presa e assegnata a maze la matrice ritornata dall'analisi
        maze = p.getMaze()
        """ in questa riga avvalendosi del sistema di ricerca di numpy all'interno
            dei numpy array è possibile sostituire i valori delle w con un valore definito 
            in questo caso 0 e le c con 1 ecco l'esempio
            Input:
                [
                    ['w' 'w' 'w' ... 'w' 'w' 'w']
                    ['w' 'c' 'c' ... 'w' 'c' 'w']
                    ['w' 'c' 'w' ... 'w' 'c' 'w']
                    ...
                    ['w' 'w' 'w' ... 'w' 'c' 'w']
                    ['w' 'c' 'c' ... 'c' 'c' 'w']
                    ['w' 'w' 'w' ... 'w' 'w' 'w']
                ]

            Output:
                [
                    [0 0 0 ... 0 0 0]
                    [0 1 1 ... 0 1 0]
                    [0 1 0 ... 0 1 0]
                    ...
                    [0 0 0 ... 0 1 0]
                    [0 1 1 ... 1 1 0]
                    [0 0 0 ... 0 0 0]
                ]
        """
        # la matrice del nostro labirinto viene sostituita con il labirinto corretto
        maze = p.getValuebleMatrixWithBreadcrumbs()
        # il labirinto viene convertito in una lista aggiunte le virgole tra i vari punti
        maze = maze.tolist()
        # Entra in azione la funzione per la ricerca del percorso migliore
        foundPath = FoundPath(maze, start, goal)
        # il nostro maze viene convertito per ottenere il grafo
        foundPath.maze2graph()
        # si procede alla ricerca del path con la funzione che usa l'algoritmo A*
        foundPath.find_multi_path_astar_return_visited()
        # viene generato una stringa json
        json = foundPath.getPathRetunrJson()
        # viene fatto output file json
        foundPath.write_json_file(json, './output/', self.get_file_name(jsonPath))