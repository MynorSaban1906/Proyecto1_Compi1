from enum import Enum

class Simbolo(Enum):
    #simbolos de lenguajes
    llaveIzq=1
    llaveDer=2
    Dpuntos=3
    Pcoma=5
    coma=6
    MenorQ=7
    MayorQ=8
    Distinto=9
    IgualF=10
    Igual=11
    MayorIQ=12
    MenorIQ=13
    Mas=14
    Menos=15
    Asterisco=16
    Division=17
    ParentIzq=18
    ParentDer=19
    NotaLambda=20
    comillaSimple=38
    Simor=39

    #palabras reservadas
    DeclaracionJS=21
    caracter=24
    boleano=25
    tipo=26
    si=27
    sino=28
    opcion=29
    ciclofor=30
    ciclowhile=31
    ciclodo=32
    econtinue=33
    ebreak=34
    ereturn=35
    funcion=36
    clase=37

    #reservadas de; css
    color=51
    border=52
    textaling=53
    fontweight=54
    paddingleft=55
    paddingtop=56
    lineheight=57
    margintop=58
    marginleft=59
    display=60
    top=61
    flotante=62
    minwidth=63
    backgroundc=64
    opacity=65
    fontfamily=66
    fontsize=67
    paddingright=68
    padding=69
    width=70
    marginright=71
    margin=72
    position=73
    clear=74
    maxheight=75
    backgroundi=76
    background=77
    fontstyle=78
    front=79
    paddingbottom=80
    
    height=82
    borderstyle=83
    left=84
    maxwidth=85
    minheight=86
    right=87
    marginbottom=88
    bottom=89

    #expresiones regulares
    epsilon=38
    ID=22
    VALOR=23

    
class Token:
    tipoToken = Simbolo.epsilon
    valorToken = ""
    posicion=0
    def __init__(self, tipo, valor,pos):
        self.tipoToken = tipo
        self.valorToken = valor
        self.posicion =pos

    def __str__(self):
        return f"Simbolo del sistema {self.valorToken}  posicion {self.posicion} "

class Errores:
    valorToken = ""
    posicion=0
    def __init__(self, valor,pos):
        
        self.valorToken = valor
        self.posicion =pos

    def __str__(self):
        return f"Simbolo Error {self.valorToken}  posicion {self.posicion} "
