# Labirinto

Il programma deve acquisire il layout di un 
labirinto costituito da una matrice di *posizioni*, 
una o più *posizioni di partenza* e una *posizione 
di arrivo*, e determinare per ogni punto di partenza 
il percorso che permette di raggiungere il punto
di arrivo o, in alternativa, se non esiste alcun 
percorso possibile.

Nel labirinto sono presenti posizioni a cui è 
associato un punteggio. Nel caso esista un percorso
che permette di raggingere da un punto di partenza 
il punto di arrivo, oltre al percorso, il programma
deve anche fornire la somma dei punti incontrati lungo
di esso. Nel caso esistano più percorsi possibili 
da un determinato punto di partenza,
il programma deve fornire il percorso con il punteggio 
minore.

Il labirinto e i punti di partenza e di arrivo possono
essere forniti attraverso un file in formato JSON o un'immagine. 
Di seguito, per ogni formato 
possibile, viene fornita la specifica 
delle convenzioni 
usate per rappresentare il layout del labirino, 
le posizioni a cui è associato un punteggio, e 
le posizioni di partenza e di arrivo.

Il risultato finale deve essere fornito attraverso: 

- un'immagine su cui è indicato il percorso con un 
colore diverso per ogni punto di partenza;

- un file JSON associato all'immagine con 
l'informazione del punteggio
raggiunto da ogni percorso o, in alternativa, 
da un messaggio nel caso non esista un 
percorso possibile da qualcuno delle posizioni 
di partenza. 


## Labirinto fornito come file JSON

Il file è un dizionario con le seguenti chiavi:

- "larghezza": un numero che indica il numero di posizioni 
    lungo la dimensione orizzontale;
- "altezza": un numero che indica il numero di posizioni 
    lungo la dimensione verticale;
- "pareti": una lista di *segmenti*, ogni 
segmento costituito da un dizionario con chiavi: 
    - "orientamento": "H" per orizzontale, "V" per verticale;
    - "posizione": un coppia di indici che indicano una posizione 
    "iniziale" (per 
    convenzione il segmento si estende in 
    orizzontale da sinistra verso destra e 
    in verticale dall'alto verso il basso);
    - "lunghezza": un numero che indica il numero 
    di posizioni occupate dal segmento;
- "iniziali": una lista di coppie di indici che 
indicano ciascuno una posizione di partenza;
- "finale": una coppia di indici che indica la 
posizione di arrivo;
- "punti": una lista di *posizioni con punteggio*,
ogni posizione costituita da un dizionario con 
chiavi:
    - "posizione": un coppia di indici che indicano 
    una posizione;
    - "punteggio": un valore da 1 a 5. 

## Labirinto fornito come immagine

L'immagine è un'immagine a colori in formato TIFF, PNG 
o JPEG che corrisponde a una
matrice rettangolare un cui i pixel neri 
corrispondono a posizioni occupate da pareti 
che non possono essere 
attraversate, e tutti gli altri pixel 
corrispondono a posizioni che possono 
essere attraversate per raggiungere il punto 
di arrivo.

I pixel bianchi sono posizioni che non assegnano 
punti, i pixel grigi indicano caselle che assegnano
punti, i pixel verdi indicano le posizioni di partenza,
il pixel rosso indica la posizione di arrivo.

I livelli di grigio possibili sono:
- 16 che assegna 1 punto
- 32 che assegna 2 punti
- 48 che assegna 3 punti
- 64 che assegna 4 punti
- 96 che assegna 5 punti

