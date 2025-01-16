import tkinter as tk
from tkinter import filedialog as fd  #boite dialogue pour ouvrir un fichier
from tkinter.messagebox import showinfo
screen = tk.Tk()
#--------------------------------------------------------------------------------

dX = 20
dY = 20
pixel_size = 15

canva_X = dX * pixel_size + dX-1
canva_Y = dY * pixel_size + dY-1

canva = tk.Canvas(screen, width = canva_X , height = canva_Y, bg = 'white')
n = 1
print((canva_X-pixel_size-dX+1)%pixel_size)
for i in range(pixel_size, canva_X-dX+1, pixel_size):
        canva.create_line(i+n, 0, i+n, canva_Y, fill='black', width = 1)
        n+=1
    

for j in range(dY):
    pass
    # canva.create_line(0,j,0,50)


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