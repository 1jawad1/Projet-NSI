import tkinter as tk
from tkinter import filedialog as fd  #boite dialogue pour ouvrir un fichier
from tkinter.messagebox import showinfo

from PIL import Image, ImageTk, ImageOps

import time
import Canva


class Game : 
     

    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.canva = False
        self.name = None
        screen.geometry(f"{width}x{height}")

        self.colors = ["black", "#ffe2c3", "red", "#f57de7", "#9329ce", "#0821b3","#35c729", "#62d4ed", "#839845", "#5c6c86"]

        self.color_buttons_frame = tk.Frame(self.screen)
        self.color_buttons_frame.grid(column=1, row=5, columnspan=4, pady=20)

        self.current_image = None
        self.label = tk.Label(screen, text="No image selected")

        self.name_entry = None
        self.name_buttun = None



    def create_color_button(self, color):
        button = tk.Canvas(self.color_buttons_frame, width=30, height=30, bg=self.screen.cget("bg"), highlightthickness=0)
        button.create_oval(2, 2, 28, 28, fill=color, outline=color)
        button.bind("<Button-1>", lambda event, c=color: self.canva.select_color(c))
        button.pack(side="left", padx=5)


    def select_file(self):
        filetypes = (('image files', '*.png'),('All files', '*.*'))
        filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    
        showinfo(title='Selected File', message=filename)
        self.editImage(filename, 50)


    def editImage(self, filename, w):
        image = Image.open(filename)

        width, height = image.size
        ratio = width / height

        image = image.resize((w, round(w/ratio)), Image.NEAREST)
        image = image.resize((200, round(200/ratio)), Image.NEAREST)
        image = image.quantize(colors=10, method=Image.Quantize.FASTOCTREE)

        self.current_image = ImageTk.PhotoImage(image)
        self.show_preview(self.current_image, w, round(w/ratio))



    def show_preview(self, image, w, h):

        self.label.config(image=image)

        if(self.canva): self.canva.canva.destroy()
            
        self.ecran = tk.Canvas(self.screen)
        self.canva = Canva.Canva(w, h, 10, self.ecran, self.screen)

        self.canva.draw()

        self.canva.canva.bind('<Motion>', self.canva.fillPixel)
        self.canva.canva.bind("<Button-1>", self.canva.fillPixel)  

        screen.bind("<Shift_L>", lambda e: self.canva.changeClickStatus())  
        
        self.canva.canva.bind("<Button-3>", self.canva.fillPixel)
        self.canva.canva.grid(column=1, row=2, columnspan=3, rowspan=3, padx=25)
    
    def start_project(slef):
        pass

    def ask_forname(self, got_name=False):
        if got_name:
            self.name = got_name
            self.display_game()
            self.name_entry.destroy()
            self.name_buttun.destroy()

            print(self.name)
            return

        self.name_entry = tk.Entry(self.screen, width=60)
        self.name_buttun = tk.Button(self.screen, text='Apply', command=lambda : self.ask_forname(self.name_entry.get()))

        self.name_entry.grid(row=2, column=1, padx=200, pady=50)
        self.name_buttun.grid(row=3, column=1, sticky='n')

    

    def display_game(self):
        for color in self.colors:
            self.create_color_button(color)

        open_btn = tk.Button(self.screen, text="open a file", command=self.select_file)
        name = tk.Label(self.screen, text=self.name, font=("Helvetica", 20))

        # les .pack() ici : 
        open_btn.grid(column=4, row=4, pady=10)
        name.grid(column=4, row=1)
        self.label.grid(column=4, row=2, columnspan=1, rowspan=1 , pady=10)

    def start_game(self):
        title = tk.Label(self.screen, text='PIxelSolo', font=("Arial", 25, "bold"))
        title.grid(column=1, row=1, columnspan=3, pady=10)

        self.ask_forname()        
        self.screen.mainloop()
     

screen = tk.Tk()

Game(screen, 800, 600).start_game()