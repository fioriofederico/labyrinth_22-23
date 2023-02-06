#TODO importantissimo fix di tutti i try except all'interno di tutto il codice per evitare troppi errori
import argparse
from utilities.menuOption import menuOption
import os
"""
Il progetto che segue è stato realizzato da un gruppo di stundeti dell'università campus bio medico di roma
che frequentano il corso di Ingegneria dei sistemi intelligenti.
Il prodotto che segue è il progetto per concludere lo studio nel corso di Programmazione del primo anno primo semestre
La richiesta era quella di creare un programma in grado di leggere un labirinto o da un immagine o da un file json.
Il codice presente è stato realizzato dai seguenti studentxwi:
    - Calandra Vincenzo Maria
    - Fiorio Federico
    - Papa Eleonora
    
con la supervisione dei docenti:
    - Iannello Giulio
    - Esposito Marcello
    
"""

"""Qui subito di seguito viene creato il menù che viene mostrato a terminale"""


def argoment():
    parser = argparse.ArgumentParser(description="Il progetto che segue è stato realizzato da un gruppo di stundeti dell'università campus bio medico di roma "
        "\nche frequentano il corso di Ingegneria dei sistemi intelligenti. "
        "\nIl prodotto che segue è il progetto per concludere lo studio nel corso di Programmazione del primo anno primo semestre"
        "\nLa richiesta era quella di creare un programma in grado di leggere un labirinto o da un immagine o da un file json."
        "\nIl codice presente è stato realizzato dai seguenti studentxwi:"
        "\n  - Calandra Vincenzo Maria"
        "\n  - Fiorio Federico"
        "\n  - Papa Eleonora"
        "\n"
        "\ncon la supervisione dei docenti:"
        "\n"
        "\n  - Iannello Giulio"
        "\n  - Esposito Marcello")
    parser.add_argument("InputType", type=str, help="Possibile scegliere tra 3 tipi di Input Image Tiff inline o Json inline oppure terminal executed", choices=["tiff", "json", "terminal"])
    args = parser.parse_args()



if __name__ == "__main__":
    argoment()
