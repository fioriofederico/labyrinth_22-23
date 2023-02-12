import os
import shutil
import time

from utilities.maze import Maze
from utilities.foundPath import FoundPath
import json
from utilities.generationMazeOutputImage import GenerationMazeOutputImage

"""
Classe che permette di prendere in input:

- def GenerateInput(self, height, width, starpoints, endpoints, breadcrumps) --> funzione di creazione maze
- def ImageInput(self, imagePath) --> funzione di caricamento immagine
- def JsonInput(self, jsonPath) --> funzione di caricamento json

E restituisce in output l'immagine in formato tiff di tutti i percorsi possibili per ogni punto di start e un'immagine in formato tiff e gif per ogni percorso.

N.B. Nel caso di un solo punto di start restituirà solo l'immagine in formato gif
"""

class menuOption:
    pass

    def __init__(self):
        self.__destinationFolder = './output/'
        self.__extTiff = '.tiff'
        self.__extJson = '.json'
        self.__extGif = '.gif'
        pass

    #Funzione che copia un file da un percorso di origine a un percorso di destinazione.
    def copyFile(self, pathOrign, pathDestination):
        #copia il file da origine a destinazione sostituendo il file se già ne esiste uno con il nome uguale.
        shutil.copy(pathOrign, pathDestination)

    # Funzione per prendere solo il nome del file che viene passatto da terminale, senza la sua estensione
    def get_file_name(self, file_path):
        return file_path.split("/")[-1].split(".")[0]

    #Funzione che calcola il tempo trascorso tra due momenti.
    def calculate_time_taken(self, start_time, end_time):
        #time_taken viene calcolata come la differenza tra end_time e start_time
        time_taken = end_time - start_time
        return time_taken

    # Funzione che verifica se esiste il path di destinazione
    def ensure_path_exists(self, file_path):
        #La variabile directory è la directory che contiene il file specificato da file_path
        directory = os.path.dirname(file_path)
        # se il controllo fallisce e la directory specificata non esiste...
        if not os.path.exists(directory):
            # ...creazione della directory che non esisteva
            os.makedirs(directory)

    # Con questa funzione avvalendosi del timestamp viene concetenato al nome del file una stringa timestemp che
    # permette di rendere univoco l'output
    def timeStamp(self):
        #La variabile timestamp è l'ora corrente della data di riferimento
        timestamp = int(time.time())
        #string viene creata come una stringa composta dal carattere "_" seguito dal valore di timestamp convertito in stringa
        string = "_"+ str(timestamp)
        return string

    # Funzione che permette di scrivere un file json
    def write_json_file(self, resultWriteOnJson, path):
        #apre il file specificato da path, per la scrittura, come json_file
        with open(path, "w") as json_file:
            #scrive il contenuto di resultWriteOnJson nel file aperto
            json.dump(resultWriteOnJson, json_file, indent=4)
            return path

    #Funzione che genera un input (opzione 1 create maze), per un'immagine e un file JSON, per un labirinto
    def GenerateInput(self, height, width, startpoints, endpoints, breadcrumps):
        #imposta il tempo di inizio dell'operazione di generazione dell'input
        startTime = time.time()
        #controlla se il percorso specificato per la cartella di destinazione esiste, e se non esiste, lo crea
        self.ensure_path_exists(self.__destinationFolder)
        #Viene instanziato un maze e passati i parametri per effettuare la sua creazione
        p = Maze(height, width, startpoints, endpoints, breadcrumps)
        # generazione del maze
        p.generate()
        #crea un nome file composto da "mazeGenerated", dalle dimensioni dell'altezza e della larghezza e dal timestamp corrente
        fileNameWithOutExt = "mazeGenerated" + str(height) + "_" + str(width) + self.timeStamp()
        #crea un nome file dell'immagine di input, composto dalla cartella di destinazione, "input_", il nome del file senza estensione e l'estensione .tiff
        fileNameImgInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extTiff
        #richiama metodo getMazeImage sull'istanza p, passando il file dell'immagine di input, per ottenere l'immagine del labirinto
        p.getMazeImage(fileNameImgInput)
        #crea un nome file JSON di input, composto dalla cartella di destinazione, "input_", il nome del file senza estensione e l'estensione .json
        fileNameJsonInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extJson
        #richiama metodo getMazeJson sull'istanza p, passando il file del JSON di input, per ottenere il file JSON del labirinto
        p.getMazeJson(fileNameJsonInput)
        # viene convertito la lista di liste in una lista di tuple
        start = [(x[0], x[1]) for x in p.startpoints]
        # converte l'elemento alla posizione 0 della lista "p.endpoints" in una tupla e la assegna alla variabile "goal"
        goal = tuple(p.endpoints[0])
        # si richiama la struttura matrice del labirinto
        """ con la riga numero 63 avvalendosi del sistema di ricerca di numpy all'interno
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
        # converte la matrice del labirinto in una lista
        maze = maze.tolist()
        # viene istanziato il FoundPath che viene utilizzato per trovare il percorso più breve
        foundPath = FoundPath(maze, start, goal)
        # si procede alla ricerca del path più breve con la funzione che usa l'algoritmo A*
        trovati = foundPath.deikstra()
        # crea il nome per il file JSON di output
        fileNameJsonOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extJson
        #scrive i dati del percorso trovato in un file JSON con il nome specificato dalla funzione sopra
        path = self.write_json_file(trovati, fileNameJsonOutput)
        # viene istanzato il GenerationMazeOutputImage con il percorso trovato
        generateImage = GenerationMazeOutputImage(path)
        #apre il file JSON con i dati sul percorso più breve trovato
        keys = generateImage.openJson()
        #utilizza i dati sul percorso più breve trovato per creare un'immagine del labirinto (con tale percorso evidenziato)
        generateImage.getParamOnTheBestPath(keys)
        #Se ci sono più punti di partenza...
        if len(start) > 1:
            #...viene eseguito un ciclo for per ognuno di questi punti di partenza
            for i in range(len(start)):
                #crea un nome per il file tiff di output che include la cartella di destinazione, "output", il nome del file senza estensione,
                #un indice che rappresenta un punto di partenza specifico e l'estensione .tiff
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extTiff
                #crea un'immagine tiff per il punto di partenza specifico
                generateImage.createImageForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
                #crea un nome per il file GIF di output
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extGif
                #crea un'immagine gif per il punto di partenza specifico
                generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
        #se c'è un solo punto di partenza
        elif len(start) == 1:
            #crea un nome per l'immagine gif di output
            fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extGif
            #crea un'immagine gif per il punto di partenza
            generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, 0, breadcrumps)
        #crea un nome per il file tiff di output
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        #crea un'immagine tiff che rappresenta tutti i percorsi migliori trovati per ogni punto di partenza
        generateImage.createImageForAllPointStart(fileNameImgInput, fileNameImgOutput, breadcrumps)
        #registra il tempo di fine del processo di creazione del labirinto
        end = time.time()
        #stampa il tempo impiegato per generare l'output (tempo trascorso dall'inizio alla fine del processo)
        print("Time taken: " + str(self.calculate_time_taken(startTime, end)) + " seconds")

    def ImageInput(self, imagePath):
        #imposta il tempo di inizio dell'operazione di generazione dell'input
        startTime = time.time()
        #richiamo il metodo per la creazione della cartella di output in caso non esista
        self.ensure_path_exists(self.__destinationFolder)
        # Istanziamo oggetto MAZE
        p = Maze()
        # Funzione per la lettura del file JSON
        p.readMazeImage(imagePath)
        #crea un nome file composto dal nome dell'immagine senza estensione (richiamato da get_file_name) e dal timestamp corrente
        fileNameWithOutExt = self.get_file_name(imagePath) + self.timeStamp()
        #richiama la funzione copyFile per copiare il file immagine di input nella cartella di destinazione con nome composto "input", nome file definito sopra e estensione .tiff
        self.copyFile(imagePath, self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extTiff)
        #crea nome file JSON di input composto da cartella di destinazione, "input", nome del file definito sopra e estensione .json
        fileNameJsonInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extJson
        #crea un file json con dentro le informazioni sul labirinto
        p.getMazeJson(fileNameJsonInput)
        # Con questa riga vengono convertiti i punti di start
        # da [[0, 29], [19, 60]] in un array di tuple [(0, 29), (19, 60)]
        start = [(x[0], x[1]) for x in p.startpoints]
        # converte l'elemento alla posizione 0 della lista "p.endpoints" in una tupla e la assegna alla variabile "goal"
        goal = tuple(p.endpoints[0])
        # viene presa e assegnata a maze la matrice ritornata dall'analisi (ottengo il labirinto sottoforma di matrice)
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
        # il labirinto viene convertito in una lista (aggiunte le virgole tra i vari punti)
        maze = maze.tolist()
        # viene istanziato il FoundPath che viene utilizzato per trovare il percorso più breve
        foundPath = FoundPath(maze, start, goal)
        # si procede alla ricerca del path più breve con la funzione che usa l'algoritmo A*
        trovati = foundPath.deikstra()
        # crea il nome per il file JSON di output
        fileNameJsonOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extJson
        #scrive i dati del percorso trovato in un file JSON con il nome specificato dalla funzione sopra
        path = self.write_json_file(trovati, fileNameJsonOutput)
        #viene istanzato il GenerationMazeOutputImage con il percorso trovato
        generateImage = GenerationMazeOutputImage(path)
        #apre il file JSON con i dati sul percorso più breve trovato
        keys = generateImage.openJson()
        #utilizza i dati sul percorso più breve trovato per creare un'immagine del labirinto (con tale percorso evidenziato)
        generateImage.getParamOnTheBestPath(keys)
        #Se ci sono più punti di partenza...
        if len(start) > 1:
            for i in range(len(start)):
                #crea un nome per il file tiff di output che include la cartella di destinazione, "output", il nome del file senza estensione,
                #un indice che rappresenta un punto di partenza specifico e l'estensione .tiff
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extTiff
                #crea un'immagine tiff per il punto di partenza specifico
                generateImage.createImageForASpecifcStartPoint(imagePath, fileNameImgOutput, i, breadcrumps)
                #crea un nome per il file GIF di output
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extGif
                #crea un'immagine gif per il punto di partenza specifico
                generateImage.createImageGifForASpecifcStartPoint(imagePath, fileNameImgOutput, i, breadcrumps)
        #se c'è un solo punto di partenza
        elif len(start) == 1:
            #crea un nome per l'immagine gif di output
            fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extGif
            #crea un'immagine gif per il punto di partenza
            generateImage.createImageGifForASpecifcStartPoint(imagePath, fileNameImgOutput, 0, breadcrumps)
        #crea un nome per il file tiff di output
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        #crea un'immagine tiff che rappresenta tutti i percorsi migliori trovati per ogni punto di partenza
        generateImage.createImageForAllPointStart(imagePath, fileNameImgOutput, breadcrumps)
        #registra il tempo di fine del processo di creazione del labirinto
        end = time.time()
        #stampa il tempo impiegato per generare l'output (tempo trascorso dall'inizio alla fine del processo)
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
        #crea un nome file composto dal nome dell'immagine senza estensione (richiamato da get_file_name) e dal timestamp corrente
        fileNameWithOutExt = self.get_file_name(jsonPath) + self.timeStamp()
        #richiama la funzione copyFile per copiare il file json di input nella cartella di destinazione con nome composto "input", nome file definito sopra e estensione .json
        self.copyFile(jsonPath, self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extJson)
        #crea nome file immagine di input composto da cartella di destinazione, "input", nome del file definito sopra e estensione .tiff
        fileNameImgInput = self.__destinationFolder + "input_" + fileNameWithOutExt + self.__extTiff
        #richiama metodo getMazeImage sull'istanza p, passando il file dell'immagine di input, per ottenere l'immagine del labirinto
        p.getMazeImage(fileNameImgInput)
        # Con questa riga vengono convertiti i punti di start
        # da [[0, 29], [19, 60]] in un array di tuple [(0, 29), (19, 60)]
        start = [(x[0], x[1]) for x in p.startpoints]
        # converte l'elemento alla posizione 0 della lista "p.endpoints" in una tupla e la assegna alla variabile "goal"
        goal = tuple(p.endpoints[0])
        # viene presa e assegnata a maze la matrice ritornata dall'analisi (ottengo il labirinto sottoforma di matrice)
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
        # il labirinto viene convertito in una lista (aggiunte le virgole tra i vari punti)
        maze = maze.tolist()
        # viene istanziato il FoundPath che viene utilizzato per trovare il percorso più breve
        foundPath = FoundPath(maze, start, goal)
        # si procede alla ricerca del path più breve con la funzione che usa l'algoritmo A*
        trovati = foundPath.deikstra()
        # crea il nome per il file JSON di output
        fileNameJsonOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extJson
        #scrive i dati del percorso trovato in un file JSON con il nome specificato dalla funzione sopra
        path = self.write_json_file(trovati, fileNameJsonOutput)
        #viene istanzato il GenerationMazeOutputImage con il percorso trovato
        generateImage = GenerationMazeOutputImage(path)
        #apre il file JSON con i dati sul percorso più breve trovato
        keys = generateImage.openJson()
        #utilizza i dati sul percorso più breve trovato per creare un'immagine del labirinto (con tale percorso evidenziato)
        generateImage.getParamOnTheBestPath(keys)
        #Se ci sono più punti di partenza...
        if len(start) > 1:
            for i in range(len(start)):
                #crea un nome per il file tiff di output che include la cartella di destinazione, "output", il nome del file senza estensione,
                #un indice che rappresenta un punto di partenza specifico e l'estensione .tiff
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extTiff
                #crea un'immagine tiff per il punto di partenza specifico
                generateImage.createImageForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
                #crea un nome per il file GIF di output
                fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + "_" + str(i) + self.__extGif
                #crea un'immagine gif per il punto di partenza specifico
                generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, i, breadcrumps)
        #se c'è un solo punto di partenza
        elif len(start) == 1:
            #crea un nome per l'immagine gif di output
            fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extGif
            #crea un'immagine gif per il punto di partenza
            generateImage.createImageGifForASpecifcStartPoint(fileNameImgInput, fileNameImgOutput, 0, breadcrumps)
        #crea un nome per il file tiff di output
        fileNameImgOutput = self.__destinationFolder + "output_" + fileNameWithOutExt + self.__extTiff
        #crea un'immagine tiff che rappresenta tutti i percorsi migliori trovati per ogni punto di partenza
        generateImage.createImageForAllPointStart(fileNameImgInput, fileNameImgOutput, breadcrumps)
        #registra il tempo di fine del processo di creazione del labirinto
        end = time.time()
        #stampa il tempo impiegato per generare l'output (tempo trascorso dall'inizio alla fine del processo)
        print("Time taken: " + str(self.calculate_time_taken(startTime, end)) + " seconds")

    def scan(self) -> None:
        #il ciclo while continuerà a eseguire il codice finché la variabile condition è vera
        condition = True
        while condition:
            #accede alla directory "./indata" e restituisce tutti i file presenti nella directory
            for file in os.listdir("./indata"):
                #controlla se il file termina con l'estensione ".json"
                if file.endswith(".json"):
                    #se si, richiama la funzione JsonInput() passando il percorso completo del file come argomento
                    self.JsonInput(os.path.join("./indata", file))
                #controlla se il file termina con l'estensione ".tiff"
                elif file.endswith(".tiff"):
                    #se si, richiama la funzione ImageInput() passando il percorso completo del file come argomento
                    self.ImageInput(os.path.join("./indata", file))
                #Rimuove il file dalla directory "./indata"
                os.remove(os.path.join("./indata", file))

                    
