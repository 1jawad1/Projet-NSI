import tkinter as tk
from tkinter import filedialog as fd  #boite dialogue pour ouvrir un fichier
from tkinter.messagebox import showinfo
import time

screen = tk.Tk()
screen.geometry("1000x700")

#--------------------------------------------------------------------------------

dX = 25
dY = 20
pixel_size = 20

canva_X = dX * pixel_size + dX-1
canva_Y = dY * pixel_size + dY-1

canva = tk.Canvas(screen, width = canva_X , height = canva_Y, bg='white', highlightbackground='black', highlightcolor='black')

n_x = 1
n_y = 1

#les lignes verticales pour le cadrillage

for i in range(pixel_size, canva_X-dX+1, pixel_size):
        canva.create_line(i+n_x, 0, i+n_x, canva_Y+1 , fill='black', width = 1)
        n_x+=1
    
# #les lignes horizontales pour le cadrillage

for i in range(pixel_size, canva_Y-dY+1, pixel_size):
        canva.create_line(0, i+n_y, canva_X+1,  i+n_y, fill='black', width = 1)
        n_y+=1
    

#recupère le pixel

def getPixelCoords(x, y):

    x_ = (x//(pixel_size+1))*(pixel_size+1) 
    coords_x = (x_, x_+pixel_size) 

    y_ = (y//(pixel_size+1))*(pixel_size+1) 
    coords_y = (y_, y_+pixel_size) 

    return (coords_x, coords_y)

#colorie la case 
current_color = 'black'

#petit bug avec les pixels de la première colonne, il ne s'éfface pas et on peut en replacer un au dessus 

def fillPixel(e):
    global current_color
    coords_x, coords_y  = getPixelCoords(e.x, e.y)

    pixel_coords = (coords_x[0]+1, coords_y[0]+1, coords_x[1]+1, coords_y[1]+1)
    pixel_tag = f"{coords_x[0]}x{coords_y[0]}"

    match e.type:
         
        case '6':
            if not canva.find_withtag('hover'):
                canva.create_rectangle(*pixel_coords, fill='#e0e0e0', tags='hover', width=0)
                canva.tag_bind('hover', '<Leave>', lambda e: canva.delete('hover'))

        case '4':
            if e.num == 1 and not canva.find_withtag(pixel_tag) :
                canva.create_rectangle( *pixel_coords, fill=current_color, tags=(current_color, pixel_tag), width=0)
                current_color = 'red'

            elif e.num == 3 and canva.find_withtag(pixel_tag):
                canva.delete(pixel_tag)



canva.bind('<Motion>', fillPixel)
canva.bind("<Button-1>", fillPixel)
canva.bind("<Button-3>", fillPixel)

#open button
def select_file():
    filetypes = (('image files', '*.png'),('All files', '*.*'))
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
 
    showinfo(title='Selected File', message=filename)
    show_preview(filename)

def show_preview(filename):
    image_preview = tk.PhotoImage(file=filename)
    label = tk.Label(screen, image=image_preview)
    label.image = image_preview
    label.pack()


open_btn = tk.Button(screen, text="open a file", command=select_file)
open_btn.pack()
canva.pack()


screen.mainloop()