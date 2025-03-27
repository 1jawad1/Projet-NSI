import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter.messagebox import showerror


class Home(ttk.Frame):
    def __init__(self, screen, controler):
        super().__init__(screen)
        self.controler = controler

        self.name_title = ttk.Label(self, text='Enter your name !!')
        self.name_entry = ttk.Entry(self, width=60)
        self.name_buttun = ttk.Button(self, text='Apply', command=lambda : self.ask_forname(self.name_entry.get()))


    def ask_forname(self, got_name=False):

        self.name_title.destroy()
        self.name_entry.destroy()
        self.name_buttun.destroy()

        if got_name:
            self.name = got_name
            self.controler.frames["game"].name = self.name 
            self.display_home()

            print(self.name)
            return
        
        self.name_title = ttk.Label(self, text='Enter your name !!')
        self.name_entry = ttk.Entry(self, width=60)
        self.name_buttun = ttk.Button(self, text='Apply', command=lambda : self.ask_forname(self.name_entry.get()))

        self.name_title.grid(row=1, column=1, pady=(100, 0))
        self.name_entry.grid(row=2, column=1, padx=200, pady=50)
        self.name_buttun.grid(row=3, column=1, sticky='n')

    def display_home(self):

        
        welcome_message = ttk.Label(self, text=f"Welcome to the home page, {self.name} !!")
        welcome_message.grid(row=0, column=0, columnspan=2)

        self.solo_img = ImageTk.PhotoImage(Image.open("client/assets/pixel (1).webp").resize((100, 100), Image.Resampling.LANCZOS))
        self.war_img = ImageTk.PhotoImage(Image.open("client/assets/pixel (2).webp").resize((100, 100), Image.Resampling.LANCZOS))
        self.social_img = ImageTk.PhotoImage(Image.open("client/assets/pixel (3).webp").resize((100, 100), Image.Resampling.LANCZOS))

        pixel_solo = ttk.LabelFrame(self, text='PixelSolo')
        solo_image = ttk.Label(pixel_solo, image=self.solo_img)
        solo_sub_title = ttk.Label(pixel_solo, text='express your creativity !')
        solo_but = ttk.Button(pixel_solo, text='draw !', command=lambda : self.controler.show_frame("game"))
        solo_sub_title.pack()
        solo_image.pack()
        solo_but.pack()

        pixel_war = ttk.LabelFrame(self, text='PixelWar')
        war_sub_title = ttk.Label(pixel_war, text='play against the strongest !')
        war_image = ttk.Label(pixel_war, image=self.war_img)
        war_but = ttk.Button(pixel_war, text='battle !', command=lambda : showerror(title="PixelWar", message="Option non disponible pour le moment !"))
        war_sub_title.pack()
        war_image.pack()
        war_but.pack()

        Pixocial = ttk.LabelFrame(self, text='Pixocial')
        social_sub_title = ttk.Label(Pixocial, text='surf in to the other creation !')
        social_image = ttk.Label(Pixocial, image=self.social_img)
        social_but = ttk.Button(Pixocial, text='surf !', command=lambda : self.controler.show_frame("pixocial"))
        social_sub_title.pack()
        social_image.pack()
        social_but.pack()



        pixel_solo.grid(row=1, column=0, sticky='nsew', padx=50, pady=40)
        pixel_war.grid(row=1, column=1, sticky='nsew', padx=50, pady=40)
        Pixocial.grid(row=2, column=0, columnspan=2, sticky='nsew', padx=250, pady=40)

        self.grid_columnconfigure((0, 1), weight=1)  
        self.grid_rowconfigure((0, 1, 2), weight=1)



    def switch_page(self, page):
        self.controller.show_frame(page)

