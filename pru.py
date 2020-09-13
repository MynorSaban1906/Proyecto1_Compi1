from simbolos import *


class Scanner:
    lista_tokens = list()   # lista de tokens
    lista_errores = list()  # lista errores lexico
    pos_errores = list()    # lista de posiciones de errores
    # estado = 0
    lexema = ""
    lista_reservadas=list()

    def __init__(self):
        self.lista_tokens = list()
        self.lista_errores = list()
        self.pos_errores = list()
        self.estado = 0
        self.lexema = ""
        self.lista_reservadas=list()

    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        #self.estado = 0
        self.caracterActual = ''
        
        pos = 0    # almacena la posicion del caracter que se esta analizando
        #for self.pos in range(0,len(self.entrada)-1):
        while pos < len(self.entrada):
            self.caracterActual = self.entrada[pos]            
            
            # S0 -> S1 (Simbolos del Lenguaje)
            if self.caracterActual == "{":
                self.addToken(Simbolo.llaveIzq, "{",pos)                   
            elif self.caracterActual == "}":
                self.addToken(Simbolo.llaveDer, "}",pos)
            elif self.caracterActual == ":":
                self.addToken(Simbolo.Dpuntos, ":",pos)
            elif self.caracterActual == ";":
                self.addToken(Simbolo.Pcoma, ";",pos)
            elif self.caracterActual == ",":
                self.addToken(Simbolo.coma, ",",pos)
            elif self.caracterActual == "+":
                self.addToken(Simbolo.Mas, "+",pos)
            elif self.caracterActual == "-":
                self.addToken(Simbolo.Menos, "-",pos)
            elif self.caracterActual == "*":
                self.addToken(Simbolo.Asterisco, "*",pos)
            elif self.caracterActual == "/":
                self.addToken(Simbolo.Division, "/",pos)
            elif self.caracterActual == "(":
                self.addToken(Simbolo.ParentIzq, "(",pos)
            elif self.caracterActual == ")":
                self.addToken(Simbolo.ParentDer, ")",pos)
            elif self.caracterActual == "'":
                self.addToken(Simbolo.comillaSimple, "'",pos)


            # S0 -> S2 (Numeros)
            elif self.caracterActual.isnumeric():
                sizeLexema = self.getSizeLexema(pos)
                self.S2(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                
            # S0 -> Reservadas | Identificadores
            elif self.caracterActual.isalpha() :  
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
            
            # S0 -> '#'
            elif self.caracterActual == "#" :  
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
            
            # S0 -> '.'
            elif self.caracterActual == "." :  
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema

            # Otros
            elif self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\r" or self.caracterActual == "\n":  
                pos += 1 #incremento del contador del while
                continue

            else:                    
                # S0 -> FIN_CADENA
                if self.caracterActual == "$" and pos == len(self.entrada)-1:
                    if len(self.lista_errores) > 0:
                        return "corregir los errores"
                    return "analisis exitoso...!!!"
                #  S0 -> ERROR_LEXICO
                else:
                    self.pos_errores.append(pos)
                    print("Error Lexico: ", self.caracterActual)

            pos += 1 #incremento del contador del while

        if len(self.pos_errores)>0:
            return "La entrada que ingresaste fue: " + self.entrada + "\nExiten Errores Lexicos"
        else:
            return "La entrada que ingresaste fue: " + self.entrada + "\nAnalisis exitoso..!!!"
            

    #--------------------------- ESTADO2 ---------------------------
    def S2(self, posActual, fin):
        c = '' 
        while posActual < fin:
            c = self.entrada[posActual]

            # S2 -> S2 (Numero)
            if c.isnumeric() :
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.VALOR, self.lexema,posActual)
                
            # S2 -> S3 (letra)
            elif c.isalpha():
                self.S3(posActual, fin)
                break
            
            elif c=="%":
                self.lexema+=c
                print("acepto el %")
                self.S2(posActual+1,fin)
                

            # S2 -> ERROR_LEXICO
            else:                    
                self.pos_errores.append(posActual)
                print("Error Lexico: ", c)
            
            posActual += 1

    #--------------------------- ESTADO3 ---------------------------
    def S3(self, posActual, fin):
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
        
            # S3 -> S3 (letra)
            if c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.VALOR, self.lexema,posActual)
                    
            # S2 -> ERROR_LEXICO
            else:
                self.pos_errores.append(posActual)
                print("Error Lexico: ", c)
            posActual += 1

    #--------------------------- RESERVADAS/ID ---------------------------
    def analizar_Id_Reservada(self, posActual, fin):
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]

        # S0 -> S4 (Palabras Reservadas)
        if (self.lexema.lower() == "color"):
            self.addTokens(Simbolo.color, "color",posActual)
            return
        elif(self.lexema.lower() == "border"):
            self.addTokens(Simbolo.border, "border",posActual)
            return
        elif(self.lexema.lower() == "text-align"):
            self.addTokens(Simbolo.textaling, "text-aling",posActual)
            return
        elif(self.lexema.lower() == "font-weight"):
            self.addTokens(Simbolo.COLOR, "font-weight",posActual)
            return
        elif(self.lexema.lower() == "padding-left"):
            self.addTokens(Simbolo.paddingleft, "padding-left",posActual)
            return
        elif(self.lexema.lower() == "padding-top"):
            self.addTokens(Simbolo.paddingtop, "padding-top",posActual)
            return
        elif(self.lexema.lower() == "line-height"):
            self.addTokens(Simbolo.lineheight, "line-height",posActual)
            return
        elif(self.lexema.lower() == "margin-top"):
            self.addTokens(Simbolo.margintop, "margin-top",posActual)
            return
        elif(self.lexema.lower() == "margin-left"):
            self.addTokens(Simbolo.marginleft, "margin-left",posActual)
            return
        elif(self.lexema.lower() == "display"):
            self.addTokens(Simbolo.display, "display",posActual)
            return
        elif(self.lexema.lower() == "top"):
            self.addTokens(Simbolo.top, "top",posActual)
            return
        elif(self.lexema.lower() == "float"):
            self.addTokens(Simbolo.flotante, "float",posActual)
            return
        elif(self.lexema.lower() == "min-width"):
            self.addTokens(Simbolo.minwidth, "min-width",posActual)
            return
        elif(self.lexema.lower() == "font-weight"):
            self.addTokens(Simbolo.COLOR, "font-weight",posActual)
            return
        elif(self.lexema.lower() == "background-color"):
            self.addTokens(Simbolo.backgroundc, "background-color",posActual)
            return
        elif(self.lexema.lower() == "opacity"):
            self.addTokens(Simbolo.opacity, "opacity",posActual)
            return        
        elif(self.lexema.lower() == "font-family"):
            self.addTokens(Simbolo.fontfamily, "font-family",posActual)
            return
        elif(self.lexema.lower() == "font-size"):
            self.addTokens(Simbolo.fontsize, "font-size",posActual)
            return
        elif(self.lexema.lower() == "padding-right"):
            self.addTokens(Simbolo.paddingright, "padding-right",posActual)
            return
        elif(self.lexema.lower() == "padding"):
            self.addTokens(Simbolo.padding, "padding",posActual)
            return
        elif(self.lexema.lower() == "width"):
            self.addTokens(Simbolo.width, "width",posActual)
            return
        elif(self.lexema.lower() == "margin-right"):
            self.addTokens(Simbolo.marginright, "margin-right",posActual)
            return
        elif(self.lexema.lower() == "position"):
            self.addTokens(Simbolo.position, "position",posActual)
            return
        elif(self.lexema.lower() == "right"):
            self.addTokens(Simbolo.right, "right",posActual)
            return
        elif(self.lexema.lower() == "clear"):
            self.addTokens(Simbolo.clear, "clear",posActual)
            return
        elif(self.lexema.lower() == "max-height"):
            self.addTokens(Simbolo.maxheight, "max-height",posActual)
            return
        elif(self.lexema.lower() == "background-image"):
            self.addTokens(Simbolo.backgroundi, "background-image",posActual)
            return
        elif(self.lexema.lower() == "background"):
            self.addTokens(Simbolo.background, "background",posActual)
            return
        elif(self.lexema.lower() == "font-style"):
            self.addTokens(Simbolo.fontstyle, "font-style",posActual)
            return
        elif(self.lexema.lower() == "font"):
            self.addTokens(Simbolo.font, "font",posActual)
            return
        elif(self.lexema.lower() == "padding-bottom"):
            self.addTokens(Simbolo.paddingbottom, "padding-bottom",posActual)
            return
        elif(self.lexema.lower() == "height"):
            self.addTokens(Simbolo.height, "height",posActual)
            return
        elif(self.lexema.lower() == "margin-bottom"):
            self.addTokens(Simbolo.marginbottom, "margin-bottom",posActual)
            return
        elif(self.lexema.lower() == "border-style"):
            self.addTokens(Simbolo.borderstyle, "border-style",posActual)
            return     
        elif(self.lexema.lower() == "bottom"):
            self.addTokens(Simbolo.bottom, "bottom",posActual)
            return
        elif(self.lexema.lower() == "left"):
            self.addTokens(Simbolo.left, "left",posActual)
            return
        elif(self.lexema.lower() == "max-width"):
            self.addTokens(Simbolo.maxwidth, "max-width",posActual)
            return
        elif(self.lexema.lower() == "min-height"):
            self.addTokens(Simbolo.minheight, "min-height",posActual)
            return

        self.lexema = ""
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
            
            # S0 -> S5 ('#')
            if c == "#":
                self.lexema += c
                
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break
            elif c == ".":
                self.lexema += c
                
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break

            # S0 -> S6 (letra)
            elif c.isalpha():
                self.S6(posActual, fin)
                break
            
            # S0 -> ERROR_LEXICO
            else:
                self.pos_errores.append(posActual)
                print("Error Lexico: ", c)
            
            posActual += 1
            
    #--------------------------- ESTADO6 ---------------------------
    def S6(self, posActual, fin):
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
        
            # S6 -> S6 (letra)
            if c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.ID, self.lexema,posActual)

            # S6 -> S6 (Numero)
            elif c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.ID, self.lexema,posActual)
            
            # S6 -> S6 ('-')
            elif c == "-":
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.ID, self.lexema,posActual)

            # S6 -> ERROR_LEXICO
            else:
                self.pos_errores.append(posActual)
                print("Error Lexico: ", c)

            posActual += 1

    #--------------------------- ESTADO_ERROR ---------------------------
    def addError(self, entrada, estado):
        
        return 0


    #--------------------------- ADD TOKEN ---------------------------
    def addToken(self, tipo, valor,pos):
        nuevo = Token(tipo, valor,pos)
        self.lista_tokens.append(nuevo)
        self.caracterActual = ""
        self.estado = 0
        self.lexema = ""

    #---------------- OBTENIENDO EL TAMAÑO DEL LEXEMA ----------------
    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                break
            longitud+=1
        return longitud

    def addTokens(self, tipo, valor,pos):
        nuevo = Token(tipo, valor,pos)
        self.lista_reservadas.append(nuevo)
        self.caracterActual = ""
        self.lexema = ""  