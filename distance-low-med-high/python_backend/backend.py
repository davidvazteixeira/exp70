#!/usr/bin/env python3
import serial
import time
from tkinter import *

# pip install pillow
from PIL import Image
from PIL import ImageTk

bauld = 57600
dev = '/dev/ttyUSB0'
port = serial.Serial(dev, bauld, timeout=1)

lights = {'red': Image.open("red.png"),
        'green':  Image.open("green.png"),
        'yellow':  Image.open("yellow.png"),
        'off': Image.open("off.png")
        }

explanation_picture = Image.open('ultrasound-600.png')

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.go_fullscreen = True

        self.master.bind('<Escape>', self.toggle_geom)
        self.toggle_geom()

        #self.pack(fill=BOTH, expand=1)

        self.red = ImageTk.PhotoImage(lights['red'])
        self.green = ImageTk.PhotoImage(lights['green'])
        self.yellow = ImageTk.PhotoImage(lights['yellow'])
        self.off = ImageTk.PhotoImage(lights['off'])
        self.explanation_photo = ImageTk.PhotoImage(explanation_picture)

        self.colors = {'red': self.red, 'green': self.green, 'yellow': self.yellow}

        sign_w = self.red.width()
        sign_h = self.red.height()

        #self._geom = self.master.winfo_geometry()
        #cx = self.master.winfo_screenwidth()
        #cy = self.master.winfo_screenheight()
        #self.img.place(x=cx/2 - sign_w/2 , y=cy/2 - sign_h/2)

        self.img = Label(image = self.off)
        self.explanation = Label(image = self.explanation_photo)

        left_label = """
        O sensor de ultrassom é composto por um microfone e um alto falante operando na frequência de ultrassom, que o homem não é capaz de escutar.

        Funciona emitindo um sinal em ultrassom na direção de um objeto distante. Quando o som refletido retorna, calcula o tempo de ida e volta.

        Relacionando este tempo com a velocidade do som podemos calcular a distância até o objeto.

        Além de medir distâncias, pode detectar a aproximação de objetos ou pessoas.
        """

        text = Label(self.master, text=left_label, font="Helvetica 26", wraplength=500)

        #label1.pack(side=LEFT, fill=X,expand=1)
        #self.img.pack(side=LEFT, fill=X)
        #label2.pack(side=LEFT, fill=X,expand=1)

        self.blank_label = Label(height=10).grid(column =0, row =0)
        self.explanation.grid(column=0, row=1)
        text.grid(column=2, row=1)
        self.img.grid(column=1, row=1)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)

    def toggle_geom(self, event = None):
        self._geom = self.master.winfo_geometry()
        if(self.go_fullscreen):
            self.master.geometry(self._geom)
        else:
            pad=3
            self._geom='640x480+0+0'
            self.master.geometry("{0}x{1}+0+0".format(
                self.master.winfo_screenwidth() - pad,
                self.master.winfo_screenheight() - pad)
            )

        self.go_fullscreen = not self.go_fullscreen

    def light(self, color):
        self.img.configure(image=self.colors[color])

    def checkDistance(self):
        root.after(100, self.checkDistance)

        port.write('c'.encode('ascii'))
        time.sleep(0.01)
        x = port.readline()
        try:
            x = int(x)
        except:
            print('Not ready')
            return

        x = int(x)
        if x > 100:
            self.light('green')
        elif x > 50:
            self.light('yellow')
        else:
            self.light('red')

root = Tk()
app = Window(root)
root.wm_title("Tkinter window")
root.geometry("200x120")
root.after(500, app.checkDistance)
root.mainloop()

