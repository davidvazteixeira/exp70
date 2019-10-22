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

col = 390       
sign_w = 220

def open_resize(name, w):
        img = Image.open(name)
        ratio = w/img.size[0]
        h = int(img.size[1]*ratio)
        img = img.resize((w, h), Image.ANTIALIAS)
        return img

lights = {
        'red': open_resize("red.png", sign_w),
        'yellow':  open_resize("yellow.png", sign_w),
        'green':  open_resize("green.png", sign_w),
        'off': open_resize("off.png", sign_w)
        }
      
explanation_picture = open_resize('ultrasound-600.png', col)

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.go_fullscreen = True

        self.master.bind('<Escape>', self.goodbye)
        self.master.bind('<Button-1>', self.goodbye)

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

        Funciona emitindo um sinal na direção de um objeto distante. Quando o som refletido retorna, calcula o tempo de ida e volta.

        Relacionando este tempo com a velocidade do som podemos calcular a distância até o objeto.

        Além de medir distâncias, pode detectar a aproximação de objetos ou pessoas.
        """

        text = Label(self.master, text=left_label, font="Helvetica 18", wraplength=col, justify=LEFT)

        #label1.pack(side=LEFT, fill=X,expand=1)
        #self.img.pack(side=LEFT, fill=X)
        #label2.pack(side=LEFT, fill=X,expand=1)

        #self.blank_label = Label(height=10).grid(column =0, row =0)
        self.explanation.grid(column=0, row=1)
        text.grid(column=2, row=1)
        self.img.grid(column=1, row=1)

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)

    def goodbye(self, event = None):
        print('Exit')
        root.destroy()


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
root.geometry("1184x624")
root.attributes('-fullscreen', True)
root.after(500, app.checkDistance)
root.mainloop()

