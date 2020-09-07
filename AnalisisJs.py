from TokenJS import *

# from NOMBRE.PY import CLASE|METODO|ENUM

def hola():
    print("")

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
        self.estado = 0
        self.lexema = ""

    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        #self.estado = 0
        self.caracterActual = ''
        
        pos = 0    # almacena la posicion del caracter que se esta analizando
        #for self.pos in range(0,len(self.entrada)-1):
        while pos < len(self.entrada):
            self.caracterActual = self.entrada[pos] 

            if self.caracterActual == "/" and self.entrada[pos+1] == "/" and self.entrada[pos-1]!=":":  
                comentario=""
                pos+=2
                while(self.entrada[pos]!="\n"):
                    comentario +=self.entrada[pos]
                    pos+=1    
                if(comentario.find("PATHW: ",pos)):
                    print(comentario.strip())
        
                   

            #   /* come
            elif self.caracterActual == "/" and self.entrada[pos+1] == "*" :  
                come=""
                pos+=2
                while self.getSizecomentario(pos)!=1:
                    come+=self.entrada[pos]
                    pos+=1

                pos+=self.getSizeLexema(pos)+1
                print(come)
                
            

            elif self.caracterActual == "{":
                self.addToken(Tipo.LLAVEIZQ, "{")
            elif self.caracterActual == "}":
                self.addToken(Tipo.LLAVEDER, "}")
            elif self.caracterActual == ":":
                self.addToken(Tipo.DPUNTOS, ":")
            elif self.caracterActual == ";":
                self.addToken(Tipo.PCOMA, ";")
            elif self.caracterActual == ",":
                self.addToken(Tipo.COMA, ",")
            elif self.caracterActual == "(":
                self.addToken(Tipo.ParentIzq, "(")
            elif self.caracterActual == ")":
                self.addToken(Tipo.ParentDer, ")")
            elif self.caracterActual == "=":
                self.addToken(Tipo.Igual, "=")
            elif self.caracterActual == "*":
                self.addToken(Tipo.Multipli, "*")
            elif self.caracterActual == "/":
                self.addToken(Tipo.Div, "/")
            elif self.caracterActual == "+":
                self.addToken(Tipo.Mas, "+")
            elif self.caracterActual == "-":
                self.addToken(Tipo.Menos, "-")
            elif self.caracterActual == "<":
                self.addToken(Tipo.Menor, "<")
            elif self.caracterActual == ">":
                self.addToken(Tipo.Mayor, ">")
            elif self.caracterActual == "'":
                self.addToken(Tipo.ComillaS, "'")
            elif self.caracterActual == '"':
                self.addToken(Tipo.ComillaD, '"')
            elif self.caracterActual==".":
                self.addToken(Tipo.Punto,".")

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
                    print("Error Lexico So: ", self.caracterActual)

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
            if not c.isalpha() and not c.isdigit():
                self.S1(posActual) 


            # S2 -> S2 (Numero)
            elif c.isnumeric():
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.VALOR, self.lexema)
                
            # S2 -> S3 (letra)
            elif c.isalpha():
                self.S3(posActual, fin)
                break

            # S2 -> ERROR_LEXICO
            else:                    
                self.pos_errores.append(posActual)
                print("Error Lexico ass: ", c)
            
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
                print("Erro en simbolo"+ letra)





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
                    self.pos_errores.append(posActual)
                    print("Error Lexico s3: ", c)
            posActual += 1

    #--------------------------- RESERVADAS/ID ---------------------------
    def analizar_Id_Reservada(self, posActual, fin):
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]

        # S0 -> S4 (Palabras Reservadas)
        if (self.lexema.lower() == "var"):
            self.addToken(Tipo.var, "var")
            return
        elif(self.lexema.lower() == "if"):
            self.addToken(Tipo.Cif, "if")
            return
        elif(self.lexema.lower() == "else"):
            self.addToken(Tipo.Celse, "else")
            return
        elif(self.lexema.lower() == "else if"):
            self.addToken(Tipo.Celseif, "else if")
            return
        elif(self.lexema.lower() == "do"):
            self.addToken(Tipo.Cdo, "do")
            return
        elif(self.lexema.lower() == "while"):
            self.addToken(Tipo.Cwhile, "while")
            return
        elif(self.lexema.lower() == "continue"):
            self.addToken(Tipo.continuacio, "continue")
            return
        elif(self.lexema.lower() == "break"):
            self.addToken(Tipo.Cbreak, "break")
            return
        elif(self.lexema.lower() == "return"):
            self.addToken(Tipo.retorno, "return")
            return
        elif(self.lexema.lower() == "while"):
            self.addToken(Tipo.Cwhile, "while")
            return
        elif(self.lexema.lower() == "funtion"):
            self.addToken(Tipo.funcion, "funtion")
            return
        elif(self.lexema.lower() == "class"):
            self.addToken(Tipo.clase, "class")
            return
        elif(self.lexema.lower() == "constructor"):
            self.addToken(Tipo.constructor, "constructor")
            return
        elif(self.lexema.lower() == "this"):
            self.addToken(Tipo.this, "this")
            return

        elif(self.lexema.lower() == "math.pow"):
            self.addToken(Tipo.Mpotencia, "math.pow")
            return
    




        self.lexema = ""
        c = ''
        while posActual < fin:
            c = self.entrada[posActual]
            
            # S0 -> S5 ('#')
            if c == "_":
                print("verifica el simbolo _")
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
                        self.pos_errores.append(posActual)
                        print("Error Lexico  id: ", c)
            
            posActual += 1
            
    
    
    
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
                    self.pos_errores.append(posActual)
                    print("Error Lexico s6: ", c)

            posActual += 1

    #--------------------------- ESTADO_ERROR ---------------------------
    def addError(self, entrada, estado):
        
        return 0


    #--------------------------- ADD TOKEN ---------------------------
    def addToken(self, tipo, valor):
    #print("|"+valor+"|")
        nuevo = Token(tipo, valor)
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


    #-------------obteniendo tamano de comentario multilinea---
    def getSizecomentario(self, posInicial):
        longitud=0  
            
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " " or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r":# or self.entrada[i] == "$":
                break
            elif self.entrada[i]=="*" and self.entrada[i+1]=="/":
                print("fin mult")
                
                longitud=1
            
          
        return longitud