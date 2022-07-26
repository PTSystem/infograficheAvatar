from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import json


class Pesca:

    # Per quanto riguarda la città non è necessario formattarlo ma meglio
    # farlo per evitare problemi
    # url corrisponde all'url del dataset di riferimento
    def __init__(self, city, url):

        self.city = city
        self.url = url
        # Questo serve per identificare se è avvenuto un errore di URL
        # oppure un errore nella risposta HTTP
        self.error = 0
        #print(url)
        try:
            response = urlopen(url)
            #print(response)
        except HTTPError as e:
            self.error = 1
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            self.error = 1
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            string = response.read()

        if(self.error != 1):

            json_obj = json.loads(string)
            self.ultimo_aggiornamento = json_obj['metadata_modified']

            # Viene utilizzato 0 pe rprendere il primo elemento della lista
            # può creare problemi nel caso più documenti vengono creati?
            self.csv_url = json_obj['resources'][0]['url']
            self.licenza = json_obj['license']
    def print(self):
        print("URL: "+self.url)
        print('--------------------------------------------------------------------')
        print("Descrizione: "+self.descrizione)
        print("Città: "+self.city)
        print("Ultimo aggiornamento: "+self.ultimo_aggiornamento)
        print('URL csv: '+ self.csv_url)
        print('Licenza: '+ self.licenza)
        print('--------------------------------------------------------------------')
