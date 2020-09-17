from simbolos import *
from TokenJS import *
from graphviz import Digraph

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
        self.transiciones=list()
        self.estado = 0
        self.lexema = ""
        self.columna=0
        self.linea=1

        
    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        self.caracterActual = ''
        self.pos = 0
        self.linea=1
        self.columna=0
        while self.pos < len(self.entrada):
            self.caracterActual = self.entrada[self.pos]

            #  comentario unilinea
            if self.caracterActual == "/" and self.entrada[self.pos+1] == "/" and self.entrada[self.pos-1]!=":":  
                comentario=""
                self.pos+=2
                while(self.entrada[self.pos]!="\n"):
                    comentario +=self.entrada[self.pos]
                    self.pos+=1  
                self.linea+=1
                path=comentario.split(" ")
                if(path[0]=="PATHW:"):
                    self.path=path[1]
                    print(F"ARCHIVO : {path[1]}")
                else:
                    print("Comentario : ",comentario)
                print("comentario en la linea ",self.linea)  
                         
            #   /* multilinea
            elif self.caracterActual == "/" and self.entrada[self.pos+1] == "*" :  
                come=""
                self.pos+=2
                while self.getSizecomentario(self.pos)!=1:
                    come+=self.entrada[self.pos]   
                    if(self.entrada[self.pos]=="\n"):
                        self.linea+=1
                    self.pos+=1
                
                self.pos+=self.getSizeLexema(self.pos)+1
                print("fin de cometario en linea ",self.linea)
                print(come)

            elif self.caracterActual=="\n":
                self.linea+=1
                self.columna=0
                


            
            elif self.caracterActual == "{":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.llaveIzq, "{",self.pos)                   
            elif self.caracterActual == "}":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.llaveDer, "}",self.pos)
            elif self.caracterActual == ":":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.Dpuntos, ":",self.pos)
            elif self.caracterActual == ";":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.Pcoma, ";",self.pos)
            elif self.caracterActual == ",":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.coma, ",",self.pos)
            elif self.caracterActual == "=":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.Igual, "=",self.pos)
            elif self.caracterActual == "+":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.Mas, "+",self.pos)
            elif self.caracterActual == "-":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.Menos, "-",self.pos)
            elif self.caracterActual == "*":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.Asterisco, "*",self.pos)
            elif self.caracterActual == "/":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.Division, "/",self.pos)
            elif self.caracterActual == "(":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.ParentIzq, "(",self.pos)
            elif self.caracterActual == ")":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.ParentDer, ")",self.pos)
            elif self.caracterActual == "'":
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.comillaSimple, "'",self.pos)
            elif self.caracterActual == '"':
                self.addTransicion(self.caracterActual,self.estado,1)
                self.addToken(Simbolo.ComillaD, "'",self.pos)
               
            # S0 -> S2 (Numeros)
            elif self.caracterActual.isnumeric():
                self.estado=0
                sizeLexema = self.getSizeLexema(self.pos)
                self.S2(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
                continue
                
            # S0 -> Reservadas | Identificadores
            elif self.caracterActual.isalpha() : 
                self.estado=0
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
                continue
        
            # S0 -> '.'
            elif self.caracterActual== ".":
                self.estado=0
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
                continue
            
            elif self.caracterActual== "#":
                self.estado=0
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
                continue

            elif self.caracterActual== "_":
                self.estado=0
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
                continue
            elif self.caracterActual== ":":
                self.estado=0
                sizeLexema = self.getSizeLexema(self.pos)
                self.analizar_Id_Reservada(self.pos, self.pos+sizeLexema)
                self.pos = self.pos+sizeLexema
                continue
            
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
        if len(self.lista_errores)>0:
            return "La entrada que ingresaste fue: " + self.entrada + "\nExiten Errores Lexicos"
        else:
            return "La entrada que ingresaste fue: " + self.entrada + "\nAnalisis exitoso..!!!"
            
    def S1(self,posActual):
            letra=self.entrada[posActual]
            if letra == "{":
                self.addTransicion(letra,self.estado,1)
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
            elif letra == '"':
                self.addToken(Simbolo.ComillaD,'"',self.pos)
            else:
                self.addToken(Simbolo.NotaLambda,letra,self.pos)
    
    #--------------------------- ESTADO2 ---------------------------  numero letra error
    def S2(self, posActual, fin):
        c = '' 
        esta=2
        while posActual < fin:
            c = self.entrada[posActual]
            if not c.isnumeric() and not c.isalpha():
                self.lexema += c
                self.addTransicion(c,self.estado,esta)
                self.estado=1
                break
            # S2 -> S2 (Numero)
            elif c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addTransicion(c,self.estado,esta)
                    self.addToken(Simbolo.VALOR, self.lexema,self.pos)
                self.addTransicion(c,self.estado,esta)
                self.estado=esta

            # S2 -> S3 (letra)
            elif c.isalpha():
                esta=2
                self.lexema += c
                if(posActual+1 == fin):
                    self.addTransicion(c,self.estado,esta)
                    self.addToken(Simbolo.VALOR, self.lexema,self.pos)
                self.addTransicion(c,self.estado,esta)
                self.estado=esta

            elif c=="%":
                self.lexema += c
                self.addTransicion(c,self.estado,1)
                self.estado=1
            
            elif c=="-":
                self.lexema += c
                self.addTransicion(c,self.estado,esta)
                self.estado=1
                break
            elif c=="_":
                self.lexema += c
                self.addTransicion(c,self.estado,esta)
                self.estado=1
                break
            
                
            # S2 -> ERROR_LEXICO
            else:
                
                self.addError(c,posActual)
                print("Error Lexico: ", c)
            
            posActual += 1

 
    def imprimirTokens(self):
        li=""
        for x in self.lista_tokens:
            li+=str(x)
            print(x)
            li+="\n"
        return li

    def imprimirErrores(self):
        
        for x in self.lista_errores:
            print(x)

    def imprimirRecorrido(self):
        li=""
        for x in self.transiciones:
            li+=str(x)
            print(x)
            li+="\n"
        return li

    #--------------------------- RESERVADAS/ID ---------------------------
    def analizar_Id_Reservada(self, posActual, fin):
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]

        # Estado 0 a estado =3
        esta=3
        if (self.lexema.lower() == "color"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.color, "color",posActual)
            return
        elif(self.lexema.lower() == "border"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.border, "border",posActual)
            return
        elif(self.lexema.lower() == "text-align"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.textaling, "text-aling",posActual)
            return
        elif(self.lexema.lower() == "font-weight"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.COLOR, "font-weight",posActual)
            return
        elif(self.lexema.lower() == "padding-left"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.paddingleft, "padding-left",posActual)
            return
        elif(self.lexema.lower() == "padding-top"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.paddingtop, "padding-top",posActual)
            return
        elif(self.lexema.lower() == "line-height"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.lineheight, "line-height",posActual)
            return
        elif(self.lexema.lower() == "margin-top"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.margintop, "margin-top",posActual)
            return
        elif(self.lexema.lower() == "margin-left"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.marginleft, "margin-left",posActual)
            return
        elif(self.lexema.lower() == "display"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.display, "display",posActual)
            return
        elif(self.lexema.lower() == "top"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.top, "top",posActual)
            return
        elif(self.lexema.lower() == "float"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.flotante, "float",posActual)
            return
        elif(self.lexema.lower() == "min-width"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.minwidth, "min-width",posActual)
            return
        elif(self.lexema.lower() == "font-weight"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.COLOR, "font-weight",posActual)
            return
        elif(self.lexema.lower() == "background-color"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.backgroundc, "background-color",posActual)
            return
        elif(self.lexema.lower() == "opacity"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.opacity, "opacity",posActual)
            return
        
        elif(self.lexema.lower() == "font-family"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.fontfamily, "font-family",posActual)
            return
        elif(self.lexema.lower() == "font-size"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.fontsize, "font-size",posActual)
            return
        elif(self.lexema.lower() == "padding-right"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.paddingright, "padding-right",posActual)
            return
        elif(self.lexema.lower() == "padding"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.padding, "padding",posActual)
            return
        elif(self.lexema.lower() == "width"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.width, "width",posActual)
            return
        elif(self.lexema.lower() == "margin-right"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.marginright, "margin-right",posActual)
            return

        elif(self.lexema.lower() == "position"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.position, "position",posActual)
            return
        elif(self.lexema.lower() == "right"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.right, "right",posActual)
            return
        elif(self.lexema.lower() == "clear"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.clear, "clear",posActual)
            return
        elif(self.lexema.lower() == "max-height"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.maxheight, "max-height",posActual)
            return
        elif(self.lexema.lower() == "background-image"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.backgroundi, "background-image",posActual)
            return
        elif(self.lexema.lower() == "background"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.background, "background",posActual)
            return

        elif(self.lexema.lower() == "font-style"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.fontstyle, "font-style",posActual)
            return
        elif(self.lexema.lower() == "font"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.font, "font",posActual)
            return
        elif(self.lexema.lower() == "padding-bottom"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.paddingbottom, "padding-bottom",posActual)
            return
        elif(self.lexema.lower() == "height"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.height, "height",posActual)
            return
        elif(self.lexema.lower() == "margin-bottom"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.marginbottom, "margin-bottom",posActual)
            return
        elif(self.lexema.lower() == "border-style"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.borderstyle, "border-style",posActual)
            return
        
        elif(self.lexema.lower() == "bottom"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.bottom, "bottom",posActual)
            return
        elif(self.lexema.lower() == "left"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.left, "left",posActual)
            return
        elif(self.lexema.lower() == "max-width"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.maxwidth, "max-width",posActual)
            return
        elif(self.lexema.lower() == "min-height"):
            self.addTransicion(self.lexema,self.estado,esta)
            self.addToken(Simbolo.minheight, "min-height",posActual)
            return
        



        self.lexema = ""
        c = ''
        self.estado=0
        esta=5
        while posActual < fin:
            c = self.entrada[posActual]
            
            # S0 -> S5 ('#')
            if c == "#":
                self.lexema += c
                self.addTransicion(c,self.estado,4)
                self.estado=4
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break
            elif c=="(" and self.entrada[posActual+1]=='"':
                posActual+=2
                get=self.getSizecadena(posActual+1)
                posActual=posActual+get
            # S0 -> S5 ('-')
            elif c == "-":
                self.lexema += c
                self.addTransicion(c,self.estado,4)
                self.estado=4
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break


            elif c == "_":
                self.lexema += c
                self.addTransicion(c,self.estado,4)
                self.estado=4
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break
            # S0 -> S5 ('.')
            elif c == ".":
                self.lexema += c
                self.addTransicion(c,self.estado,4)
                self.estado=4
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break

            elif c == "-":
                self.lexema += c
                self.addTransicion(c,self.estado,4)
                self.estado=4
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                break

            # S0 -> S6 (letra)
            elif c.isalpha():
                self.S6(posActual, fin)
                break
            elif c.isalnum():
                self.S6(posActual, fin)
                break
            # S0 -> ERROR_LEXICO
            else:
                self.addError(c,posActual)
                print("Error Lexico: ", c)
            
            posActual += 1        
    #--------------------------- ESTADO6 ---------------------------
    def S6(self, posActual, fin):
        c = ""
        esta=5
        while posActual < fin:
            c = self.entrada[posActual]
        
            # S6 -> S6 (letra)
            if c.isalpha():
                esta=5
                self.lexema += c
                if(posActual+1 == fin):
                    self.addTransicion(c,self.estado,esta)
                    self.addToken(Simbolo.ID, self.lexema,self.pos)
                    self.estado=esta
                self.addTransicion(c,self.estado,esta)
                self.estado=esta

                    
            # S6 -> S6 (Numero)
            elif c.isnumeric():
                esta=5
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Simbolo.ID, self.lexema,self.pos)
                    self.addTransicion(c,self.estado,esta)
                    self.estado=esta
                self.addTransicion(c,self.estado,esta) 
                self.estado=esta

            elif c=="_":
                self.lexema += c
                self.addTransicion(c,self.estado,6)
                self.estado=6
            elif c=="-":
                self.lexema += c
                self.addTransicion(c,self.estado,6)
                self.estado=6
            elif c=="#":
                self.lexema += c
                self.addTransicion(c,self.estado,6)
                self.estado=6
            elif c==".":
                self.lexema += c
                self.addTransicion(c,self.estado,6)
                self.estado=6



            # S6 -> ERROR_LEXICO
            else:
                if not c.isalpha() and not c.isnumeric():
                    self.S1(posActual)
                else:
                    self.addError(c,posActual)
                    print("Error Lexico: ", c)

            posActual += 1
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


 

    #---------------- OBTENIENDO EL TAMAÑO DEL LEXEMA ----------------
    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                break
            longitud+=1
        return longitud



    def addTransicion(self,valor,inicial,final):
        nuevo= Transiciones(valor,inicial,final)
        self.transiciones.append(nuevo)
        
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

    def getSizecadena(self, posInicial):
        longitud=0
            
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                
                break
            elif self.entrada[i]=="\n":
                self.linea+=1
            elif self.entrada[i]=='"' and self.entrada[i+1]==")":
                self.linea+=1
                print("fin cadena",self.linea)

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

    def generarGrafo(self):
        Digraph
        dot = Digraph(comment="hkol")
        dot.node("Estado 0","Estado 0",shape='circle')
        dot.edge("Estado 0","Estado 2", label='Numero')
        dot.node("Estado 2","Estado 2",shape='doublecircle')
        dot.edge("Estado 2","Estado 2", label='Numero')
        dot.node("Estado 1","Estado 1",shape='doublecircle')
        dot.edge("Estado 2","Estado 1", label='Punto')
        dot.edge("Estado 1","Estado 2", label='Numero')

        

        #print(dot)
        #dot.render(filename="pruebaAFD", directory='AFDs' + "/", format='png', view=True)
        self.generarGrafo2()

    def generarGrafo2(self):

        Digraph
        dot = Digraph(comment="hkol")
        dot.node("Estado 0","Estado 0",shape='circle')
        dot.edge("Estado 0","Estado 5", label='(# | :)*')
        dot.node("Estado 5","Estado 5",shape='circle')
        dot.edge("Estado 5","Estado 6", label='Letra')
        dot.node("Estado 6","Estado 6",shape='doublecircle')
        dot.edge("Estado 6","Estado 7", label='(Numero| Letra | _ |-)*')
        dot.node("Estado 7","Estado 7",shape='doublecircle')

        #print(dot)
        dot.render(filename="pruebaAFD2", directory='AFDs' + "/", format='png', view=True)
        self.generarGrafo3()

    def generarGrafo3(self):

        Digraph
        dot = Digraph(comment="hkol")
        dot.node("Estado 0","Estado 0",shape='circle')
        dot.edge("Estado 0","Estado 4", label='!')
        dot.node("Estado 4","Estado 4",shape='circle')
        dot.edge("Estado 4","Estado 5", label='Letra')
        dot.node("Estado 5","Estado 5",shape='doublecircle')
        dot.edge("Estado 5","Estado 5", label='Numero| Letra | _ |-')
  

        #print(dot)
        dot.render(filename="pruebaAFD3", directory='AFDs' + "/", format='png', view=True)
        self.ht()

    
    def ht(self):
        f = open ("reporte2.txt",'w')
        
        f.write("<p>Las transciones hechas<p>")
        
        for x in self.lista_transiciones:
            f.write("\n")
            f.writelines(f"<p>{str(x)}<p>")

        f.write("<p>\n\n\t AFD DE DIGITOS  -> NUMERO(NUMERO|PUNTO)*\n<p>")
        
        f.write("<img src='C:/Users/myale/OneDrive/Escritorio/Proyecto1Compi/AFDs/pruebaAFD.png'>")

        f.write("<p>\n\n\t AFD DE LOS ID'S  -> LETRA(LETRA|NUMERO|_ |-)*\n<p>")
        
        f.write("<img src='C:/Users/myale/OneDrive/Escritorio/Proyecto1Compi/AFDs/pruebaAFD2.png'>") 
        
        f.write("<p>\n\n\t AFD DE ID'S  -> !LETRA(LETRA|NUMERO|_ |-)*\n<p>")
        
        f.write("<img src='C:/Users/myale/OneDrive/Escritorio/Proyecto1Compi/AFDs/pruebaAFD3.png'>") 
        
        f.close()

        self.lo()


    def lo(self):
        template = open("reporte2.txt","r")
        output=open("reporte2.html","w")
        text=template.read()
        html=output.writelines(str(text))
        template.close()
        output.close()