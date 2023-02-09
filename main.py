#TODO importantissimo fix di tutti i try except all'interno di tutto il codice per evitare troppi errori

from utilities.menuOption import menuOption
from utilities.funzioni_finali import *
import os
from sys import exit,argv
from getopt import getopt

"""
Il progetto che segue è stato realizzato da un gruppo di stundeti dell'università campus bio medico di roma
che frequentano il corso di Ingegneria dei sistemi intelligenti.
Il prodotto che segue è il progetto per concludere lo studio nel corso di Programmazione del primo anno primo semestre
La richiesta era quella di creare un progra1mma in grado di leggere un labirinto o da un immagine o da un file json.
Il codice presente è stato realizzato dai seguenti studentxwi:
    - Calandra Vincenzo Maria
    - Fiorio Federico
    - Papa Eleonora
    
con la supervisione dei docenti:
    - Iannello Giulio
    - Esposito Marcello
    
"""

"""Qui subito di seguito viene creato il menù che viene mostrato a terminale"""
def main_menu():
    print("Main Menu:")
    print("1. Create maze")
    print("2. Upload image")
    print("3. Upload JSON")
    print("4. Exit")
    menu = menuOption()
    choice = int(input("Enter your choice: "))

    #Il controllo che segue identifica che sottoprogramma lanciare per eseguire il codice
    if choice == 1:
        create_maze(menu)
    elif choice == 2:
        upload_image(menu)
    elif choice == 3:
        upload_json(menu)
    elif choice == 4:
        exit()
    else:
        print("Invalid choice. Please try again.")
    
    main_menu()
  

def create_maze(menu):
    height = int(input("Insert the height of the maze: "))
    width = int(input("Insert the width of the maze: "))
    #viene istanziato lo startPoint a vuoto in quanto viene richiesto
    # una lista di liste questo permette di fare l'inserimento iniziale e subito dopo aggiunto alla
    # lista successiva tramite append
    startPoint = []
    start = list(map(int, input("Insert the start point as a list: ").split()))
    startPoint.append(start)
    #il while permette di inserire molti punti di partenza
    while True:
        add_start = input("Do you want to add another start point? (yes/no): ")
        if add_start == 'no':
            break
        start = list(map(int, input("Insert the start point as a list: ").split()))
        startPoint.append(start)

    # da richiesta è stato definto un solo endpoint goal all'interno del labirinto
    goal = list(map(int, input("Insert the goal point as a list: ").split()))
    goal = [goal]

    #breadcrumps sono i tasselli di grigio che vengono posti in mezzo al labirinto nel percorso che si dovrà effettuare.
    # questi possono assumere valori da 0 a 256 e ogni valore avrà una tonalità e un peso differente
    breadcrumps = []
    add_breadcrumps = int(input("Do you want to add breadcrumps? (0/1): "))
    while add_breadcrumps:
        bc = list(map(int, input("Insert the breadcrump (x y weight): ").split()))
        breadcrumps.append(bc)
        add_breadcrumps = int(input("Do you want to add another breadcrump? (0/1): "))
    #tutti i dati inseriti dall'utente vengono passati
    menu.GenerateInput(height, width, startPoint, goal, breadcrumps)


#Funzione che permette di verificare che il file corrisponda a quello richiesto
def check_file_extension(file_path, extension):
    # Get the file name and extension
    file_name, file_ext = os.path.splitext(file_path)

    # Check if the extension matches the expected extension
    return file_ext.lower() == extension.lower()


def upload_image(menu):
    #caricamento di un tiff in un while che verifica se si tratta davvero di un tiff file
    while True:
        path = input("Enter the path of the image on tiff: ")
        if check_file_extension(path, '.tiff'):
            # Aggiunto un try except per evitare l'interruzione del programma per errori dell'utente
            menu.ImageInput(path)
        else:
            print("Incorrect file th extension is not tiff, please enter the correct file path.")

def upload_json(menu):
    #caricamento di un json file all'interno di un while che controlla se si tratta di un json
    while True:
        path = input("Enter the path of the json file: ")
        if check_file_extension(path,'.json'):
            #Aggiunto un try except per evitare l'interruzione del programma per errori dell'utente
            menu.JsonInput(path)
                #print("The file doesn't exist or the path is wrong")
        else:
            print("Incorrect file extension is not json, please enter the correct file path.")


if __name__ == "__main__":

    heigth=0
    width=0
    breadcrumbs=[]
    startpoints=[]
    endpoint=[]
    generate=True
    tiff_path=""
    json_path=""
    it =False
    argv = argv[1:]

    # try:
    #     options, args = getopt(argv, "i:h:w:s:e:b:g:tp:jp",
    #                             ["interactive=",
    #                             "height=",
    #                             "width=",
    #                             "startpoints=",
    #                             "endpoint=",
    #                             "breadcrumbs=",
    #                             "generate=",
    #                             "tiff-path=",
    #                             "json-path="])
    # except:
    #     print("Invalid parameters")
    
    # for name, value in options:
    #     if name in ['-i', '--interactive']:
    #         it = True
    #     elif name in ['-h', '--height']:
    #         height = value
    #     elif name in ['-w', '--width']:
    #         width = value
    #     elif name in ['-s', '--startpoints']:
    #         startpoints = value
    #     elif name in ['-e', '--endpoint']:
    #         endpoint = value
    #     elif name in ['-b', '--breadcrumbs']:
    #         breadcrumbs = value
    #     elif name in ['-g', '--generate']:
    #         generate = value
    #     elif name in ['-tp', '--json-path']:
    #         generate = value
    #     elif name in ['-jp', '--tiff-path']:
    #         generate = value
    
    # print(options)

    import argparse
    from typing import List
    parser = argparse.ArgumentParser(prog='maze', description='Create,read and solve a maze.')
    parser.add_argument('-i', '--interactive', action='store_true',
                        help="Start an interactive session.")
    parser.add_argument('-sp', '--startpoints', nargs="+", type=int,
                        description="Must be a sequence of two digit")
    parser.add_argument('-ep', '--endpoint', nargs="+", type=int,
                        description="Must be a sequence of two digit")
    args = parser.parse_args()
    print(args.startpoints)
        
    

    