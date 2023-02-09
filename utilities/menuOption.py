# TODO aggiungere i richiami alle funzioni di eleonora
# TODO fix problem generation destinazione fissa Vincenzo vedi se riesci

import os
import shutil
import time

from utilities.maze import Maze
from utilities.foundPath import FoundPath
import json
from utilities.generationMazeOutputImage import GenerationMazeOutputImage


class menuOption:
    pass

    def __init__(self):
        self.__destinationFolder = './output/'
        self.__extTiff = '.tiff'
        self.__extJson = '.json'
        pass

    #Funzione di copia di un file
    def copyFile(self, pathOrign, pathDestination):
        shutil.copy(pathOrign, pathDestination)

    # Funzione per prendere solo il nome del file che viene passatto da terminale
    def get_file_name(self, file_path):
        return file_path.split("/")[-1].split(".")[0]

    # Funzione di verifica se esiste il path di destinazione
    def ensure_path_exists(self, file_path):
        directory = os.path.dirname(file_path)
        # in caso il controllo fallisce viene creata la cartella aggiuntiva
        if not os.path.exists(directory):
            # creazione della directory che non esisteva
            os.makedirs(directory)

    # Con questa funzione avvalendosi del timestamp viene concetenato al nome del file una stringa timestemp che
    # permette di rendere univoco l'output
    def timeStamp(self):
        timestamp = int(time.time())
        string = "_"+ str(timestamp)
        return string

    # Funzione che permette di scrivere un file json
    def write_json_file(self, resultWriteOnJson, path):
        with open(path, "w") as json_file:
            json.dump(resultWriteOnJson, json_file, indent=4)
            return path

    def GenerateInput(self, height, width, startpoints, endpoints, breadcrumbs):
        # Con la riga subito sotto viene instanziato un maze e passati i parametri per effettuare la sua crezione
        p = Maze(height, width, startpoints, endpoints, breadcrumbs)
        # generazione del maze
        p.generate()
        # viene anche creata l'immagine tiff per visualizzare l'esito dei parametri inseriti
        p.getMazeImage()
        # viene convertito la lista di liste in una lista di tuple
        start = [(x[0], x[1]) for x in p.startpoints]
        # il goal viene convertito in tupla
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
        maze, breadcrumbs = p.getValuebleMatrixWithBreadcrumbs()
        # viene convertito il tutto in lista
        maze = maze.tolist()
        # viene istanziato il foundpath
        foundPath = FoundPath(maze, start, goal)
        # viene creato il grafo per poi procedere alla ricerca del path
        foundPath.maze2graph()
        # viene cercato il path all'interno del maze
        foundPath.find_multi_path_astar_return_visited(breadcrumbs)
        # creato il file output json
        foundPath.write_json_file('./outputJsonFile/', 'outputGenerated')
        foundPath.write_json_file_from_dumps(foundPath.getPathRetunrJson(), './output/', 'outputGenerated')


    def ImageInput(self, imagePath):
        #richiamo il metodo per la creazione della cartella di output in caso non esista
        self.ensure_path_exists(self.__destinationFolder)
        # Istanziamo oggetto MAZE
        p = Maze()
        # Funzione per la lettura del file JSON
        p.readMazeImage(imagePath)
        fileNameWithOutExt = self.get_file_name(imagePath) + self.timeStamp()
        self.copyFile(imagePath, self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extTiff)
        fileNameJsonInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extJson
        p.getMazeJson(fileNameJsonInput)
        # Con questa riga vengono convertiti i punti di start
        # da [[0, 29], [19, 60]] in un array di tuple [(0, 29), (19, 60)]
        start = [(x[0], x[1]) for x in p.startpoints]
        # viene settato il goal dai endpoin in una tupla
        goal = tuple(p.endpoints[0])
        # viene presa e assegnata a maze la matrice ritornata dall'analisi
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
        maze, breadcrumps = p.getValuebleMatrixWithBreadcrumbs()
        # il labirinto viene convertito in una lista aggiunte le virgole tra i vari punti
        maze = maze.tolist()
        # Entra in azione la funzione per la ricerca del percorso migliore
        foundPath = FoundPath(maze, start, goal)
        # si procede alla ricerca del path con la funzione che usa l'algoritmo A*
        trovati = foundPath.deikstra()
        # viene fatto output file json e viene preso il path
        fileNameJsonOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extJson
        path = self.write_json_file(trovati, fileNameJsonOutput)
        generateImage = GenerationMazeOutputImage(path)
        keys = generateImage.openJson()
        generateImage.getParamOnTheBestPath(keys)
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        generateImage.createMultiImageForPath(imagePath, fileNameImgOutput, breadcrumps)
        generateImage.createImageForAllPointStart(imagePath, fileNameImgOutput, breadcrumps)

    # Come il processo precedente in questo caso ci si aspetta un JSON in Input
    def JsonInput(self, jsonPath):
        #richiamo il metodo per la creazione della cartella di output in caso non esista
        self.ensure_path_exists(self.__destinationFolder)
        # Istanziamo oggetto MAZE
        p = Maze()
        # Funzione per la lettura del file JSON
        p.readMazeJson(jsonPath)
        fileNameWithOutExt = self.get_file_name(jsonPath) + self.timeStamp()
        self.copyFile(jsonPath, self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extJson)
        fileNameImgInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extTiff
        p.getMazeImage(fileNameImgInput)
        # Con questa riga vengono convertiti i punti di start
        # da [[0, 29], [19, 60]] in un array di tuple [(0, 29), (19, 60)]
        start = [(x[0], x[1]) for x in p.startpoints]
        # viene settato il goal dai endpoin in una tupla
        goal = tuple(p.endpoints[0])
        # viene presa e assegnata a maze la matrice ritornata dall'analisi
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
        maze, breadcrumps = p.getValuebleMatrixWithBreadcrumbs()
        # il labirinto viene convertito in una lista aggiunte le virgole tra i vari punti
        maze = maze.tolist()
        # Entra in azione la funzione per la ricerca del percorso migliore
        foundPath = FoundPath(maze, start, goal)
        # si procede alla ricerca del path con la funzione che usa l'algoritmo A*
        trovati = foundPath.deikstra()
        # viene fatto output file json e viene preso il path
        fileNameJsonOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extJson
        path = self.write_json_file(trovati, fileNameJsonOutput)
        generateImage = GenerationMazeOutputImage(path)
        keys = generateImage.openJson()
        generateImage.getParamOnTheBestPath(keys)
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        generateImage.createImage(fileNameImgInput, fileNameImgOutput, breadcrumps)
