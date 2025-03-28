import pathlib as pt
import json as js
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np

from post import Post
from detail_page import Detail_page as dt


class Pixocial(ttk.Frame):

    def __init__(self, path, screen, controller):

        self.screen = screen 
        super().__init__(screen)

        self.controller = controller

        self.path = pt.Path(path)

        self.canva = tk.Canvas(self)  # Ajout d'une bordure pour visualiser la taille
        self.canva.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.canva.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canva.configure(yscrollcommand=scrollbar.set)

        self.content_frame = ttk.Frame(self.canva)
        self.content_window = self.canva.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.canva.bind("<Configure>", self.resize_content_frame)

        self.canva.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def resize_content_frame(self, event):
        """ Ajuste la taille du content_frame pour qu'il occupe toute la place du Canvas """
        self.canva.itemconfig(self.content_window, width=event.width)
        self.update_content_frame_height()

    def update_content_frame_height(self):
        """ Met à jour la hauteur de content_frame en fonction du contenu réel pour éviter les espaces vides """
        height = 0
        for widget in self.content_frame.winfo_children():
            height += widget.winfo_height() + 5  # Ajoute un peu d'espacement entre les éléments
        self.canva.itemconfig(self.content_window, height=max(height, self.canva.winfo_height()))
        self.canva.config(scrollregion=self.canva.bbox(self.content_window))  # Met à jour la zone de défilement

    def on_mouse_wheel(self, e):
        """ Limite le défilement vers le haut et vers le bas """
        if e.delta > 0:
            # Si on défile vers le haut
            self.canva.yview_scroll(-1*(e.delta//120), "units")
            if self.canva.yview()[0] < 0:
                self.canva.yview_moveto(0)  # Empêche de scroller au-dessus du premier élément
        else:
            # Si on défile vers le bas
            self.canva.yview_scroll(-1*(e.delta//120), "units")
            if self.canva.yview()[1] > 1:
                self.canva.yview_moveto(1)  # Empêche de scroller en dessous du dernier élément

    def get_directories_paths(self):
        return [i for i in self.path.iterdir() if i.suffix == ".json"]

    def draw_blog(self):

        title = ttk.Label(self.content_frame, text="Pixocial", font=("Helvetica", 24, "bold"), style="Title.TLabel")
        title.grid(row=0, column=0, columnspan=3, pady=10)
        
        position = 0
        for i in self.get_directories_paths():
            with open(str(i), 'r') as f:
                data = js.load(f)

                image = self.draw_image(data['matrice'], data["width"], data["height"], 220, 110)
                bigger_image = self.draw_image(data['matrice'], data["width"], data["height"], 350, 180)

                detailed_page = dt(ttk, data, bigger_image, self.screen)

                cell = Post(data, ttk, js,  str(i), image, detailed_page.show_details)
                frame = tk.Frame(self.content_frame, borderwidth=0, bg="#7f8c8d")

                cell.draw_cell(frame)

                frame.grid(row=position//2+1, column=position%2, pady=5, padx=5, sticky="nsew")
                
                position += 1



        # Une fois les éléments ajoutés, met à jour la taille de content_frame
        self.update_content_frame_height()

    def draw_image(self, matrice, w, h, max_w, max_h):
        coef = min(max_w//w, max_h//h)
        return ImageTk.PhotoImage(Image.fromarray(np.array(matrice, dtype=np.uint8), "RGB").resize((w*coef, h*coef), resample=0))


if __name__ == '__main__':
    page = Pixocial('./client/data', tk.Tk())

    page.draw_blog()
