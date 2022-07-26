import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
from pyproj import Proj
import os
import matplotlib as mpl
#from ..utils.utils import UTILS

# Ubuntu
# shp_path = os.getcwd() +"/citymap/comuni_dettagliata/Com01012022_WGS84.shp"
shp_path = os.getcwd() +"\citymap\comuni_dettagliata\Com01012022_WGS84.shp"

class CityMap:
    def __init__(self, city = "", df = "", onlyCity = 0):
        self.city = city
        self.df = df
        # onlyCity per effettuare la stampa solo della mappa senza le coordinate
        # di latitudine e Longitudine
        self.onlyCity = onlyCity
        # Lettura dello shapefile
        comuniDett = geopandas.read_file(shp_path)

        # Printare gli headers
        #print ("List of headers are: ", list(comuniDett.columns.values))
        # Prima scrematura prendo solamente i campi selezionati
        comuniDett=comuniDett[['COD_REG','COMUNE','geometry']]

        # Trovare solo una determinata regione conoscendo il codice regione
        # 5 = codice regione veneto
        comuniVenetiDett=comuniDett[comuniDett['COD_REG'] == 5]

        # Nel caso la city passata sia ALL significa che ci aspettiamo di
        # ottenere i dati aggregati
        if(self.city == "ALL"):
            self.federazioneComuni = comuniVenetiDett[comuniVenetiDett['COMUNE'].isin(["Isola Vicentina", "Malo","Marano Vicentino","Monte di Malo","San Vito di Leguzzano",
            "Santorso",
            "Schio",
            "Thiene",
            "Torrebelvicino",
            "Valdagno",
            "Villaverla",
            "Zugliano"
            ]) == True]
        else:
            # Trovare comune singolo
            self.comuneSingoloDett = comuniVenetiDett[comuniVenetiDett['COMUNE'].isin([self.city]) == True]

    def plot_points(self, df = []):

        if(self.city == "ALL"):
            # Pyproj per convertire le coordinate da wgs84 a ED50/UTM
            p = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=True)

            # Creo due nuovi campi utilizzati per plottare correttamente le
            # coordinate
            self.df["x"], self.df["y"] = p(self.df['Longitudine'], self.df['Latitudine'])

            # Creazione dell'oggetto geometry che andrà ad indicare un punto
            # specifico all'interno del grafico
            gdf = geopandas.GeoDataFrame(
                self.df, geometry=geopandas.points_from_xy(self.df.x, self.df.y))

            print("Tipo dato Federazione comuni: " +str(type(self.federazioneComuni)))
            # Styling della mappa
            ax = self.federazioneComuni.plot(
                color='white', edgecolor='black')

            # Styling dei punti
            gdf.plot(ax=ax, color='red')
            plt.axis('off')
            plt.suptitle('Distribuzione in mappa', fontsize=16)
        else:
            if(self.onlyCity == 1):
                ax = self.comuneSingoloDett.plot(
                    color='white', edgecolor='black')
                plt.axis('off')
                plt.suptitle('Distribuzione in mappa', fontsize=16)
            else:
                # Pyproj per convertire le coordinate da wgs84 a ED50/UTM
                p = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=True)

                # Creo due nuovi campi utilizzati per plottare correttamente le
                # coordinate
                self.df["x"], self.df["y"] = p(self.df['Longitudine'], self.df['Latitudine'])

                # Creazione dell'oggetto geometry che andrà ad indicare un punto
                # specifico all'interno del grafico
                gdf = geopandas.GeoDataFrame(
                    self.df, geometry=geopandas.points_from_xy(self.df.x, self.df.y))

                # Styling della mappa
                ax = self.comuneSingoloDett.plot(
                    color='white', edgecolor='black')

                # Styling dei punti
                gdf.plot(ax=ax, color='red')
                plt.axis('off')
                plt.suptitle('Distribuzione in mappa', fontsize=16)
        if(isinstance(df, pd.DataFrame)):
            #df["Latitudine"].replace({float("NaN"): <<inserisci posizione valida>>}, inplace=True)
            #print(str(Latitudine+ str(df["Latitudine"]) + " Longitudine: "+ str(df["Longitudine"])))
            # Restituisc NaN dove non c'è la longitudine o la latitudine il campo però è sempre float
            # Utilizzo il sorting per vedere se esiste una fontanella con valore latitudine e longitudine
            # per poi utilizzarlo nel replace del NaN se è presente
            s = df.sort_values(by='Latitudine', ascending=False)
            if(s.iloc[0].Latitudine != float("NaN") and s.iloc[0].Longitudine != float("NaN")):
                df["Latitudine"].replace({float("NaN"): s.iloc[0].Latitudine}, inplace=True)
                df["Longitudine"].replace({float("NaN"): s.iloc[0].Longitudine}, inplace=True)
                # Pyproj per convertire le coordinate da wgs84 a ED50/UTM
                p = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=True)

                # Creo due nuovi campi utilizzati per plottare correttamente le
                # coordinate
                self.df["x"], self.df["y"] = p(self.df['Longitudine'], self.df['Latitudine'])

                # Creazione dell'oggetto geometry che andrà ad indicare un punto
                # specifico all'interno del grafico
                gdf = geopandas.GeoDataFrame(
                    self.df, geometry=geopandas.points_from_xy(self.df.x, self.df.y))
                gdf.plot(color= "red")




    def plotAllBased(self, df = "", columnLeft="", columnRight="", cmap = "", title = "", fontsize_title = 8, columnDisplay = "", df2 = ""):
        '''
            Viene plottata l'intera mappa
            Se si necessita di colorarla in base ad un campo esso viene passato per parametro
            e in questa funzione verrà aggregato (utilizzando l'id del campo oppure
            direttamente il campo comune del geodataframe?)
            df              ->  Contiene i valori che verranno utilizzati per la diversa colorazione
                            il dataset deve contenere un campo uguale con il dataframe di destinazione per poi effetuare l'aggregazione
                            per esempio "COMUNE"
            columnLeft      ->  Nome della colonna dello shapefile su cui aggregare
            columnRight     ->  Nome della colonna del dataframe su cui aggregare
            cmap            ->  Mappa colori che si è intenzionati ad usare
            columnDisplay   ->  Colonna sulla quale si baserà la colorazione
            df2             ->  dataframe che serve per prendere le coordinate di latitudine e longitudine
        '''

        comuniDett = geopandas.read_file(shp_path)

        # Salviamo il
        comuniVenetiDett=comuniDett[comuniDett['COD_REG'] == 5]
        comuniAvatar = comuniVenetiDett[comuniVenetiDett['COMUNE'].isin(["Isola Vicentina", "Malo","Marano Vicentino","Monte di Malo","San Vito di Leguzzano",
        "Santorso",
        "Schio",
        "Thiene",
        "Torrebelvicino",
        "Valdagno",
        "Villaverla",
        "Zugliano"
        ]) == True]

        res = pd.merge(comuniAvatar, df, how = "left", left_on=columnLeft, right_on=columnRight)

        # Se non facciamo il replace ci troviamo solo nan e non viene rivelato come numero dalla colonna per fare il display
        res[columnDisplay].replace({float("NaN"): 0}, inplace=True)

        # In questo modo andiamo a inserire le stesso coordinate dei punti
        # dove ho la presenza di punti vuoti, per ovviare ad errori che possono
        # sorgere dovuti alla non presenza di delle coordinate
        if(isinstance(df2, pd.DataFrame)):
            s = df2.sort_values(by='Latitudine', ascending=False)
            if(s.iloc[0].Latitudine != float("NaN") and s.iloc[0].Longitudine != float("NaN")):
                df2["Latitudine"].replace({float("NaN"): s.iloc[0].Latitudine}, inplace=True)
                print("Latitudine: " + str(s.iloc[0].Latitudine))
                df2["Longitudine"].replace({float("NaN"): s.iloc[0].Longitudine}, inplace=True)
                print("Longitudine: " + str(s.iloc[0].Longitudine))
                # Pyproj per convertire le coordinate da wgs84 a ED50/UTM
                p = Proj(proj='utm',zone=32,ellps='WGS84', preserve_units=True)

                # Creo due nuovi campi utilizzati per plottare correttamente le
                # coordinate
                df2["x"], df2["y"] = p(df2['Longitudine'], df2['Latitudine'])

                # Creazione dell'oggetto geometry che andrà ad indicare un punto
                # specifico all'interno del grafico
                gdf = geopandas.GeoDataFrame(
                    df2, geometry=geopandas.points_from_xy(df2.x, df2.y))
                gdf.plot(color= "red")
        # Styling dei punti
        ax = res.plot(column=columnDisplay,cmap=cmap, edgecolor='black', legend=True)

        if(isinstance(df2, pd.DataFrame)):
            gdf.plot(ax=ax, color='red')
        plt.axis('off')
        plt.suptitle(title, fontsize=fontsize_title)

    def save(self, name):
        plt.savefig(name + '.jpg', dpi=300)
        return name + '.jpg'
    def saveXL (self, name):
        plt.savefig(name + '.jpg', dpi=800)
        return name + '.jpg'

    def plotNumberCenter(self, df = "", columnLeft="", columnRight="", cmap = "", columnDisplay="", title = "", fontsize_title = 13, secondaria_no_print=0):
        '''
            Viene plottata l'intera mappa
            Se si necessita di colorarla in base ad un campo esso viene passato per parametro
            e in questa funzione verrà aggregato (utilizzando l'id del campo oppure
            direttamente il campo comune del geodataframe?)
            df              ->  Contiene i valori che verranno utilizzati per la diversa colorazione
                                il dataset deve contenere un campo uguale con il dataframe di destinazione per poi effetuare l'aggregazione
                                per esempio "COMUNE"
            columnLeft      ->  Nome della colonna dello shapefile su cui aggregare
            columnRight     ->  Nome della colonna del dataframe su cui aggregare
            cmap            ->  Mappa colori che si è intenzionati ad usare
            columnDisplay   ->  Colonna sulla quale si baserà la colorazione
            df2             ->  dataframe che serve per prendere le coordinate di latitudine e longitudine
        '''

        comuniDett = geopandas.read_file(shp_path)

        # Salviamo il
        comuniVenetiDett=comuniDett[comuniDett['COD_REG'] == 5]
        comuniAvatar = comuniVenetiDett[comuniVenetiDett['COMUNE'].isin(["Isola Vicentina", "Malo","Marano Vicentino","Monte di Malo","San Vito di Leguzzano",
        "Santorso",
        "Schio",
        "Thiene",
        "Torrebelvicino",
        "Valdagno",
        "Villaverla",
        "Zugliano"
        ]) == True]

        ax = comuniAvatar.plot(edgecolor='black')
        # In res abbiamo solo le voci selezionate
        res = pd.merge(comuniAvatar, df, how = "left", left_on=columnLeft, right_on=columnRight)
        res["Counts"].replace({float("NaN"): 0}, inplace=True)

        min = res["Counts"].min()
        max = res["Counts"].max()

        res.plot(ax = ax, column=columnDisplay,cmap=cmap, edgecolor='black')

        for i,comune in res.iterrows():

            center = comune.geometry.centroid
            if(int(comune.Counts) != 0):
                # Se vado sulla scala colore scura cambio il testo in bianco
                if(int(comune.Counts) > (max-min)/2):
                    plt.text(center.x, center.y, comune.COMUNE, fontsize=7, ha="center", va="center", color="white")
                    plt.text(center.x, center.y-1300, str(int(comune.Counts)), fontsize=18, ha="center", va="center", color="white")
                else:
                    #plt.text(center.x, center.y, comune.COMUNE +"\n"+ str(int(comune.Counts)), fontsize=7, ha="center", va="center")
                    plt.text(center.x, center.y, comune.COMUNE, fontsize=7, ha="center", va="center")
                    plt.text(center.x, center.y-1300, str(int(comune.Counts)), fontsize=18, ha="center", va="center")
            else:
                #plt.text(center.x, center.y, comune.COMUNE, fontsize=7, ha="center", va="center")
                if(secondaria_no_print != 1):
                    plt.text(center.x, center.y, comune.COMUNE, fontsize=7, ha="center", va="center")
                #plt.text(center.x, center.y-50, str(int(comune.Counts)), fontsize=12, ha="center", va="center")

        plt.axis('off')
        plt.suptitle(title, fontsize=fontsize_title)
