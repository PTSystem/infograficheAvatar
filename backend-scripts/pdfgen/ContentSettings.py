
class ContentSettings:
    '''
    Classe padre per ereditarietà
    '''
    def __init__(self,x,y):

        '''
        x           -> posizione x espressa in mm da cui partire con la creazione
        y           -> posizione y espressa in mm da cui partire con la creazione
        '''
        self.x = x
        self.y = y

# Cominciamo con l'introduzione delle classi
class Immagine(ContentSettings):
    def __init__(self, location, x, y, w, h):
        '''
        location    -> nome del file o percorso + nome
        x           -> posizione x in mm
        y           -> posizione y in mm
        w           -> width
        h           -> height
        '''
        self.location = location
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        super().__init__(x,y)

class Tabella(ContentSettings):
    def __init__(self, x, y,dataframe= 0,
        header = 0,
        header_spacing = 6,
        campi = 0,wcampi = 0, acampi = 0,
        offsetY = 6, fontsize = 6, border = 1):
        super().__init__(x,y)
        '''
        dataframe   -> DATI
        x           -> posizione x espressa in mm da cui partire con la creazione
        y           -> posizione y espressa in mm da cui partire con la creazione
        header      -> header della tabella
        campi       -> array dei campi che si vogliono stampare ex. ["campo1", "campo2", "campo3"]
        wcampi      -> width della tabella per ciascun campo
        acampi      -> align dei vari campi
        offsetY     -> offset tra i vari elementi della tabella
        fontsize    -> grandezza del carattere all'interno della tabella
        border      -> 1 = mostra, 0 = non mostrare
        '''
        self.dataframe = dataframe
        self.header = header
        self.header_spacing = header_spacing
        self.campi = campi
        self.wcampi = wcampi
        self.acampi = acampi
        self.offsetY = offsetY
        self.fontsize = fontsize
        self.border = border
    def print(self):
        print(
        "dataframe   ->" +"DATI\n" +
        "x           ->" +str(self.x)+ "\n" +
        "y           ->" +str(self.y)+"\n" +
        "header      ->" + str(self.header)+"\n" +
        "campi       ->" + str(self.campi)+"\n" +
        "wcampi      ->" + str(str(self.wcampi))+"\n" +
        "acampi      ->" + str(str(self.acampi))+"\n" +
        "offsetY     ->" +str(self.offsetY)+"\n" +
        "fontsize    ->" +str(self.fontsize)+"\n" +
        "border      ->" +str(self.border)+"\n")

class Testo(ContentSettings):
    def __init__(self, text, x, y, size = 8, align = '', font = "Arial", w = 10):
        super().__init__(x,y)
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.align = align
        self.font = font
        self.w = w

class TestoMulti(ContentSettings):
    def __init__(self, text, x, y, size = 8, align = '', font = "Arial", w = 0, h = 0, border = 0):
        super().__init__(x,y)
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.align = align
        self.font = font
        self.w = w
        self.h = h
        self.border = border

