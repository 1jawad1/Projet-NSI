import pathlib as pt
import json as js
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

from post import Post
from detail_page import Detail_page as dt


class Pixocial(tk.Frame):

    def __init__(self, path, screen, controller):

        self.screen = screen 
        super().__init__(screen)

        self.controller = controller

        self.path = pt.Path(path)

        self.canva = tk.Canvas(self)
        self.canva.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canva.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canva.configure(yscrollcommand=scrollbar.set)
        self.canva.bind("<Configure>", lambda e: self.canva.configure(scrollregion=self.canva.bbox("all")))

        self.content_frame = tk.Frame(self.canva)
        self.canva.create_window((0,0), window=self.content_frame, anchor="nw")

        self.canva.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def on_mouse_wheel(self, e):
        self.canva.yview_scroll(-1*(e.delta//120), "units")

    def get_directories_paths(self):
        return [i for i in self.path.iterdir() if i.suffix == ".json"]

    def draw_blog(self):

        play_game = tk.Button(self.content_frame, text='pixelsolo', command=lambda : self.switch_page("game"))
        play_game.grid(row=0, column=0, padx=5)

        title = tk.Label(self.content_frame, text="Pixocial", font=("Helvetica", 24, "bold"))
        title.grid(row=0, column=1, columnspan=2, pady=10)
        
        position = 0
        for i in self.get_directories_paths():
            with open(str(i), 'r') as f:
                data = js.load(f)

                image = self.draw_image(data['matrice'], data["width"], data["height"], 220, 110)
                bigger_image = self.draw_image(data['matrice'], data["width"], data["height"], 320, 160)

                detailed_page = dt(tk, data, bigger_image, self.screen)

                cell = Post(data, tk, js,  str(i), image, detailed_page.show_details)
                frame = tk.LabelFrame(self.content_frame)

                cell.draw_cell(frame)

                frame.grid(row=position//3+1, column=position%3, pady=5)
                position+=1
        


    def draw_image(self, matrice, w, h, max_w, max_h):
        coef = min(max_w//w, max_h//h)
        return ImageTk.PhotoImage(Image.fromarray(np.array(matrice, dtype = np.uint8), "RGB").resize((w*coef, h*coef), Image.Resampling.LANCZOS))
    
    def switch_page(self, page):
        self.controller.show_frame(page)


if __name__ == '__main__':

    page = Pixocial('./client/data', tk.Tk())

    page.draw_blog()

