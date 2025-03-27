import tkinter as tk
from tkinter import ttk

class Game(tk.Frame):
    def __init__(self, screen, controler):
        super().__init__(screen)
        self.controler = controler

    def start_game(self):
        pass