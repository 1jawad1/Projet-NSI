import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd  #boite dialogue pour ouvrir un fichier
from tkinter.messagebox import showinfo
import json as js



from PIL import Image, ImageTk, ImageOps
import numpy as np

from datetime import date
import time
import Canva
 

class Game(tk.Frame) : 
     
    def __init__(self, screen, controller):
        super().__init__(screen)
        self.screen = screen

        self.controller =controller
        self.canva = False
        self.name = None

        self.colors = ["#000000", "#ffe2c3", "#ff0000", "#f57de7", "#9329ce", "#0821b3","#35c729", "#62d4ed", "#839845", "#5c6c86"]

        self.color_buttons_frame = tk.Frame(self)
        self.color_buttons_frame.grid(column=1, row=6, columnspan=5, pady=20)

        self.current_image = None
        self.label = tk.Label(self, text="No image selected")

        self.name_entry = tk.Entry(self, width=60)
        self.name_buttun = tk.Button(self, text='Apply', command=lambda : self.ask_forname(self.name_entry.get()))

    def switch_page(self, page):
        self.controller.show_frame(page)


    #pixelsolo
    def create_color_button(self, color):
        button = tk.Canvas(self.color_buttons_frame, width=30, height=30, bg=self.cget("bg"), highlightthickness=0)
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

    def download_pixel(self):
        pop_up = tk.Toplevel()
        pop_up.geometry("300x300")
        
        labelTop = tk.Label(pop_up, text="Choose your favourite month")
        labelTop.grid(column=1, row=0)
        export = tk.Button(pop_up, text='exporter', command=self.download_image)
        export.grid(row=1, column=2)
        comboExample = ttk.Combobox(pop_up, values=["png", "jpg", "jpeg"])
        comboExample.grid(column=1, row=1)
        comboExample.current(1)
        pop_up.mainloop()


    def download_image(self):

        pixels = np.array(self.canva.matrix_pixels(self.canva.Nx, self.canva.Ny), dtype=np.uint8)
        img = Image.fromarray(pixels, "RGB")
        img.save('test.jpg')

    def get_project_data(self, message = False):
        self.share_page = tk.Toplevel()

        title = tk.Label(self.share_page, text="Share your project !", font=("Helvetica", 16, "bold"))
        title.grid(column=1, row=1, padx=20, pady=5)

        if message:
            error = tk.Label(self.share_page, text=message, fg='red')
            error.grid(column=1, row=2, sticky='s', pady=5)

        name_label = tk.Label(self.share_page, text="your project's name : " )
        project_name = tk.Entry(self.share_page, width=25)

        description_label = tk.Label(self.share_page, text="a description of your project : " )
        project_description = tk.Entry(self.share_page, width=25)

        tags_label = tk.Label(self.share_page, text="some tags (seperate each tag with a space): " )
        project_tags = tk.Entry(self.share_page, width=25)

        name_label.grid(column=1, row=3, sticky='sw', pady=(5, 0), padx=20)
        project_name.grid(column=1, row=4, sticky='wn', pady=(0, 5), padx=20)

        description_label.grid(column=1, row=5, sticky='sw', pady=(5, 0), padx=20)
        project_description.grid(column=1, row=6, sticky='nw', pady=(0, 5), padx=20)

        tags_label.grid(column=1, row=7, sticky='sw', pady=(5, 0), padx=20)
        project_tags.grid(column=1, row=8, sticky='nw', pady=(0, 5), padx=20)

        sub_button = tk.Button(self.share_page, text='Share!', command=lambda : self.user_log({"name":project_name.get(), "description":project_description.get(), "tags":project_tags.get()}) )
        sub_button.grid(column=1, row=9, pady=5)

        
    def user_log(self, data):

        self.share_page.destroy()
        
        if( not ( data['name'] and data['description'] and data["tags"] ) ):
            self.get_project_data('please enter the required data !')
            return

        user_data = data

        user_data["author"] = self.name
        user_data["width"] = self.canva.Nx
        user_data["height"] = self.canva.Ny
        user_data["date_created"] = date.today().isoformat()
        user_data["like"] = 0
        user_data["dislike"] = 0
        user_data["palette"] = self.colors
        user_data["matrice"] = self.canva.matrix_pixels(self.canva.Nx, self.canva.Ny)
        
        with open(f"client/data/{data['name']}.json", 'w', encoding='utf8') as file_data:
            js.dump(user_data, file_data, indent=4)


    def show_preview(self, image, w, h):

        self.label.config(image=image)

        if(self.canva): self.canva.canva.destroy()
            
        self.ecran = tk.Canvas(self)
        self.canva = Canva.Canva(w, h, 10, self.ecran, self)
        log_button = tk.Button(self, text='enregistrer', command=self.download_pixel)
        log_button.grid(column=5, row=3)

        share_button = tk.Button(self, text='partager', command=self.get_project_data)
        share_button.grid(row=4, column=5)

        self.canva.draw()

        self.canva.canva.bind('<Motion>', self.canva.fillPixel)
        self.canva.canva.bind("<Button-1>", self.canva.fillPixel)  

        
        
        self.canva.canva.bind("<Button-3>", self.canva.fillPixel)
        self.canva.canva.grid(column=1, row=2, columnspan=4, rowspan=4, padx=25)
    
    def start_project(slef):
        pass

    def ask_forname(self, got_name=False):
        self.name_entry.destroy()
        self.name_buttun.destroy()

        if got_name:
            self.name = got_name
            self.display_game()
            

            print(self.name)
            return

        self.name_entry = tk.Entry(self, width=60)
        self.name_buttun = tk.Button(self, text='Apply', command=lambda : self.ask_forname(self.name_entry.get()))

        self.name_entry.grid(row=2, column=1, padx=200, pady=50)
        self.name_buttun.grid(row=3, column=1, sticky='n')

    

    def display_game(self):

        see_social = tk.Button(self, text='pixocial', command=lambda : self.switch_page("pixocial"))
        see_social.grid(row=1, column=1, padx=5)

        title = tk.Label(self, text='PIxelSolo', font=("Arial", 25, "bold"))
        title.grid(column=2, row=1, columnspan=3, pady=10)

        for color in self.colors:
            self.create_color_button(color)

        open_btn = tk.Button(self, text="open a file", command=self.select_file)
        name = tk.Label(self, text=self.name, font=("Helvetica", 20))

        open_btn.grid(column=5, row=5, pady=10)
        name.grid(column=5, row=1)
        self.label.grid(column=5, row=2, columnspan=1, rowspan=1 , pady=10)

    def start_game(self):
        self.ask_forname()        
     

if __name__ == '__main__':

    screen = tk.Tk()

    Game(screen).start_game()