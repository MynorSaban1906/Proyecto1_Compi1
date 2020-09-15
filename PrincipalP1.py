
from tkinter import *               # ventana
from tkinter import Menu            # barra de tareas
from tkinter import filedialog      # filechooser
from tkinter import scrolledtext    # textarea
from tkinter import messagebox      # message box
from pru import *     # llamando a una funcion externa
from AnalisisJs import *

class GUI:
 # Metodo que contiene la definicion de la interfaz grafica 
    def __init__(self):
        self.window = Tk()
        
        self.txtEntrada = Entry(self.window,width=10)
        self.txtConsola = Entry(self.window,width=10)
        # Propiedades de la ventana
        self.window.title("Proyecto 1 - ML WEB EDITOR")
        self.window.geometry('1000x700')
        self.window.configure(bg = '#9ACFEF')
    
        root = self.window
        states = []
        lenguaje = IntVar()
        chk = Checkbutton(root, text="JS",  variable=lenguaje,command=self.seleccionar(lenguaje))

        chk.pack(side=LEFT)
        chk.place(x=0,y=0)
        
        chk = Checkbutton(root, text="CSS",  variable=lenguaje,command=self.seleccionar(lenguaje))

        chk.pack(side=LEFT)
        chk.place(x=50,y=0)

        chk3 = Checkbutton(root, text="HTML",  variable=lenguaje, 
            onvalue=1, offvalue=0,command=self.seleccionar(lenguaje))

        chk3.pack(side=LEFT)
        chk3.place(x=100,y=0)
        

       
              

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


        self.lbl = Label(self.window, text="Console:")  #label 
        self.lbl.place(x=50, y = 465)
        self.txtConsola = scrolledtext.ScrolledText(self.window,width=80,height=10)   # textArea consola
        self.txtConsola.place(x=50, y = 490)
        self.btn = Button(self.window, text="Analyze", bg="black", fg="white", command=self.Analyze)    #btn Analyze
        self.btn.place(x=400, y = 460)
        # Dispara la interfaz
        self.window.mainloop()


    def Analyze(self):
        entrada = self.txtEntrada.get("1.0", END) #fila 1 col 0 hasta fila 2 col 10
        miScanner = ANALIZADORJS()
        retorno = miScanner.analizar(entrada)
        miScanner.imprimirErrores()
        print("\n\n")
        miScanner.imprimirtoken()
        #analiza= Scanner()
        #retorno =analiza.analizar(entrada)
        #analiza.res()
        #print("\n\n")
        #analiza.res1()
        #self.txtConsola.delete("1.0", END)
        #self.txtConsola.insert("1.0", retorno)
    
        
        

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
