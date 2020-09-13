from TokenJS import *

class Scanner:
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
        self.columna=0
        self.lexema = ""
        self.path=""

    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        
        pos = 0    # almacena la posicion del caracter que se esta analizando
        
        while pos < len(self.entrada):
            self.caracterActual = self.entrada[pos] 
            
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
                
        
                   

            #   /* come
            elif self.caracterActual == "/" and self.entrada[pos+1] == "*" :  
                come=""
                self.columna+=2
                pos+=2
                while self.getSizecomentario(pos)!=1:
                    
                    come+=self.entrada[pos]
                    self.columna+=1
                    pos+=1
                pos+=self.getSizeLexema(pos)+1
                print(come)
                
            

            elif self.caracterActual == "{":
                self.addToken(Tipo.LLAVEIZQ, "{")
                self.columna+=1
            elif self.caracterActual == "}":
                self.addToken(Tipo.LLAVEDER, "}")
                self.columna+=1
            elif self.caracterActual == ":":
                self.addToken(Tipo.DPUNTOS, ":")
                self.columna+=1
            elif self.caracterActual == ";":
                self.addToken(Tipo.PCOMA, ";")
                self.columna+=1
            elif self.caracterActual == ",":
                self.addToken(Tipo.COMA, ",")
                self.columna+=1
            elif self.caracterActual == "(":
                self.addToken(Tipo.ParentIzq, "(")
                self.columna+=1
            elif self.caracterActual == ")":
                self.addToken(Tipo.ParentDer, ")")
                self.columna+=1
            elif self.caracterActual == "=":
                self.addToken(Tipo.Igual, "=")
                self.columna+=1
            elif self.caracterActual == "*":
                self.addToken(Tipo.Multipli, "*")
                self.columna+=1
            elif self.caracterActual == "/":
                self.addToken(Tipo.Div, "/")
                self.columna+=1
            elif self.caracterActual == "+":
                self.addToken(Tipo.Mas, "+")
                self.columna+=1
            elif self.caracterActual == "-":
                self.addToken(Tipo.Menos, "-")
                self.columna+=1
            elif self.caracterActual == "<":
                self.addToken(Tipo.Menor, "<")
                self.columna+=1
            elif self.caracterActual == ">":
                self.addToken(Tipo.Mayor, ">")
                self.columna+=1
            elif self.caracterActual == "'":
                self.addToken(Tipo.ComillaS, "'")
                self.columna+=1
            elif self.caracterActual == '"':
                self.addToken(Tipo.ComillaD, '"')
                self.columna+=1
            elif self.caracterActual==".":
                self.addToken(Tipo.Punto,".")
                self.columna+=1

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
            
            
            elif self.caracterActual=="_" : 
                
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema

            # Otros
            elif self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\r" or self.caracterActual == "\n":  
                if self.caracterActual=="\n":
                    self.columna=0
                else:
                    self.columna+=1
                pos += 1 #incremento del contador del while
                
                
            
            else:                    
                # S0 -> FIN_CADENA
                if self.caracterActual == "$" and pos == len(self.entrada)-1:
                    if len(self.lista_errores) > 0:
                        print("corregir")
                        self.eliminarErrores(cadena)
                    return "analisis exitoso...!!!\n"+ self.eliminarErrores(cadena)
                #  S0 -> ERROR_LEXICO
                else:
                    self.columna+=1
                    print("Error Lexico So: ", self.caracterActual," columna ",self.columna," linea",self.linea)
                    self.addError(self.caracterActual,pos,self.columna)
  
            pos += 1 #incremento del contador del while
            
            
        if len(self.lista_errores)>0:
            print(self.linea)
            return "La entrada que ingresaste fue: " + self.entrada + "\nExiten Errores Lexicos" + "\nYa se elimino "+self.eliminarErrores(cadena)
            
            
        else:
            return "La entrada que ingresaste fue: " + self.entrada + "\nAnalisis exitoso..!!!"
            

    #--------------------------- ESTADO2 ---------------------------
    def S2(self, posActual, fin):
        c = '' 
        while posActual < fin:
            c = self.entrada[posActual]
            if not c.isalpha() and not c.isdigit():
                self.columna+=1
                self.S1(posActual) 


            # S2 -> S2 (Numero)
            elif c.isnumeric():
                self.lexema += c
                self.columna+=1
                if(posActual+1 == fin):
                    self.addToken(Tipo.VALOR, self.lexema)
                
            # S2 -> S3 (letra)
            elif c.isalpha():
                self.columna+=1
                self.S3(posActual, fin)
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
                self.columna+=1
            elif letra == "}":
                self.addToken(Tipo.LLAVEDER, "}")
                self.columna+=1
            elif letra == ":":
                self.addToken(Tipo.DPUNTOS, ":")
                self.columna+=1
            elif letra == ";":
                self.addToken(Tipo.PCOMA, ";")
                self.columna+=1
            elif letra == ",":
                self.addToken(Tipo.COMA, ",")
                self.columna+=1
            elif letra == "(":
                self.addToken(Tipo.ParentIzq, "(")
                self.columna+=1
            elif letra == ")":
                self.addToken(Tipo.ParentDer, ")")
                self.columna+=1
            elif letra == "=":
                self.addToken(Tipo.Igual, "=")
                self.columna+=1
            elif letra == "*":
                self.addToken(Tipo.Multipli, "*")
                self.columna+=1
            elif letra == "/":
                self.addToken(Tipo.Div, "/")
                self.columna+=1
            elif letra == "+":
                self.addToken(Tipo.Mas, "+")
                self.columna+=1
            elif letra == "-":
                self.addToken(Tipo.Menos, "-")
                self.columna+=1
            elif letra == "<":
                self.addToken(Tipo.Menor, "<")
                self.columna+=1
            elif letra == ">":
                self.addToken(Tipo.Mayor, ">")
                self.columna+=1
            elif letra == "'":
                self.addToken(Tipo.ComillaS, "'")
                self.columna+=1
            elif letra == '"':
                self.addToken(Tipo.ComillaD, '"')
                self.columna+=1
            elif letra==".":
                self.addToken(Tipo.Punto,".")
                self.columna+=1
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



    #--------------------------- ESTADO3 ---------------------------
    def S3(self, posActual, fin):
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
            
        
            # S3 -> S3 (letra)
            if c.isalpha():
                self.columna+=1
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.VALOR, self.lexema)
                    
            # S2 -> ERROR_LEXICO
            else:
                if not c.isalpha() and not c.isdigit() and not c.isalnum():
                    self.columna+=1
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

        # S0 -> S4 (Palabras Reservadas)
        if (self.lexema.lower() == "var"):
            self.addToken(Tipo.var, "var")
            self.columna+=1
            return
        elif(self.lexema.lower() == "if"):
            self.addToken(Tipo.Cif, "if")
            self.columna+=1
            return
        elif(self.lexema.lower() == "else"):
            self.addToken(Tipo.Celse, "else")
            self.columna+=1
            return
        elif(self.lexema.lower() == "else if"):
            self.addToken(Tipo.Celseif, "else if")
            self.columna+=1
            return
        elif(self.lexema.lower() == "do"):
            self.addToken(Tipo.Cdo, "do")
            self.columna+=1
            return
        elif(self.lexema.lower() == "while"):
            self.addToken(Tipo.Cwhile, "while")
            self.columna+=1
            return
        elif(self.lexema.lower() == "continue"):
            self.addToken(Tipo.continuacio, "continue")
            self.columna+=1
            return
        elif(self.lexema.lower() == "break"):
            self.addToken(Tipo.Cbreak, "break")
            self.columna+=1
            return
        elif(self.lexema.lower() == "return"):
            self.addToken(Tipo.retorno, "return")
            self.columna+=1
            return
        elif(self.lexema.lower() == "while"):
            self.addToken(Tipo.Cwhile, "while")
            self.columna+=1
            return
        elif(self.lexema.lower() == "funtion"):
            self.addToken(Tipo.funcion, "funtion")
            self.columna+=1
            return
        elif(self.lexema.lower() == "class"):
            self.addToken(Tipo.clase, "class")
            self.columna+=1
            return
        elif(self.lexema.lower() == "constructor"):
            self.addToken(Tipo.constructor, "constructor")
            self.columna+=1
            return
        elif(self.lexema.lower() == "this"):
            self.addToken(Tipo.this, "this")
            self.columna+=1
            return

        elif(self.lexema.lower() == "math.pow"):
            self.addToken(Tipo.Mpotencia, "math.pow")
            self.columna+=1
            return
    




        self.lexema = ""
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
            
            # S0 -> S5 ('#')
            if c == "_":
                self.columna+=1
                print("verifica el simbolo _")
                self.lexema += c
                
                # S5 -> S6 (letra)
                self.S6(posActual+1, fin)
                self.columna+=1
                posActual += 1
                break

            # S0 -> S6 (letra)
            elif c.isalpha():
                self.columna+=1
                self.S6(posActual, fin)
                break
            
            # S0 -> ERROR_LEXICO
            else:
                #verificacion si tiene un simbolo
                for x in self.simbolosS:
                    if x==c:
                        self.columna+=1
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
        f = open (self.path,'r+')
        
        
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
                self.columna+=1
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)

            # S6 -> S6 (Numero)
            elif c.isnumeric():
                self.columna+=1
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
            
            elif c=="_":
                self.columna+=1
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
            

            # S6 -> ERROR_LEXICO
            else:
                if not c.isalpha() and not c.isdigit():
                    self.columna+=1
                    self.S1(posActual) 
                else:
                    self.columna+=1
                    print("Error Lexico s6: ", c," columna ",self.columna," linea",self.linea)
                    self.addError(self.lexema,posActual,self.columna)
                    

            posActual += 1

    #--------------------------- ESTADO_ERROR ---------------------------
    def addError(self, entrada, pos,column):
        nuevo = Errores(entrada,pos,column)
        self.lista_errores.append(nuevo)
        self.caracterActual = ""
        self.lexema = ""
        return 0


    #--------------------------- ADD TOKEN ---------------------------
    def addToken(self, tipo, valor):
    #print("|"+valor+"|")
        nuevo = Token(tipo, valor)
        self.lista_tokens.append(nuevo)
        self.caracterActual = ""

        self.lexema = ""

    #---------------- OBTENIENDO EL TAMAÑO DEL LEXEMA ----------------
    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                if self.entrada[i]=="\n":
                    
                    self.columna=0
                break
            
            longitud+=1
            self.columna+=1
        return longitud


    #-------------obteniendo tamano de comentario multilinea---
    def getSizecomentario(self, posInicial):
        longitud=0  
            
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                self.columna+=1
                break
            elif self.entrada[i]=="\n":
               
                self.columna=0
            elif self.entrada[i]=="*" and self.entrada[i+1]=="/":
                self.columna+=2
                print("fin mult")
                
                longitud=1
            
          
        return longitud