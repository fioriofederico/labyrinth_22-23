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
        self.__extGif = '.gif'
        pass

    #Funzione di copia di un file
    def copyFile(self, pathOrign, pathDestination):
        shutil.copy(pathOrign, pathDestination)

    # Funzione per prendere solo il nome del file che viene passatto da terminale
    def get_file_name(self, file_path):
        return file_path.split("/")[-1].split(".")[0]

    def calculate_time_taken(self, start_time, end_time):
        time_taken = end_time - start_time
        return time_taken

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

    def GenerateInput(self, height, width, startpoints, endpoints, breadcrumps):
        startTime = time.time()
        self.ensure_path_exists(self.__destinationFolder)
        # Con la riga subito sotto viene instanziato un maze e passati i parametri per effettuare la sua crezione
        p = Maze(height, width, startpoints, endpoints, breadcrumps)
        # generazione del maze
        p.generate()
        # viene anche creata l'immagine tiff per visualizzare l'esito dei parametri inseriti
        fileNameWithOutExt = "mazeGenerated" + str(height) + "_" + str(width) + self.timeStamp()
        fileNameImgInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extTiff
        p.getMazeImage(fileNameImgInput)
        fileNameJsonInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extJson
        p.getMazeJson(fileNameJsonInput)
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
        maze, breadcrumps = p.getValuebleMatrixWithBreadcrumbs()
        # viene convertito il tutto in lista
        maze = maze.tolist()
        # viene istanziato il foundpath
        foundPath = FoundPath(maze, start, goal)
        # si procede alla ricerca del path con la funzione che usa l'algoritmo A*
        trovati = foundPath.deikstra()
        # viene fatto output file json e viene preso il path
        fileNameJsonOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extJson
        path = self.write_json_file(trovati, fileNameJsonOutput)
        generateImage = GenerationMazeOutputImage(path)
        keys = generateImage.openJson()
        generateImage.getParamOnTheBestPath(keys)
        if len(start) > 1:
            for i in range(len(start)):
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extTiff
                generateImage.createImageForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extGif
                generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
        elif len(start) == 1:
            fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extGif
            generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, 0, breadcrumps)
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        generateImage.createImageForAllPointStart(fileNameImgInput, fileNameImgOutput, breadcrumps)
        end = time.time()
        print("Time taken: " + str(self.calculate_time_taken(startTime, end)) + " seconds")

    def ImageInput(self, imagePath):
        startTime = time.time()
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
        if len(start) > 1:
            for i in range(len(start)):
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extTiff
                generateImage.createImageForASpecifcStartPoint(imagePath, fileNameImgOutput, i, breadcrumps)
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extGif
                generateImage.createImageGifForASpecifcStartPoint(imagePath, fileNameImgOutput, i, breadcrumps)
        elif len(start) == 1:
            fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extGif
            generateImage.createImageGifForASpecifcStartPoint(imagePath, fileNameImgOutput, 0, breadcrumps)
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        generateImage.createImageForAllPointStart(imagePath, fileNameImgOutput, breadcrumps)
        end = time.time()
        print("Time taken: " + str(self.calculate_time_taken(startTime, end)) + " seconds")

    # Come il processo precedente in questo caso ci si aspetta un JSON in Input
    def JsonInput(self, jsonPath):
        startTime = time.time()
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
        if len(start) > 1:
            for i in range(len(start)):
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extTiff
                generateImage.createImageForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extGif
                generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
        elif len(start) == 1:
            fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extGif
            generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, 0, breadcrumps)
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        generateImage.createImageForAllPointStart(fileNameImgInput, fileNameImgOutput, breadcrumps)
        end = time.time()
        print("Time taken: " + str(self.calculate_time_taken(startTime, end)) + " seconds")

    def scan(self) -> None:
        condition = True
        while condition:
            for file in os.listdir("./indata"):
                if file.endswith(".json"):
                    self.JsonInput(os.path.join("./indata", file))
                elif file.endswith(".tiff"):
                    self.ImageInput(os.path.join("./indata", file))
                os.remove(os.path.join("./indata", file))

                    
