from enum import Enum


class Tipo(Enum):
    # Simbolos del Lenguaje
    LLAVEIZQ = 1
    LLAVEDER = 2
    DPUNTOS = 3
    PCOMA = 4
    COMA = 5

    # Palabras reservadas
    color=6
    border=7
    textaling=8
    fontweight=9
    paddingleft=10
    paddingtop=11
    lineheight=12
    margintop=13
    marginleft=14
    display=15
    top=16
    flotante=17
    minwidth=17
    backgroundc=18
    opacity=19
    fontfamily=20
    fontsize=21
    paddingright=22
    padding=23
    width=24
    marginright=25
    margin=26
    position=27
    clear=28
    maxheight=29
    backgroundi=30
    background=31
    fontstyle=32
    front=33
    paddingbottom=34
    
    height=35
    borderstyle=36
    left=37
    maxwidth=38
    minheight=39
    right=40
    marginbottom=41

    bottom=42
   

    # Expresiones Regulares
    VALOR = 43
    ID = 44
    NINGUNO = 45


class Token:
    tipoToken = Tipo.NINGUNO
    valorToken = ""
    def __init__(self, tipo, valor ):
        self.tipoToken = tipo
        self.valorToken = valor
    def __str__(self):
        return f"Palabra Reservada {self.valorToken}"
