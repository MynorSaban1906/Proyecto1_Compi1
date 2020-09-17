from TokenJS import *
from graphviz import Digraph

class ANALIZADORJS:
    lista_tokens = list()   # lista de tokens
    lista_errores = list()  # lista errores lexico
    pos_errores = list()    # lista de posiciones de errores
    estado = 0
    lexema = ""

    def __init__(self):
        self.simbolosS={"{","}","(",")",":",";",",","=","<",">","+","-","/","*",'"',"'","."}
        self.simboloFun={'&','|'}
        self.lista_tokens = list()
        self.lista_errores = list()
        self.pos_errores = list()
        self.lista_transiciones=list()
        self.lista=list()
        self.linea=0
        self.columna=0
        self.lexema = ""
        self.path=""
        self.estado=0
#alex400404k@gmail.com
    #--------------------------- ESTADO0 ---------------------------
    def analizar(self, cadena):
        self.entrada = cadena + "$"
        
        pos = 0    # almacena la posicion del caracter que se esta analizando
        self.linea= 1#inicia en linea 1
        self.columna=0
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
                self.columna=0
                
            elif self.caracterActual == "{":
                self.addTransicion(self.caracterActual,0,1,Tipo.LLAVEIZQ)
                self.addToken(Tipo.LLAVEIZQ, "{")
              
            elif self.caracterActual == "}":
                self.addTransicion(self.caracterActual,0,1,Tipo.LLAVEDER)
                self.addToken(Tipo.LLAVEDER, "}")
            
            elif self.caracterActual == ":":
                self.addTransicion(self.caracterActual,0,1,Tipo.DPUNTOS)
                self.addToken(Tipo.DPUNTOS, ":")
                
            elif self.caracterActual == ";":
                self.addTransicion(self.caracterActual,0,1,Tipo.PCOMA)
                self.addToken(Tipo.PCOMA, ";")
               
            elif self.caracterActual == ",":
                self.addTransicion(self.caracterActual,0,1,Tipo.COMA)
                self.addToken(Tipo.COMA, ",")
                
            elif self.caracterActual == "(":
                self.addTransicion(self.caracterActual,0,1,Tipo.ParentIzq)
                self.addToken(Tipo.ParentIzq, "(")
            
            elif self.caracterActual == ")":
                self.addTransicion(self.caracterActual,0,1,Tipo.ParentDer)
                self.addToken(Tipo.ParentDer, ")")
              
            elif self.caracterActual == "=":
                self.addTransicion(self.caracterActual,0,1,Tipo.Igual)
                self.addToken(Tipo.Igual, "=")
                
            elif self.caracterActual == "*":
                self.addTransicion(self.caracterActual,0,1,Tipo.Multipli)
                self.addToken(Tipo.Multipli, "*")
               
            elif self.caracterActual == "/":
                self.addTransicion(self.caracterActual,0,1,Tipo.Div)
                self.addToken(Tipo.Div, "/")
                
            elif self.caracterActual == "+":
                self.addTransicion(self.caracterActual,0,1,Tipo.Mas)
                self.addToken(Tipo.Mas, "+")
                
            elif self.caracterActual == "-":
                self.addTransicion(self.caracterActual,0,1,Tipo.Menos)
                self.addToken(Tipo.Menos, "-")
                
            elif self.caracterActual == "<":
                self.addTransicion(self.caracterActual,0,1,Tipo.Menor)
                self.addToken(Tipo.Menor, "<")
                
            elif self.caracterActual == ">":
                self.addTransicion(self.caracterActual,0,1,Tipo.Mayor)
                self.addToken(Tipo.Mayor, ">")
              
            elif self.caracterActual == "'":
                self.addTransicion(self.caracterActual,0,1,Tipo.ComillaS)
                self.addToken(Tipo.ComillaS, "'")
                
            elif self.caracterActual == '"':
                self.addTransicion(self.caracterActual,0,1,Tipo.ComillaD)
                self.addToken(Tipo.ComillaD, '"')
                
            elif self.caracterActual==".":
                self.addTransicion(self.caracterActual,0,1,Tipo.Punto)
                self.addToken(Tipo.Punto,".")
             

            # S0 -> S2 (Numeros) . numero
            elif self.caracterActual.isnumeric():
                self.estado=0
                sizeLexema = self.getSizeDigito(pos)
                self.S2(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue
                
            # S0 -> Reservadas | Identificadores
            elif self.caracterActual.isalpha() :  
                self.estado=0
                sizeLexema = self.getSizeLexema(pos)
               
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue
            
            
            elif self.caracterActual=="_" : 
                self.columna+=1
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue
            elif self.caracterActual=="!" : 
                self.estado=0
                self.columna+=1
                sizeLexema = self.getSizeLexema(pos)
                self.analizar_Id_Reservada(pos, pos+sizeLexema)
                pos = pos+sizeLexema
                continue

            # Otros
            elif self.caracterActual == " " or self.caracterActual == "\t" or self.caracterActual == "\r" or self.caracterActual == "\n":  
                if self.caracterActual!="\n" and self.caracterActual==" ":
                    self.columna+=1
                elif self.caracterActual=="\n":
                    self.linea+=1
                    self.columna=0
                pos += 1 #incremento del contador del while
                continue
                
            
            else:                    
                # S0 -> FIN_CADENA
                if self.caracterActual == "$" and pos == len(self.entrada)-1:
                    if len(self.lista_errores) > 0:
                        return "errores \n\n"+self.eliminarErrores(cadena)
                        
                    return "analisis exitoso...!!!"+ self.eliminarErrores(cadena)
                #  S0 -> ERROR_LEXICO
                else:
                    self.columna+=1
                    print("Error Lexico S1: ", self.caracterActual,"  POSICION -> ",pos," LINEA -" ,self.linea,"  COLUMA -> ", self.columna)
                    self.addError(self.caracterActual,pos,self.columna,self.linea)
  
            pos += 1 #incremento del contador del while
            
            
        if len(self.lista_errores)>0:
            
            return "Exiten Errores Lexicos\n\t\t\t\t\tYA SE ELIMINO LOS ERRORES "+self.eliminarErrores(cadena)
            
            
            
        else:
            return "Cadena Limpia sin Errores: " + self.entrada + "\nAnalisis exitoso..!!!"
            
    #--------------------------- ESTADO2 ---------------------------
    def S2(self, posActual, fin):
        c = '' 
        esta=2
        while posActual < fin:
            c = self.entrada[posActual]
      
            if not c.isalpha() and not c.isdigit():
                self.columna+=1
                self.lexema+=c
                esta=self.S1(posActual,self.estado) 
                self.estado=esta
                

            # S2 -> S2 (Numero) 
            elif c.isnumeric():
                esta=2
                self.columna+=1
                self.lexema += c
                if(posActual+1 == fin):
                    self.addTransicion(c,self.estado,esta,Tipo.VALOR)
                    self.addToken(Tipo.VALOR, self.lexema)
                    self.estado=esta
                self.addTransicion(c,self.estado,esta,Tipo.VALOR)
                    
                self.estado=esta
                
                
            # S2 -> S3 (letra)
            elif c.isalpha():
                esta=2
                self.columna+=1
                self.lexema+=c
                self.addTransicion(c,self.estado,esta,Tipo.VALOR)
                self.addToken(Tipo.ID, self.lexema)
                self.estado=esta
                

            # S2 -> ERROR_LEXICO
            else: 
                self.columna+=1
                print("Error Lexico Estado 2 : ", c," columna-> ",self.columna," linea->",self.linea)                   
                self.pos_errores.append(posActual)
                self.addError(c,posActual,self.columna,self.linea)
                
              
            posActual += 1
    
    #-----------------ESTADO 1   simbolos y simbolos -----------------------------

    def S1(self,posActual,estadoI):
            letra=self.entrada[posActual]
            if letra == "{":
                self.addTransicion(letra,estadoI,1,Tipo.LLAVEIZQ)
                estadoI=1
            elif letra == "}":
                self.addTransicion(letra,estadoI,1,Tipo.LLAVEDER)
                estadoI=1
            elif letra == ":":
                self.addTransicion(letra,estadoI,1,Tipo.DPUNTOS)
                estadoI=1
            elif letra == ";":
                self.addTransicion(letra,estadoI,1,Tipo.PCOMA)
                estadoI=1
            elif letra == ",":
                self.addTransicion(letra,estadoI,1,Tipo.COMA)
                estadoI=1
            elif letra == "(":
                self.addTransicion(letra,estadoI,1,Tipo.ParentIzq)
                estadoI=1
            elif letra == ")":
                self.addTransicion(letra,estadoI,1,Tipo.ParentDer)
                estadoI=1
            elif letra == "=":
                self.addTransicion(letra,estadoI,1,Tipo.Igual)
                estadoI=1
            elif letra == "*":
                self.addTransicion(letra,estadoI,1,Tipo.Multipli)
                estadoI=1
            elif letra == "/":
                self.addTransicion(letra,estadoI,1,Tipo.Div)
                estadoI=1
            elif letra == "+":
                self.addTransicion(letra,estadoI,1,Tipo.Mas)
                estadoI=1
            elif letra == "-":
                self.addTransicion(letra,estadoI,1,Tipo.Menos)
                estadoI=1
            elif letra == "<":
                self.addTransicion(letra,estadoI,1,Tipo.Menor) 
                estadoI=1
            elif letra == ">":
                self.addTransicion(letra,estadoI,1,Tipo.Mayor)
                estadoI=1
            elif letra == "'":
                self.addTransicion(letra,estadoI,1,Tipo.ComillaS)
                estadoI=1
            elif letra == '"':
                self.addTransicion(letra,estadoI,1,Tipo.ComillaD)
                estadoI=1
            elif letra==".":
                self.addTransicion(letra,estadoI,1,Tipo.Punto)
                estadoI=1
                
            else:
                self.columna+=1
                print("Error en simbolo S1"+ letra," columna ", self.columna, " linea ",self.linea)
                
                self.addError(letra,posActual,self.columna,self.linea)
            return estadoI
            

    #=------------ IMPRIMIR LOS ERRROES CON SUS POSICONES --------------
    def imprimirErrores(self):
        if(self.lista_errores.__sizeof__==0):
            print("No hay errores")
        else:
            for x in self.lista_errores:
                print(x)


    # -------- IMPRIMIR LOS TOKEN ====
    def imprimirtoken(self):
        li=""
        for i in self.lista_tokens:
            li+=str(i)
            print(i)
            li+="\n"
        return li
    # -------- IMPRIMIR LOS transiciones ====
    def imprimirtra(self):
        li=""
        for i in self.lista_transiciones:
            li+=str(i)
            print(i)
            li+="\n"
        return li

    #--------------------------- RESERVADAS/ID ---------------------------
    def analizar_Id_Reservada(self, posActual, fin):
        
        for x in range(posActual,fin):
            self.lexema += self.entrada[x]
            

        # S0 -> S4 (Palabras Reservadas)
        if (self.lexema.lower() == "var"):
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.var)
            self.addToken(Tipo.var, "var")
            self.columna+=4
            return
        elif (self.lexema.lower() == "new"):
            self.columna+=4
            self.addToken(Tipo.var, "new")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.ID)
            return
        elif(self.lexema.lower() == "if"):
            self.columna+=3
            self.addToken(Tipo.Cif, "if")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.Cif)
            return
        elif(self.lexema.lower() == "else"):
            self.columna+=5
            self.addToken(Tipo.Celse, "else")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.Celse)
            return
        elif(self.lexema.lower() == "else if"):
            self.columna+=8
            self.addToken(Tipo.Celseif, "else if")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.Celseif)
            return
        elif(self.lexema.lower() == "do"):
            self.columna+=3
            self.addToken(Tipo.Cdo, "do")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.Cdo)
            return
        elif(self.lexema.lower() == "while"):
            self.columna+=6
            self.addToken(Tipo.Cwhile, "while")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.Cwhile)
            return
        elif(self.lexema.lower() == "continue"):
            self.columna+=9
            self.addToken(Tipo.continuacio, "continue")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.continuacio)
            return
        elif(self.lexema.lower() == "break"):
            self.columna+=6
            self.addToken(Tipo.Cbreak, "break")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.Cbreak)
            return
        elif(self.lexema.lower() == "return"):
            self.columna+=7
            self.addToken(Tipo.retorno, "return")   
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.retorno)
            return
        elif(self.lexema.lower() == "funtion"):
            self.columna+=8
            self.addToken(Tipo.funcion, "funtion")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.funcion)
            return
        elif(self.lexema.lower() == "class"):
            self.columna+=6
            self.addToken(Tipo.clase, "class")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.clase)
            return
        elif(self.lexema.lower() == "constructor"):
            self.columna+=12
            self.addToken(Tipo.constructor, "constructor")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.constructor)
            return
        elif(self.lexema.lower() == "this"):
            self.columna+=5
            self.addToken(Tipo.this, "this")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.this)
            return
        elif(self.lexema.lower() == "math.pow"):
            self.columna+=9
            self.addToken(Tipo.Mpotencia, "math.pow")
            self.addTransicion(f"Reservada {self.lexema}",0,3,Tipo.Mpotencia)
            return
    
        



        self.lexema = ""
        self.estado=0
        c = ''
        esta=4
        while posActual < fin:
            c = self.entrada[posActual]
            # L(L|N|_)*
            # S0 -> S5 ('_')
            if c == "_":
                self.columna+=1
                self.lexema += c
                
                # S5 -> S6 (letra)
                self.addTransicion(c,self.estado,esta,Tipo.ID)
                self.S6(posActual+1, fin)
                self.estado=esta
                posActual += 1
                break
            # S0 -> S5 ('!')
            elif c == "!":
                self.columna+=1
                self.lexema += c
                self.addTransicion(c,self.estado,esta,Tipo.NINGUNO)
                # S5 -> S6 (letra)
                self.estado=esta
                self.S6(posActual+1, fin)

                posActual += 1
                break
            elif c == "-":
                self.columna+=1
                self.lexema += c
                self.addTransicion(c,self.estado,esta,Tipo.ID)
                # S5 -> S6 (letra)
                self.estado=esta
                self.S6(posActual+1, fin)

                posActual += 1
                break
            # S0 -> S6 (letra)
            elif c.isalpha():
                self.S6(posActual, fin)
                break
            
            # S0 -> ERROR_LEXICO
            else:
                self.columna+=1
                print("Error Lexico  id: ", c," columna ",self.columna," linea",self.linea)
                self.addError(c,posActual,self.columna,self.linea)
                        
            
            posActual += 1
            
    #-------- borrar errores ----
    def eliminarErrores(self,cadena):
        self.entrada = cadena + "$"
        f = open (self.path,'w')
        
        
        pos = 0    # almacena la posicion del caracter que se esta analizando
        caract=""
        cad=""
        while pos < len(self.entrada): 
            
            if not self.entrada[pos].isalpha() and ( not self.entrada[pos].isdigit()):
                for x in self.lista_errores:
                    if x.posicion == pos:
                        pos+=1
            caract=self.entrada[pos]
            cad+=self.entrada[pos]
            f.write(caract)
              
                        
            pos+=1
        
        f.close()
        return cad
    
    
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
        esta=5
        while posActual < fin:
            c = self.entrada[posActual]
            #verificacion si tiene un simbolo
            
            # S6 -> S6 (letra)
            if c.isalpha():
                self.addTransicion(c,self.estado,esta,Tipo.ID)
                self.estado=esta
                self.lexema += c
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
                    

            # S6 -> S6 (Numero)
            elif c.isnumeric():
                self.lexema += c
                self.addTransicion(c,self.estado,esta,Tipo.ID)
                self.estado=esta
                if(posActual+1 == fin):
                    self.addToken(Tipo.ID, self.lexema)
                    
            
            elif c=="_":
                self.addTransicion(c,self.estado,esta,Tipo.ID)
                self.estado=esta
                self.lexema += c
            elif c=="-":
                self.addTransicion(c,self.estado,esta,Tipo.ID)
                self.estado=esta
                self.lexema += c
                
            

            # S6 -> ERROR_LEXICO
            else:
                self.columna+=1
                print("Error Lexico s6: ", c," columna ",self.columna," linea",self.linea)
                self.addError(c,posActual,self.columna,self.linea)
                    

            posActual += 1

    #--------------------------- ESTADO_ERROR ---------------------------
    def addError(self, entrada, pos,column,linea):

        nuevo = Errores(entrada,pos,column,linea)
        self.lista_errores.append(nuevo)
        self.caracterActual = ""
        self.lexema = ""
        
        return 0


    #--------------------------- ADD TOKEN ---------------------------
    def addToken(self, tipo, valor):

        nuevo = Token(tipo, valor)
        self.lista_tokens.append(nuevo)
        self.caracterActual = ""
        self.lexema=""

    #---------------- OBTENIENDO EL TAMAÑO DEL LEXEMA ----------------
    def getSizeLexema(self, posInicial):
        longitud = 0
        for i in range(posInicial, len(self.entrada)-1):
            if self.entrada[i] == " "or self.entrada[i] == "="or self.entrada[i] == "{" or self.entrada[i] == "}" or self.entrada[i] == "," or self.entrada[i] == ";" or self.entrada[i] == ":" or self.entrada[i] == "\n" or self.entrada[i] == "\t" or self.entrada[i] == "\r" or self.entrada[i]=="." or self.entrada[i] == "(" or self.entrada[i]==")"or self.entrada[i]=="'" or self.entrada[i] =='"' or self.entrada[i]=="/" or self.entrada[i]=="*"or self.entrada[i] =='+':
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


    #-----Guardando Transiciones ----
    def addTransicion(self,simbolo,einicial,efinal,tipo):
        transicion= Recorrido(simbolo,einicial,efinal,tipo)
        self.lista_transiciones.append(transicion)
        


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
        dot.edge("Estado 0","Estado 5", label='Letra')
        dot.node("Estado 5","Estado 5",shape='doublecircle')
        dot.edge("Estado 5","Estado 5", label='Numero| Letra | _ |-')
  

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
        f = open ("reporte1.txt",'w')
        
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
        template = open("reporte1.txt","r")
        output=open("reporte1.html","w")
        text=template.read()
        html=output.writelines(str(text))
        template.close()
        output.close()