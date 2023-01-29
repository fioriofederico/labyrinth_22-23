import json
from random import random, randint
from colorama import Fore
from PIL import Image, ImageDraw
import numpy as np
#from utilities.maze import Maze 


"""
Questo script crea un labirinto utilizzando una matrice di 1 e 0, 
dove 1 rappresenta un muro e 0 rappresenta un percorso. 
Utilizza quindi l'algoritmo Breadth-First Search per trovare il percorso più breve da un punto iniziale a un punto finale. 
Utilizza inoltre le librerie PIL e numpy per creare un'animazione del processo di ricerca, in cui ogni fotogramma mostra lo stato corrente del labirinto 
e il percorso esplorato. L'animazione viene salvata come file gif chiamato 'maze.gif'. 
"""
#inizializziamo una lista vuota
images = []

"""
Matrice di 1 e di 0 che rappresenta un labirinto a cui si vanno ad aggiungere i valori dei costi lungo il percorso:
- gli 0 rappresentano gli spazi vuoti/bianchi (255,255,255)
- gli 1 rappresentano gli spazi neri/muri (0,0,0) 
"""

a = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0 ,0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0 ,0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0 ,0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0 ,0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

zoom = 20
borders = 6
#Do in input 2 ingressi...
#start1 = (1,1)
#start2 = (4,6)
starts = [(1, 1), (4, 6)]

#...e un'uscita
end = 5,19
"""
Questa funzione prende in input una variabile "k" e itera attraverso un array bidimensionale "m" e un array bidimensionale "a". 
Per ogni elemento "m[i][j]" che è uguale a "k", la funzione controlla gli elementi nella posizione superiore, inferiore, sinistra e destra di "m[i][j]" per vedere se sono uguali a 0
 e se l'elemento corrispondente in "a" è anche uguale a 0. Se le condizioni sono soddisfatte, la funzione assegna "k + 1" a quell'elemento. 
 Questa funzione diffonde un valore di "k + 1" verso l'esterno da un punto di partenza iniziale di valore "k" nell'array bidimensionale "m", 
 controllando anche gli elementi corrispondenti nell'array bidimensionale "a".
"""
def make_step(k):
  for i in range(len(m)):
    for j in range(len(m[i])):
      if m[i][j] == k:
        if i>0 and m[i-1][j] == 0 and a[i-1][j] == 0:
          m[i-1][j] = k + 1
        if j>0 and m[i][j-1] == 0 and a[i][j-1] == 0:
          m[i][j-1] = k + 1
        if i<len(m)-1 and m[i+1][j] == 0 and a[i+1][j] == 0:
          m[i+1][j] = k + 1
        if j<len(m[i])-1 and m[i][j+1] == 0 and a[i][j+1] == 0:
           m[i][j+1] = k + 1

"""
Questa è una funzione Python che prende come input una matrice 2D (lista di liste) e la stampa sulla console. 
La funzione utilizza un ciclo for annidato per iterare attraverso le righe e le colonne della matrice, e il metodo "ljust(2)" viene utilizzato per 
aggiungere uno spazio dopo ogni elemento in modo che la matrice sia allineata in colonne quando viene stampata. Il parametro "end=' '" nella dichiarazione di stampa 
viene utilizzato per evitare l'aggiunta di un carattere di nuova riga dopo ogni elemento, consentendo di stampare la matrice su una sola riga.
"""
def print_m(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            print( str(m[i][j]).ljust(2),end=' ')
        print()

"""
Questa è una funzione Python che prende tre input: una matrice 2D (a), un valore intero (m) e una lista (the_path). 
La funzione viene utilizzata per disegnare una rappresentazione immagine della matrice, dove ogni cella della matrice è rappresentata da un rettangolo nell'immagine. 
Il colore del rettangolo è determinato dal valore nella matrice, con il valore 1 che diventa nero e 0 bianco. La funzione utilizza anche i moduli Image e ImageDraw 
dalla libreria Python Imaging (PIL) per creare e disegnare sull'immagine.

La funzione crea prima una nuova immagine con uno sfondo blu e poi utilizza un ciclo for annidato per iterare attraverso le celle della matrice. 
Per ogni cella, la funzione controlla il suo valore e imposta il colore del rettangolo di conseguenza. La funzione controlla anche il punto di partenza e di arrivo del percorso 
e se corrisponde con qualsiasi cella, imposta il colore del rettangolo a verde e disegna un rettangolo intorno ad esso.

Inoltre, controlla se la cella è nel percorso e se lo è, disegna un'ellisse su di essa e collega l'ellisse con una linea con la cella successiva del percorso.

Infine, la funzione disegna un contorno verde intorno all'intera immagine e appende l'immagine a una lista di immagini.
"""
def draw_matrix(a,m, the_path = []):
    im = Image.new('RGB', (zoom * len(a[0]), zoom * len(a)), (0, 0, 255)) #rettangolino blu intorno ai punti di partenza e arrivo
    draw = ImageDraw.Draw(im)
    for i in range(len(a)):
        for j in range(len(a[i])):
            color = (255, 255, 255)
            r = 0
            if a[i][j] == 1:
                color = (0, 0, 0)  
            #if i == start1[0] and j == start1[1]:
            #    color = (0, 255, 0)  
            #    r = borders
            if i == starts[0] and j == starts[1]:
                color = (0, 255, 0)
                r = borders
            if i == end[0] and j == end[1]:
                color = (0, 255, 0)   
                r = borders
            draw.rectangle((j*zoom+r, i*zoom+r, j*zoom+zoom-r-1, i*zoom+zoom-r-1), fill=color)
            if m[i][j] > 0:
                r = borders
                draw.ellipse((j * zoom + r, i * zoom + r, j * zoom + zoom - r - 1, i * zoom + zoom - r - 1),
                               fill=(255,0,0))
    for u in range(len(the_path)-1):
        y = the_path[u][0]*zoom + int(zoom/2)
        x = the_path[u][1]*zoom + int(zoom/2)
        y1 = the_path[u+1][0]*zoom + int(zoom/2)
        x1 = the_path[u+1][1]*zoom + int(zoom/2)
        draw.line((x,y,x1,y1), fill=(255, 0,0), width=5)
    draw.rectangle((0, 0, zoom * len(a[0]), zoom * len(a)), outline=(0,255,0), width=2)
    images.append(im)

"""
Questo codice inizializza una matrice 2D vuota (m) con le stesse dimensioni della matrice di input (a). 
Utilizza un ciclo for annidato per iterare attraverso le righe e le colonne della matrice di input e aggiunge una nuova riga alla matrice vuota per ogni riga nella matrice di input. 
All'interno del ciclo interno, un valore di 0 viene aggiunto a ogni colonna della nuova riga. 
Ciò crea una matrice con le stesse dimensioni della matrice di input, ma con tutte le celle che contengono un valore di 0.

Successivamente, si utilizza un altro ciclo per controllare il valore del tuple starts e i relativi valori di i e j, e quindi assegna il valore di 1 alla cella corrispondente 
della matrice m.
"""
m = []
for i in range(len(a)):
    m.append([])
    for j in range(len(a[i])):
        m[-1].append(0)
for i,j in starts:
    m[i][j] = 1

#m = [[0 for _ in range(len(a[0]))] for _ in range(len(a))]
#for i, j in start2:
#    m[i][j] = 1

#for i in range(len(a)):
#    m.append([])
#    for j in range(len(a[i])):
#        m[-1].append(0)
#i,j = start2
#m[i][j] = 1

"""
Questo codice utilizza un ciclo while per chiamare ripetutamente una funzione chiamata "make_step" e "draw_matrix", 
fino a quando non viene soddisfatta una determinata condizione. La variabile k viene inizializzata a 0 prima che il ciclo inizi e viene incrementata di 1 
all'inizio di ogni iterazione del ciclo.

La funzione "make_step" viene chiamata con l'argomento "k" e questa funzione modifica la matrice "m" in qualche modo. La funzione "draw_matrix" viene chiamata con gli argomenti 
"a" e "m", questa funzione crea un'immagine in base ai valori della matrice "a" e "m".

Il ciclo continua ad eseguire finché il valore nella matrice "m" nella posizione specificata dal tuple "end" (che è la posizione di destinazione) è uguale a 0. 
Una volta che il valore in quella posizione non è più 0, il ciclo uscirà.
"""

k = 0
while m[end[0]][end[1]] == 0:
    k += 1
    make_step(k)
    draw_matrix(a, m)

"""
In questo codice viene utilizzato un ciclo while per costruire un percorso dalla posizione di destinazione (end) alla posizione di partenza (starts) seguendo i valori nella matrice "m".
La variabile k viene inizializzata con il valore presente nella matrice "m" alla posizione di destinazione (end), mentre la variabile "the_path" viene inizializzata 
con una lista contenente la posizione di destinazione (end).

Il ciclo while continua finché k è maggiore di 1. Ad ogni iterazione, il codice controlla se il valore presente nella matrice "m" nella posizione sopra, sotto, 
a sinistra e a destra della posizione corrente è uguale a k-1. Se una di queste condizioni è vera, la posizione corrente viene aggiornata a quella posizione e il valore di k 
viene decrementato di 1. Inoltre, la posizione corrente viene aggiunta alla lista "the_path".

Dopo che il ciclo while si è concluso, la funzione "draw_matrix" viene chiamata 10 volte con gli argomenti "a", "m" e "the_path". In alcune chiamate la funzione "draw_matrix" 
viene chiamata solo con "a" e "m".

Alla fine, la matrice "m" viene stampata e la lista "the_path" viene stampata.
"""

i, j = end
k = m[i][j]
the_path = [(i,j)]
while k > 1:
  if i > 0 and m[i - 1][j] == k-1:
    i, j = i-1, j
    the_path.append((i, j))
    k-=1
  elif j > 0 and m[i][j - 1] == k-1:
    i, j = i, j-1
    the_path.append((i, j))
    k-=1
  elif i < len(m) - 1 and m[i + 1][j] == k-1:
    i, j = i+1, j
    the_path.append((i, j))
    k-=1
  elif j < len(m[i]) - 1 and m[i][j + 1] == k-1:
    i, j = i, j+1
    the_path.append((i, j))
    k -= 1
  draw_matrix(a, m, the_path)

for i in range(10):
    if i % 2 == 0:
        draw_matrix(a, m, the_path)
    else:
        draw_matrix(a, m)

print_m(m)
print(the_path)

"""
Questa riga di codice utilizza la libreria Image del pacchetto PIL per salvare un'animazione in formato gif. 
Il nome del file è "maze.gif" e la prima immagine dell'animazione è "images[0]".

L'opzione "save_all=True" indica che tutte le immagini successive nella lista "images" devono essere salvate come parte dell'animazione. 
L'opzione "append_images=images[1:]" indica che tutte le immagini successive alla prima immagine nella lista "images" devono essere aggiunte all'animazione.

L'opzione "optimize=False" indica che l'animazione non deve essere ottimizzata, in modo che tutte le immagini nell'animazione abbiano la stessa qualità. 
L'opzione "duration=1" indica che ogni immagine deve essere visualizzata per 1 secondo, mentre l'opzione "loop=0" indica che l'animazione non deve essere riprodotta in loop.
"""
images[0].save('./output/maze.gif',
               save_all=True, append_images=images[1:],
               optimize=False, duration=1, loop=0)

