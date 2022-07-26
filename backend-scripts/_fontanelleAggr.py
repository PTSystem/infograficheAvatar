import pesca.pesca as p
import pandas as pd
from pyproj import Proj
import geopandas
from graph.graph import Graph
from pdfgen.pdfgen import PdfGen
from pdfgen.ContentSettings import ContentSettings
from pdfgen.ContentSettings import Immagine
from pdfgen.ContentSettings import Tabella
from pdfgen.ContentSettings import Testo
import time
import matplotlib.pyplot as plt
import numpy as np
from citymap.citymap import CityMap
import utils.strings as utils

# URL EXAMPLE
# https://dati.veneto.it/SpodCkanApi/api/1/rest/dataset/comune_di_thiene_fontanelle

#################################################################################################################################
# Fontanelle pubblicati #  Corretto #                       id                  #                      NOTE                     #
#################################################################################################################################
#       Schio           #   XX      #                                           #
#        Thiene         #   Si      #   5a1e289a-0879-4a14-9b73-1b1bec8cc0ca    #
#       Valdagno        #   Si      #   0c44efdd-1364-467b-94ce-0e74262f034c    #   longitudine, latitudine non disponibile     #
#    Isola Vicentina    #   XX      #                                           #
#       Malo            #   XX      #                                           #
#      Marano           #   XX      #                                           #
#    Monte di Malo      #   XX      #                                           #
#    Santorso           #   XX      #                                           #
#   SanVitodiLeguzzano  #   Ni      #   7fdf73c8-0d72-49f3-a3c5-580bf8748912    #
#     Torrebelvicino    #   XX      #                                           #
#       Villaverla      #   Ni      #   c07b7e7e-e036-4c00-8a1c-d2e84e4b104e    #
#       Zugliano        #   XX      #                                           #
#################################################################################################################################


# Portiamo tutto su il v2 di ckan api quindi andiamo a vedere i vari id

url = 'https://dati.veneto.it/SpodCkanApi/api/2/rest/dataset/'
list_id =   [   "0c44efdd-1364-467b-94ce-0e74262f034c",
                "5a1e289a-0879-4a14-9b73-1b1bec8cc0ca",
                "eb0a5873-06d3-420c-8846-5d2cbe48664a",
                "7fdf73c8-0d72-49f3-a3c5-580bf8748912",
                "c07b7e7e-e036-4c00-8a1c-d2e84e4b104e",
            ]
list_comuni = ["Valdagno", "Thiene", "Santorso", "San Vito di Leguzzano", "Villaverla"]
################################################################################
contents = []
grafici = Graph()
# Dobbiamo ciclare per ogni comune, stiamo attenti nei corner case dove non si
# trova il dato
df = ""
lista_aggiornamenti = []
print("Dataset - Fontanelle")
for index, id in enumerate(list_id):
    dati = p.Pesca(list_comuni[index], url+id)

    if(dati.error != 1):
        # Questo ci servirà dopo per trovare il dato più aggiornato da stampare
        # nell'infografica
        print(dati.ultimo_aggiornamento)
        lista_aggiornamenti.append(dati.ultimo_aggiornamento)
        s = pd.read_csv(dati.csv_url, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
        # Prima occorrenza, df non settato
        if(isinstance(df, pd.DataFrame)):
            df = pd.concat([df,s])
        else:
            df = s

# Verifichiamo che nel dfTot ci sia qualcosa
# Se è un'istanza di DataFrame vuol dire che è stato riempito sopra e quindi
# sono sicuro che contenga qualcosa
if(isinstance(df, pd.DataFrame)):

    # Conteggio fontanelle

    dfAggr = df.groupby('Comune').size().reset_index(name='Counts')
    dfAggr = dfAggr.sort_values(by='Counts', ascending=False)

    # Variabile citymap per l'utilizzo dell funzione contenuta nella classe
    pezzato = CityMap()
    # PRO_COM nello shapefile è il numero identificativo del comune utilizzando il codice istat
    pezzato.plotNumberCenter(   dfAggr, 'COMUNE', 'Comune', "Blues",
                            columnDisplay = "Counts", title="Fontanelle totali per comune")
    # Salvo e aggiungo al contenuto del display
    supp = pezzato.save("allcomuni")
    contents.append(Immagine(supp, -8, 70, 220, 180))


    contents.append(Testo("*Dove non è presente il dato sarà disponibile prossimamente", 110, 258))
    

    generator = PdfGen("Fontanelle presenti sul territorio", "", "cc-by-4.0")
    generator.setHeader()
    generator.setFooter("fontanelle")
    generator.content(contents)
    generator.savePdf("aggrFontanelle")
