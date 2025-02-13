import tkinter as tk
from tkinter import filedialog as fd  #boite dialogue pour ouvrir un fichier
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk, ImageOps

import time
import Canva


class Game : 
     def __init__(self):
          pass
     
     
screen = tk.Tk()
screen.geometry("1000x700")

#--------------------------------------------------------------------------------


canva = False


#palette de couleurs

colors = ["black", "#ffe2c3", "red", "#f57de7", "#9329ce", "#0821b3","#35c729", "#62d4ed", "#839845", "#5c6c86"]

color_buttons_frame = tk.Frame(screen)
color_buttons_frame.grid(column=1, row=5, columnspan=4, pady=20)

def create_color_button(color):
        button = tk.Canvas(color_buttons_frame, width=30, height=30, bg=screen.cget("bg"), highlightthickness=0)
        button.create_oval(2, 2, 28, 28, fill=color, outline=color)
        button.bind("<Button-1>", lambda event, c=color: canva.select_color(c))
        button.pack(side="left", padx=5)

for color in colors:
    create_color_button(color)


#open button

current_image = None
label = tk.Label(screen, text="No image selected")

def select_file():
    filetypes = (('image files', '*.png'),('All files', '*.*'))
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
 
    showinfo(title='Selected File', message=filename)
    editImage(filename, 50)

def editImage(filename, w):
    global current_image
    image = Image.open(filename)

    width, height = image.size
    ratio = width / height

    image = image.resize((w, round(w/ratio)), Image.NEAREST)
    image = image.resize((200, round(200/ratio)), Image.NEAREST)
    image = image.quantize(colors=10, method=Image.Quantize.FASTOCTREE)



    current_image = ImageTk.PhotoImage(image)
    show_preview(current_image, w, round(w/ratio))


def show_preview(image, w, h):

    label.config(image=image)
    
    global canva

    if(canva): canva.canva.destroy()
    
    ecran = tk.Canvas(screen)
    canva = Canva.Canva(w, h, 10, ecran, screen)

    canva.draw()

    canva.canva.bind('<Motion>', canva.fillPixel)

    canva.canva.bind("<Button-1>", canva.fillPixel)  

    screen.bind("<Shift_L>", lambda e: canva.changeClickStatus())  

    canva.canva.bind("<Button-3>", canva.fillPixel)
    
    canva.canva.grid(column=1, row=2, columnspan=3, rowspan=3, padx=25)


open_btn = tk.Button(screen, text="open a file", command=select_file)

title = tk.Label(screen, text='PIxelSolo', font=("Arial", 25, "bold"))

# les .pack() ici : 
title.grid(column=1, row=1, columnspan=4, pady=10)
open_btn.grid(column=4, row=4, pady=10)
label.grid(column=4, row=2, columnspan=1, rowspan=1 , pady=10)

 
screen.mainloop()
str("ffff")






