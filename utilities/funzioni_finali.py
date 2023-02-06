import json
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import os
from datetime import datetime
from skimage.morphology import skeletonize

"""
Prima di lanciare il codice assicurarsi di aver inserito nella cartella "indata" il file json con il labirinto e il file .tiff dell'immagine che lo rappresenta.
Se non si ha a disposizione un labirinto, tornare sul main e crearne uno prima di lanciare il codice.

N.B: L'immagine che si desidera sovrascrivere deve essere l'ultima caricata in indata
"""
#recupero il percorso corrente del file
current_path = os.getcwd()
#creo un percorso combinando il percorso corrente con la cartella "output"
path = os.path.join(current_path,"./output/")
#utilizzo una list comprehension per creare una lista di file nella cartella specificata che terminano con ".json"
json_files = [f for f in os.listdir(path) if f.endswith('.json')]
print(json_files)

"""
---------------------------------------------------------------------------------------
"""

#imposto la variabile "latest_file" come una stringa vuota e la variabile "latest_timestamp" come una data iniziale molto vecchia (1 gennaio 1)
latest_file = ""
latest_timestamp = datetime(1, 1, 1)
#verifico se ci sono file nella directory specificata
if json_files:
    for file in json_files:
        # ottengo la data di modifica del file in formato timestamp
        timestamp = os.path.getmtime(os.path.join(path, file))
        # la converto in un oggetto datetime
        timestamp = datetime.fromtimestamp(timestamp)
        # confronto la data di modifica con quella del file più recente 
        if timestamp > latest_timestamp:
            latest_file = file  #se è più recente, la variabile "latest_file" viene impostata come il nome del file corrente 
            latest_timestamp = timestamp    #e la variabile "latest_timestamp" viene impostata come la data di modifica del file corrente.


"""
--------------------------------------------------------------------------------------
"""

# apro e manipolo il file più recente
with open(os.path.join(path, latest_file)) as f:
    #leggo i dati del file e li carica in una stringa json.
    json_string = json.load(f)
    data = json.loads(json_string)
#print(data)

"""
-----------------------------------------------------------------------------------
"""

#best_path e best_cost inizializzano due variabili rispettivamente come {} e infinito.
best_path = None
best_cost = float('inf')
#Il ciclo for scorre attraverso tutti i valori del dizionario data, che rappresentano percorsi
for percorso in data.values():
    #e controlla se il costo di un determinato percorso è minore di best_cost
    if percorso['cost'] < best_cost:
        #Se è così, assegna quel percorso e il suo costo a best_path e best_cost.
        best_path = percorso
        best_cost = percorso['cost']
#stampo il percorso con il costo minimo
#print(best_path)

"""
-------------------------------------------------------------------------------------
"""

path_json = json.dumps(best_path)
#print(path_json)
#genero un nome univoco per il file a seconda dellea data e dell'ora attuali
now = datetime.now()
filename = now.strftime("./output/path_%Y%m%d_%H%M%S.json")

#creo il file JSON (scrivo il contenuto di "path_json" in un file json con nome "filename".
with open(filename, 'w') as f:
    #e il contenuto viene scritto utilizzando il metodo "dump" di json
    json.dump(path_json, f)
#print(filename)
#print(path_json)

"""
-----------------------------------------------------------------------------------
"""

path_json = json.loads(path_json)
start = tuple(map(int, path_json["start"]))
goal = tuple(map(int, path_json["goal"]))
path_cord = path_json["path_cord"]
path_visited = path_json["pathVisited"]
for x, y in path_visited:
    if (x, y) == start:
        start_x, start_y = x, y
    elif (x, y) == goal:
        goal_x, goal_y = x, y
print(path_cord)
print(start)
print(goal)

"""
----------------------------------------------------------------------------
"""

x0,y0 = start
y0,x0 = x0,y0
x1,y1 = goal
y1,x1 = x1,y1
print(x0,y0)
print(x1,y1)
start = x0,y0
goal = x1,y1
print(start)
print(goal)

"""
----------------------------------------------------------------------------
"""

print(path_cord)
path_cord = path_cord.split(')(')
path_cord = [coord.replace('(','').replace(')','') for coord in path_cord]
path_cord = [(int(coord.split(',')[0]), int(coord.split(',')[1])) for coord in path_cord]

print(path_cord)
#new_path_cord = [(y, x) for x, y in path_cord]            #in più
#print (new_path_cord)

"""
---------------------------------------------------------------------------
"""

new_path_cord = [(y, x) for x, y in path_cord]            #in più
print (new_path_cord)

"""
---------------------------------------------------------------------------
"""

#recupero il percorso corrente del file
current_path = os.getcwd()
#creo un percorso combinando il percorso corrente con la cartella "indata"
img_files = os.path.join(current_path,"./img_input/")
#utilizzo una list comprehension per creare una lista di file nella cartella specificata che terminano con ".tiff"
img = [f for f in os.listdir(img_files) if f.endswith('.tiff')]
print(img)

"""
-------------------------------------------------------------------------
"""

#imposto la variabile "latest_file" come una stringa vuota e la variabile "latest_timestamp" come una data iniziale molto vecchia (1 gennaio 1)
latest_file = ""
latest_timestamp = datetime(1, 1, 1)
#verifico se ci sono file nella directory specificata
if img:
    for file in img:
        # ottengo la data di modifica del file in formato timestamp
        timestamp = os.path.getmtime(os.path.join(img_files, file))
        # la converto in un oggetto datetime
        timestamp = datetime.fromtimestamp(timestamp)
        # confronto la data di modifica con quella del file più recente 
        if timestamp > latest_timestamp:
            latest_file = file  #se è più recente, la variabile "latest_file" viene impostata come il nome del file corrente 
            latest_timestamp = timestamp    #e la variabile "latest_timestamp" viene impostata come la data di modifica del file corrente.

"""
-----------------------------------------------------------------------------------
"""

img = os.path.join(img_files, latest_file)
im = Image.open(img)
draw = ImageDraw.Draw(im)
color = (255, 0, 0)
draw.line(new_path_cord, fill=color)
color1 = (0, 255, 255) # colore rosso
color2 = (0, 0, 255) # colore verde

draw.point(start, fill=color1)
draw.point(goal, fill=color2)
im.save("./output/maze_finale.tiff")
im.show()

