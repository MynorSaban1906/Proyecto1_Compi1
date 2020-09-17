from enum import Enum
class Tipo(Enum):
    # Simbolos del Lenguaje
    LLAVEIZQ = 1
    LLAVEDER = 2
    DPUNTOS = 3
    PCOMA = 4
    COMA = 5
    ParentIzq=6
    ParentDer=7
    Igual=8
    IgualF=9
    Multipli=10
    Div=11
    Mas=12
    Menos=13
    Menor=14
    Mayor=15
    ComillaS=16
    ComillaD=17
    Punto=18
    Amperson=19
    Or=20



    # Palabras reservadas
    this=21
    constructor=22
    clase=23
    funcion=24
    retorno=25
    Mpotencia=26
    verdad=27
    falso=28
    continuacio=29
    Cwhile=30
    Cif=31
    Cbreak=32
    Celse=33
    Celseif=34
    Cdo=35
    cfor=36  
    comeline=40
    comemult=41
    var=43


  
    # Expresiones Regulares
    VALOR = 37
    ID = 38
    NINGUNO = 39


class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor ):
        self.tipoToken = tipo
        self.valorToken = valor
    def __str__(self):
        return f"TOKEN ->  {self.valorToken}  TIPO -> {self.tipoToken}"
        
class Recorrido:
    simbolo=""
    inicial=0
    final=0
    tipo=Tipo.NINGUNO
    def __init__(self,simbolo,einicial,efinal,tipo):
        self.simbolo=simbolo
        self.inicial=einicial
        self.final=efinal
        self.tipo=tipo
    def __str__(self):
        return f"Estado Inicial {self.inicial}  Transicion -> {self.simbolo}    Estado Final {self.final}"
        

class Errores:
    valorToken = ""
    posicion=0
    colum=0
    line=0
    def __init__(self, valor,pos,columnas,linea):
        
        self.valorToken = valor
        self.posicion =pos
        self.colum=columnas
        self.line=linea

    def __str__(self):
        return f"Simbolo Error -> {self.valorToken}   posicion -> {self.posicion}  columna -> {self.colum }  linea -> {self.line}"
