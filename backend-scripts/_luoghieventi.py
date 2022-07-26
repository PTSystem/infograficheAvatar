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
from pdfgen.ContentSettings import ContentSettings
from pdfgen.ContentSettings import Tabella
from pdfgen.ContentSettings import Testo
from pdfgen.ContentSettings import Immagine

#################################################################################################################################
#LuoghiEventi pubblicati#  Corretto #                       id                  #                      NOTE                     #
#################################################################################################################################
#       Schio           #   Si      #   3dde3436-845c-424e-9fd2-a2b6c630b3e1    #
#       Thiene          #   Si      #   530606db-dad7-4647-9a35-a5fc7bdc5e80    #
#      Valdagno         #   No      #   38cd59f3-e443-4bd9-b2aa-c0e3654ea433    # header Accessibilità sbagliato, campi corretti#
#    Isola Vicentina    #   XX      #                                           #
#       Malo            #   XX      #                                           #
#      Marano           #   XX      #                                           #
#    Monte di Malo      #   XX      #                                           #
#       Santorso        #   Si      #   ec4cbe1d-7379-4c85-9fe3-628eb5833e65    #
# San Vito di Leguzzano #   Si      #   b91ad85f-7621-42fb-90e8-67e031c4902a    #
#     Torrebelvicino    #   XX      #                                           #
#      Villaverla       #   Si      #   38cd59f3-e443-4bd9-b2aa-c0e3654ea433    #                                               #
#       Zugliano        #   XX      #                                           #
#################################################################################################################################

###################################
#        Creazione singolo        #
###################################

url = 'https://dati.veneto.it/SpodCkanApi/api/2/rest/dataset/'
list_id =   [   "3dde3436-845c-424e-9fd2-a2b6c630b3e1",
                "530606db-dad7-4647-9a35-a5fc7bdc5e80",
                "0093b8a9-fd9f-4a18-b166-492ce8b6f95f",
                "ec4cbe1d-7379-4c85-9fe3-628eb5833e65",
                "b3656841-4627-4046-8801-04a61ea3a844",
                "b91ad85f-7621-42fb-90e8-67e031c4902a",
                "a22433ff-ee62-4a0a-a8eb-c11a2b8e1a97",
                "38cd59f3-e443-4bd9-b2aa-c0e3654ea433",
            ]
list_comuni = [ "Schio", "Thiene", "Valdagno", "Malo",  "Santorso", "San Vito di Leguzzano", "Torrebelvicino", "Villaverla"]
#################################################################################
contents = []


# Le seguenti variabili serviranno poi per effettuare la parte di generazione
# con i dati aggregati
lista_aggiornamenti = []
dfTot = ""
print("Dataset - Luoghi Eventi")
for index,id in enumerate(list_id):
    # Qui andiamo sia a prendere i dati sia a salvarli su un'altra
    # variabile per poi andare a manipolare per creare il dato aggregato
    grafici = Graph()
    dati = p.Pesca(list_comuni[index], url + list_id[index])
    contents.clear()
    df = ""

    # Check dati non trovati o errori nella chiamata
    if(dati.error != 1):
        # Lettura del file csv direttamente da web e poi importato nel pandas
        # Lettura da url per ora facciamo in locale finchè il dataset non viene messo apposto
        df = pd.read_csv(dati.csv_url, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')
        try:
            df = df.rename(columns={'Presenza_wi-fi': 'Presenza_Wi-fi'})
            df['Presenza_Wi-fi'].replace({"No":"NO","Si":"SI"}, inplace=True)
            df['Accessibilita'].replace({"No":"NO","Si":"SI"}, inplace=True)
        except Exception as e:
            print("Errore")

        # SALVO PER L'ASSOCIAZIONE SUCCESSIVA
        if(isinstance(dfTot, pd.DataFrame)):
            dfTot = pd.concat([dfTot,df])
        else:
            dfTot = df
        print("Dati ultimo aggiornamento di "+list_comuni[index]+": "+dati.ultimo_aggiornamento)
        lista_aggiornamenti.append(dati.ultimo_aggiornamento)



################################################################################
        #########################
        #        Content        #
        #########################

        mappaPng = CityMap(list_comuni[index], df)

        mappaPng.plot_points()
        graficoMappa = mappaPng.save('mappa'+list_comuni[index])

        contents.append(Immagine(graficoMappa, -10, 75, 140, 110))

        # Accessibilità disabili
        dfAccesibilita = df.groupby('Accessibilita').size().reset_index(name='Counts')
        graficoA = grafici.luoghiEventiPercentageAccess(dfAccesibilita)

        contents.append(Immagine(graficoA, 60, 190, 50, 60))
        dfTop3 = ""
        # Restituisce e printa le prima tre ricorrrenze per capienza
        # Questo funziona il problema è che il dataset non è formattato correttamente
        dfTop3 = df.nlargest(3, 'Capacita_max')
        a = Tabella(125, 190, dataframe = dfTop3,
            header = ["I 3 luoghi più capienti", "Posti"],
            header_spacing = 13,
            campi = ["Denominazione", "Capacita_max"], wcampi = [60,10], acampi = ["", "C"],
            offsetY = 10,
            fontsize = 8)
        contents.append(a)

        # Accesso wifi

        # Serve un rename prechè per esempio alcuna compialzione dei dataset hanno messo tutto in minuscolo
        try:
            df = df.rename(columns={'Presenza_wi-fi': 'Presenza_Wi-fi'})
        except Exception as e:
            print("Errore")
        dfWifi = df.groupby('Presenza_Wi-fi').size().reset_index(name='Counts')
        graficoB = grafici.luoghiEventiPercentageWifi(dfWifi)
        contents.append(Immagine(graficoB, 10, 190, 50, 60))

        # Luoghi per tipologia (teatro, sala, etc.) HORIBAR
        dfAggr = df.groupby('Tipo').size().reset_index(name='Counts')
        dfAggr = dfAggr.sort_values(by='Counts', ascending=False)



        title="Luoghi per tipologia"
        contents.append(Testo(title, 135, 75, size=16, align='C'))

        nomeBar = grafici.barH(dfAggr['Tipo'], dfAggr['Counts'], "horiBar", cmaps = "RdPu", title="")
        contents.append(Immagine(nomeBar, 105, 91, 90, 60))

        supp = dati.ultimo_aggiornamento.split("T")[0].split("-")
        aggiornamento = supp[2]+"-"+supp[1]+"-"+supp[0]

        generator = PdfGen("Luoghi per Eventi del comune di "+list_comuni[index], aggiornamento, dati.licenza)
        generator.setHeader()
        generator.setFooter("luoghieventi")
        generator.content(contents)
        generator.savePdf(list_comuni[index].replace(" ", "")+"Eventi")

# Clear del content per fare passare ai dati aggregati
contents.clear()

#####################################
#        Creazione aggregato        #
#####################################

# Verifichiamo che nel dfTot ci sia qualcosa
# Se è un'istanza di DataFrame vuol dire che è stato riempito sopra e quindi
# sono sicuro che contenga qualcosa
if(isinstance(dfTot, pd.DataFrame)):
    mappaPng = CityMap("ALL", dfTot)
    grafici = Graph()
    dfGroupComune = dfTot.groupby("Comune").size().reset_index(name='Counts')


    mappaPng.plotNumberCenter(dfGroupComune, "COMUNE", "Comune", "RdPu", "Counts", title="")
    graficoMappa = mappaPng.save('mappaAll')

    contents.append(Immagine(graficoMappa, -10, 75, 140, 110))

    #def __init__(self, text, x, y, size = 8, align = '', font = "Arial", w = 10):
    title = "Numero luoghi per comune"
    contents.append(Testo(title, 25, 75, size=16, align='C'))

    # % Accessibilità disabili
    dfAccesibilita = dfTot.groupby('Accessibilita').size().reset_index(name='Counts')
    graficoA = grafici.luoghiEventiPercentageAccess(dfAccesibilita)
    contents.append(Immagine(graficoA, 60, 190, 50, 60))

    # Restituisce e printa le prima tre ricorrrenze per capienza
    dfTop5 = dfTot.nlargest(5, 'Capacita_max')

    contents.append(Tabella(120, 190, dataframe = dfTop5,
        header = ["I 5 luoghi più capienti", "", "Posti"],
        header_spacing = 12,
        campi = ["Denominazione", "Comune", "Capacita_max"], wcampi = [40, 30, 10], acampi = ["", "","C"],
        offsetY = 10,
        fontsize = 8))

    # Accesso wifi
    dfWifi = dfTot.groupby('Presenza_Wi-fi').size().reset_index(name='Counts')
    graficoB = grafici.luoghiEventiPercentageWifi(dfWifi)
    contents.append(Immagine(graficoB, 10, 190, 50, 60))

    # Luoghi per tipologia (teatro, sala, etc.)
    dfAggr = dfTot.groupby('Tipo').size().reset_index(name='Counts')
    # In questo modo vado a sortare le varie tipologie partendo da chi ne ha di piuu a chi ne ha di meno
    dfAggr = dfAggr.sort_values(by='Counts', ascending=False)
    nomeBar = grafici.barH(dfAggr['Tipo'], dfAggr['Counts'], "horiBar", cmaps="RdPu", labelsize = 16, title="")
    contents.append(Immagine(nomeBar, 105, 91, 90, 60))

    title="Luoghi per tipologia"
    contents.append(Testo(title, 135, 75, size=16, align='C'))

    contents.append(Testo("*Dove non è presente il dato sarà disponibile prossimamente", 10, 258))

    # Stampa del pdfgen

    generator = PdfGen("Luoghi per eventi presenti sul territorio", "", "cc-by-4.0")
    generator.setHeader()
    generator.setFooter("luoghieventi")
    generator.content(contents)
    generator.savePdf("aggrEventi")
