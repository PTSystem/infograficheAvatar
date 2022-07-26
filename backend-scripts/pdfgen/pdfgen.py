from fpdf import FPDF
from datetime import date
import os, sys
from pdfgen.ContentSettings import ContentSettings
from pdfgen.ContentSettings import Immagine
from pdfgen.ContentSettings import Tabella
from pdfgen.ContentSettings import Testo
from pdfgen.ContentSettings import TestoMulti

class PdfGen:
    def __init__ (self, descrizione, ultimo_aggiornamento, licenza):
        self.pdf = FPDF()
        self.descrizione = descrizione
        self.ultimo_aggiornamento = ultimo_aggiornamento
        self.licenza = licenza
        self.pdf.add_page()
        self.pdf.set_auto_page_break(False)

    def setHeader (self):
        # Header
        self.pdf.image(os.getcwd()+'\pdfgen\header\header_xl.png', 10, 12, w=50, h=15)
        self.pdf.image(os.getcwd()+'\pdfgen\header\por.png', 180, 10, w=20, h =20)
        self.pdf.image(os.getcwd()+'\pdfgen\header\comuni_partecipanti.png', 10, 35, 190)
        self.pdf.line(10,53, 200,53)

    # Standard Footer
    def setFooter (self, webapp = ""):
        # Position at 260 mm from top
        self.pdf.set_font('Arial', 'I', 8)
        self.pdf.line(10,265, 200,265)
        self.pdf.set_y(273)
        self.pdf.cell(0, 0, 'Fonte dati: Portale Open Data Veneto - https://dati.veneto.it')
        self.pdf.ln(5)
        if(self.ultimo_aggiornamento == ""):
            self.pdf.cell(0, 0, 'Data pubblicazione: '+date.today().strftime("%d-%m-%Y"))
        else:
            self.pdf.cell(0, 0, 'Data pubblicazione: '+date.today().strftime("%d-%m-%Y") + "  |  "+ 'Ultimo aggiornamento dataset: '+self.ultimo_aggiornamento)
        self.pdf.ln(5)
        self.pdf.cell(0, 0, 'Tipo di licenza: '+self.licenza) #qui inserire i dati presi dall'api
        self.pdf.ln(5)
        self.pdf.cell(0, 0, 'Progetto Finanziato con il POR FESR 2014-2020 Regione del Veneto - www.avatarlab.it')

        self.pdf.set_y(270)
        self.pdf.set_x(180)
        cur_dir = sys.path[0]
        # a questo punto inserire l'immagine e il testo relativo

        self.pdf.set_font('Arial', '', 8)
        if(webapp == "areeverdi"):
            self.pdf.image(cur_dir+"\\pdfgen\\qr\\areeVerdi.jpg", 125, 270, 20, 20)
            #self.pdf.cell()
            self.pdf.set_y(272)
            self.pdf.cell(140)
            self.pdf.cell(0, 0, "Scopri le aree verdi presenti sul territorio")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Scannerizza il codice!")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Oppure vai su:")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"https://areeverdiapp.avatarlab.it/")

        if(webapp == "fontanelle"):
            self.pdf.image(os.getcwd()+"\\pdfgen\\qr\\fontanelle.jpg", 125, 270, 20, 20)
            self.pdf.set_y(272)
            self.pdf.cell(140)
            self.pdf.cell(0, 0, "Scopri le fontanelle presenti sul territorio")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Scannerizza il codice!")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Oppure vai su:")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"https://fontanelleapp.avatarlab.it/")
        if(webapp == "luoghieventi"):
            self.pdf.image(os.getcwd()+"\\pdfgen\\qr\\luoghiEventi.jpg", 125, 270, 20, 20)
            self.pdf.set_y(272)
            self.pdf.cell(140)
            self.pdf.cell(0, 0, "Scopri i luoghi per eventi presenti sul territorio")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Scannerizza il codice!")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Oppure vai su:")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"https://luoghipereventiapp.avatarlab.it/")
        if(webapp == "offertaformativa"):
            self.pdf.image(os.getcwd()+"\\pdfgen\\qr\\offertaformativa.jpg", 125, 270, 20, 20)
            self.pdf.set_y(272)
            self.pdf.cell(140)
            self.pdf.cell(0, 0, "Scopri l'offerta formativa nel territorio")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Scannerizza il codice!")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Oppure vai su:")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"https://offertaformativaapp.avatarlab.it/")
        if(webapp == "parcheggi"):
            self.pdf.image(os.getcwd()+"\\pdfgen\\qr\\parcheggi.jpg", 125, 270, 20, 20)
            self.pdf.set_y(272)
            self.pdf.cell(140)
            self.pdf.cell(0, 0, "Scopri i parcheggi presenti sul territorio")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Scannerizza il codice!")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"Oppure vai su:")
            self.pdf.ln(5)
            self.pdf.cell(140)
            self.pdf.cell(0, 0,"https://parcheggiapp.avatarlab.it/")



    #qua si potrebbe inserire una lista all'interno della quale
    #riuscire a posizionare gli elementi
    def content(self, contents=[]):

        # Content
        self.pdf.set_font('Arial', '', 16)
        self.pdf.set_y(55)
        self.pdf.set_fill_color(222, 222, 222)

        # Titolo - da mettere il dato .notes trovato dal retrieving dell'API
        self.pdf.cell(0, 10, self.descrizione, 0, 1, 'C', fill=1)

        # Qui usare il cont, per ogni elemento passato al cont lo andiamo ad
        # ad inserire all'interno del pdf
        '''
            Struttura content:
                type: testo, immagine, multiline etc.
                nomefile:
                x: Position
                y: Position
                size: grandezza
        '''
        for content in contents:
            if(isinstance(content, ContentSettings)):
                if isinstance(content, Immagine):
                    self.handle_image(content)
                if isinstance(content, Tabella):
                    self.handle_table(content)
                if isinstance(content, Testo):
                    self.handle_testo(content)
                if isinstance(content, TestoMulti):
                    self.handle_testo_multi(content)



    def handle_image (self, content):
        self.pdf.image(
            content.location,
            content.x, content.y,
            content.w, content.h
            )
    def handle_table(self, content):
        line_height = content.fontsize * 1.2
        self.pdf.set_xy(content.x, content.y)
        y = content.y

        # HEADER
        for index, campo in enumerate(content.campi):
            self.pdf.set_font('Arial', size = content.fontsize*2)
            self.pdf.cell(content.wcampi[index], line_height, str(content.header[index]), border=0, align = content.acampi[index])

        y += content.header_spacing
        # CONTENT
        self.pdf.set_font('Arial', size = content.fontsize)
        #print("CONTENT DA STAMPARE NEL FILE")
        #print(content.dataframe)

        # TODO: verificare perchè vengono stampate anche cose che non hanno a che fare con il comune di appartenenza
        for index, row in content.dataframe.iterrows():
            #print(row["Denominazione"], row["Capacita_max"])
            #print(row)
            self.pdf.set_xy(content.x, y)
            for index, campo in enumerate(content.campi):
                self.pdf.cell(content.wcampi[index], line_height, str(row[campo]), border= content.border, align = content.acampi[index])

            self.pdf.ln(line_height)
            y += content.offsetY

    def handle_testo(self, content):
        self.pdf.set_font('Arial', size = content.size)
        self.pdf.set_xy(content.x, content.y)
        self.pdf.cell(0, content.w, content.text)

    def handle_testo_multi(self, content):
        self.pdf.set_font('Arial', size = content.size)
        self.pdf.set_xy(content.x, content.y)
        self.pdf.multi_cell(content.w, content.h, content.text)

    def insertImage (self, loc, x, y, w, h):
        self.pdf.image(loc, x, y, w, h)

    def insertText (self, text, x, y, sz = 8):
        self.pdf.set_font('Arial', size = sz)
        self.pdf.set_xy(x, y)
        self.pdf.cell(0, 10, text)

    def insertMulti (self, text, x, y, sz = 8):
        self.pdf.set_font('Arial', size = sz)
        self.pdf.set_xy(x, y)
        self.pdf.cell(0, 10, text)

    def insertMultiLine (self, text, x, y):
        self.pdf.set_font('Arial', '', 8)
        self.pdf.set_xy(x, y)
        self.pdf.multi_cell(0, 3, text)

    def savePdf (self, name):
        self.pdf.output(name+'.pdf')
        self.pdf.close()

    def insertTableFromDf(self, dataframe, x, y):
        y += 5
        self.pdf.set_font('Arial', size = 8)
        line_height = self.pdf.font_size * 2
        for index, row in dataframe.iterrows():
            #print(row["Denominazione"], row["Capacita_max"])
            self.pdf.set_xy(x, y)
            self.pdf.cell(40, line_height, str(row["Denominazione"]), border=1)
            self.pdf.cell(20, line_height, str(row["Capacita_max"]), border=1, align='C')
            self.pdf.ln(line_height)
            y += 10
    def insertTableFromDfMod(self, dataframe, x, y, c1, c2, w=40):
        y += 5
        self.pdf.set_font('Arial', size = 6)
        line_height = self.pdf.font_size * 2
        for index, row in dataframe.iterrows():
            #print(row["Denominazione"], row["Capacita_max"])
            self.pdf.set_xy(x, y)
            if(index == 0):
                self.pdf.set_font('Arial', size = 12)
                self.pdf.cell(w, line_height, str(row[c1]), border=0)
                self.pdf.cell(20, line_height, str(row[c2]), border=0, align='C')
            else:
                self.pdf.set_font('Arial', size = 6)
                self.pdf.cell(w, line_height, str(row[c1]), border=1)
                self.pdf.cell(20, line_height, str(row[c2]), border=1, align='C')
            self.pdf.ln(line_height)
            y += 10
    def insertTableFromDfMod3(self, dataframe, x, y, c1, c2, c3):
        y += 5
        self.pdf.set_font('Arial', size = 6)
        line_height = self.pdf.font_size * 2
        for index, row in dataframe.iterrows():
            #print(row["Denominazione"], row["Capacita_max"])
            self.pdf.set_xy(x, y)
            if(index == 0):
                self.pdf.set_font('Arial', size = 6)
                self.pdf.cell(40, line_height, str(row[c1]), border=1)
                self.pdf.cell(20, line_height, str(row[c2]), border=1)
                self.pdf.cell(20, line_height, str(row[c3]), border=1, align='C')
            else:
                self.pdf.set_font('Arial', size = 6)
                self.pdf.cell(40, line_height, str(row[c1]), border=1)
                self.pdf.cell(20, line_height, str(row[c2]), border=1)
                self.pdf.cell(20, line_height, str(row[c3]), border=1, align='C')
            self.pdf.ln(line_height)
            y += 10
    def insertTableFromDfModAll(self, dataframe, x, y, header, campi, wCampi, offsetY, fontsize):
        '''
        Questo metodo è utilizzato per poter modificare tutti i parametri di
        ingresso in tabella:
        dataframe   -> DATI
        x           -> posizione x espressa in mm da cui partire con la creazione
        y           -> posizione y espressa in mm da cui partire con la creazione
        header      -> header della tabella
        campi       -> campi del dataframe che si volgiono stampare
        wCampi      -> width della tabella per ciascun campo
        offsetY     -> offset tra i vari elementi della tabella
        fontsize    -> grandezza del carattere all'interno della tabella
        '''
        line_height = self.pdf.font_size * 2
        self.pdf.set_xy(x, y)
        for index, campo in enumerate(campi):
            self.pdf.set_font('Arial', size = fontsize*2)
            self.pdf.cell(wCampi[index], line_height, str(header[index]), border=0)
            y += offsetY

        self.pdf.set_font('Arial', size = fontsize)
        for index, row in dataframe.iterrows():
            self.pdf.set_xy(x, y)
            for index, campo in enumerate(campi):
                self.pdf.cell(wCampi[index], line_height, str(row[campo]), border=1)

            self.pdf.ln(line_height)
            y += offsetY
