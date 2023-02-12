import json
from PIL import Image, ImageDraw
import random

"""
Classe che immagazzina tutti i percorsi migliori per ogni punto di start e definisce le seguenti funzioni:

- def createImageForAllPointStart(self, pathImgInput, pathImgOutput, breadcrumps) --> funzione che crea l'immagine che con tutti i percorsi
- def createImageForASpecificStartPoint(self, pathImgInput, pathImgOutput, startPoint, breadcrumps) --> funzione che crea l'immagine per un percorso specifico
- def createImageGifForASpecificStartPoint (self, pathImgInput, pathImgOutput, startPoint, breadcrumps) --> funzione che crea l'immagine in formato git per un percorso specifico

N.B. I colori dei percorsi vengono generati randomicamente con la funzione def generateColorLine(self), pertanto, cambiano di volta in volta.
"""

class GenerationMazeOutputImage:

    def __init__(self, jsonFile):
        self.__json = jsonFile
        self.__dataOfJson = None
        self.__percorsi = []
        self.__start = []
        self.__goal = None
        self.__movimentPath = []
        pass

    def getParamOnTheBestPath(self, keys):
        # ciclo per ottenere tutti i percorsi dalla struttura dati
        for i in range(len(keys)):
            #appende il valore "Opzione1" per la chiave corrispondente nella variabile "__dataOfJson" alla lista "__percorsi"
            self.__percorsi.append(self.__dataOfJson[i][keys[i][0]]["Opzione1"])
        # ciclo per estrarre le informazioni su start, goal e il movimento
        for i in range(len(self.__percorsi)):
            # verifica se il valore corrente in "__percorsi" è diverso da "NO WAY!". 
            # Se la condizione è vera, le istruzioni all'interno del blocco "if" verranno eseguite.
            if not self.__percorsi[i] == "NO WAY!":
                #appende il valore per la chiave "start" nel dizionario corrente in "__percorsi" alla lista "__start"
                #La lista "self.__start" viene utilizzata per immagazzinare i valori di "start" per tutti i percorsi che non sono "NO WAY!"
                self.__start.append(self.__percorsi[i]["start"])
                #assegna il valore per la chiave "goal" nel dizionario corrente in "__percorsi" alla variabile "__goal"
                self.__goal = self.__percorsi[i]["goal"]
                #appende il valore per la chiave "movimentPath" nel dizionario corrente in "__percorsi" alla lista "__movimentPath"
                #La lista "self.__movimentPath" viene utilizzata per immagazzinare i valori di "movimentPath" per tutti i percorsi che non sono "NO WAY!"
                self.__movimentPath.append(self.__percorsi[i]["movimentPath"])
            else:
                # caso in cui non esiste un percorso
                self.__movimentPath.append("NO WAY!")

    #Questa funzione tramite random
    #genere RGB output random
    def generateColorLine(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        #Aggiunta eliminazione scala grey e nero e bianco
        if r != g or r != b or g != b:
            return (r, g, b)


    #Grey Scale restituisce il grigio per il
    #breadcrumps che si sta analizzando
    #la moltiplicazione è dovuta al fatto che il value
    #corrisponde al value che è presente nel matrix che è
    #il costo del passo aggiuntivo
    def generateGreyScale(self, value):
        value = value * 16
        return (value, value, value)

    #Per la stampa dell'immagine bisogna invertire le cordinate
    #dei vari punti del path percors
    def invert_coordinates(self, point):
        x, y = point
        return (y, x)

    def createImageForAllPointStart(self, pathImgInput, pathImgOutput, breadcrumps):
        # Apro l'immagine in input
        im = Image.open(pathImgInput)
        # Inizializzo l'oggetto per disegnare sull'immagine
        draw = ImageDraw.Draw(im)
        # Definisco il colore per il punto goal
        colorGoal = (255, 0, 0)
        # Ciclo su ogni movimentPath presente nella lista
        for i in range(len(self.__movimentPath)):
            # Se il movimentPath non è "NO WAY!", disegno una linea
            if not self.__movimentPath[i] == "NO WAY!":
                # Trasformo i dati del movimentPath in un formato adatto per disegnare una linea
                tuple_data = [(x[1], x[0]) for x in self.__movimentPath[i]]
                # Genero un colore casuale per la linea
                color = self.generateColorLine()
                # Disegno la linea
                draw.line(tuple_data, fill=color)
        # Disegno il punto goal
        draw.point(self.invert_coordinates(self.__goal), fill=colorGoal)
        # Trasformo i dati del breadcrumps in un formato adatto per disegnare un punto
        converted_data = [(point[::-1], value) for point, value in breadcrumps]
        # Ciclo su ogni punto nel breadcrumps
        for i in range(len(converted_data)):
            # Disegno ogni punto del breadcrumps
            draw.point(converted_data[i][0], self.generateGreyScale(converted_data[i][1]))
        # Salvo l'immagine risultante
        im.save(pathImgOutput)

    def createImageForASpecifcStartPoint(self, pathImgInput, pathImgOutput, startPoint, breadcrumps):
        # Apre l'immagine presente nel percorso specificato
        im = Image.open(pathImgInput)
        # Crea un oggetto disegno per l'immagine aperta
        draw = ImageDraw.Draw(im)
        # Colore rosso per il punto finale
        colorGoal = (255, 0, 0)

        # Se il percorso esiste per il punto di partenza specificato
        if not self.__movimentPath[startPoint] == "NO WAY!":
            # Converte i punti del percorso in un formato adatto per il disegno
            tuple_data = [(x[1], x[0]) for x in self.__movimentPath[startPoint]]
            # Genera un colore casuale per la linea del percorso
            color = self.generateColorLine()
            # Disegna la linea del percorso con il colore generato
            draw.line(tuple_data, fill=color)
            # Disegna il punto finale con il colore rosso
            draw.point(self.invert_coordinates(self.__goal), fill=colorGoal)
            # Inverte le coordinate dei punti dei segnalini per adattarli al disegno
            converted_data = [(point[::-1], value) for point, value in breadcrumps]
            # Per ogni punto dei segnalini
            for i in range(len(converted_data)):
                # Disegna il punto con una scala di grigio calcolata in base alla sua importanza
                draw.point(converted_data[i][0], self.generateGreyScale(converted_data[i][1]))
            # Salva l'immagine modificata nel percorso specificato
            im.save(pathImgOutput)


    #Aggiunta possibilità di ritornare una gif image
    def createImageGifForASpecifcStartPoint(self, pathImgInput, pathImgOutput, startPoint, breadcrumps):
        # Apre l'immagine presente nel percorso specificato
        im = Image.open(pathImgInput)
        # Crea un oggetto disegno per l'immagine aperta
        draw = ImageDraw.Draw(im)
        # Colore rosso per il punto finale
        colorGoal = (255, 0, 0)
        # Lista per salvare tutti i frame della gif animata
        frames = []

        # Se il percorso esiste per il punto di partenza specificato
        if not self.__movimentPath[startPoint] == "NO WAY!":
            # Converte i punti del percorso in un formato adatto per il disegno
            tuple_data = [(x[1], x[0]) for x in self.__movimentPath[startPoint]]
            # Genera un colore casuale per la linea del percorso
            color = self.generateColorLine()
            # Inverte le coordinate dei punti dei segnalini per adattarli al disegno
            converted_data = [(point[::-1], value) for point, value in breadcrumps]

            # Per ogni punto nel percorso
            for i in range(len(tuple_data) - 1):
                # Crea una copia dell'immagine di base
                im_frame = im.copy()
                # Crea un nuovo oggetto disegno per la copia dell'immagine
                draw_frame = ImageDraw.Draw(im_frame)
                # Disegna la linea del percorso fino al punto corrente
                draw_frame.line(tuple_data[:i + 1], fill=color)
                # Disegna il punto finale con il colore rosso
                draw_frame.point(self.invert_coordinates(self.__goal), fill=colorGoal)
                # Per ogni punto dei segnalini
                for j in range(len(converted_data)):
                    # Disegna il punto con una scala di grigio calcolata in base alla sua importanza
                    draw_frame.point(converted_data[j][0], self.generateGreyScale(converted_data[j][1]))
                # Aggiungi il frame corrente alla lista dei frame
                frames.append(im_frame)

            # Genera la gif animata dalla lista dei frame
            frames[0].save(pathImgOutput, format='gif', save_all=True, append_images=frames[1:], duration=100, loop=0)

    #Nella sezione sotto vengono caricati i dati dal file json che è stato scritto
    #A seguito della ricerca effettuata con l'algoritmo di Dijkstra
    def openJson(self):
        # Apre il file JSON specificato in __json
        with open(self.__json) as json_file:
            # Carica i dati del file JSON
            data = json.load(json_file)
            # Assegna i dati del file JSON alla variabile d'istanza __dataOfJson
            self.__dataOfJson = data
            # Inizializza una lista vuota per le chiavi
            myKeys = []
            # Loop sui dati per ottenere le chiavi
            for i in range(len(data)):
                # Aggiungi la chiave corrente alla lista di chiavi
                myKeys.append(list(data[i]))
            # Restituisce la lista di chiavi
            return myKeys
