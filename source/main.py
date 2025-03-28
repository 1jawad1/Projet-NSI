import pixocial
import game
import home

import tkinter as tk

from tkinter import ttk

import style

password = "#PgR8QnbEV;%f:&"


class App(tk.Tk):
    def __init__(self, width, height):
        super().__init__()
        self.geometry(f"{width}x{height}")

        self.style = ttk.Style()
        self.theme = 'dark'

        style.apply_theme(self.style, self.theme)

        self.navigation_bar = ttk.Notebook(self, style="TNotebook")
        self.navigation_bar.pack(expand=True, fill="both")
        # self.navigation_bar.bind('<Button-1>', widget_chnage)

        self.frames = {
            "home" : home.Home(self.navigation_bar, self),
            "game" : game.game_systeme(self.navigation_bar, self),
            "pixocial" : pixocial.Pixocial('./data', self.navigation_bar, self)
        }

        for i in self.frames:
           self.navigation_bar.add(self.frames[i], text=i)

        self.show_frame("home")  

       

        self.frames['home'].ask_forname()
        # self.frames['game'].start_game()
        self.frames['pixocial'].draw_blog()

    def widget_change(self):
        self.file_menu.delete('Sauvegarder')
        self.file_menu.delete('Ouvrir Projet')
    def show_frame(self, tab):
        self.navigation_bar.select(self.frames[tab])

    def draw_menu(self):
        self.Game_menu = tk.Menu(self)
        self.config(menu=self.Game_menu)

        self.file_menu = tk.Menu(self.Game_menu, tearoff=0)
        self.file_menu.add_command(label="Nouveau Projet") 
        self.file_menu.add_command(label="Ouvrir Projet",command=game.all_project[game.current_project].canva.canva_setup)
        self.file_menu.add_command(label="Sauvegarder",command=game.all_project[game.current_project].download_pixel)
        self.file_menu.add_separator()  # Ajout d'une séparation
        self.file_menu.add_command(label="Quitter",command=self.destroy)
        self.Game_menu.add_cascade(label="Fichier", menu=self.file_menu)

        # Settings menu (Paramètres du jeu)
        settings_menu = tk.Menu(self.Game_menu, tearoff=0)
        themes_menu  = tk.Menu(settings_menu, tearoff=0)
        themes_menu.add_command(label='light', command= lambda :self.change_theme('light'))
        themes_menu.add_command(label='dark', command= lambda :self.change_theme('dark'))
        settings_menu.add_cascade(label='themes', menu=themes_menu)
        self.Game_menu.add_cascade(label="Paramètres", menu=settings_menu)

        # Help menu (Aide)
        help_menu = tk.Menu(self.Game_menu, tearoff=0)
        help_menu.add_command(label="Aide")
        self.Game_menu.add_cascade(label="Aide", menu=help_menu)

    def change_theme(self, theme):
        style.apply_theme(self.style, theme)
        self.theme = theme

        # for widget in self.get_all_children():
        #     widget.configure(style=widget.winfo_class())

    
    def get_all_children(self):
        self.all_children = []
        self.get_children(self)
        return self.all_children

    def get_children(self, widget):
        for child in widget.winfo_children():
            self.all_children.append(child)
            self.get_children(child)


    

app = App(900, 600)
app.mainloop()