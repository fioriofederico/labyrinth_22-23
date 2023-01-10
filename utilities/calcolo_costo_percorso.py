import json
from maze import Maze
import random
import math
from colorama import Fore
from PIL import Image
import numpy as np


##Apro il file json
##leggo file json preso dall'output della funzione implementata da federico
with open('../indata/20-10_marked.json', 'r') as input_data:
    #read_json = json.load(input_data)
    read_json = input_data.read()
#    print(read_json)


#def read_maze(input_data):
#    mz = []
#    with open(input_data, 'U') as id:
#        for r in id:
#            mz.append(list(r.replace('\n', '')))
#        return mz
#
#mz = read_maze('../indata/20-10_marked.json')
##for r in mz:
##    print .join(r)
#
#maze = Maze(7,10)
#maze.getTiff()
#maze.printMaze()
if __name__ == '__main__':
    mz = Maze(7,10)
    mz.printMaze()

##Creo un dizionario che memorizza i passaggi nel labirinto tramite opportuni caratteri
MOVES = {(-1, 0):'^', (1, 0):'.', (0, -1):'<', (0, 1): '>'}

##risolviamo il labirinto
def solve(mz) :
    nr, nc = len(mz), len(mz[0])
    ex = (nr - 2, nc - 2)   #blocco d'uscita
    blk = [(1, 1)]  #blocco d'entrata
    mz[1][1] = '*'

    while len(blk) > 0 and ex not in pos:
        newblk = []
        for r, c in pos:
            for (dr, dc), ch in MOVES.items():
                rr, cc = r + dr, c + dc
                if mz[rr][cc] == ' ':
                    if mz[rr + dr][cc + dc] == ' ':
                        mz[rr][cc] = ch
                        mz[rr + dr][cc + dc] = '*'
                        pos = (rr + dr, cc + dc)
                        newblk.append((rr + dr, cc + dc))
        blk = newblk

def find_path(mz) :
    nr, nc = len(mz), len(mz[0])
    start = (1, 1)  #il blocco d'entrata
    path = [(nr - 2, nc - 2)] #il blocco d'uscita

    while path[0] != start:
        r, c = path[0]
        for dr, dc in MOVES:
            rr, cc = r + dr, c + dc
            if mz[rr][cc] == MOVES[(-dr, -dc)]:
                pos = (rr + dr, cc + dc)
                path.insert(0, pos)
                break
    return path

#Stampo in output il percorso ottimo in un altro file json
#Stampo un immagine con il percorso ottimo

path = mz.find_path
mz.getTiff()
Maze.draw_path (mz, path)
mz.save('maze1_sol.tiff', mz)


####restituisco in output un json con i costi valorizzati
##with open('../indata/20-10_marked_NEW.json', 'w') as output_data:
##
##    # write contents to output_data file
##    output_data.write(read_json) #scrive nel json di output il json letto in input
##    # da qui in poi implementiamo il codice per modificare il file di input il calcolo dei costi dei vari percorsi e la ricerca del percorso ottimo.
##    #output_data.write('costi valorizzati')
#
#