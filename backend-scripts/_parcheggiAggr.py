import pesca.pesca as p
import pandas as pd
from pyproj import Proj
import geopandas
from citymap.citymap import CityMap
from graph.graph import Graph
from pdfgen.pdfgen import PdfGen
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import graphviz
import random
from pdfgen.ContentSettings import ContentSettings
from pdfgen.ContentSettings import Immagine
from pdfgen.ContentSettings import Tabella
from pdfgen.ContentSettings import Testo

#################################################################################################################################
# Parcheggi pubblicati  #  Corretto #                       id                  #                      NOTE                     #
#################################################################################################################################
#        Schio          #     Si    #   2191f61c-1aa4-4503-9a46-28efbd9d2e2d    # v.doc                                             #
#       Thiene          #     No    #   1c9d782a-dc7a-4396-a137-fd3d868e738d    # un campo è vuoto
#     Valdagno          #     Si    #   bea93de5-27ff-4115-b630-8364c115635f    #
#   Isola Vicentina     #     Si    #   8bb817ec-6b64-46ad-8fff-421aa167efb1    #
#         Malo          #     Si    #   8766998d-0b06-4cbb-9234-c470507ec10c    #
#      Marano           #     XX    #                                           #
#     Monte di Malo     #     Si    #   57dd74bc-84ad-4c7c-8949-069ce5ca1b06    #
#    Santorso           #     XX    #                                           #
#   SanVitodiLeguzzano  #     XX    #
#     Torrebelvicino    #     XX    #
#       Villaverla      #     XX    #
#       Zugliano        #     XX    #
#################################################################################################################################


# Portiamo tutto su il v2 di ckan api quindi andiamo a vedere i vari id

url = 'https://dati.veneto.it/SpodCkanApi/api/2/rest/dataset/'
list_id =   [   "2191f61c-1aa4-4503-9a46-28efbd9d2e2d",
                "1c9d782a-dc7a-4396-a137-fd3d868e738d",
                "bea93de5-27ff-4115-b630-8364c115635f",
                "8bb817ec-6b64-46ad-8fff-421aa167efb1",
                "57dd74bc-84ad-4c7c-8949-069ce5ca1b06",
                "8766998d-0b06-4cbb-9234-c470507ec10c",
            ]
list_comuni = ["Schio", "Thiene", "Valdagno", "Isola Vicentina", "Monte di Malo", "Malo"]
################################################################################
contents = []
grafici = Graph()
# Dobbiamo ciclare per ogni comune, stiamo attenti nei corner case dove non si
# trova il dato
df = ""
lista_aggiornamenti = []
print("Dataset - Parcheggi")


for index, id in enumerate(list_id):

    dati = p.Pesca(list_comuni[index], url+id)
    if(dati.error != 1):
        # Questo ci servirà dopo per trovare il dato più aggiornato da stampare
        # nell'infografica
        print("Ultimo aggiornamento comune di "+list_comuni[index] + " : " +dati.ultimo_aggiornamento)

        lista_aggiornamenti.append(dati.ultimo_aggiornamento)
        s = pd.read_csv(dati.csv_url, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
        try:
            df = df.rename(columns={'Posti_totali': 'Posti_totale'})
        except Exception as e:
            print("Errore nella conversione colonne")
        # Prima occorrenza, df non settato
        if(isinstance(df, pd.DataFrame)):
            df = pd.concat([df,s])
        else:
            df = s


# Creazione del contenuto
# Controllo se il dataframe è stato riempito

if(isinstance(df, pd.DataFrame)):
    # 1 - Percentuali di posti liberi, posti a pagamento, posti disabili
    # Lo creiamo con un tondino
    # TODO: devo fare una scrematura perchè non sono sicuro si possa manipolare dati diversi
    # anche perchè probabilemnte i dati che avrò in mano saranno degli object
    # Forse nonostante siano object posso castarli nel tipo che mi serve ogni volta (?)
    names = ["A pagamento", "Disco orario", "Liberi", "Disabili"]
    values = []
    campi  =['Posti_a_pagamento', 'Posti_con_disco_orario', 'Posti_liberi', 'Posti_disabili']
    # Faccio il replace della nomenclatura scomodo
    for c in campi:
        df[c].replace({'n.d.': '0'}, inplace =True)
        df[c].replace({'N.d.': '0'}, inplace =True)
    #print(df["Posti_totale"])
    df["Posti_a_pagamento"].replace({'': '0'}, inplace =True)
    df["Posti_con_disco_orario"].replace({'': '0'}, inplace =True)
    df["Posti_liberi"].replace({'': '0'}, inplace =True)
    df["Posti_disabili"].replace({'': '0'}, inplace =True)

    # Replace in posti totali del non definito
    df["Posti_totale"].replace({'n.d.': '0'}, inplace =True)
    df["Posti_totale"].replace({'N.d.': '0'}, inplace =True)
    df["Posti_totale"] = pd.to_numeric(df["Posti_totale"])
    #print("-----------------------------------------")
    #print(df["Posti_totale"])
    # Casto il campo in uno più facile da utilizzare (anche per somme largest etc.)
    for c in campi:
        df[c] = pd.to_numeric(df[c], downcast="integer")

    # Per ciascuno campo prelevo la somma dei parcheggi
    for c in campi:
        values.append(df[c].sum())



    dfAggrComuni = df.groupby("Comune")["Posti_totale"].sum().reset_index(name='Counts')

    # 3 - Mappa con colorazione diverse a seconda dei parcheggi totali disponibili
    pezzato = CityMap()
    # PRO_COM nello shapefile è il numero identificativo del comune utilizzando il codice istat
    #plotNumberCenter(self, df = "", columnLeft="", columnRight="", cmap = "", columnDisplay="", title = "", fontsize_title = 13):
    pezzato.plotNumberCenter(   dfAggrComuni, 'COMUNE', 'Comune', "Oranges",
                            columnDisplay = "Counts", title="Parcheggi - Posti totali per comune*")
    #pezzato.plot_points(df)
    # Salvo e aggiungo al contenuto del display
    supp = pezzato.save("allcomuni")
    contents.append(Immagine(supp, 18, 70, 170, 140))

    # 4 - I cinque parcheggi più grandi qui mettiamo anche il nome del comune
    dfTop5Park = df.nlargest(5, 'Posti_totale')

    contents.append(Tabella(15, 200, dataframe = dfTop5Park,
                            header = ["I 5 parcheggi con più posti auto", "", ""],
                            header_spacing = 8,
                            campi = ["Nome_struttura", "Comune", "Posti_totale"], wcampi = [60,30,20], acampi = ["","", 'C'],
                            offsetY = 9, fontsize = 7,
                            ))



    # Richiamo la funzione per la generazione del tondino
    percPark = grafici.parcheggiPercentVariPosti(names, values)
    contents.append(Immagine(percPark, 140, 200, 60, 60))

    contents.append(Testo('*Dove non è presente il dato sarà disponibile prossimamente', 10, 258))

    # Effettuo il salvataggio
    if(lista_aggiornamenti != []):
        agg = max(lista_aggiornamenti)

    aggiornamento = agg.split("T")[0].split("-")
    agg = aggiornamento[2]+"-"+aggiornamento[1]+"-"+aggiornamento[0]

    generator = PdfGen("Parcheggi presenti sul territorio", "", "cc-by-4.0")
    generator.setHeader()
    generator.setFooter("parcheggi")
    generator.content(contents)
    generator.savePdf("aggrParcheggi")
