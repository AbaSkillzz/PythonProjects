"""
ALGORITMO:
-input immagine
-dimensioni immagini(o fare il resize)
-mettere i valori rgb in un array 2d(matrice) = a quelli della lunghezza e larghezza della foto --> NON NECESSARIO
-matrice luminosità, ogni luminosità è media dei valori della tupla(con valori rgb di ogni pixel)
-associare ad un certo range di valori delle luminosità, un carattere ascii(asscoaire in un dizionario): -- quindi: range(chiave dict) = ascii(valore della key)
    algoritmo: _creo dict vuot
           _valore incremento = 255(val max che si puo vedere) // n ascii --> per i range
           _variabile = 0 --> ad ogni ciclo faccio x += incremento + 1

-output della matrice con il risultato

----------------------------------------------------------------------------------------------------------------------------------
"""

from PIL import Image
import numpy


#IMPORTAZIONE IMMAGINE DA CONVERTIRE, RESIZE
new_size = (200, 340)
i = Image.open("C:\\Users\\1975k\\OneDrive\\Desktop\\monalisa.jpg").resize(new_size)
image = numpy.array(i)

#VALORI RGB IN MATRICE  ---> PASSAGGIO NON NECESSARIO

#CALCOLO LUMINOSITà PER OGNI PIXEL
luminosita = numpy.empty((new_size[0], new_size[1]), dtype=int) #matrice con intensita di luminosita di ogni pixel

for x in range(new_size[0]):
    for y in range(len(image[x])):
        pixel = image[x][y]
        media = sum(pixel) // 3
        luminosita[x][y] = media


#ASSOCIARE AD OGNI CARATTERE ASCII UN CERTO RANGE DI VALORI DI LUMINOSITà
#ascii_chars = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
set_ascii = ['`','^','"',',',':',';','I','l','!','i','~','+','_','-','?',']',
        '[','}','{','1',')','(','|','/','t','f','j','r','x','n','u','v','c','z',
        'X','Y','U','J','C','L','Q','0','O','Z','m','w','q','p','d','b','k','h',
        'a','o','*','#','M','W','&','8','%','B','@','$']

conversione = {}
n_ascii = int(len(set_ascii))
inizo_range = 0   #sara l'inizio di ogni pezzo di range per ogni caratteri ascii
incremento = 255 // n_ascii  #di quanto in quanto andranno i vari range


for a in set_ascii:
    conversione[(inizo_range, inizo_range+incremento)] = a  #primo membro(aggiungo una key nel dict), secondo membro(associo alla key un valore, carattere ascii)
    inizo_range += incremento + 1

"""for key, val in conversione.items():
    print(f"{val}: {key}")"""

#rimpiazzo dei caratteri in base ai range e al loro carattere ascii corrispondente
risultato = []

for x in range(len(luminosita)): #righe
    riga = []  #ad ogni ciclo(riga 67) diventa vuoto, salvera ogni valore di ogni riga

    for y in range(len(luminosita[x])):  #colonne
        val_intensita = luminosita[x][y]

        for minore, maggiore in conversione.keys(): #minore e maggiore sono gli estremi dei vari range che vado a controllare in tutte le keys del dict "conversion"
            if val_intensita>=minore and val_intensita<=maggiore:
                riga.append(conversione[(minore, maggiore)])  #aggiungo ad ogni riga i valori delle chiavi(min, mag) del dict
                break

    risultato.append(riga) #aggiungo al risultato ogni riga ad ogni ciclo(della riga 67)



#OUTPUT  PATH=PycharmProjects/myProjects/projects/
for riga in risultato:
    line = [x+x+x for x in riga]
    print("".join(line))
