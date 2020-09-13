from simbolos import *

class analizadorCSS:
    lista_tokens = list()   # lista de tokens
    lista_errores = list()  # lista errores lexico
    pos_errores = list()    # lista de posiciones de errores
    lista_reservadas=list()
    # estado = 0
    lexema = ""

    #estado 1 simbolo
    #estado 2 reservadas
    #estado 3 ids
    #estado 4 los string

    def __init__(self):
        self.lista_tokens = list()
        self.lista_errores = list()
        self.pos_errores = list()
        self.lista_reservadas=list()
        self.estado = 0
        self.lexema = ""

        
    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        self.caracterActual = ''
        self.pos = 0

        while self.pos < len(self.entrada):
            self.caracterActual = self.entrada[self.pos]            
            
            if self.caracterActual == "{":
                self.addToken(Simbolo.llaveIzq, "{",self.pos)                   
            elif self.caracterActual == "}":
                self.addToken(Simbolo.llaveDer, "}",self.pos)
            elif self.caracterActual == ":":
                self.addToken(Simbolo.Dpuntos, ":",self.pos)
            elif self.caracterActual == ";":
                self.addToken(Simbolo.Pcoma, ";",self.pos)
            elif self.caracterActual == ",":
                self.addToken(Simbolo.coma, ",",self.pos)
            elif self.caracterActual == "=":
                self.addToken(Simbolo.Igual, "=",self.pos)
            elif self.caracterActual == "+":
                self.addToken(Simbolo.Mas, "+",self.pos)
            elif self.caracterActual == "-":
                self.addToken(Simbolo.Menos, "-",self.pos)
            elif self.caracterActual == "*":
                self.addToken(Simbolo.Asterisco, "*",self.pos)
            elif self.caracterActual == "/":
                self.addToken(Simbolo.Division, "/",self.pos)
            elif self.caracterActual == "(":
                self.addToken(Simbolo.ParentIzq, "(",self.pos)
            elif self.caracterActual == ")":
                self.addToken(Simbolo.ParentDer, ")",self.pos)
            elif self.caracterActual == "'":
                self.addToken(Simbolo.comillaSimple, "'",self.pos)
               
            # S0 -> S2 (Numeros)
            elif self.caracterActual.isnumeric():
        
                sizeLexema = self.getSizeLexema(self.pos)
                self.S2(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
                
            # S0 -> Reservadas | Identificadores
            elif self.caracterActual.isalpha() : 
                
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
            
        
            # S0 -> '.'
            elif self.caracterActual== ".":
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
            
            elif self.caracterActual== "#":
               
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema

            elif self.caracterActual== "_":
                print("ebnto en fbajop")
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema

            
            # Otros
            elif self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\r" or self.caracterActual == "\n":  
                self.pos += 1 #incremento del contador del while
                continue

            else:   
                                
                # S0 -> FIN_CADENA
                if self.caracterActual == "$" and self.pos == len(self.entrada)-1:
                    if len(self.lista_errores) > 0:
                        return "corregir los errores"
                    return "analisis exitoso...!!!"
                #  S0 -> ERROR_LEXICO
                else:
                    self.addError(self.caracterActual,self.pos)

            self.pos += 1 #incremento del contador del while
        if len(self.pos_errores)>0:
            return "La entrada que ingresaste fue: " + self.entrada + "\nExiten Errores Lexicos"
        else:
            return "La entrada que ingresaste fue: " + self.entrada + "\nAnalisis exitoso..!!!"
            
    def S1(self,posActual):
            letra=self.entrada[posActual]
            if letra == "{":
                self.addToken(Simbolo.llaveIzq, "{",posActual)                   
            elif letra == "}":
                self.addToken(Simbolo.llaveDer, "}",self.pos)
            elif letra == ":":
                self.addToken(Simbolo.Dpuntos, ":",self.pos)
            elif letra == ";":
                self.addToken(Simbolo.Pcoma, ";",self.pos)
            elif letra == ",":
                self.addToken(Simbolo.coma, ",",self.pos)
            
            elif letra == "=":
                self.addToken(Simbolo.Igual, "=",self.pos)
            
            elif letra == "+":
                self.addToken(Simbolo.Mas, "+",self.pos)
            elif letra == "-":
                self.addToken(Simbolo.Menos, "-",self.pos)
            elif letra == "*":
                self.addToken(Simbolo.Asterisco, "*",self.pos)
            elif letra == "/":
                self.addToken(Simbolo.Division, "/",self.pos)
            elif letra == "(":
                self.addToken(Simbolo.ParentIzq, "(",self.pos)
            elif letra == ")":
                self.addToken(Simbolo.ParentDer, ")",self.pos)
            elif letra == "'":
                self.addToken(Simbolo.comillaSimple, "'",self.pos)
           
            else:
                print(" ERROR LEXICO ", self.entrada[self.pos])
    
    #--------------------------- ESTADO2 ---------------------------  numero letra error
    def S2(self, posActual, fin):
        c = '' 
        while posActual < fin:
            c = self.entrada[posActual]

            # S2 -> S2 (Numero)
            if c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.VALOR, self.lexema,self.pos)
                
            # S2 -> S3 (letra)
            elif c.isalpha():
                self.S3(posActual, fin)
                break

            elif c=="%":
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.VALOR, self.lexema,self.pos)
                
                
            # S2 -> ERROR_LEXICO
            else:
                if not c.isalpha() and not c.isdigit() and not c.isalnum():
                    self.S1(posActual)
                    break               
                else:
                    self.addError(c,posActual)
                    print("Error Lexico: ", c)
            
            posActual += 1

        print("estado 2 ", self.lexema)

    #--------------------------- ESTADO3 ---------------------------  letra tras letra NUMERO
    def S3(self, posActual, fin):
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
        
            # S3 -> S3 (letra)
            if c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.VALOR, self.lexema,self.pos)
                    print(f" estoy en el estado {self.estado}  con el simbolo {c} ")
            #S3 -> S2 NUMERO
            elif c.isnumeric():
                self.S2(posActual,fin)
                break
            
                
            # S2 -> ERROR_LEXICO
            else:
                if not c.isalpha() and not c.isdigit() and not c.isalnum():
                    self.S1(posActual)
                    break               
                else:
                    self.addError(c,posActual)
                    print("                 Error Lexico: ", c)
            posActual += 1
        print("estado 3 ", self.lexema)

    def imprimirSimbolos(self):
        for x in self.lista_tokens:
             print(x)

    def imprimirErrores(self):
        if(self.lista_errores.__sizeof__==0):
            print("No hay errores")
        else:
            for x in self.lista_errores:
                print(x)

    def imprimirReservadas(self):
        if(len(self.lista_reservadas)==0):
            print("No hay reservadas")
        else:
            for x in self.lista_reservadas:
                print(x)

    #--------------------------- RESERVADAS/ID ---------------------------
    def analizar_Id_Reservada(self, posActual, fin):
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]

        # Estado 0 a estado =2
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

            # S0 -> S5 ('-')
            elif c == "-":
                self.lexema += c
                
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break


            elif c == "_":
                self.lexema += c
                print("entra en de reservada")
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break
            # S0 -> S5 ('.')
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
                self.addError(c,posActual)
                print("Error Lexico: ", c)
            
            posActual += 1
        print("reservadas ", self.lexema)          
    #--------------------------- ESTADO6 ---------------------------
    def S6(self, posActual, fin):
        c = ""
        while posActual < fin:
            c = self.entrada[posActual]
        
            # S6 -> S6 (letra)
            if c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    #self.addToken(Simbolo.ID, self.lexema,self.pos)
                    self.S3(posActual+1,fin)
            # S6 -> S6 (Numero)
            elif c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    #self.addToken(Simbolo.ID, self.lexema,self.pos)
                    self.S2(posActual+1,fin)

            elif c=="_":
                self.lexema += c
                if(posActual+1 == fin):
                    #self.addToken(Tipo.ID, self.lexema)
                    self.S2(posActual+1,fin)

            # S6 -> ERROR_LEXICO
            else:
                
                self.addError(c,posActual)
                print("Error Lexico: ", c)

            posActual += 1

        print("estado 6 ", self.lexema)
    #--------------------------- ESTADO_ERROR ---------------------------
    def addError(self ,valor,pos):
        nuevo = Errores( valor,pos)
        self.lista_errores.append(nuevo)
        self.caracterActual = ""
        self.lexema = ""


    #--------------------------- ADD TOKEN ---------------------------
    def addToken(self, tipo, valor,pos):
    #print("|"+valor+"|")
        nuevo = Token(tipo, valor,pos)
        self.lista_tokens.append(nuevo)
        self.caracterActual = ""
        self.lexema = ""


    #-------------------- add palabra reservada ------------------
    def addTokens(self, tipo, valor,pos):
    #print("|"+valor+"|")
        nuevo = Token(tipo, valor,pos)
        self.lista_reservadas.append(nuevo)
        self.caracterActual = ""
        self.lexema = ""   

    #---------------- OBTENIENDO EL TAMAÑO DEL LEXEMA ----------------
    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                break
            longitud+=1
        return longitud



 