import json

##Apro il file json
##leggo file json preso dall'output della funzione implementata da federico
#data = open('../indata/20-10_marked.json', 'r')
##Leggo il file json
#read_json = data.read()
#print (read_json)
##chiudiamo il file
#data.close()

#in alternativa possiamo usare
with open('../indata/20-10_marked.json', 'r') as input_data:
    #read_json = json.load(input_data)
    read_json = input_data.read()
    print(read_json)

##restituisco in output un json con i costi valorizzati
#data_output = { ... } #in data devo inserire i valori che staranno all'interno del JSON, quinid JSON di input + costi valorizzati
#with open("output.json", "w") as outfile:
#    json.dump(data_output, outfile)

#in alternativa possiamo usare

with open('../indata/20-10_marked_NEW.json', 'w') as output_data:

    # write contents to output_data file
    output_data.write(read_json) #scrive nel json di output il json letto in input
    # da qui in poi implementiamo il codice per modificare il file di input il calcolo dei costi dei vari percorsi e la ricerca del percorso ottimo.
    output_data.write('costi valorizzati')

