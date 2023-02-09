#TODO importantissimo fix di tutti i try except all'interno di tutto il codice per evitare troppi errori

from utilities.menuOption import menuOption
from utilities.funzioni_finali import *
import os
from sys import exit
import argparse

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

    condition = True
    while condition:
        try:
            choice = int(input("Enter your choice: "))
            if choice > 0 and choice < 5:
                break
            else:
                raise ValueError(f"Invalid choice: {choice}")
        except ValueError as e:
            print(e)

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

    condition = True

    while condition:
        try:
            height = int(input("Insert the height of the maze: "))
            condition = False
        except ValueError as e:
            print(e)
    
    condition = True
    while condition:
        try:
            width = int(input("Insert the width of the maze: "))
            condition = False
        except ValueError as e:
            print(e)
    #viene istanziato lo startPoint a vuoto in quanto viene richiesto
    # una lista di liste questo permette di fare l'inserimento iniziale e subito dopo aggiunto alla
    # lista successiva tramite append
    condition = True
    startPoint = []
    while condition:
        try:
            start = list(map(int, input("Insert the start point as a list: ").split()))
            startPoint.append(start)
            condition = False
        except ValueError as e:
            print(e)

    #il while permette di inserire molti punti di partenza
    condition = True
    while condition:
        try:
            add_start = (input("Do you want to add another start point? (yes/no): ")).strip()
            if add_start == 'no':
                break
            elif add_start == 'yes':
                start = list(map(int, input("Insert the start point as a list: ").split()))
                startPoint.append(start)
                continue
            else:
                raise ValueError(f"Invalid choice: {add_start}")
        except ValueError as e:
            print(e)

    # da richiesta è stato definto un solo endpoint goal all'interno del labirinto

    condition = True
    while condition:
        try:
            goal = list(map(int, input("Insert the goal point as a list: ").split()))
            goal = [goal]
            condition = False
        except ValueError as e:
            print(e)

    #breadcrumps sono i tasselli di grigio che vengono posti in mezzo al labirinto nel percorso che si dovrà effettuare.
    # questi possono assumere valori da 0 a 256 e ogni valore avrà una tonalità e un peso differente
    breadcrumps = []
    condition = True
    while condition:
        try:
            add_breadcrumps = (input("Do you want to add breadcrumps? (yes/no): ")).strip()
            if add_breadcrumps == 'no':
                condition = False
            elif add_breadcrumps == 'yes':
                break
            else:
                raise ValueError(f"Invalid choice: {add_start}")
        except ValueError as e:
            print(e)

    while condition:
        try:
            bc = list(map(int, input("Insert the breadcrump (x y weight): ").split()))
            breadcrumps.append(bc)
            add_breadcrumps = (input("Do you want to add another breadcrump? (yes/no): ")).strip()
            if add_breadcrumps == 'no':
                condition = False
            elif add_breadcrumps == 'yes':
                continue
            else:
                raise ValueError(f"Invalid choice: {add_start}")
        except ValueError as e:
            print(e)

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
    condition = True
    while condition:
        try:
            path = input("Enter the path of the image on tiff: ")
            if check_file_extension(path, '.tiff'):
                # Aggiunto un try except per evitare l'interruzione del programma per errori dell'utente
                menu.ImageInput(path)
                condition = False
            else:
                raise ValueError("Incorrect file th extension is not tiff, please enter the correct file path.")
        except ValueError as e:
            print(e)
        

def upload_json(menu):
    #caricamento di un json file all'interno di un while che controlla se si tratta di un json
    condition = True

    while condition:
        try:
            path = input("Enter the path of the json file: ")
            if check_file_extension(path,'.json'):
                #Aggiunto un try except per evitare l'interruzione del programma per errori dell'utente
                menu.JsonInput(path)
                condition = False
                #print("The file doesn't exist or the path is wrong")
            else:
                raise ValueError("Incorrect file extension is not json, please enter the correct file path.")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(prog='maze', description='Create,read and solve a maze.')
    parser.add_argument('-it', '--interactive', action='store_true',
                        help="Start an interactive session.")
    parser.add_argument('-g', '--generate', action='store_true',
                        help="Generate a maze.")
    parser.add_argument('-sp', '--startpoints', nargs="+", type=int,
                        help="Must be a sequence of two digit")
    parser.add_argument('-ep', '--endpoint', nargs="+", type=int,
                        help="Must be a sequence of two digit")
    parser.add_argument('-bc', '--breadcrumbs', nargs="+", type=int,
                        help="Must be a sequence of 3 digit")
    parser.add_argument('-he', '--heigth', type=int,
                        help="Must be a digit")
    parser.add_argument('-w', '--width', type=int,
                        help="Must be a digit")
    parser.add_argument('-tp', '--tiff-path',
                        help="Must be a path to a tiff file")
    parser.add_argument('-jp', '--json-path',
                        help="Must be a path to a json file")
    
    args = parser.parse_args()
    print(args)
    if args.interactive == True:
        main_menu()
    else:
        menu = menuOption()
        if args.generate == True:
            menu.GenerateInput(args.heigth, args.width, [args.startpoints], [args.endpoint], [args.breadcrumbs])
        elif args.tiff_path != None:
            if check_file_extension(args.tiff_path, '.tiff'):
                # Aggiunto un try except per evitare l'interruzione del programma per errori dell'utente
                menu.ImageInput(args.tiff_path)
            else:
                print("Incorrect file th extension is not tiff, please enter the correct file path.")
        elif args.json_path != None:
            if check_file_extension(args.json_path,'.json'):
                #Aggiunto un try except per evitare l'interruzione del programma per errori dell'utente
                menu.JsonInput(args.json_path)
                    #print("The file doesn't exist or the path is wrong")
            else:
                print("Incorrect file extension is not json, please enter the correct file path.")


        
    

    