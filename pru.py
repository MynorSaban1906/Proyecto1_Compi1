from simbolos import *


class Scanner:
    lista_tokens = list()   # lista de tokens
    lista_errores = list()  # lista errores lexico
    pos_errores = list()    # lista de posiciones de errores
    # estado = 0
    lexema = ""
    lista_reservadas=list()
    transiciones=list()


    def __init__(self):
        self.transiciones=list()
        self.lista_tokens = list()
        self.lista_errores = list()
        self.pos_errores = list()
        self.estado = 0
        self.lexema = ""
        self.lista_reservadas=list()



    def imprimirTokens(self):
        li=""
        for i in self.lista_tokens:
            li+=str(i)
            print(i)
            li+="\n"
        return li
    

    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        self.estado = 0
        self.caracterActual = ''
        self.columna=0
        self.linea=1
        pos = 0    # almacena la posicion del caracter que se esta analizando
        #for self.pos in range(0,len(self.entrada)-1):
        while pos < len(self.entrada):
            self.caracterActual = self.entrada[pos]            
            
            # comentario uni linea 
            if self.caracterActual == "/" and self.entrada[pos+1] == "/" and self.entrada[pos-1]!=":":  
                comentario=""
                pos+=2
                while(self.entrada[pos]!="\n"):
                    comentario +=self.entrada[pos]
                    pos+=1  
                path=comentario.split(" ")
                if(path[0]=="PATHW:"):
                    self.path=path[1]
                    print(F"ARCHIVO : {path[1]}")
                else:
                    print("Comentario : ",comentario)           

            #   /* comentario multiliea
            elif self.caracterActual == "/" and self.entrada[pos+1] == "*" :  
                come=""
                pos+=2
                while (self.getSizecomentario(pos)!=1):
                    
                        come+=self.entrada[pos]
                    
                        pos+=1
                pos+=self.getSizeLexema(pos)+1
                print(come)
            
            elif self.caracterActual=="\n":
                self.linea+=1
                self.columna=0
                continue

            # S0 -> S1 (Simbolos del Lenguaje)
            elif self.caracterActual == "{":
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
                self.estado=0
                sizeLexema = self.getSizeDigito(pos)
                self.S2(pos, pos+sizeLexema)
                pos = pos+sizeLexema
            
                
            # S0 -> Reservadas | Identificadores
            elif self.caracterActual.isalpha() :  
                self.estado=0
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue
            
            # S0 -> '#' -> letra
            elif self.caracterActual == "#" and self.entrada[pos+1].isalpha() :  
                self.estado=0
                sizeLexema = self.getSizeLexema(pos)
                self.S6(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue
            
            # S0 -> '#' -> numero color hexadecimal
            elif self.caracterActual == "#" and self.entrada[pos+1].isalnum():
                self.estado=0 
                sizeLexema = self.getSizeLexema(pos)
                self.S6(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue


            # S0 -> '.' Q
            elif self.caracterActual == "." : 
                self.estado=0
                sizeLexema = self.getSizeLexema(pos)
                self.S3(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue
            elif self.caracterActual == ":" :  
                self.estado=0
                sizeLexema = self.getSizeLexema(pos)
                self.S3(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue
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
            
    #======re
    def recorri(self):
        for x in self.transiciones:
            print(x)
    #--------------------------- ESTADO2 ---------------------------
    def S2(self, posActual, fin): 
        c = '' 
        esta=2
        while posActual < fin:
            c = self.entrada[posActual]

            # S2 -> S2 (Numero)
            if c.isnumeric():
                esta=2
                self.lexema += c
                if(posActual+1 == fin):
                    self.addTransicion(c,self.estado,esta)
                    self.addToken(Simbolo.VALOR, self.lexema,posActual)
                self.addTransicion(c,self.estado,esta)
                self.estado=esta
                
            # S2 -> S3 (letra)
            elif c.isalpha():
                esta=2
                self.lexema += c
                if(posActual+1 == fin):
                    self.addTransicion(c,self.estado,esta)
                    self.addToken(Simbolo.ID, self.lexema,posActual)
                self.addTransicion(c,self.estado,esta)
                self.estado=esta

            elif c=="%":
                self.lexema += c
                if(posActual+1 == fin):
                    self.addTransicion(c,self.estado,1)
                    self.addToken(Simbolo.ID, self.lexema,posActual)
                    self.estado=1

            elif c==".":
                self.lexema += c
                self.addTransicion(c,self.estado,1)
                self.estado=1

            # S2 -> ERROR_LEXICO
            else:
                
                print("Error Lexico: ", c)
            
            posActual += 1
        self.recorri()
        self.imprimirTokens()
    #--------------------------- ESTADO3 ---------------------------
    def S3(self, posActual, fin):
        c = ''
        esta=4
        while posActual < fin:
            c = self.entrada[posActual]
        
            # S3 -> S3 (letra)
            if c.isalpha():
                esta=4
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.ID, self.lexema,posActual)
                    self.addTransicion(c,self.estado,esta)
                self.addTransicion(c,self.estado,4)
                self.estado=esta
                    
            elif c.isalnum():
                esta=4
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.ID, self.lexema,posActual)
                    self.addTransicion(c,self.estado,esta)
                self.addTransicion(c,self.estado,esta)
                self.estado=esta

            elif c=="-":
                self.lexema += c
                self.addTransicion(c,self.estado,5)
                self.estado=5
            
            elif c==".":
                self.lexema += c
                self.addTransicion(c,self.estado,5)
                self.estado=5

            elif c==":":
                self.lexema += c
                self.addTransicion(c,self.estado,5)
                self.estado=5

            elif c=="_":
                self.lexema += c
                self.addTransicion(c,self.estado,5)
                self.estado=5
            
            # S2 -> ERROR_LEXICO
            else:
                self.pos_errores.append(posActual)
                print("Error Lexico: ", c)
            posActual += 1

        self.imprimirTokens()
        self.recorri()

    #--------------------------- RESERVADAS/ID ---------------------------
    def analizar_Id_Reservada(self, posActual, fin):
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]

        # S0 -> S4 (Palabras Reservadas)
        if (self.lexema.lower() == "color"):
            self.addToken(Simbolo.color, "color",posActual)
            self.addTransicion(self.lexema,self.estado,6)
            return
        elif(self.lexema.lower() == "border"):
            self.addToken(Simbolo.border, "border",posActual)
            return
        elif(self.lexema.lower() == "text-align"):
            self.addToken(Simbolo.textaling, "text-aling",posActual)
            return
        elif(self.lexema.lower() == "font-weight"):
            self.addToken(Simbolo.COLOR, "font-weight",posActual)
            return
        elif(self.lexema.lower() == "padding-left"):
            self.addToken(Simbolo.paddingleft, "padding-left",posActual)
            return
        elif(self.lexema.lower() == "padding-top"):
            self.addToken(Simbolo.paddingtop, "padding-top",posActual)
            return
        elif(self.lexema.lower() == "line-height"):
            self.addToken(Simbolo.lineheight, "line-height",posActual)
            return
        elif(self.lexema.lower() == "margin-top"):
            self.addToken(Simbolo.margintop, "margin-top",posActual)
            return
        elif(self.lexema.lower() == "margin-left"):
            self.addToken(Simbolo.marginleft, "margin-left",posActual)
            return
        elif(self.lexema.lower() == "display"):
            self.addToken(Simbolo.display, "display",posActual)
            return
        elif(self.lexema.lower() == "top"):
            self.addToken(Simbolo.top, "top",posActual)
            return
        elif(self.lexema.lower() == "float"):
            self.addToken(Simbolo.flotante, "float",posActual)
            return
        elif(self.lexema.lower() == "min-width"):
            self.addToken(Simbolo.minwidth, "min-width",posActual)
            return
        elif(self.lexema.lower() == "font-weight"):
            self.addToken(Simbolo.COLOR, "font-weight",posActual)
            return
        elif(self.lexema.lower() == "background-color"):
            self.addToken(Simbolo.backgroundc, "background-color",posActual)
            return
        elif(self.lexema.lower() == "opacity"):
            self.addToken(Simbolo.opacity, "opacity",posActual)
            return        
        elif(self.lexema.lower() == "font-family"):
            self.addToken(Simbolo.fontfamily, "font-family",posActual)
            return
        elif(self.lexema.lower() == "font-size"):
            self.addToken(Simbolo.fontsize, "font-size",posActual)
            return
        elif(self.lexema.lower() == "padding-right"):
            self.addToken(Simbolo.paddingright, "padding-right",posActual)
            return
        elif(self.lexema.lower() == "padding"):
            self.addToken(Simbolo.padding, "padding",posActual)
            return
        elif(self.lexema.lower() == "width"):
            self.addToken(Simbolo.width, "width",posActual)
            return
        elif(self.lexema.lower() == "margin-right"):
            self.addToken(Simbolo.marginright, "margin-right",posActual)
            return
        elif(self.lexema.lower() == "position"):
            self.addToken(Simbolo.position, "position",posActual)
            return
        elif(self.lexema.lower() == "right"):
            self.addToken(Simbolo.right, "right",posActual)
            return
        elif(self.lexema.lower() == "clear"):
            self.addToken(Simbolo.clear, "clear",posActual)
            return
        elif(self.lexema.lower() == "max-height"):
            self.addToken(Simbolo.maxheight, "max-height",posActual)
            return
        elif(self.lexema.lower() == "background-image"):
            self.addToken(Simbolo.backgroundi, "background-image",posActual)
            return
        elif(self.lexema.lower() == "background"):
            self.addToken(Simbolo.background, "background",posActual)
            return
        elif(self.lexema.lower() == "font-style"):
            self.addToken(Simbolo.fontstyle, "font-style",posActual)
            return
        elif(self.lexema.lower() == "font"):
            self.addToken(Simbolo.font, "font",posActual)
            return
        elif(self.lexema.lower() == "padding-bottom"):
            self.addToken(Simbolo.paddingbottom, "padding-bottom",posActual)
            return
        elif(self.lexema.lower() == "height"):
            self.addToken(Simbolo.height, "height",posActual)
            return
        elif(self.lexema.lower() == "margin-bottom"):
            self.addToken(Simbolo.marginbottom, "margin-bottom",posActual)
            return
        elif(self.lexema.lower() == "border-style"):
            self.addToken(Simbolo.borderstyle, "border-style",posActual)
            return     
        elif(self.lexema.lower() == "bottom"):
            self.addToken(Simbolo.bottom, "bottom",posActual)
            return
        elif(self.lexema.lower() == "left"):
            self.addToken(Simbolo.left, "left",posActual)
            return
        elif(self.lexema.lower() == "max-width"):
            self.addToken(Simbolo.maxwidth, "max-width",posActual)
            return
        elif(self.lexema.lower() == "min-height"):
            self.addToken(Simbolo.minheight, "min-height",posActual)
            return

        
        
            # S0 -> ERROR_LEXICO
        
        self.estado=0
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

            # S0 -> S6 (letra)
            elif c.isalpha():
                self.S6(posActual, fin)
                break
            
            # S0 -> ERROR_LEXICO
            else:
                self.pos_errores.append(posActual)
                print("Error Lexico: ", c)
            
            posActual += 1


    # ------------------------ ESTADO 1--------------------------

    def S1(self,posActual,inicio):
            letra=self.entrada[posActual]
            if letra == "{":
                self.addTransicion("{",inicio,1)
                inicio=1                 
            elif letra == "}":
                self.addTransicion("}",inicio,1)
                inicio=1 
            elif letra == ":":
                self.addTransicion(":",inicio,1)
                inicio=1 
            elif letra == ";":
                self.addTransicion(";",inicio,1)
                inicio=1 
            elif letra == ",":
                self.addTransicion(",",inicio,1)
                inicio=1 
            elif letra == "=":
                self.addTransicion("=",inicio,1)
                inicio=1 
            elif letra == "+":
                self.addTransicion("+",inicio,1)
                inicio=1 
            elif letra == "-":
                self.addTransicion("-",inicio,1)
                inicio=1 
            elif letra == "*":
                self.addTransicion("*",inicio,1)
                inicio=1 
            elif letra == "/":
                self.addTransicion("/",inicio,1)
                inicio=1 
            elif letra == "(":
                self.addTransicion("(",inicio,1)
                inicio=1 
            elif letra == ")":
                self.addTransicion(")",inicio,1)
                inicio=1 
            elif letra == "'":
                self.addTransicion("'",inicio,1)
                inicio=1 
            elif letra=='"':
                self.addTransicion('"',inicio,1)
                inicio=1 
            

            else:
                self.columna+=1
                print(" ERROR LEXICO S1 ", self.entrada[posActual])
            
            return inicio
            
    
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
 
    #--------------------------- ADD TOKEN ---------------------------
    def addToken(self, tipo, valor,pos):
        nuevo = Token(tipo, valor,pos)
        self.lista_tokens.append(nuevo)
        self.lexema=""
        self.caracterActual==""

    #--------- add transicion -- --------
      
    def addTransicion(self,valor,inicial,final):
        nuevo= Transiciones(valor,inicial,final)
        self.transiciones.append(nuevo)
        

    #---------------- OBTENIENDO EL TAMAÑO DEL LEXEMA ----------------
    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " "or self.entrada[i] == "="or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r"  or self.entrada[i] == "(" or self.entrada[i]==")"or self.entrada[i]=="'" or self.entrada[i] =='"' or self.entrada[i]=="/" or self.entrada[i]=="*"or self.entrada[i] =='+':
                if self.entrada[i]!="\n":
                    self.columna+=1
                if self.entrada[i]=="\n":
                    self.linea+=1
                    self.columna=0
                
                break
            if self.entrada[i]=="\n":
                self.linea+=1
            elif self.entrada[i].isnumeric() or self.entrada[i].isalpha():
                self.columna+=1
            longitud+=1
        return longitud

    #-------------obteniendo tamano de comentario multilinea---
    def getSizecomentario(self, posInicial):
        longitud=0
            
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                
                break
            elif self.entrada[i]=="\n":
                self.linea+=1
            elif self.entrada[i]=="*" and self.entrada[i+1]=="/":
                self.linea+=1
                print("fin mult",self.linea)

                longitud=1 
          
        return longitud

    #----------OBTENIENDO TAMANIO DE DIGITOS ----
    def getSizeDigito(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":
                if self.entrada[i]!="\n":
                    self.columna+=1
                if self.entrada[i]=="\n":
                    self.linea+=1
                    self.columna=0
                break
            if self.entrada[i]=="\n":
                self.linea+=1
            elif self.entrada[i].isnumeric() or self.entrada[i].isalpha():
                self.columna+=1
                
            longitud+=1
        return longitud
