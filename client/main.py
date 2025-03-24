import pixocial
import game

import tkinter as tk

class App(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.geometry(f"{width}x{height}")

        self.container = tk.Frame(self, bd=5, relief="solid")
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {
            "pixocial" : pixocial.Pixocial('./client/data', self.container, self),
            "game" : game.Game(self.container, self)
        }

        for i in self.frames.values():
            i.grid(row=0, column=0, sticky="nsew")

        self.show_frame("game")  

        self.bind("<Shift_L>", lambda e: self.frames["game"].canva.changeClickStatus()) 

        self.frames['game'].start_game()
        self.frames['pixocial'].draw_blog()

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise() 

    

app = App(900, 600)
app.mainloop()