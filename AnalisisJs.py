from TokenJS import *
from graphviz import Digraph

class ANALIZADORJS:
    lista_tokens = list()   # lista de tokens
    lista_errores = list()  # lista errores lexico
    pos_errores = list()    # lista de posiciones de errores
    # estado = 0
    lexema = ""

    def __init__(self):
        self.simbolosS={"{","}","(",")",":",";",",","=","<",">","+","-","/","*",'"',"'","."}
        self.simboloFun={'&','|'}
        self.lista_tokens = list()
        self.lista_errores = list()
        self.pos_errores = list()
        self.linea=0
        self.columna=1
        self.lexema = ""
        self.path=""
#alex400404k@gmail.com
    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        
        pos = 0    # almacena la posicion del caracter que se esta analizando
        self.linea=1 #inicia en linea 1
        self.columna=1
        while pos < len(self.entrada):
            self.caracterActual = self.entrada[pos] 
            #  comentario unilinea
            if self.caracterActual == "/" and self.entrada[pos+1] == "/" and self.entrada[pos-1]!=":":  
                comentario=""
                pos+=2
                while(self.entrada[pos]!="\n"):
                    comentario +=self.entrada[pos]
                    pos+=1  
                self.linea+=1
                path=comentario.split(" ")
                if(path[0]=="PATHW:"):
                    self.path=path[1]
                    print(F"ARCHIVO : {path[1]}")
                else:
                    print("Comentario : ",comentario)
                print("comentario en la linea ",self.linea)  
                         
            #   /* multilinea
            elif self.caracterActual == "/" and self.entrada[pos+1] == "*" :  
                come=""
                pos+=2
                while self.getSizecomentario(pos)!=1:
                    come+=self.entrada[pos]   
                    if(self.entrada[pos]=="\n"):
                        self.linea+=1
                    pos+=1

                pos+=self.getSizeLexema(pos)+1
                print("fin de cometario en linea ",self.linea)
                print(come)

            elif self.caracterActual=="\n":
                self.linea+=1
                self.columna=1
                
            elif self.caracterActual == "{":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.LLAVEIZQ, "{")
                
            elif self.caracterActual == "}":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.LLAVEDER, "}")
               
            elif self.caracterActual == ":":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.DPUNTOS, ":")
                
            elif self.caracterActual == ";":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.PCOMA, ";")
                
            elif self.caracterActual == ",":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.COMA, ",")
                
            elif self.caracterActual == "(":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.ParentIzq, "(")
               
            elif self.caracterActual == ")":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.ParentDer, ")")
               
            elif self.caracterActual == "=":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Igual, "=")
               
            elif self.caracterActual == "*":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Multipli, "*")
                
            elif self.caracterActual == "/":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Div, "/")
               
            elif self.caracterActual == "+":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Mas, "+")
             
            elif self.caracterActual == "-":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Menos, "-")
                
            elif self.caracterActual == "<":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Menor, "<")
                
            elif self.caracterActual == ">":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Mayor, ">")
                
            elif self.caracterActual == "'":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.ComillaS, "'")
                
            elif self.caracterActual == '"':
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.ComillaD, '"')
                
            elif self.caracterActual==".":
                print("Estado S0 -> ",self.caracterActual,"  -> Estado S1")
                self.addToken(Tipo.Punto,".")
                

            # S0 -> S2 (Numeros)
            elif self.caracterActual.isnumeric():
                print("numero")
                sizeLexema = self.getSizeLexema(pos)
                self.S2(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                
            # S0 -> Reservadas | Identificadores
            elif self.caracterActual.isalpha() :  
                print("letra")
                sizeLexema = self.getSizeLexema(pos)
                print(sizeLexema," ta")
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
            
            
            elif self.caracterActual=="_" : 
                
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
            elif self.caracterActual=="!" : 
                
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema

            # Otros
            elif self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\r" or self.caracterActual == "\n":  
                if self.caracterActual!="\n" and self.caracterActual==" ":
                    self.columna+=1

                pos += 1 #incremento del contador del while
                
                
            
            else:                    
                # S0 -> FIN_CADENA
                if self.caracterActual == "$" and pos == len(self.entrada)-1:
                    if len(self.lista_errores) > 0:
                        print("errores \n")
                        self.imprimirErrores()
                        print("\n\ntoken \n\n")
                        self.imprimirtoken()
                        print("corregir")
                        self.eliminarErrores(cadena)
                    return "analisis exitoso...!!!\n"+ self.eliminarErrores(cadena)
                #  S0 -> ERROR_LEXICO
                else:
                    self.columna+=1
                    print("Error Lexico S1: ", self.caracterActual," columna ",self.columna," linea",self.linea)
                    self.addError(self.caracterActual,pos,self.columna)
  
            pos += 1 #incremento del contador del while
            
            
        if len(self.lista_errores)>0:
            print("errores \n")
            self.imprimirErrores()
            print("\n\ntoken \n\n")
            self.imprimirtoken()
            return "La entrada que ingresaste fue: " + self.entrada + "\nExiten Errores Lexicos" + "\nYa se elimino "+self.eliminarErrores(cadena)
            
            
        else:
            print("errores \n")
            self.imprimirErrores()
            print("\n\ntoken \n\n")
            self.imprimirtoken()
            return "La entrada que ingresaste fue: " + self.entrada + "\nAnalisis exitoso..!!!"
            

    #--------------------------- ESTADO2 ---------------------------
    def S2(self, posActual, fin):
        c = '' 
        while posActual < fin:
            c = self.entrada[posActual]
            if not c.isalpha() and not c.isdigit():
                self.columna+=1
                print(" columan s2 ", self.columna)
                self.S1(posActual) 


            # S2 -> S2 (Numero)
            elif c.isnumeric():
                self.columna+=1
                self.lexema += c
                print(" columan s2 1", self.columna)
                if(posActual+1 == fin):
                    self.addToken(Tipo.VALOR, self.lexema)
                
            # S2 -> S3 (letra)
            elif c.isalpha():
                self.columna+=1
                self.lexema+=c
                print(" columan s2   2 ", self.columna)
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
                break

            # S2 -> ERROR_LEXICO
            else: 
                self.columna+=1
                print("Error Lexico ass: ", c," columna ",self.columna," linea",self.linea)                   
                self.pos_errores.append(posActual)
                self.addError(c,posActual,self.columna)
                
            
            posActual += 1
    
    #-----------------ESTADO 1 -----------------------------

    def S1(self,posActual):
            letra=self.entrada[posActual]
            if letra == "{":
                self.addToken(Tipo.LLAVEIZQ, "{")
            
            elif letra == "}":
                self.addToken(Tipo.LLAVEDER, "}")
                
            elif letra == ":":
                self.addToken(Tipo.DPUNTOS, ":")
                
            elif letra == ";":
                self.addToken(Tipo.PCOMA, ";")
                
            elif letra == ",":
                self.addToken(Tipo.COMA, ",")
               
            elif letra == "(":
                self.addToken(Tipo.ParentIzq, "(")
               
            elif letra == ")":
                self.addToken(Tipo.ParentDer, ")")
             
            elif letra == "=":
                self.addToken(Tipo.Igual, "=")
                
            elif letra == "*":
                self.addToken(Tipo.Multipli, "*")
                
            elif letra == "/":
                self.addToken(Tipo.Div, "/")
               
            elif letra == "+":
                self.addToken(Tipo.Mas, "+")
                
            elif letra == "-":
                self.addToken(Tipo.Menos, "-")
          
            elif letra == "<":
                self.addToken(Tipo.Menor, "<")
                
            elif letra == ">":
                self.addToken(Tipo.Mayor, ">")
          
            elif letra == "'":
                self.addToken(Tipo.ComillaS, "'")
           
            elif letra == '"':
                self.addToken(Tipo.ComillaD, '"')
             
            elif letra==".":
                self.addToken(Tipo.Punto,".")
                
            else:
                self.columna+=1
                print("Error en simbolo S1"+ letra," columna ", self.columna, " linea ",self.linea)
                
                self.addError(letra,posActual,self.columna)
            

    #=------------ IMPRIMIR LOS ERRROES CON SUS POSICONES --------------
    def imprimirErrores(self):
        if(self.lista_errores.__sizeof__==0):
            print("No hay errores")
        else:
            for x in self.lista_errores:
                print(x)


    # -------- IMPRIMIR LOS TOKEN ====
    def imprimirtoken(self):
        for i in self.lista_tokens:
            print(i)

    #--------------------------- ESTADO3 ---------------------------
    def S3(self, posActual, fin):
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
            
        
            # S3 -> S3 (letra)
            if c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.VALOR, self.lexema)
                    
            # S2 -> ERROR_LEXICO
            else:
                if not c.isalpha() and not c.isdigit() and not c.isalnum():
                    
                    self.S1(posActual)
                    break
                else:
                    self.columna+=1
                    print("Error Lexico s3: ", c ," columna ",self.columna," linea",self.linea)
                    self.addError(c,posActual,self.columna)
                    
            posActual += 1

    #--------------------------- RESERVADAS/ID ---------------------------
    def analizar_Id_Reservada(self, posActual, fin):
        
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]
            print("1")

        # S0 -> S4 (Palabras Reservadas)
        if (self.lexema.lower() == "var"):
        
            self.addToken(Tipo.var, "var")
            self.columna+=4
            return
        elif (self.lexema.lower() == "new"):
            self.columna+=4
            self.addToken(Tipo.var, "var")
        
            return
        elif(self.lexema.lower() == "if"):
            self.columna+=3
            self.addToken(Tipo.Cif, "if")
            
            return
        elif(self.lexema.lower() == "else"):
            self.columna+=5
            self.addToken(Tipo.Celse, "else")
            
            return
        elif(self.lexema.lower() == "else if"):
            self.columna+=8
            self.addToken(Tipo.Celseif, "else if")
            
            return
        elif(self.lexema.lower() == "do"):
            self.columna+=3
            self.addToken(Tipo.Cdo, "do")
            
            return
        elif(self.lexema.lower() == "while"):
            self.columna+=6
            self.addToken(Tipo.Cwhile, "while")
            
            return
        elif(self.lexema.lower() == "continue"):
            self.columna+=9
            self.addToken(Tipo.continuacio, "continue")
            
            return
        elif(self.lexema.lower() == "break"):
            self.columna+=6
            self.addToken(Tipo.Cbreak, "break")
           
            return
        elif(self.lexema.lower() == "return"):
            self.columna+=7
            self.addToken(Tipo.retorno, "return")   
            return
        elif(self.lexema.lower() == "funtion"):
            self.columna+=8
            self.addToken(Tipo.funcion, "funtion")
      
            return
        elif(self.lexema.lower() == "class"):
            self.columna+=6
            self.addToken(Tipo.clase, "class")
            return
        elif(self.lexema.lower() == "constructor"):
            self.columna+=12
            self.addToken(Tipo.constructor, "constructor")
            return
        elif(self.lexema.lower() == "this"):
            self.columna+=5
            self.addToken(Tipo.this, "this")
            return

        elif(self.lexema.lower() == "math.pow"):
            self.columna+=9
            self.addToken(Tipo.Mpotencia, "math.pow")
            return
    




        self.lexema = ""

        c = ''
        
        while posActual < fin:
            c = self.entrada[posActual]
            
            # S0 -> S5 ('#')
            if c == "_":

                self.lexema += c
                
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)

                posActual += 1
                break
            # S0 -> S5 ('!')
            elif c == "!":

                self.lexema += c
                
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)

                posActual += 1
                break
            # S0 -> S6 (letra)
            elif c.isalpha():
                self.S6(posActual, fin)
                break
            
            # S0 -> ERROR_LEXICO
            else:
                #verificacion si tiene un simbolo
                for x in self.simbolosS:
                    if x==c:
                        self.S1(posActual)
                        break
                    else:
                        self.columna+=1
                        print("Error Lexico  id: ", c," columna ",self.columna," linea",self.linea)
                        self.addError(c,posActual,self.columna)
                        
            
            posActual += 1
            
    #-------- borrar errores ----
    def eliminarErrores(self,cadena):
        self.entrada = cadena + "$"
        f = open (self.path,'w')
        
        
        pos = 0    # almacena la posicion del caracter que se esta analizando
        caract=""
        while pos < len(self.entrada): 
            
            if not self.entrada[pos].isalpha() and ( not self.entrada[pos].isdigit()):
                for x in self.lista_errores:
                    if x.posicion == pos:
                        pos+=1
            caract=self.entrada[pos]
            f.write(caract)
              
                        
            pos+=1
        
        f.close()
        return cadena
    
    
    #-------------------------Comentarios -----------
    def analizarComentario(self,posActual,fin):
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]

        self.lexema = ""
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
            
            # S0 -> S5 ('#')
            if c == "/" and self.entrada[posActual+1]=="/":
                print("Signos de comentario una Linea")
                break

            # S0 -> S6 (letra)
            elif c=="/" and self.entrada[posActual+1]=="*":
                print("Signo Inicio de Comentario Multilinea")
                break
            elif c=="*" and self.entrada[posActual+1]=="/":
                print("Signo Fin de Comentario Multilinea")
                break
            # S0 -> ERROR_LEXICO
            else:
                print("no hay"+ c)
            
            posActual += 1
            
        
    
    
    #--------------------------- ESTADO6 ---------------------------
    def S6(self, posActual, fin):
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
            #verificacion si tiene un simbolo
            if c=="!":
                self.columna+=1
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)

            # S6 -> S6 (letra)
            elif c.isalpha():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)

            # S6 -> S6 (Numero)
            elif c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
            
            elif c=="_":
            
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
            

            # S6 -> ERROR_LEXICO
            else:
                if not c.isalpha() and not c.isdigit():
                
                    self.S1(posActual) 
                else:
                    self.columna+=1
                    print("Error Lexico s6: ", c," columna ",self.columna," linea",self.linea)
                    self.addError(self.lexema,posActual,self.columna)
                    

            posActual += 1

    #--------------------------- ESTADO_ERROR ---------------------------
    def addError(self, entrada, pos,column):
        self.columna+=1
        nuevo = Errores(entrada,pos,column)
        self.lista_errores.append(nuevo)
        self.caracterActual = ""
        self.lexema = ""
        
        return 0


    #--------------------------- ADD TOKEN ---------------------------
    def addToken(self, tipo, valor):
        self.columna+=1
        nuevo = Token(tipo, valor)
        self.lista_tokens.append(nuevo)
        self.caracterActual = ""
        print("se guarda ",self.lexema)
        self.lexema = ""

    #---------------- OBTENIENDO EL TAMAÑO DEL LEXEMA ----------------
    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r" or self.entrada[i] == ".":
                if self.entrada[i]!="\n":
                    self.columna+=1
                break
            longitud+=1
        return longitud


    #-------------obteniendo tamano de comentario multilinea---
    def getSizecomentario(self, posInicial):
        longitud=0  
        lont=0
            
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                
                break
            elif self.entrada[i]=="\n":
                self.linea+=1

            elif self.entrada[i]=="*" and self.entrada[i+1]=="/":
                
                print("fin mult",self.linea)
                
                lont=1
        if lont==1:
            longitud=1   
          
        return longitud



    def generarGrafo(self):
        Digraph
        dot = Digraph(comment=self.Nombre)
        for x in self.Transicion:
            if self.Transicion:
                for w in self.EstadoAcep:
                    if w == x.estadoI:
                        dot.node(x.estadoI, x.estadoI, shape='doublecircle')
                    elif w == x.estadoF:
                        dot.node(x.estadoF, x.estadoF, shape='doublecircle')

                dot.edge(x.estadoI, x.estadoF, label=x.simbolo)

            else:
                dot.node(x.estadoI, x.estadoI, shape='circle')
                dot.node(x.estadoF, x.estadoF, shape='circle')
                dot.edge(x.estadoI, x.estadoF, label=x.simbolo)


        dot.render(filename=self.Nombre, directory='AFDs' + "/", format='png', view=True)