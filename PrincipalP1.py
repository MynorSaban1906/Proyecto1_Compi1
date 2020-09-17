
from tkinter import *               # ventana
from tkinter import Menu            # barra de tareas
from tkinter import filedialog      # filechooser
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from pru import *     # llamando a una funcion externa
from AnalisisJs import *
from analizadorCSS import *

class GUI:
 # Metodo que contiene la definicion de la interfaz grafica 
    def __init__(self):
        self.window = Tk()
        
        self.txtEntrada = Entry(self.window,width=10)
        self.txtConsola = Entry(self.window,width=10)
        self.txtrecorrido=Entry(self.window,width=10)
        self.txtTOKEN=Entry(self.window,width=10)
        # Propiedades de la ventana
        self.window.title("Proyecto 1 - MYNOR SABAN")
        self.window.geometry('1600x1000')
        self.window.configure(bg = '#9ACFEF')
              

        # propiedades del menu 
        self.menu = Menu(self.window)
        self.file_item = Menu(self.menu)  #Menu File
        self.file_item.add_command(label='Open File', command=self.abrirFile)
        self.file_item.add_separator()
        self.file_item.add_command(label='Analyze')
        self.file_item.add_separator()
        self.file_item.add_command(label='Exit')
 
        self.report_item = Menu(self.menu)    # menu Reports
        self.report_item.add_separator()
        self.report_item.add_command(label='Errors')
        self.report_item.add_separator()
        self.report_item.add_command(label='Tree')
        
        self.menu.add_cascade(label='File', menu=self.file_item)
        self.menu.add_cascade(label='Reports', menu=self.report_item) 
        self.window.config(menu=self.menu)
        
        # propiedades del textarea
        self.txtEntrada = scrolledtext.ScrolledText(self.window,width=80,height=25)   # textArea Entrada
        self.txtEntrada.place(x=50, y = 50)
        #ent = txtEntrada.get("1.0","10.10")
        #print("ent: ",ent)
        self.lbl1 = Label(self.window, text="RECORRIDO:")  #label 
        self.lbl1.place(x=800, y =35)
        self.txtrecorrido = scrolledtext.ScrolledText(self.window,width=50,height=20)   # textArea Entrada
        self.txtrecorrido.place(x=800, y =50)
        self.lbl2 = Label(self.window, text="TOKENS:")  #label 
        self.lbl2.place(x=800, y =400)
        self.txtTOKEN = scrolledtext.ScrolledText(self.window,width=50,height=15)   # textArea Entrada
        self.txtTOKEN.place(x=800, y = 425)

        self.lbl = Label(self.window, text="Console:")  #label 
        self.lbl.place(x=50, y = 465)
        self.txtConsola = scrolledtext.ScrolledText(self.window,width=80,height=10)   # textArea consola
        self.txtConsola.place(x=50, y = 490)
        self.btn = Button(self.window, text="JS", bg="black", fg="white", command=self.Analyze)    #btn Analyze
        self.btn1 = Button(self.window, text="CSS", bg="black", fg="white", command=self.anaCSS) 
        self.btn.place(x=400, y = 460)
        self.btn1.place(x=350, y = 460)
        # Dispara la interfaz
        self.window.mainloop()


    def Analyze(self):
        entrada = self.txtEntrada.get("1.0", END) #fila 1 col 0 hasta fila 2 col 10
        miScanner = ANALIZADORJS()
        retorno = miScanner.analizar(entrada)
        print("\nIMPRESION DE ERRORES\n")
        miScanner.imprimirErrores()
        self.txtConsola.insert("1.0", retorno)
        toke=miScanner.imprimirtoken()
        self.txtTOKEN.insert("1.0",toke)
        record=miScanner.imprimirtra()
        self.txtrecorrido.insert("1.0",record)
        miScanner.generarGrafo()

    def anaCSS(self):
        """entrada = self.txtEntrada.get("1.0", END)
        analiza= Scanner()
        retorno =analiza.analizar(entrada)
        self.txtConsola.insert("1.0", retorno)
        token =analiza.imprimirTokens()
        self.txtTOKEN.insert("1.0",token)"""
        entrada= self.txtEntrada.get("1.0",END)
        analiza=  analizadorCSS()
        retorno =analiza.analizar(entrada)
        self.txtConsola.insert("1.0", retorno)
        token =analiza.imprimirTokens()
        self.txtTOKEN.insert("1.0",token)
        recor =analiza.imprimirRecorrido()
        self.txtrecorrido.insert("1.0",recor)
        print("Errores")
        analiza.imprimirErrores()
        analiza.generarGrafo()
        

    # Dispara el Filechooser
    def abrirFile(self):
        nameFile=filedialog.askopenfilename(title = "Seleccione archivo",filetypes = (("js files","*.js"), ("html files","*.html"),("css files","*.css"),("All Files","*.*")))
        if nameFile!='':
            archi1=open(nameFile, "r", encoding="utf-8")
            contenido=archi1.read()
            archi1.close()
            self.txtEntrada.delete("1.0", END)
            self.txtEntrada.insert("1.0", contenido) 
    
    def seleccionar(self,lenguaje):
        cadena = ""
        if (lenguaje.get()):
            print("selecciono css")
        else:
            print(" no css")

        

start = GUI()
