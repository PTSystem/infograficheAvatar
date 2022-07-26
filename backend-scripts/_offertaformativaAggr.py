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
from pdfgen.ContentSettings import TestoMulti
import inspect
import json


#################################################################################################################################
#Offerta Form pubblicati#  Corretto #                       id                  #                      NOTE                     #
#################################################################################################################################
#       Schio           #   Si      #   d77468ec-87a0-4845-ad83-91c948606568    #   v.documento                                 #
#       Thiene          #   Si      #   8fe96193-d1d0-4296-9d1d-2e33db85cad8    #                                               #
#      Valdagno         #   Si      #   bc0fc473-4816-4347-ba63-d7eb642645b9    #   mancano le coord geografiche(non necess)    #
# Isola Vicentina       #   Si      #   c7bc4ea3-9329-42b2-82d8-748b3e6f3807    #                                               #
#       Malo            #   Si      #   57b5a2b0-c50b-4457-813d-85aa78efbd1f    #
#      Marano           #   XX      #                                           #
#    Monte di Malo      #   XX      #                                           #
# San Vito di  Leguzzano#   Si      #   b38bd593-81e9-4407-b127-ced8d83ade4b    #                                               #
# Torrebelvicino        #   Si      #   bdaff55a-c3b0-4862-9884-f3fbc107e29e    #
#       Villaverla      #   Si      #   ee8df645-c178-4b53-a0fd-b35e1be83e64    #
#       Zugliano        #   XX      #                                           #                                           #
#################################################################################################################################


# Portiamo tutto su il v2 di ckan api quindi andiamo a vedere i vari id

url = 'https://dati.veneto.it/SpodCkanApi/api/2/rest/dataset/'
list_id =   [   "d77468ec-87a0-4845-ad83-91c948606568",
                "8fe96193-d1d0-4296-9d1d-2e33db85cad8",
                "bc0fc473-4816-4347-ba63-d7eb642645b9",
                "c7bc4ea3-9329-42b2-82d8-748b3e6f3807",
                "57b5a2b0-c50b-4457-813d-85aa78efbd1f",
                "b38bd593-81e9-4407-b127-ced8d83ade4b",
                "bdaff55a-c3b0-4862-9884-f3fbc107e29e",
                "ee8df645-c178-4b53-a0fd-b35e1be83e64",

            ]
list_comuni = ["Schio", "Thiene", "Valdagno","Isola Vicentina", "Malo", "San Vito di Leguzzano", "Torrebelvicino", "Villaverla", ]
################################################################################
contents = []
grafici = Graph()
# Dobbiamo ciclare per ogni comune, stiamo attenti nei corner case dove non si
# trova il dato
df = ""
lista_aggiornamenti = []
# Variabile utilizzata per il conteggio di quante occorenze sono state trovate
da_inserire = 0

print("Dataset - Offerta Formativa")
for index, id in enumerate(list_id):
    dati = p.Pesca(list_comuni[index], url+id)

    if(dati.error != 1):
        # Questo ci servirà dopo per trovare il dato più aggiornato da stampare
        # nell'infografica
        print(dati.ultimo_aggiornamento)
        lista_aggiornamenti.append(dati.ultimo_aggiornamento)
        s = pd.read_csv(dati.csv_url, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
        da_inserire += 1
        # Prima occorrenza, df non settato
        if(isinstance(df, pd.DataFrame)):
            df = pd.concat([df,s])
        else:
            df = s

# Se è un'istanza di DataFrame vuol dire che è stato riempito sopra e quindi
# sono sicuro che contenga qualcosa
if(isinstance(df, pd.DataFrame)):

    dfCatComCount = df.groupby(["Categoria", "Comune"]).size().reset_index(name="Counts")

    mappa = CityMap()
    dfOnlyCat = dfCatComCount.loc[dfCatComCount["Categoria"].isin(["Scuola Infanzia"])]
    # Somma perchè potrebbero esserci il comune duplicato nel caso abbia
    # la scuole dell'infanzia e anche i servizi educativi della prima infanza
    x = dfOnlyCat.groupby(by=['Comune'])['Counts'].sum()

    mappa.plotNumberCenter(x, "COMUNE", "Comune", title="SCUOLE PER L'INFANZIA\nNumero per comune", cmap = "OrRd", columnDisplay="Counts")
    name = mappa.save("mappaInfanzia")
    contents.append(Immagine(name, -8, 68, 120 ,100))

    y = dfCatComCount.loc[dfCatComCount["Categoria"].isin(["Scuola Primaria"])]

    mappa.plotNumberCenter(y, "COMUNE", "Comune", title="SCUOLE PRIMARIE\nNumero per comune", cmap = "Greens", columnDisplay="Counts")
    name = mappa.save("mappaPrimaria")
    contents.append(Immagine(name, 95, 68, 120 ,100))

    z = dfCatComCount.loc[dfCatComCount["Categoria"].isin(["Scuola Secondaria di Secondo Grado", "Centro Formazione Professionale"])]
    z = z.groupby(by=['Comune'])['Counts'].sum()
    mappa.plotNumberCenter(z, "COMUNE", "Comune", title="SCUOLE SECONDARIE DI SECONDO GRADO\nNumero per comune", cmap = "Purples", columnDisplay="Counts", secondaria_no_print=1)
    name = mappa.save("mappaSecondariaSecondo")
    contents.append(Immagine(name, -8, 160, 120 ,100))

    a = df.loc[df["Categoria"].isin(["Scuola Primaria", "Scuola Secondaria di Secondo Grado", "Centro Formazione Professionale", "Servizi Educativi Prima Infanzia", "Scuola Infanzia", "Scuola Secondaria di Primo Grado"])  == False]
    #     1 - prendiamo i valori relativi ai percoris formativi esterni
    #     2 - prendiamo i valori relativi alle scuole secondarie di primo grado
    #     3 - plottiamo i due cerchi
    #     4 - aggiungiamo il testo
    nmr_post_diploma = len(a.index)
    df_medie = df.loc[df["Categoria"].isin(["Scuola Secondaria di Primo Grado"])]
    nmr_medie = len(df_medie.index)

    # Scuole secondarie di primo grado
    name = grafici.offertaFormativaTondo(str(nmr_medie), "nmr_medie", "#FFFFB3")
    contents.append(Immagine(name, 100, 175, 25 , 25))
    contents.append(Testo("Scuole secondarie di primo grado", 132,182, size=12))

    # Percorsi post diploma
    #def offertaFormativaTondo (self, centerValue, filename):
    name = grafici.offertaFormativaTondo(str(nmr_post_diploma), "nmr_post_diploma", "#80AAFF")
    contents.append(Immagine(name, 100, 215, 25 , 25))
    #class TestoMulti(ContentSettings):
    #    def __init__(self, text, x, y, size = 8, align = '', font = "Arial", w = 0, h = 0, border = 0):
    contents.append(TestoMulti("Percosi formativi post diploma presenti nel territorio tra cui anche a livello universitario", 132, 220 , w=60, h=5, size=12, border=0))

    #def __init__(self, text, x, y, size = 8, align = '', font = "Arial", w = 10):
    contents.append(Testo("*Dove non è presente il dato sarà disponibile prossimamente", 10, 258))




    # Effettuo il salvataggio

    generator = PdfGen("Offerta formativa presente sul territorio", "", "cc-by-4.0")
    generator.setHeader()
    generator.setFooter("offertaformativa")
    generator.content(contents)
    generator.savePdf("aggrOfferta")
