import json
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
import os
from datetime import datetime
from skimage.morphology import skeletonize

"""
Queste tre righe combinate cercano tutti i file con estensione .json all'interno della cartella "output" rispetto alla posizione corrente del file.
"""
#recupero il percorso corrente del file
current_path = os.getcwd()
#creo un percorso combinando il percorso corrente con la cartella "output"
path = os.path.join(current_path,"./output/")
#utilizzo una list comprehension per creare una lista di file nella cartella specificata che terminano con ".json"
json_files = [f for f in os.listdir(path) if f.endswith('.json')]
print(json_files)

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


# apro e manipolo il file più recente
with open(os.path.join(path, latest_file)) as f:
    #leggo i dati del file e li carica in una stringa json.
    json_string = json.load(f)
    data = json.loads(json_string)
#print(data)


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


path_json = json.dumps(best_path)
#print(path_json)
#genero un nome univoco per il file a seconda dellea data e dell'ora attuali
now = datetime.now()
filename = now.strftime("./output/path_%Y%m%d_%H%M%S.json")

#creo il file JSON (scrivo il contenuto di "path_json" in un file json con nome "filename".
with open(filename, 'w') as f:
    #e il contenuto viene scritto utilizzando il metodo "dump" di json
    json.dump(path_json, f)
print(filename)
#print(path_json)


path_json = json.loads(path_json)
start = tuple(map(int, path_json["start"]))
goal = tuple(map(int, path_json["goal"]))
path_visited = path_json["pathVisited"]
for x, y in path_visited:
    if (x, y) == start:
        start_x, start_y = x, y
    elif (x, y) == goal:
        goal_x, goal_y = x, y

print(start)
print(goal)


x0,y0 = start
y0,x0 = x0,y0
x1,y1 = goal
y1,x1 = x1,y1
print(x0,y0)
print(x1,y1)


img_name = './indata/labirinto2_marked.tiff'
rgb_img = plt.imread(img_name)

plt.figure(figsize=(10,10))
plt.imshow(rgb_img)

plt.plot(x0,y0, 'gx', markersize = 14)
plt.plot(x1,y1, 'rx', markersize = 14)


thr_img = rgb_img[:,:,0] > 128
skeleton = skeletonize(thr_img)
plt.figure(figsize=(10,10))
plt.imshow(skeleton)
#map of routes
mapT = ~skeleton
plt.imshow(mapT)
plt.plot(x0,y0, 'gx', markersize=14)
plt.plot(x1,y1, 'rx', markersize=14)

#let'go a temporanery copy of this
_mapt = np.copy(mapT)

#searching to our endpoint and connect to the path
boxr = 2

cpys, cpxs = np.where(_mapt[y1-boxr:y1+boxr, x1-boxr:x1+boxr]==0) #x e y di destinazione


#calibrate points to main scale
cpys += y1-boxr #x e y di destinazione
cpxs += x1-boxr

#find clooset point of possible path endpoints
idx = np.argmin(np.sqrt((cpys-y1)**2 + (cpxs-x1)**2)) #x e y di destinazione
y, x = cpys[idx], cpxs[idx]

pts_x = [x]
pts_y = [y]
pts_c = [0]

#mesh of displacements
xmesh, ymesh = np.meshgrid(np.arange(-1,2),np.arange(-1,2))
ymesh = ymesh.reshape(-1)
xmesh = xmesh.reshape(-1)

dst = np.zeros(thr_img.shape)

#Breath first algorithm exploring a tree
while(True):
    #update distance
    idc = np.argmin(pts_c)
    ct = pts_c.pop(idc)
    x = pts_x.pop(idc)
    y = pts_y.pop(idc)
    #Search 3x3 neighbourhood for possible
    ys, xs = np.where(_mapt[y-1:y+2,x-1:x+2] == 0) #x e y generici diversi da destinazione e arrivo
    #Invalidate these point from future searchers
    _mapt[ys+y-1, xs+x-1] = ct
    _mapt[y,x] = 999999
    #Set the distance in the distance image
    dst[ys+y-1,xs+x-1] = ct + 1
    #
    pts_x.extend(xs+x-1)
    pts_y.extend(ys+y-1)
    pts_c.extend([ct+1]*xs.shape[0])
    #If we run of points
    if pts_x == []:
        break;
    if np.sqrt((x-x0)**2 +(y-y0)**2) < boxr: #x0 di partenza
        edx = x
        edy = y
        break;

plt.figure(figsize=(5,5))
plt.imshow(dst)

path_x = []
path_y = []

y = edy
x = edx
while(True):
    nbh = dst[y-1:y+2,x-1:x+2]
    nbh[1,1] = 9999999
    nbh[nbh==0] = 9999999
    #if we reach a deadend
    if np.min(nbh) == 9999999:
        break;
    idx = np.argmin(nbh)
    #find direction
    y += ymesh[idx]
    x += xmesh[idx]

    if np.sqrt((x-x1)**2 + (y-y1)**2) < boxr:   #arrivo
        print('Optimum route found.')
        break
    path_y.append(y)
    path_x.append(x)


plt.figure(figsize=(10,10))
plt.imshow(rgb_img)
plt.plot(x0,y0, 'gx', markersize=14)
plt.plot(x1,y1, 'rx', markersize=14)
plt.plot(path_x, path_y, 'r-', linewidth=4)
plt.savefig('./output/labirinto_finale.tiff')


"""
Per trovare solo la lista delle coordinate all'interno del percorso con costo inferiore facciamo questo comando:

#estraggo la chiave "pathVisited" dall'oggetto "best_path" e la assegno alla variabile "path_visited"
path_visited = best_path["pathVisited"]
print(path_visited)

#path_visited la vogliamo trasformare in una lista di tuple dove ogni tupla rappresenta un punto sulla mappa (x, y). 
#Sto convertendo tutti gli elementi della lista path_visited in tuple, in modo che ogni elemento della lista sia una tupla anziché una lista
path_visited = list(map(tuple, path_visited))
print(path_visited)

"""

