import pesca.pesca as p
import pandas as pd
from pyproj import Proj
import geopandas
from graph.graph import Graph
from pdfgen.pdfgen import PdfGen
import time
import matplotlib.pyplot as plt
import numpy as np
from citymap.citymap import CityMap
from pdfgen.ContentSettings import ContentSettings
from pdfgen.ContentSettings import Tabella
from pdfgen.ContentSettings import Testo
from pdfgen.ContentSettings import Immagine
from graph.graph import percentAreeVerdi
from graph.graph import make_autopct


#################################################################################################################################
# Verdi pubblicati      #  Corretto #                       id                  #                      NOTE                     #
#################################################################################################################################
#       Schio           #   Si      #   dd6e674f-bd15-4783-add6-435e5ddadd53    # v. doc
#       Thiene          #   XX      #
#      Valdagno         #   Si      #   079ff64c-c985-4e19-9ee3-a0cd6b555449    #
#    Isola Vicentina    #   Si      #   1a18213d-e244-4478-ad7d-0f35df8fe90f    #
#       Malo            #   Si      #   07a36923-3aea-446a-921c-efd424be9d3c    #
#      Marano           #   XX      #                                           #
#    Monte di Malo      #   Si      #   2af8039a-48a4-42f8-a046-6233a3704cd7    #
#    Santorso           #   XX      #                                           #
# San Vito di Leguzzano #   XX      #                                           #
#     Torrebelvicino    #   XX      #                                           #
#     Villaverla        #   XX      #                                           #
#       Zugliano        #   XX      #                                           #
#################################################################################################################################


###################################
#        Creazione singolo        #
###################################
url = 'https://dati.veneto.it/SpodCkanApi/api/2/rest/dataset/'
list_id =   [   "07a36923-3aea-446a-921c-efd424be9d3c",
                "dd6e674f-bd15-4783-add6-435e5ddadd53",
                "3a5f32a2-97d6-4edc-84c5-84edacc6852a",
                "079ff64c-c985-4e19-9ee3-a0cd6b555449",
                "2af8039a-48a4-42f8-a046-6233a3704cd7",
                "1a18213d-e244-4478-ad7d-0f35df8fe90f",

            ]
# Questo mi serve per poi creare il pdf su servant
list_comuni = [ "Malo","Schio", "Thiene", "Valdagno", "Monte di Malo", "Isola Vicentina",]
################################################################################
contents = []
grafici = Graph()

# Le seguenti variabili serviranno poi per effettuare la parte di generazione
# con i dati aggregati
lista_aggiornamenti = []
dfTot = ""

print("Dataset - Aree Verdi")
for index,id in enumerate(list_id):
    # Qui andiamo sia a prendere i dati sia a salvarli su un'altra
    # variabile per poi andare a manipolare per creare il dato aggregato

    dati = p.Pesca(list_comuni[index], url + list_id[index])

    # Check dati non trovati o errori nella chiamata
    if(dati.error != 1):
        # Lettura del file csv direttamente da web e poi importato nel pandas
        # Lettura da url per ora facciamo in locale finchè il dataset non viene messo apposto
        df = pd.read_csv(dati.csv_url, sep=';', encoding='ISO-8859-1', on_bad_lines='skip')

        try:
            print("Comune di " + list_comuni[index])
            df = df.rename(columns={'Classificazione': 'CLASSIFICAZIONE'})
            df = df.rename(columns={'Area_mq': 'AREA_MQ'})
            df = df.rename(columns={'Nome_area': 'NOME_AREA'})
            print("Tipo della colonna")
            if(type(df["AREA_MQ"].loc[0]) == str):
                df['AREA_MQ'] = df['AREA_MQ'].str.replace(',', '.').astype(float)
            df["AREA_MQ"] = np.round(df['AREA_MQ'], decimals=2)

        except Exception as e:
            print("Errore")

        # Replace delle stringhe non valida - pulizia dataset
        try:
            df["CLASSIFICAZIONE"] = df["CLASSIFICAZIONE"].str.replace('2 - Parchi Urbani','2 - Parchi urbani')
        except Exception as e:
            print("Errore conversione classificazione")

        # Convertiamo in due decimali l'area mq

        # SALVO PER L'ASSOCIAZIONE SUCCESSIVA
        if(isinstance(dfTot, pd.DataFrame)):
            dfTot = pd.concat([dfTot,df])
        else:
            dfTot = df
        print("Dati ultimo aggiornamento di "+list_comuni[index]+": "+dati.ultimo_aggiornamento)
        lista_aggiornamenti.append(dati.ultimo_aggiornamento)

        #########################
        #        Content        #
        #########################

        # Raggruppamento per istat class e la somma dei mq corrispondenti
        # Tondino
        dfIstatArea = df.groupby('CLASSIFICAZIONE')['AREA_MQ'].agg('sum').to_frame()
        graficoDonutArea = percentAreeVerdi(dfIstatArea)
        contents.append(Immagine(graficoDonutArea, 110, 80, 90 ,60))
        contents.append(Testo("Percentuale sul totale dei metri quadri", 110, 75, align="C", size=14))

        # Luoghi per tipologia (di ISTAT_CLAS)
        dfAggr = df.groupby('CLASSIFICAZIONE').size().reset_index(name='Counts')

        sorted = dfAggr.sort_values(by='Counts', ascending=False)
        nomeBar = grafici.barH(sorted['CLASSIFICAZIONE'], sorted['Counts'], "horiBarVerdi", "Greens", labelsize = 18, title= "")

        contents.append(Immagine(nomeBar, 10, 85,90,55))
        contents.append(Testo("Aree Verdi - Numero per tipologia", 25, 75, align="C", size=14))

        # 5 aree più grandi a livello di mq
        # Aggiungere campo all'inizio del dataframe
        dfTop5 = df.nlargest(5, 'AREA_MQ')

        # Questo viene inserito per fare l'header, ma posso farlo anche attraverso
        # le classi apposite di ContentSettings

        contents.append(Tabella(10, 175, dataframe = dfTop5,
            header = ["Le 5 aree verdi più estese", "m²"],
            header_spacing = 12,
            campi = ["NOME_AREA", "AREA_MQ"], wcampi = [70, 20], acampi = ['', 'C'],
            offsetY = 9,
            fontsize = 7))

        # Somma totale mq
        dfCountMQ = df['AREA_MQ'].sum()
        # Per la formattazione a due come decimali
        nfloat = "%.2f" %(dfCountMQ)
        text = "Totale m² presenti nel comune"

        #def areeVerdiSingoloTondo (self, centerValue, filename, color = "red"):
        tondo = grafici.areeVerdiSingoloTondo(nfloat, "tondomq", color ="#33cc33")

        # Addiamo il tondo e il realtivo testo
        #Immagine def __init__(self, location, x, y, w, h):
        contents.append(Immagine(tondo, 140, 190, 30, 30))
        contents.append(Testo(text, 120, 175, size= 14, align= 'C'))

        supp = dati.ultimo_aggiornamento.split("T")[0].split("-")
        aggiornamento = supp[2]+"-"+supp[1]+"-"+supp[0]

        generator = PdfGen("Aree verdi presenti nel comune di " + list_comuni[index], aggiornamento, "cc-by-4.0")
        generator.setHeader()
        generator.setFooter("areeverdi")
        generator.content(contents)
        generator.savePdf(list_comuni[index].replace(" ", "")+"AreeVerdi")
        contents.clear()



# Clear del content per fare passare ai dati aggregati
contents.clear()

#####################################
#        Creazione aggregato        #
#####################################


# Verifichiamo che nel dfTot ci sia qualcosa
# Se è un'istanza di DataFrame vuol dire che è stato riempito sopra e quindi
# sono sicuro che contenga qualcosa
if(isinstance(dfTot, pd.DataFrame)):
    dfMQxComune = dfTot.groupby('COD_ISTAT_Comune')['AREA_MQ'].sum().to_frame()
    # Variabile citymap per l'utilizzo dell funzione contenuta nella classe
    pezzato = CityMap()

    # PRO_COM nello shapefile è il numero identificativo del comune utilizzando il codice istat
    # Aggreghiamo il dataframe con i dati presenti nello shapefile con chiave comune -> il codice istat
    # sul dataframe dfMQxComune codice istat è COD_ISTAT mentre nei dati dello shapefile è PRO_COM
    pezzato.plotAllBased(   dfMQxComune, 'PRO_COM', 'COD_ISTAT_Comune', "Greens", "", 14,
                            columnDisplay = "AREA_MQ")
    supp = pezzato.save("allcomuni")
    contents.append(Immagine(supp, 90, 160, 120, 100))
    contents.append(Testo("Distribuzione m² totali per comune", 113, 155, align="C", size= 14))

    # Variabile divisa per CLASSIFICAZIONE e per ciascuno la somma di MQ
    dfIstatArea = dfTot.groupby('CLASSIFICAZIONE')['AREA_MQ'].agg('sum').to_frame()

    graficoDonutArea = percentAreeVerdi(dfIstatArea)
    contents.append(Immagine(graficoDonutArea, 110, 80, 90 ,60))
    contents.append(Testo("Percentuale sul totale dei metri quadri", 110, 75, align="C", size=14))

    # Raggruppare per CLASSIFICAZIONE e fare i counts di ciascuno
    # Luoghi per tipologia (di CLASSIFICAZIONE)

    dfAggr = dfTot.groupby('CLASSIFICAZIONE').size().reset_index(name='Counts')

    sorted = dfAggr.sort_values(by='Counts', ascending=False)
    nomeBar = grafici.barH(sorted['CLASSIFICAZIONE'], sorted['Counts'], "horiBarVerdi", "Greens", labelsize = 18, title= "")

    contents.append(Immagine(nomeBar, 10, 85,90,55))
    contents.append(Testo("Aree Verdi - Numero per tipologia", 25, 75, align="C", size=14))

    # Mostrare la top 5 delle aree mq e il relativo comune di appartenenza
    dfTop5 = dfTot.nlargest(5, 'AREA_MQ')
    contents.append(Tabella(10, 175, dataframe = dfTop5,
        header = ["Le 5 aree più estese", "", "m²"],
        header_spacing = 10,
        campi = ["NOME_AREA", "Comune", "AREA_MQ"], wcampi = [60, 20, 15], acampi = ['', '', 'C'],
        offsetY = 9,
        fontsize = 7))

    contents.append(Testo('*Dove non è presente il dato sarà disponibile prossimamente', 110, 258))

    # Trovo l'aggionamento più recente e lo salvo in agg
    if(lista_aggiornamenti != []):
        agg = max(lista_aggiornamenti)

    # Reversing dell stringa da formato AAAA-MM-GG a GG-MM-AAAA
    aggiornamento = agg.split("T")[0].split("-")
    agg = aggiornamento[2]+"-"+aggiornamento[1]+"-"+aggiornamento[0]

    generator = PdfGen("Aree verdi presenti sul territorio", "", "cc-by-4.0")
    generator.setHeader()
    generator.setFooter("areeverdi")
    generator.content(contents)
    generator.savePdf("aggrAreeVerdi")
